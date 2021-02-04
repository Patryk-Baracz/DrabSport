from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import UserData, Exercise, TrainingPlan, ExerciseSet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import LoginForm, CreateUserForm, ExerciseSetForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from datetime import date


class LoginUserView(View):
    """Logging screen."""

    def get(self, request):
        """Two fields to fill: 'login' and 'password'."""

        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        """Checking database for user with filled login and password."""

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
    """Logging out current user."""

    def get(self, request):
        logout(request)
        return redirect('/')


class Home(View):
    def get(self, request):
        if request.user.has_perm('Gym.add_exercise'):
            return render(request, 'base.html', {"trainer": True})
        return render(request, 'base.html')


class AddUserView(View):
    """Registration new user."""

    def get(self, request):
        """Form to fill."""

        form = CreateUserForm()
        return render(request, 'create_user.html', {"form": form})

    def post(self, request):
        """If form is valid, adding new user to database."""

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
    """Adding users body parameters to database"""

    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = UserData
    fields = ['age', 'height', 'weight', 'muscle_weight', 'fat_weight', 'metabolic_age',
              'chest_circuit', 'biceps_circuit', 'biceps_circuit_tight', 'buttock_circuit', 'thigh_circuit',
              'waist_circuit', 'calf_circuit']
    success_url = '/'

    def get(self, request):
        """ Checking if user already added data today."""

        if UserData.objects.filter(owner=self.request.user):
            last = UserData.objects.filter(owner=self.request.user).latest('id')
            if last.date == date.today():
                return redirect(f"/userdata_update/{last.pk}/")
        return super().get(request)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        """Form is filled with latest data of logged user."""

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
    """If user already added body parameters today, he edit those data nor create new."""

    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = UserData
    fields = ['age', 'height', 'weight', 'muscle_weight', 'fat_weight', 'metabolic_age',
              'chest_circuit', 'biceps_circuit', 'biceps_circuit_tight', 'buttock_circuit', 'thigh_circuit',
              'waist_circuit', 'calf_circuit']
    success_url = '/'


class ExerciseCreateView(PermissionRequiredMixin, CreateView):
    """Adding new exercise objects to database."""

    permission_required = 'Gym.add_exercise'
    model = Exercise
    fields = ['name', 'description', 'link']
    success_url = '/exercise_list/'


class ExerciseUpdateView(PermissionRequiredMixin, UpdateView):
    """Editing exercise objects in database."""

    permission_required = 'Gym.update_exercise'
    model = Exercise
    fields = ['name', 'description', 'link']
    success_url = '/exercise_list/'


class ExerciseDeleteView(PermissionRequiredMixin, DeleteView):
    """Removing an exercise object from database."""

    permission_required = 'Gym.delete_exercise'
    model = Exercise
    success_url = '/exercise_list/'


class ExerciseListView(PermissionRequiredMixin, View):
    """List of all exercise objects in database."""

    permission_required = 'Gym.view_exercise'

    def get(self, request):
        exercises = Exercise.objects.all()
        return render(request, 'exercise_list.html', {"exercises": exercises})


class TrainingPlanCreateView(PermissionRequiredMixin, CreateView):
    """Adding training plan for a specific user to databse."""

    permission_required = 'Gym.add_trainingplan'
    model = TrainingPlan
    fields = ['name']

    def get_success_url(self, **kwargs):
        """Redirecting to get after successful adding plan."""

        next = self.request.POST.get('next', '/')
        return next

    def get_context_data(self, **kwargs):
        """Allowing to see all training plans for specyfic user."""

        context = super().get_context_data(**kwargs)
        context['plans'] = TrainingPlan.objects.filter(user=User.objects.get(pk=self.kwargs.get('pk')))
        return context

    def form_valid(self, form, **kwargs):
        form.instance.user = User.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)


class UserListView(PermissionRequiredMixin, View):
    """ List of all users. """

    permission_required = 'Gym.view_user'

    def get(self, request):
        users = User.objects.all()
        return render(request, 'user_list.html', {"users": users})


class UserPlanListView(LoginRequiredMixin, View):
    """ List of all training plans of specific user. """

    def get(self, request, pk):
        plans = TrainingPlan.objects.filter(user=pk)
        userplan = User.objects.get(pk=pk)
        return render(request, 'user_plan_list.html', {"plans": plans, "userplan": userplan})


class TrainingPlanDetailView(LoginRequiredMixin, View):
    """Shows exercises, reps, etc. in specific training plan."""

    def get(self, request, pk):
        plan = TrainingPlan.objects.get(pk=pk)
        exercise_set = ExerciseSet.objects.filter(training_plan=plan, start_date__lte=date.today()).exclude(
            finish_date__lte=date.today())
        return render(request, 'trainingplan_detail.html', {"plan": plan, "exerciseset": exercise_set})


class ExerciseSetAddView(PermissionRequiredMixin, CreateView):
    """Adding exercises with details to specific training plan"""

    permission_required = 'Gym.add_exerciseset'
    model = ExerciseSet
    fields = ['exercise', 'exercise_rounds', 'exercise_reps', 'exercise_weight', 'start_date']

    def get_success_url(self, **kwargs):
        next = self.request.POST.get('next', '/')
        return next

    def get_context_data(self, **kwargs):
        """Catching context for training plan detail view."""

        context = super().get_context_data(**kwargs)
        context['plan'] = TrainingPlan.objects.get(pk=self.kwargs.get('pk'))
        context['exerciseset'] = ExerciseSet.objects.filter(
            training_plan=TrainingPlan.objects.get(pk=self.kwargs.get('pk')), start_date__lte=date.today()).exclude(
            finish_date__lte=date.today())
        return context

    def form_valid(self, form, **kwargs):
        form.instance.user = TrainingPlan.objects.get(pk=self.kwargs.get('pk')).user
        form.instance.training_plan = TrainingPlan.objects.get(pk=self.kwargs.get('pk'))
        return super().form_valid(form)


