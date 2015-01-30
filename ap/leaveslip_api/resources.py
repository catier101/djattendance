from itertools import chain

from tastypie import fields, utils
from tastypie.resources import ModelResource
from tastypie.validation import Validation, CleanedDataFormValidation
from tastypie.authentication import Authentication, BasicAuthentication
from tastypie.authorization import Authorization

from accounts.models import Profile, User, Trainee, TrainingAssistant
from attendance.models import Roll
from leaveslips.models import LeaveSlip, IndividualSlip, GroupSlip, IndividualSlipForm
from schedules.models import Event


''' leaveslip_api resources.py

All the API resources for leaveslips. For each model, GET, POST, and PUT are supported.

See schemas.txt for sample formats.

'''

class EventResource(ModelResource):
	class Meta:
		authorization = Authorization()
		queryset = Event.objects.all()
        resource_name = 'events'

class TraineeResource(ModelResource):
	class Meta:
		authorization = Authorization()
		queryset = Trainee.objects.all()
        resource_name = 'trainee'


class TrainingAssistantResource(ModelResource):
	class Meta:
		authorization = Authorization()
		queryset = TrainingAssistant.objects.all()
		resource_name = 'TA'


class IndividualSlipResource(ModelResource):
	trainee = fields.ForeignKey(TraineeResource, 'trainee')
	TA = fields.ForeignKey(TrainingAssistantResource, 'TA')
	events = fields.ToManyField(EventResource, 'events')

	class Meta:
		queryset = IndividualSlip.objects.all()
		allowed_methods = ['get', 'post', 'put', 'delete']
		authentication = Authentication()
		authorization = Authorization()
		form = CleanedDataFormValidation(form_class=IndividualSlipForm)

	def get_object_list(self, bundle, **kwargs):
		if hasattr(bundle, 'request'):
			query = bundle.request.GET.get('event-id', None)
			if query:
				individual_objects = IndividualSlip.objects.filter(events__id=query)[:1]
				# Note: currently not dealing with other kinds of leave slips.
				# If more than one leaveslip covers an event, we only display the first one.
				# (User can view all leaveslips on the list page)

				# group_objects = GroupSlip.objects.filter(events__id=query)[:1]
				# return chain(individual_objects, group_objects)[:1]
				return individual_objects
		return super(IndividualSlipResource, self).get_object_list(bundle, **kwargs)

	def obj_get_list(self, bundle, **kwargs):
		return self.get_object_list(bundle, **kwargs)

class RollResource(ModelResource):
	event = fields.ForeignKey(EventResource, 'event')
	trainee = fields.ForeignKey(TraineeResource, 'trainee')
	monitor = fields.ForeignKey(TraineeResource, 'monitor')

	class Meta:
		queryset = Roll.objects.all()
		allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
		authentication = Authentication()
		authorization = Authorization()


class GroupSlipResource(ModelResource):
	class Meta:
		queryset = GroupSlip.objects.all()
		allowed_methods = ['get', 'post', 'put']
