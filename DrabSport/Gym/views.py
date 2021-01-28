from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import UserData, Exercise
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import LoginForm, CreateUserForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import date

class LoginUserView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        rec_form = LoginForm(request.POST)
        if rec_form.is_valid():
            user_name = rec_form.cleaned_data['login']
            password = rec_form.cleaned_data['password']
            user = authenticate(username=user_name, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse('Nie udało się zalogować!')


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class Home(View):
    def get(self, request):
        return render(request, 'base.html')


class AddUserView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'create_user.html', {"form": form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['login'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            return redirect('/')


class UserDataViewCreate(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = UserData
    fields = ['age', 'height', 'weight', 'muscle_weight', 'fat_weight', 'metabolic_age',
              'chest_circuit', 'biceps_circuit', 'biceps_circuit_tight', 'buttock_circuit', 'thigh_circuit',
              'waist_circuit', 'calf_circuit']
    success_url = '/'

    def get(self, request):
        if UserData.objects.filter(owner=self.request.user):
            last = UserData.objects.filter(owner=self.request.user).latest('id')
            if last.date == date.today():
                return redirect(f"'userdata_edit/{last.pk}/'")
        return super().get(request)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        if UserData.objects.filter(owner=self.request.user):
            last_data = UserData.objects.filter(owner=self.request.user).latest('id')
            FIELDS = ['age', 'height', 'weight', 'muscle_weight', 'fat_weight', 'metabolic_age',
                      'chest_circuit', 'biceps_circuit', 'biceps_circuit_tight', 'buttock_circuit', 'thigh_circuit',
                      'waist_circuit', 'calf_circuit']
            dictionary = {}
            for field in FIELDS:
                dictionary[field] = getattr(last_data, field)
            return dictionary

class UserDataViewUpdate(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = UserData
    fields = ['age', 'height', 'weight', 'muscle_weight', 'fat_weight', 'metabolic_age',
                      'chest_circuit', 'biceps_circuit', 'biceps_circuit_tight', 'buttock_circuit', 'thigh_circuit',
                      'waist_circuit', 'calf_circuit']
    success_url = '/'

class ExerciseCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'Gym.add_exercise'
    model = Exercise
    fields = ['name', 'description', 'link']
    success_url = '/exercise_list/'

class ExerciseUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'Gym.update_exercise'
    model = Exercise
    fields = ['name', 'description', 'link']
    success_url = '/exercise_list/'


class ExerciseDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'Gym.delete_exercise'
    model = Exercise
    success_url = '/exercise_list/'

class ExerciseListView(PermissionRequiredMixin, View):
    permission_required = 'Gym.view_exercise'
    def get(self, request):
        exercises = Exercise.objects.all()
        return render(request, 'exercise_list.html', {"exercises": exercises})

