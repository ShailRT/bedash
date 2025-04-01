from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user),
    path('users/', views.list_users),
    path('register/', views.register_user),
    path('create-todo/', views.create_todo),
    path('todos/', views.list_todos),
    path('get-employee/', views.list_employee_users),
    path('employee-todos/<int:employee_id>/', views.get_task_by_employee),
    path('update-todo-status/<int:todo_id>/', views.update_todo_status),
    path('get-users/', views.get_users),
    path('delete-todo/<int:todo_id>/', views.delete_todo),
    path('profile/<int:id>/', views.view_profile),
    path('create-team/', views.create_team),
    path('get-managers/', views.get_managers),
    path('get-teams/', views.get_teams),
    path('get-team-by-manager/<int:manager_id>/', views.get_team_by_manager),
    path('get-team-tasks/<int:team_id>/', views.get_team_task),
    path('update-user-role/<int:user_id>/', views.update_user_role),
    path('update-user-details/<int:user_id>/', views.update_user_details),
    path('change-password/<int:user_id>/', views.change_user_password),
    path('delete-user/<int:user_id>/', views.delete_user),
    path('delete-team/<int:team_id>/', views.delete_team),
    path('update-team/<int:team_id>/', views.edit_team_members)
]
