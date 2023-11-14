from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
# Importar formulario de Task
from .forms import TaskForm
from .models import Task
from django.utils import timezone
# Porteger las rutas
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'home.html')
# Crete user
def signup(request):
    if request.method=='GET':
        return render(request, 'signup.html', {'form':UserCreationForm})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                # Register user
                user=User.objects.create_user(username=request.POST['username'], password=request.POST["password1"])
                user.save()
                # Sesión del usuario
                login(request,user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        return render(request, 'signup.html',{
            'form':UserCreationForm,
            'error':'Password don not match'
        })
    
# Tareas NO completadas    
# Debe estar logueado para ver las tareas
@login_required
def tasks(request):
    # Traer todas las tareas del usuario que está logueado. (Mostrar las tareas que datecompleted no sea vacío es decir que se hayan completado)
    tasks=Task.objects.filter(user=request.user, datecompleted__isnull=True).order_by('-created')
    # Le pasamos las tareas al front
    return render(request, 'tasks.html', {'tasks':tasks, 'title':'Task pending'})

# Tareas completadas
# Debe estar logueado para ver las tareas completadas
@login_required
def tasks_completed(request):
    # Traer todas las tareas del usuario que está logueado. (Mostrar las tareas que datecompleted no sea vacío es decir que se hayan completado)
    tasks=Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    # Le pasamos las tareas al front
    return render(request, 'tasks.html', {'tasks':tasks, 'title':'Task completed'})

# Debe estar logueado para crear tareas
@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html',{
        'form':TaskForm
    })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'create_task.html',{
            'form':TaskForm,
            'error':'Please provide valid data'
            })

# Debe estar logueado para ver el detalle de las tareas
@login_required      
def task_detail(request, task_id):
    if request.method == 'GET':
        print(task_id)
        # Con task.objects al momento de pasar una tarea que no existe, se cae el servidor.
        # task=Task.objects.get(pk=task_id)
        # Por eso utilizamos get_object_or_404 desde django shortcuts
        # Debo agregar user=request.user para que solo el usuario logueado pueda modificar sus tareas.
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        # Enviamos task a task_detail
        return render(request, 'task_detail.html',{'task':task, 'form':form})
    else:
        try:
            # Debo agregar user=request.user para que solo el usuario logueado pueda modificar sus tareas.
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html',{'task':task, 'form':form, 'error': "Error updating task"})

# Debe estar logueado para poner una tarea pendiente en completa
@login_required 
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method=='POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    
# Debe estar logueado para poner una tarea completa en pendiente
@login_required 
def pending_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method=='POST':
        task.datecompleted = None
        task.save()
        return redirect('tasks')
    
# Debe estar logueado para eliminar una tarea
@login_required 
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method=='POST':
        task.delete()
        return redirect('tasks')
    
# Debe estar logueado para desloguearse
@login_required 
# Logout
def signout(request):
    logout(request)
    return redirect('home')

# Signin
def signin(request):
    if request.method=='GET':
        return render(request, 'signin.html',{
            'form':AuthenticationForm
        })
    else:
        # Validar que el usuario exista
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # Si user está vacío es por que no encontró ninguno válido
        if user is None:
            return render(request, 'signin.html', {
                'form':AuthenticationForm,
                'error':'Username or password is incorrect'
            })
        else:
            # Guardamos la sesión
            login(request, user)
            return redirect('tasks')