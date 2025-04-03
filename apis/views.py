from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .models import Todo, Team
from .serializers import TodoSerializer
from .serializers import TeamSerializer
import json
User = get_user_model()

@csrf_exempt
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    print("user", user, username, password)
    if user is not None:
        login(request, user)
        serializer = UserSerializer(user, many=False)
        return JsonResponse({'status': 'success', 'user': serializer.data})
    else:
        return JsonResponse({'status': 'fail', 'message': 'Invalid credentials'}, status=400)

@csrf_exempt
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    role = request.data.get('user_type')
    
    if not username or not password:
        return JsonResponse({'status': 'fail', 'message': 'Missing fields'}, status=400)
    
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'fail', 'message': 'Username already exists'}, status=400)
    user = User.objects.create_user(username=username, password=password, user_type=role)
    print("user", user, username, password)

    serializer = UserSerializer(user)
    return JsonResponse({'status': 'success', 'user': serializer.data})

@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data)

@csrf_exempt
@api_view(['POST'])
def create_todo(request):
    try:
        print("request", request.data)
        task = request.data.get('task')
        employee = request.data.get('employee')
        manager = request.data.get('manager')
        
        if not task or not employee:
            return JsonResponse({'status': 'fail', 'message': 'Missing fields'}, status=400)
        
        employee = User.objects.get(id=int(employee))
        manager = User.objects.get(id=int(manager))

        todo = Todo.objects.create(task=task, user_assigned_to=employee, user_assigned_by=manager)
        serializer = TodoSerializer(todo)
        return JsonResponse({'status': 'success', 'todo': serializer.data})
    except:
        return JsonResponse({'status': 'fail', 'message': 'Invalid employee'}, status=400)

