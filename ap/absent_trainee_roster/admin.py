from datetime import date, timedelta
from pdf import render_to_pdf

from django.contrib import admin
from django.template import loader,Context
from django.conf.urls import patterns
from django.core.mail import EmailMessage
from django.conf import settings # to get admin email addresses
from django.http import HttpResponse

from .models import Absentee, Roster, Entry
from houses.models import House
from accounts.models import User

class EntryAdmin(admin.ModelAdmin):
	def house(obj):
		return obj.absentee.house

	def term(obj):
		return obj.absentee.term

	list_display = ('roster', 'absentee', 'reason', 'comments', house,)


class EntryInline(admin.TabularInline):
	model = Entry
	fk_name = 'roster'
	verbose_name_plural = 'entries'
	extra = 1


class RosterAdmin(admin.ModelAdmin):
	generate_roster = 'absent_trainee_roster/generate_roster.html'
	
	inlines = [
		EntryInline,
	]

	readonly_fields = ('unreported_houses',)

	
	def save_related(self, request, form, formsets, change):
		roster = Roster.objects.get(date=request.REQUEST['date'])

		# when roster is created, add all houses as unreported.
		# --this is also done in RosterManager.create_roster(), but  
		# admin doesn't call this function to create objects.
		if change == False:
			for house in House.objects.all():
				roster.unreported_houses.add(house)
			roster.save()

		for formset in formsets:
			self.save_formset(request, form, formset, change)

		return True

	def save_formset(self, request, form, formset, change):
		roster = Roster.objects.get(date=request.REQUEST['date'])
		entries = formset.save(commit=False)
		for entry in entries:
			roster.unreported_houses.remove(entry.absentee.house)
			entry.save()
		formset.save_m2m()
		return True

	def get_urls(self):
		urls = super(RosterAdmin, self).get_urls()
		my_urls =patterns('',
			#(r'\d+/generate/$', self.admin_site.admin_view(self.myview)),
			(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d+)/generate/$', self.admin_site.admin_view(self.generate_pdf)),
			(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d+)/email/$', self.admin_site.admin_view(self.send_mail)),
			
		)
		return my_urls +urls
	
	#using Pisa
	def generate_pdf(self, request, year, month, day):
		#Retrieve data or whatever you need
		d=date(int(year),int(month),int(day))
		roster = Roster.objects.get(date=d)
		entries = roster.entry_set.all().order_by('-absentee')
		bro_unreported_houses = roster.unreported_houses.filter(gender='B')
		sis_unreported_houses = roster.unreported_houses.filter(gender='S')
		
		days = self.calculate_days(d)
		unreported_list = self.list_unreported_houses(d)
		return render_to_pdf(
			'absent_trainee_roster/generate_roster.html',
			{
				'pagsize': 'letter',
				'roster': roster,
				'entries': entries,
				'genders': User.GENDER,
				'bro_unreported_houses': bro_unreported_houses,
				'sis_unreported_houses': sis_unreported_houses,
				'days': days,
				'unreported_list': unreported_list,
			}
		)

	#calculate how many days a trainee has been absent in the last 7 days
	def calculate_days(self,date):
		days = {}
		for i in range(7):
			try:
				roster = Roster.objects.get(date=date)
				for entry in roster.entry_set.all():
					if str(entry.absentee) in days:
						days[str(entry.absentee)] += 1
					else:
						days[str(entry.absentee)] = 1
			except:
				pass
			
			date = date - timedelta(days=1)
		return days
	
	#makes list of trainee houses that are unreported within the last 7 days
	def list_unreported_houses(self, date):
		list = []
		for i in range(7):
			try:
				roster = Roster.objects.get(date=date)
				for house in roster.unreported_houses.all():
					if house not in list:
						list.append(house)
			except:
				pass
			
			date = date - timedelta(days=1)
		return list
	
	#sends absent trainee roster to admins
	def send_mail(self,request, year, month, day):
		d=date(int(year),int(month),int(day))
		roster = Roster.objects.get(date=d)
		entries = roster.entry_set.all().order_by('-absentee')
		bro_unreported_houses = roster.unreported_houses.filter(gender='B')
		sis_unreported_houses = roster.unreported_houses.filter(gender='S')
		
		days = self.calculate_days(d)
		unreported_list = self.list_unreported_houses(d)
		
		subject = "Absent Trainee Roster for " +str(d)
		email_template = loader.get_template('absent_trainee_roster/generate_roster.html')
		context = Context({
				'pagsize': 'letter',
				'roster': roster,
				'entries': entries,
				'bro_unreported_houses': bro_unreported_houses,
				'sis_unreported_houses': sis_unreported_houses,
			'days': days,
				'unreported_list': unreported_list,
				
			})
		
		admin_emails = [v for k,v in settings.ADMINS]
		email =EmailMessage(subject, email_template.render(context), 'djattendanceproject@gmail.com', admin_emails)
		email.content_subtype ="html"
		#email.attach('roster.pdf', self.generate_pdf, 'application/pdf')
		email.send()
		
		
		return HttpResponse("Email was sent")
	
admin.site.register(Absentee)
admin.site.register(Roster, RosterAdmin)
admin.site.register(Entry, EntryAdmin)
