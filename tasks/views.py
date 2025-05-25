from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.utils.timezone import now
from .forms import CustomUserCreationForm, CustomAuthenticationForm  # Importa tu formulario personalizado
from django.db.models import Case, When, Value, IntegerField

# Create your views here.

def index(request):
    return render(request, 'files/index.html')

def signup(request):
    
    if request.method == 'GET':
        return render(request, 'files/signup.html', {
            'form': CustomUserCreationForm()
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                #Intenta guardar el usuario en la base de datos
                # Si el nombre de usuario ya existe, lanzará una excepción
                user = User.objects.create_user(
                    username=request.POST['username'],  
                    password=request.POST['password1'],
                    email=request.POST['email']
                )
                user.save()
                login(request, user)  # Inicia sesión automáticamente al crear la cuenta
                return redirect('index')
            except IntegrityError:
                # Si ocurre una excepción, significa que el nombre de usuario ya existe
                # Devuelve el formulario con un mensaje de error
                return render(request, 'files/signup.html', {
                    'form': CustomUserCreationForm(),
                    'error': 'El nombre de usuario ya existe'
                })
        else:
            return render(request, 'files/signup.html', {
                'form': CustomUserCreationForm(),
                'error': 'Las contraseñas no coinciden'
            })

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'files/login.html', {
        'form': CustomAuthenticationForm()
        })
    else: 
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'files/login.html', {
                'form': CustomAuthenticationForm(),
                'error': 'Nombre de usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            # Imprime los datos del usuario en la consola
            return redirect('index')

@login_required
def tasks(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.terminated_at = now()
        task.save()
    user_tasks = Task.objects.filter(
    user=request.user, terminated_at__isnull=True
).annotate(
    priority_order=Case(
        When(priority='H', then=Value(1)),
        When(priority='M', then=Value(2)),
        When(priority='L', then=Value(3)),
        default=Value(4),
        output_field=IntegerField(),
    )
).order_by('priority_order')  # Filtra las tareas por el usuario actual y las ordena por prioridad
    return render(request, 'files/tasks.html', {
        'tasks': user_tasks
    })
    
@login_required
def create_task(request):
    if request.method == 'GET':
        form  = TaskForm() 
        return render(request, 'files/create_task.html', {
            'form': form
        })
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit = False)# Crea la instancia del modelo pero no la guarda aún
            task.user = request.user  # Asigna el usuario actual a la tarea
            task.save()  # Guarda la tarea en la base de datos
            return redirect('tasks')  # Redirige a la lista de tareas
        else:
            return render(request, 'files/create_task.html', {'form': form, 'error': 'Error al crear la tarea'})
        
@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Obtiene la tarea del usuario actual
    if request.method == 'GET':
        form = TaskForm(instance=task)# Pre-rellena el formulario con los datos de la tarea
        return render(request, 'files/update_task.html', {
            form
        })
        
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':    
        task = get_object_or_404(Task, id=task_id, user=request.user)# Obtiene la tarea del usuario actual
        form = TaskForm(instance=task)
        return render(request, 'files/task_detail.html', {
            'form': form,
            'task': task
        })
    else: 
        task = get_object_or_404(Task, id=task_id, user=request.user)# Obtiene la tarea del usuario actual
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit = False)# Crea la instancia del modelo pero no la guarda aún
            task.user = request.user  # Asigna el usuario actual a la tarea
            task.save()  # Guarda la tarea en la base de datos
            return redirect('tasks')  # Redirige a la lista de tareas
        else:
            return render(request, 'files/task_detail.html', {'form': form, 'error': 'Error al modificar la tarea'})
        

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id = task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
@login_required
def completed_tasks(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.terminated_at = None
        task.save()
        return redirect('completed_tasks')
    completed = Task.objects.filter(user=request.user, terminated_at__isnull=False)
    return render(request, 'files/completed_tasks.html', {
        'tasks':completed
    })