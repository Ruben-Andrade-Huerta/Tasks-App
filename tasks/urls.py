from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),  # Ruta principal de tasks
    path('signup/', views.signup, name='signup'),  # Ruta para la vista de registro
    path('login/', views.login_view, name='login'),  # Ruta para la vista de inicio de sesión
    path('logout/', views.logout_view, name='logout'),  # Ruta para cerrar sesión
    path('tasks/', views.tasks, name='tasks'),  # Ruta para la vista de tareas
    path('tasks/create_task/', views.create_task, name='create_task'),  # Ruta para crear una tarea
    path('tasks/task_detail/<int:task_id>/', views.task_detail, name='task_detail'),  # Ruta para seleccionar una tarea(task_id) y modificarla 
    path('tasks/task_detail/<int:task_id>/delete', views.delete_task, name='delete_task'),  # Ruta para seleccionar una tarea(task_id) y modificarla 
    path('completed_tasks/', views.completed_tasks, name='completed_tasks'),  # Ruta para seleccionar una tarea(task_id) y modificarla 
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]
