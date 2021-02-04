import pytest
import django.test
import datetime
from django.contrib.auth.models import User, Permission
from Gym.models import UserData, Exercise, TrainingPlan, ExerciseSet


@pytest.fixture
def client():
    return django.test.Client()


@pytest.fixture
def unauthorized_user():
    return User.objects.create_user("Tester")


@pytest.fixture
def authorized_user():
    return User.objects.create_superuser(username="Test Trainer")


@pytest.fixture
def test_userdata():
    return UserData.objects.create(age=15, height=15, weight=15, muscle_weight=15, fat_weight=15,
                                   metabolic_age=15, chest_circuit=15, biceps_circuit=15, biceps_circuit_tight=15,
                                   buttock_circuit=15, thigh_circuit=15,
                                   waist_circuit=15, calf_circuit=15, date=datetime.date(2015, 1, 15),
                                   owner=User.objects.get(username="Tester"))


@pytest.fixture
def test_exercise():
    return Exercise.objects.create(name="test", description='Test, test', link='www.test.pl')


@pytest.fixture
def test_training_plan():
    return TrainingPlan.objects.create(name="test training", user=User.objects.get(username="Tester"))


@pytest.fixture
def test_exercise_set():
    return ExerciseSet.objects.create(user=User.objects.get(username="Tester"),
                                      training_plan=TrainingPlan.objects.get(name='test training'),
                                      exercise=Exercise.objects.get(name='test'),
                                      exercise_reps=1,
                                      exercise_rounds=1,
                                      exercise_weight=1,)
