from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .models import Todo
from .serializers import TodoSerializer
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
        serializer = UserSerializer(user)
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
        task = request.data.get('task')
        employee = request.data.get('employee')
        
        if not task or not employee:
            return JsonResponse({'status': 'fail', 'message': 'Missing fields'}, status=400)
        
        employee = User.objects.get(id=int(employee))
        todo = Todo.objects.create(task=task, user_assigned_to=employee)
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



