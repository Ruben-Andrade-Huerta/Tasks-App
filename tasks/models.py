from django.db import models

# Create your models here.
class Task(models.Model):
    # Definir las opciones para el campo priority
    PRIORITY_CHOICES = [
        ('H', 'High'),      # Alta prioridad
        ('M', 'Medium'),    # Prioridad media
        ('L', 'Low'),       # Baja prioridad
    ]
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField(null = True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    terminated_at = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default='M',  # Valor por defecto
    )
    # Relación con el modelo User
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title 