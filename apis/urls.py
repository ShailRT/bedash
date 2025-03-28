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
]
