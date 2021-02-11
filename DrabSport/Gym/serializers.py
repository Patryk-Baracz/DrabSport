from rest_framework import serializers
from .models import ExerciseSet, ExerciseHistory


class ExerciseSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseSet
        fields = '__all__'

class ExerciseHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseHistory
        fields = '__all__'


