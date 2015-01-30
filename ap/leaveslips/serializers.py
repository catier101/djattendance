from rest_framework.serializers import ModelSerializer
from .models import IndividualSlip, GroupSlip


class IndividualSlipSerializer(ModelSerializer):
    class Meta:
        model = IndividualSlip


class GroupSlipSerializer(ModelSerializer):
    class Meta:
        model = GroupSlip
