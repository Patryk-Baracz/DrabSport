from rest_framework import routers
from .api import ExercisesetViewSet, ExerciseHistoryViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'exerciseset', ExercisesetViewSet)
router.register(r'exercisehistory', ExerciseHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),

]