@api_view(['GET'])
def list_todos(request):
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def list_employee_users(request):
    employees = User.objects.filter(user_type='employee')
    serializer = UserSerializer(employees, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_task_by_employee(request, employee_id):
    employee = User.objects.get(id=employee_id)
    todos = Todo.objects.filter(user_assigned_to=employee)
    serializer = TodoSerializer(todos, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@api_view(['POST'])
def update_todo_status(request, todo_id):
    print("request", request.data)
    try:
        status = request.data.get('status')
        print("status", status)
        if not status:
            return JsonResponse({'status': 'fail', 'message': 'Missing status field'}, status=400)
        
        todo = Todo.objects.get(id=todo_id)
        todo.status = status
        todo.save()
        
        serializer = TodoSerializer(todo)
        return JsonResponse({'status': 'success', 'todo': serializer.data})
    except Todo.DoesNotExist:
        return JsonResponse({'status': 'fail', 'message': 'Todo not found'}, status=404)
    except Exception as e:
        print("error", e)
        return JsonResponse({'status': 'fail', 'message': str(e)}, status=400)

@api_view(['GET'])
def get_users(request):
    exclude_user_id = request.GET.get('user_id')
    if exclude_user_id:
        users = User.objects.exclude(id=exclude_user_id)
    else:
        users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def delete_todo(request, todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
        return JsonResponse({'status': 'success', 'message': 'Todo deleted successfully'})
    except Todo.DoesNotExist:
        return JsonResponse({'status': 'fail', 'message': 'Todo not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'fail', 'message': str(e)}, status=400)

@api_view(['GET'])
def view_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user, many=False)
        return JsonResponse(serializer.data)
    except Exception as e:
        return JsonResponse({'status': 'fail', 'message': e})

@api_view(['POST'])
def create_team(request):
    try:
        manager_ids = request.data.get('manager', [])
        member_ids = request.data.get('employees', [])
        
        if not manager_ids or not member_ids:
            return JsonResponse({'status': 'fail', 'message': 'Missing manager or member IDs'}, status=400)
        
        # Convert string IDs to integers if they're coming as strings
        manager_ids = [int(id) for id in manager_ids]
        member_ids = [int(id) for id in member_ids]
        
        # Get managers and members using id__in
        managers = User.objects.filter(id__in=manager_ids)
        members = User.objects.filter(id__in=member_ids)
        print("managers", managers)
        print("members", members)
        
        # Create team and add relationships
        team = Team.objects.create()
        team.managers.set(managers)
        team.members.set(members)
        
        serializer = TeamSerializer(team)
        return JsonResponse({'status': 'success', 'team': serializer.data})
    except ValueError:
        return JsonResponse({'status': 'fail', 'message': 'Invalid ID format'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'fail', 'message': str(e)}, status=400)

@api_view(['GET'])
def get_managers(request):
    managers = User.objects.filter(user_type='manager')
    serializer = UserSerializer(managers, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_teams(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    print("teams", serializer.data)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_team_by_manager(request, manager_id):
    try:
        team = Team.objects.get(managers__in=[int(manager_id)])
        serializer = TeamSerializer(team)
        return JsonResponse(serializer.data, safe=False)
    except Team.DoesNotExist:
        return JsonResponse({'status': 'fail', 'message': 'Team not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'fail', 'message': str(e)}, status=400)

@api_view(['GET'])
def get_team_task(request, team_id):
    team = Team.objects.get(id=team_id)
    tasks = Todo.objects.filter(user_assigned_to__in=team.members.all())
    serializer = TodoSerializer(tasks, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def update_user_role(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.user_type = request.data.get('user_type')
        user.save()
        return JsonResponse({'status': 'success', 'message': 'User role updated successfully'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'fail', 'message': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'fail', 'message': str(e)}, status=400)

@api_view(['POST'])
def update_user_details(request, user_id):
    try:
        print("request", request.data)
        user = User.objects.get(id=user_id)
        if request.data.get('username') and User.objects.filter(username=request.data.get('username')).exclude(id=user_id).exists():
            return JsonResponse({'status': 'fail', 'message': 'Username already exists'}, status=400)
            
        if request.data.get('email') and User.objects.filter(email=request.data.get('email')).exclude(id=user_id).exists():
            return JsonResponse({'status': 'fail', 'message': 'Email already exists'}, status=400)
        user.username = request.data.get('username')
        user.email = request.data.get('email')
        user.save()
        serializer = UserSerializer(user)
        return JsonResponse({'status': 'success', 'user': serializer.data})
    except User.DoesNotExist:
        return JsonResponse({'status': 'fail', 'message': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'fail', 'message': str(e)}, status=400)

@api_view(['POST'])
def change_user_password(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')
        
        # Verify current password
        print("current_password", current_password)
        print("user.check_password", user.check_password(current_password))
        if not user.check_password(current_password):
            print("current password is incorrect")
            return JsonResponse({
                'status': 'fail',
                'message': 'Current password is incorrect'
            }, status=400)
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Password updated successfully'
        })
        
    except User.DoesNotExist:
        return JsonResponse({
            'status': 'fail',
            'message': 'User not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'fail',
            'message': str(e)
        }, status=400)

@api_view(['POST'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'User deleted successfully'
        })
    except User.DoesNotExist:
        return JsonResponse({
            'status': 'fail',
            'message': 'User not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'fail',
            'message': str(e)
        }, status=400)
    
@api_view(['POST'])
def delete_team(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
        team.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Team deleted successfully'
        })
    except Team.DoesNotExist:
        return JsonResponse({
            'status': 'fail',
            'message': 'Team not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'fail',
            'message': str(e)
        }, status=400)

@api_view(['POST'])
def edit_team_members(request, team_id):
    try:
        team = Team.objects.get(id=team_id)
        member_ids = request.data.get('employees', [])
        manager_ids = request.data.get('manager', [])
        print("request.data", request.data)
        # Update team members
        if member_ids:
            members = User.objects.filter(id__in=member_ids)
            team.members.clear()  # Clear existing members
            for member in members:
                team.members.add(member)
        
        # Update team managers
        if manager_ids:
            managers = User.objects.filter(id__in=manager_ids)
            team.managers.clear()  # Clear existing managers
            for manager in managers:
                team.managers.add(manager)
        
        team.save()
        serializer = TeamSerializer(team)
        return JsonResponse({
            'status': 'success',
            'message': 'Team members updated successfully',
            'team': serializer.data
        })
    except Team.DoesNotExist:
        return JsonResponse({
            'status': 'fail',
            'message': 'Team not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'fail',
            'message': str(e)
        }, status=400)






