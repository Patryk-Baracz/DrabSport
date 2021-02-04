from .models import ExerciseSet
from .serializers import ExerciseSetSerializer
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
