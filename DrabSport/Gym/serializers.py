from rest_framework import serializers
from .models import ExerciseSet


class ExerciseSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseSet
        fields = '__all__'



