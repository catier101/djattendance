from .models import Chart, Seat
from accounts.models import Trainee
from terms.models import Term

from rest_framework.serializers import ModelSerializer

import pdb

class ChartSerializer(ModelSerializer):
    class Meta:
        model = Chart
        fields = ('name', 'desc', 'height', 'width', 'trainees')
    def to_internal_value(self, data):
        internal_value = super(ChartSerializer, self).to_internal_value(data)
        internal_value.update({
            "trainees": data.get("trainees"),
            "id": data.get("id"),
        })
        return internal_value
    def create(self, validated_data):
        if validated_data.get("id"):
            #this is pretty naive and inefficient, needs to be optimized later
            chart = Chart.objects.get(pk=validated_data.get("id"))
            seats = Seat.objects.filter(chart=chart).delete()

            chart.width = validated_data.get("width")
            chart.height = validated_data.get("height")
            chart.name = validated_data.get("name")
            chart.save()

            seats = validated_data.pop('trainees')
            print seats
            for y in range(0, validated_data.get('height')):
                for x in range(0, validated_data.get('width')):
                    if seats[y][x] != {} and seats[y][x].get('pk') != '':
                        trainee = Trainee.objects.get(pk=seats[y][x]['pk'])
                        s = Seat(trainee=trainee, chart=chart, x=x, y=y)
                        s.save()

            return chart
        seats = validated_data.pop('trainees')
        print seats
        validated_data['term'] = Term.current_term()
        new_chart = Chart.objects.create(**validated_data)
        for y in range(0, validated_data.get('height')):
            for x in range(0, validated_data.get('width')):
                if seats[y][x] != {} and seats[y][x].get('pk') != '':
                    trainee = Trainee.objects.get(pk=seats[y][x]['pk'])
                    s = Seat(trainee=trainee, chart=new_chart, x=x, y=y)
                    s.save()

        return new_chart

class SeatSerializer(ModelSerializer):
    class Meta:
        model = Seat
        fields = ('trainee', 'chart', 'x', 'y')