from rest_framework.serializers import ModelSerializer
from .models import Event, Schedule


class EventSerializer(ModelSerializer):
    class Meta:
        model = Event


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
