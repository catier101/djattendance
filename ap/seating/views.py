from django.views.generic import TemplateView, DetailView, ListView
from django.views import generic
from .models import Chart, Seat
from terms.models import Term
from accounts.models import Trainee
from .serializers import ChartSerializer, SeatSerializer
from accounts.serializers import TraineeSerializer, BasicUserSerializer

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

class ChartListView(generic.ListView):
    model = Chart
    template_name = 'seating/chart_list.html'

    def get_queryset(self):
         return Chart.objects.filter(term=Term.current_term())

class ChartCreateView(generic.ListView):
    model = Chart
    template_name = 'seating/chart_create.html'

    context_object_name = 'context'

    def get_context_data(self, **kwargs):
        listJSONRenderer = JSONRenderer()
        l_render = listJSONRenderer.render

        trainees = Trainee.objects.filter(is_active=True)

        context = super(ChartCreateView, self).get_context_data(**kwargs)
        context['trainees'] = trainees
        context['trainees_bb'] = l_render(BasicUserSerializer(trainees, many=True).data)

        return context

    # def get_queryset(self):

class ChartEditView(generic.DetailView):
    model = Chart
    template_name = 'seating/chart_edit.html'

    context_object_name = 'context'

    def get_context_data(self, **kwargs):
        listJSONRenderer = JSONRenderer()
        l_render = listJSONRenderer.render

        trainees = Trainee.objects.filter(is_active=True)

        context = super(ChartEditView, self).get_context_data(**kwargs)
        context['trainees'] = trainees
        context['trainees_bb'] = l_render(BasicUserSerializer(trainees, many=True).data)

        chart = Chart.objects.filter(pk=self.pk)
        context['chart'] = chart
        context['chart_bb'] = l_render(ChartSerializer(chart, many=True).data)
        context['chart_id'] = self.pk

        seats = Seat.objects.filter(chart=chart)
        context['seats'] = seats
        context['seats_bb'] = l_render(SeatSerializer(seats, many=True).data)

        return context

    def get_queryset(self):
        self.pk = self.kwargs['pk']
        queryset = super(ChartEditView, self).get_queryset()
        return queryset


class ChartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows charts to be viewed or edited.
    """
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer

class SeatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows seats to be viewed or edited.
    """
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
