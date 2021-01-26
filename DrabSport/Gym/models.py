from django.db import models
from django.contrib.auth.models import User
from datetime import date


class UserData(models.Model):
    first_name = models.CharField(max_length=32, unique=True, verbose_name="Imię")
    last_name = models.CharField(max_length=32, unique=True, verbose_name="Nazwisko")
    Age = models.IntegerField(verbose_name="Wiek")
    height = models.IntegerField(verbose_name="Wzrost")
    weight = models.FloatField(verbose_name="Waga")
    muscle_weight = models.FloatField(verbose_name="Waga mięśni", null=True)
    fat_weight = models.FloatField(verbose_name="Waga tłuszczu", null=True)
    metabolic_age = models.IntegerField(verbose_name="Wiek metaboliczny", null=True)
    chest_circuit = models.FloatField(verbose_name="Obwód klatki piersiowej", null=True)
    biceps_circuit = models.FloatField(verbose_name="Obwód bicepsa", null=True)
    biceps_circuit_tight = models.FloatField(verbose_name="Obwód bicepsa w spięciu", null=True)
    buttock_circuit = models.FloatField(verbose_name="Obwód pośladka", null=True)
    thigh_circuit = models.FloatField(verbose_name="Obwód uda", null=True)
    waist_circuit = models.FloatField(verbose_name="Obwód talii", null=True)
    calf_circuit = models.FloatField(verbose_name="Obwód łydki", null=True)
    date = models.DateField(auto_now_add=True, verbose_name="Data pomiarów")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Exercise(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Nazwa")
    description = models.TextField(verbose_name="Opis ćwiczenia")
    link = models.CharField(max_length=120, verbose_name="Link do You Tube")


class TrainingPlan(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Nazwa planu")
    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE, verbose_name="Użytkownik planu")
    exercise = models.ManyToManyField(Exercise, through='ExerciseSet')


class ExerciseSet(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    exercise_reps = models.IntegerField(verbose_name="Liczba powtórzeń w serii")
    exercise_rounds = models.IntegerField(verbose_name="Liczba serii")
    exercise_weight = models.FloatField(null=True, verbose_name="Obciążenie")
    start_date = models.DateField(default=date.today, verbose_name="Data rozpoczęcia")
    finish_date = models.DateField(null=True, verbose_name="Data zakończenia")


class ExerciseHistory(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE, verbose_name="Użytkownik")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, verbose_name="Ćwiczenie")
    total_reps = models.IntegerField(verbose_name="Suma powtórzeń")
    weight = models.FloatField(verbose_name="Obciążenie")
    date = models.DateField(auto_now_add=True, verbose_name="Data treningu")
