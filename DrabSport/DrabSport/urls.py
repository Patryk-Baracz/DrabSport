from django.contrib import admin
from django.urls import path, include
from Gym.views import LoginUserView, LogoutUserView, Home, AddUserView, UserDataViewCreate, ExerciseCreateView, \
    ExerciseUpdateView, ExerciseDeleteView, ExerciseListView, UserDataViewUpdate, TrainingPlanCreateView, UserListView, \
    UserPlanListView, TrainingPlanDetailView, ExerciseSetAddView, ExerciseDetailView, ExerciseSetEditView, \
    ExerciseSetDeleteView, TrainingPlanHistoryView, UserTrainingList, UserTraining

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
    path('exercise_set_edit/<int:pk>/', ExerciseSetEditView.as_view()),
    path('exercise_set_delete/<int:pk>/', ExerciseSetDeleteView.as_view()),
    path('user_plan_history/<int:pk>/', TrainingPlanHistoryView.as_view()),
    path('user_training_list/', UserTrainingList.as_view()),
    path('user_training/<int:pk>/', UserTraining.as_view()),
    path('api_exerciseset/', include('Gym.urls')),


]
