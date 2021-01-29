"""DrabSport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Gym.views import LoginUserView, LogoutUserView, Home, AddUserView, UserDataViewCreate, ExerciseCreateView, \
    ExerciseUpdateView, ExerciseDeleteView, ExerciseListView, UserDataViewUpdate, TrainingPlanCreateView, UserListView, \
    UserPlanListView, TrainingPlanDetailView, ExerciseSetAddView, ExerciseDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginUserView.as_view()),
    path('logout/', LogoutUserView.as_view()),
    path('', Home.as_view()),
    path('create_user/', AddUserView.as_view()),
    path('user_data/', UserDataViewCreate.as_view()),
    path('exercise_add/', ExerciseCreateView.as_view()),
    path('exercise_edit/<int:pk>/', ExerciseUpdateView.as_view()),
    path('exercise_delete/<int:pk>/', ExerciseDeleteView.as_view()),
    path('exercise_list/', ExerciseListView.as_view()),
    path('userdata_update/<int:pk>/', UserDataViewUpdate.as_view()),
    path('training_create/<int:pk>/', TrainingPlanCreateView.as_view()),
    path('user_plan_list/<int:pk>/', UserPlanListView.as_view()),
    path('user_list/', UserListView.as_view()),
    path('user_plan_detail/<int:pk>/', TrainingPlanDetailView.as_view()),
    path('exercise_set_add/<int:pk>/', ExerciseSetAddView.as_view()),
    path('exercise_detail/<int:pk>/', ExerciseDetailView.as_view()),

]
