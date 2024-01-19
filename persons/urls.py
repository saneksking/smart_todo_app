from django.contrib.auth.decorators import login_required
from django.urls import path
from persons import views


app_name = 'persons'

urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('tasks/', login_required(views.task_list), name='task_list'),
]