class Trainer(PermissionRequiredMixin, View):
    """Home page just for trainer."""

    permission_required = 'Gym.add_exercise'

    def get(self, request):
        return render(request, 'trainer.html')


class ExerciseDetailView(LoginRequiredMixin, View):
    """Showing name, description and link to YouTube of an exercise."""

    def get(self, request, pk):
        exercise = Exercise.objects.get(pk=pk)
        return render(request, 'exercise_detail.html', {"exercise": exercise})

    # def get_success_url(self, **kwargs):
    #     next = self.request.POST.get('next', '/')
    #     return next


class ExerciseSetEditView(PermissionRequiredMixin, View):
    """Creating new exerciseset object with changed data."""

    permission_required = 'Gym.add_exerciseset'

    def get(self, request, pk):
        """Fills edited exerciseset details into form"""

        ex_exercise_set = ExerciseSet.objects.get(pk=pk)
        exercise_name = ex_exercise_set.exercise.name
        form = ExerciseSetForm(instance=ex_exercise_set)
        plan = ex_exercise_set.training_plan
        exerciseset = ExerciseSet.objects.filter(training_plan=plan, start_date__lte=date.today()).exclude(
            finish_date__lte=date.today())
        return render(request, 'Gym/exerciseset_form.html',
                      {'form': form, 'plan': plan, 'exerciseset': exerciseset, 'exercise_name': exercise_name})

    def post(self, request, pk):
        ex_exercise_set = ExerciseSet.objects.get(pk=pk)
        form = ExerciseSetForm(request.POST)
        if form.is_valid():
            ExerciseSet.objects.create(
                user=ex_exercise_set.user,
                training_plan=ex_exercise_set.training_plan,
                exercise=form.cleaned_data['exercise'],
                exercise_reps=form.cleaned_data['exercise_reps'],
                exercise_rounds=form.cleaned_data['exercise_rounds'],
                exercise_weight=form.cleaned_data['exercise_weight'],
                start_date=form.cleaned_data['start_date'],
                finish_date=None
            )
            ex_exercise_set.finish_date = form.cleaned_data['start_date']
            ex_exercise_set.save()
            return redirect(f'/user_plan_detail/{ex_exercise_set.training_plan.pk}')


class ExerciseSetDeleteView(PermissionRequiredMixin, View):
    """Removing Exercise from training plan."""

    permission_required = 'Gym.delete_exerciseset'

    def get(self, request, pk):
        ex_exercise_set = ExerciseSet.objects.get(pk=pk)
        plan = ex_exercise_set.training_plan
        exerciseset = ExerciseSet.objects.filter(training_plan=plan, start_date__lte=date.today()).exclude(
            finish_date__lte=date.today())
        exercise_name = ExerciseSet.objects.get(pk=pk).exercise.name
        warning = f'Jeśteś pewny, że chcesz usunąć {exercise_name} z treningu?'
        return render(request, 'trainingplan_detail.html',
                      {'warning': warning, 'plan': plan, 'exerciseset': exerciseset})

    def post(selfself, request, pk):
        """Setting finish date of Exerciseset on today so it isn't listed in actual training anymore."""

        ex_exercise_set = ExerciseSet.objects.get(pk=pk)
        ex_exercise_set.finish_date = date.today()
        ex_exercise_set.save()
        return redirect(f'/user_plan_detail/{ex_exercise_set.training_plan.pk}')


class TrainingPlanHistoryView(PermissionRequiredMixin, View):
    """Presenting all variants of all training plans for a user sorted by date."""

    permission_required = 'Gym.create_exerciseset'

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        exercise_sets = ExerciseSet.objects.filter(user=user)
        training_plans = TrainingPlan.objects.filter(user=user)
        exercise_sets_by_plan = {}
        for training in training_plans:
            training_exercise_sets = exercise_sets.filter(training_plan=training)
            date_list = []
            exercise_set_by_date = {}
            for e_set in training_exercise_sets:
                date_list.append(e_set.start_date)
                if e_set.finish_date:
                    date_list.append(e_set.finish_date)
            date_list = sorted(list(set(date_list)), reverse=True)
            for date in date_list:
                exercise_set_by_date[f'{date}'] = training_exercise_sets.filter(
                    start_date__lte=date).exclude(
                    finish_date__lte=date)
            exercise_sets_by_plan[f'{training.name}'] = exercise_set_by_date
        return render(request, 'user_plan_list_history.html',
                      {"userplan": user, "exercise_sets_by_plan": exercise_sets_by_plan})


class UserTrainingList(LoginRequiredMixin, View):
    """List of actual trainings for user."""

    def get(self, request):
        plans = TrainingPlan.objects.filter(user=request.user)
        return render(request, 'user_training_list.html', {"plans": plans})


class UserTraining(LoginRequiredMixin, View):
    """Details of chosen workout for user."""

    def get(self, request, pk):
        plan = TrainingPlan.objects.get(pk=pk)
        exercise_set = ExerciseSet.objects.filter(training_plan=plan, start_date__lte=date.today()).exclude(
            finish_date__lte=date.today())
        return render(request, 'user_training.html', {'exerciseset': exercise_set})
