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
    path('tasks/create/', login_required(views.create_task), name='create_task'),
    path('tasks/update/<int:task_id>/', login_required(views.update_task), name='update_task'),
    path('tasks/delete/<int:task_id>/', login_required(views.delete_task), name='delete_task'),
    path('settings/', login_required(views.settings), name='settings'),
    path('task/end-task/<int:task_id>/', login_required(views.end_task), name='end_task'),
    path('admin-panel/', login_required(views.admin_panel), name='admin_panel'),
    path('admin-panel/delete/<int:person_id>/',
         login_required(views.admin_panel_delete_person),
         name='admin_panel_delete'
         ),
    path('admin-panel/profile/<int:person_id>/',
         login_required(views.person_profile),
         name='person_profile'
         )

]
