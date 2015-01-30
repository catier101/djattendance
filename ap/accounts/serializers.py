from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import User, Trainee, TrainingAssistant


class UserSerializer(ModelSerializer):
    class Meta:
        model = User


class TraineeSerializer(ModelSerializer):
	name = SerializerMethodField('get_trainee_name')

	class Meta:
		model = Trainee

	def get_trainee_name(self, obj):
		return obj.__unicode__()

class TrainingAssistantSerializer(ModelSerializer):
    class Meta:
        model = TrainingAssistant
