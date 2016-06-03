import django_filters
from rest_framework.serializers import ModelSerializer
from .models import Event, Schedule
from rest_framework import serializers
from rest_framework import serializers, filters
from rest_framework_bulk import (
  BulkListSerializer,
  BulkSerializerMixin,
  ListBulkCreateUpdateDestroyAPIView,
)


class EventSerializer(BulkSerializerMixin, ModelSerializer):
  class Meta:
    model = Event
    list_serializer_class = BulkListSerializer
    fields = '__all__'

class EventWithDateSerializer(BulkSerializerMixin, ModelSerializer):
  date = serializers.DateField(read_only=True)
  class Meta:
    model = Event
    list_serializer_class = BulkListSerializer
    fields = ['id', 'date']

class AttendanceEventWithDateSerializer(BulkSerializerMixin, ModelSerializer):
  start_datetime = serializers.DateTimeField(read_only=True)
  end_datetime = serializers.DateTimeField(read_only=True)
  class Meta:
    model = Event
    list_serializer_class = BulkListSerializer
    fields = '__all__'

class EventFilter(filters.FilterSet):
  start__lt = django_filters.DateTimeFilter(name = 'start', lookup_expr = 'lt')
  start__gte = django_filters.DateTimeFilter(name = 'start', lookup_expr = 'gte')
  end__lt = django_filters.DateTimeFilter(name = 'end', lookup_expr = 'lt')
  end__gte = django_filters.DateTimeFilter(name = 'end', lookup_expr = 'gte')
  id__lt = django_filters.NumberFilter(name = 'id', lookup_expr = 'lt')
  id__gte = django_filters.NumberFilter(name = 'id', lookup_expr = 'gte')
  class Meta:
    model = Event
    fields = ['id','name']

class ScheduleSerializer(BulkSerializerMixin, ModelSerializer):
  class Meta:
    model = Schedule
    list_serializer_class = BulkListSerializer
    fields = '__all__'

class ScheduleFilter(filters.FilterSet):
  class Meta:
    model = Schedule
    fields = ['id','trainees','weeks','events']