import pytest
from .models import UserData, Exercise, TrainingPlan, ExerciseSet
from django.contrib.auth.models import User
import datetime


@pytest.mark.django_db
def test_exercise_add(client, authorized_user):
    client.force_login(authorized_user)
    response = client.post('/exercise_add/', {'name': 'test', 'description': 'Test, test', 'link': 'www.test.pl'})
    assert Exercise.objects.get(name='test')


@pytest.mark.django_db
def test_exercise_add_missing_permission(client, unauthorized_user):
    client.force_login(unauthorized_user)
    response = client.post('/exercise_add/', {'name': 'test', 'description': 'Test, test', 'link': 'www.test.pl'})
    assert response.status_code == 403


@pytest.mark.django_db
def test_exercise_update(client, authorized_user, test_exercise):
    client.force_login(authorized_user)
    key = test_exercise.pk
    response = client.post(f'/exercise_edit/{key}/',
                           {'name': 'test2', 'description': 'Test, test', 'link': 'www.test.pl'})
    assert Exercise.objects.get(name='test2')


@pytest.mark.django_db
def test_exercise_update_missing_permission(client, unauthorized_user, test_exercise):
    client.force_login(unauthorized_user)
    key = test_exercise.pk
    response = client.post(f'/exercise_edit/{key}/',
                           {'name': 'test2', 'description': 'Test, test', 'link': 'www.test.pl'})
    assert response.status_code == 403


@pytest.mark.django_db
def test_exercise_delete(client, authorized_user, test_exercise):
    client.force_login(authorized_user)
    key = test_exercise.pk
    response = client.post(f'/exercise_delete/{key}/')
    assert len(Exercise.objects.filter(name='test')) == 0


@pytest.mark.django_db
def test_exercise_delete_missing_permission(client, unauthorized_user, test_exercise):
    client.force_login(unauthorized_user)
    key = test_exercise.pk
    response = client.post(f'/exercise_delete/{key}/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_exercise_list(client, authorized_user, test_exercise):
    client.force_login(authorized_user)
    response = client.get('/exercise_list/')
    assert response.context['exercises'][0].name == 'test'


@pytest.mark.django_db
def test_exercise_list_missing_permission(client, unauthorized_user, test_exercise):
    client.force_login(unauthorized_user)
    response = client.get('/exercise_list/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_training_plan_add(client, authorized_user, unauthorized_user):
    client.force_login(authorized_user)
    response = client.post(f'/training_create/{unauthorized_user.pk}/', {'name': "test plan"})
    assert TrainingPlan.objects.get(name="test plan")


@pytest.mark.django_db
def test_training_plan_add_missing_permission(client, unauthorized_user):
    client.force_login(unauthorized_user)
    response = client.post(f'/training_create/{unauthorized_user.pk}/', {'name': "test plan"})
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_list(client, authorized_user):
    client.force_login(authorized_user)
    response = client.get('/user_list/')
    assert len(response.context['users']) != 0


@pytest.mark.django_db
def test_user_list_missing_permission(client, unauthorized_user):
    client.force_login(unauthorized_user)
    response = client.get('/user_list/')
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_plan_list(client, authorized_user, unauthorized_user):
    client.force_login(authorized_user)
    TrainingPlan.objects.create(name='test plan', user=unauthorized_user)
    response = client.get(f'/user_plan_list/{unauthorized_user.pk}/')
    assert len(response.context['plans']) != 0


@pytest.mark.django_db
def test_training_detail(client, authorized_user, unauthorized_user, test_exercise, test_training_plan,
                         test_exercise_set):
    client.force_login(authorized_user)
    response = client.get(f'/user_plan_detail/{test_training_plan.pk}/')
    assert response.context['plan'].name == 'test training'


@pytest.mark.django_db
def test_exercise_add_to_training(client, authorized_user, unauthorized_user, test_exercise, test_training_plan):
    client.force_login(authorized_user)
    response = client.post(f'/exercise_set_add/{test_training_plan.pk}', {'exercise': "1",
                                                                          'exercise_reps': '1',
                                                                          'exercise_rounds': '1',
                                                                          'exercise_weight': '1',
                                                                          'start_date': "2021-02-04"})
    assert ExerciseSet.objects.get(user=User.objects.get(username="Tester")).exercise_reps == '1'
