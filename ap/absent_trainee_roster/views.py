from datetime import date

from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import user_passes_test

from absent_trainee_roster.models import Entry, Roster
from absent_trainee_roster.forms import AbsentTraineeForm, NewEntryFormSet


# @user_passes_test(lambda u: u.groups.filter(name='house_coordinator').count() == 1, login_url = '/')
def absent_trainee_form(request):
	EntryFormSet = modelformset_factory(Entry, AbsentTraineeForm, formset=NewEntryFormSet, max_num=10, extra=1, can_delete=True)
	
	# get today's roster. create it if it doesn't exist.
	if Roster.objects.filter(date=date.today()).exists():
		roster = Roster.objects.get(date=date.today())
	else:
		roster = Roster.objects.create_roster(date=date.today())

	if request.method == 'POST':
		formset = EntryFormSet(request.POST, request.FILES, user=request.user)
		if formset.is_valid():
			new_absentees = {}
			for i in xrange(int(request.POST['form-TOTAL_FORMS'])):
				if request.POST['form-' + str(i) + '-absentee']:
					absentee = int(request.POST['form-' + str(i) + '-absentee'])
					new_absentees[absentee] = i
			for form in formset.forms:
				if form.cleaned_data: # only save entry if it's not empty
					entry = form.save(commit=False)

					# check for overriding entry for absentee already in database
					for existing_entry in roster.entry_set.filter(absentee__account__trainee__house=request.user.trainee.house):
						if entry.absentee == existing_entry.absentee:
							existing_entry.delete()
							
					entry.roster = roster
					entry.save()
			
			# delete entries for absentees not in newly submitted form
			entries = roster.entry_set.filter(absentee__account__trainee__house=request.user.trainee.house)
			for entry in entries:
				if entry.absentee.id not in new_absentees.keys():
					entry.delete()

			roster.unreported_houses.remove(request.user.trainee.house)
			return redirect('/')
		
	else:
		# shows existing entries from user's house, i.e. if form was already submitted and user revisits the page
		formset = EntryFormSet(user=request.user, queryset=roster.entry_set.filter(absentee__account__trainee__house=request.user.trainee.house))

	c = {'formset': formset, 'user': request.user}
	c.update(csrf(request))

	return render_to_response('absent_trainee_roster/absent_trainee_form.html', c)
