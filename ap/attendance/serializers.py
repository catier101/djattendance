from rest_framework.serializers import ModelSerializer
from .models import Roll


class RollSerializer(ModelSerializer):
    class Meta:
        model = Roll
