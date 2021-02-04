from rest_framework import routers
from .api import ExercisesetViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'exerciseset', ExercisesetViewSet)

urlpatterns = [
    path('', include(router.urls)),

]