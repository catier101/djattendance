import django_filters
from rest_framework.serializers import ModelSerializer
from .models import IndividualSlip, GroupSlip, LeaveSlip, Roll
from schedules.models import Event
from schedules.serializers import EventWithDateSerializer
from rest_framework import serializers, filters
from rest_framework_bulk import (
  BulkListSerializer,
  BulkSerializerMixin,
  ListBulkCreateUpdateDestroyAPIView,
)

from sets import Set
from datetime import datetime

class IndividualSlipSerializer(BulkSerializerMixin, ModelSerializer):
  events = EventWithDateSerializer(many=True,)

  class Meta(object):
    model = IndividualSlip
    list_serializer_class = BulkListSerializer
    exclude = ['rolls']

  def to_internal_value(self, data):
    internal_value = super(IndividualSlipSerializer, self).to_internal_value(data)
    events = data.get('events')
    internal_value.update({
      'events': events
    })
    return internal_value

  def update(self, instance, validated_data):
    events = validated_data.get('events', instance.events)
    rolls = Set()
    #TODO: Get all rolls and events in one go to save on db trips (optimization)
    #TODO: Delete empty rolls if events are removed
    for event in events:
      roll = Roll.objects.filter(event=event['id'], date=event['date'])
      if roll:
        rolls.add(roll[0])
      else:
        roll_dict = {'trainee': instance.trainee, 'event': Event.objects.get(id=event['id']), 'status': 'P', 'submitted_by': instance.trainee, 'date': event['date']}
        newroll = Roll.update_or_create(roll_dict)
        rolls.add(newroll)
    instance.rolls = rolls
    instance.type = validated_data.get('type', instance.type)
    instance.submitted = validated_data.get('submitted', instance.submitted)
    instance.last_modified = validated_data.get('last_modified', instance.last_modified)
    instance.finalized = validated_data.get('finalized', instance.finalized)
    instance.description = validated_data.get('description', instance.description)
    instance.comments = validated_data.get('comments', instance.comments)
    instance.texted = validated_data.get('texted', instance.texted)
    instance.informed = validated_data.get('informed', instance.informed)
    instance.TA = validated_data.get('TA', instance.TA)
    instance.trainee = validated_data.get('trainee', instance.trainee)
    instance.save()
    return instance

  def create(self, validated_data):
    trainee = validated_data['trainee']
    events = validated_data.pop('events')

    slip = IndividualSlip.objects.create(**validated_data)

    rolls = Roll.objects.filter(trainee=trainee)

    ev_db = {}

    for roll in rolls:
      ev_db[(roll.date, roll.event.id)] = roll
    
    # create rolls for given days and events
    for ev in events:
      date = datetime.strptime(ev['date'], "%Y-%m-%d").date()
      key = (date, int(ev['id']))
      if key not in ev_db:
        # create roll
        # Create dummy roll if it doesn't exist
        event_object = Event.objects.get(id=ev['id'])
        roll_dict = {'trainee': trainee, 'event': event_object, 'status': 'P', 'submitted_by': trainee, 'date': date}
        newroll = Roll.update_or_create(roll_dict)

        # Add rolls to the leaveslip's rolls
        if newroll:
          slip.rolls.add(newroll)
      else:
        slip.rolls.add(ev_db[key])

    return slip

class IndividualSlipFilter(filters.FilterSet):
  submitted__lt = django_filters.DateTimeFilter(name = 'submitted', lookup_expr = 'lt')
  submitted__gt = django_filters.DateTimeFilter(name = 'submitted', lookup_expr = 'gt')
  last_modified__lt = django_filters.DateTimeFilter(name = 'last_modified', lookup_expr = 'lt')
  last_modified__gt = django_filters.DateTimeFilter(name = 'last_modified', lookup_expr = 'gt')
  finalized__lt = django_filters.DateTimeFilter(name = 'finalized', lookup_expr = 'lt')
  finalized__gt = django_filters.DateTimeFilter(name = 'finalized', lookup_expr = 'gt')
  class Meta:
    model = IndividualSlip
    fields = ['id','type','status','submitted','last_modified','finalized','description','comments','texted','informed','TA','trainee','rolls']

class GroupSlipSerializer(BulkSerializerMixin, ModelSerializer):
  class Meta(object):
    model = GroupSlip
    list_serializer_class = BulkListSerializer
    fields = '__all__'

class GroupSlipFilter(filters.FilterSet):
  submitted__lt = django_filters.DateTimeFilter(name = 'submitted', lookup_expr = 'lt')
  submitted__gt = django_filters.DateTimeFilter(name = 'submitted', lookup_expr = 'gt')
  last_modified__lt = django_filters.DateTimeFilter(name = 'last_modified', lookup_expr = 'lt')
  last_modified__gt = django_filters.DateTimeFilter(name = 'last_modified', lookup_expr = 'gt')
  finalized__lt = django_filters.DateTimeFilter(name = 'finalized', lookup_expr = 'lt')
  finalized__gt = django_filters.DateTimeFilter(name = 'finalized', lookup_expr = 'gt')
  start__lt = django_filters.DateTimeFilter(name = 'start', lookup_expr = 'lt')
  start__gt = django_filters.DateTimeFilter(name = 'start', lookup_expr = 'gt')
  end__lt = django_filters.DateTimeFilter(name = 'end', lookup_expr = 'lt')
  end__gt = django_filters.DateTimeFilter(name = 'end', lookup_expr = 'gt')

  class Meta:
    model = GroupSlip
    fields = ['id','type','status','submitted','last_modified','finalized','description','comments','texted','informed','start','end','TA','trainee','trainees']