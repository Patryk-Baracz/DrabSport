from .models import ExerciseSet, ExerciseHistory
from .serializers import ExerciseSetSerializer, ExerciseHistorySerializer
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'exercisesets': reverse('exerciseset-list', request=request, format=format)
    })


class ExercisesetViewSet(viewsets.ModelViewSet):
    queryset = ExerciseSet.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ExerciseSetSerializer

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'exercisehistory': reverse('exercisehistory-list', request=request, format=format)
    })


class ExerciseHistoryViewSet(viewsets.ModelViewSet):
    queryset = ExerciseHistory.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ExerciseHistorySerializer