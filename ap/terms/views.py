from .models import Term
from rest_framework import viewsets
from .serializers import TermSerializer

class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
