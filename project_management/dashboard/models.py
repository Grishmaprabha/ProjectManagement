from django.db import models
from account.models import User,CustomUser
from django.utils import timezone

# Create your models here.

class Project(models.Model):
    
    status_choice = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    )

    duration_choice = (
        ('Hours', 'Hours'),
        ('Days', 'Days')
    )

    title = models.CharField(max_length=100,null=False)
    description = models.TextField(blank=True)
    startdate = models.DateField()
    enddate = models.DateField()    
    status = models.CharField(max_length=12, choices=status_choice, default='Pending')
    user = models.ManyToManyField(CustomUser, related_name='projects')
    # user = models.ForeignKey(User, on_delete=models.CASCADE) 
    # user = models.ManyToManyField(User, related_name='projects', blank=True)
    # totalduration = models.DecimalField(max_digits=5, decimal_places=2)
    # durationunit = models.CharField(max_length=6, choices=duration_choice, default='Hours')
    

    def __str__(self):
        return self.title
    


class List(models.Model):
    list = models.CharField(max_length=250)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='lists')

    def __str__(self):
        return self.title
    

class Task(models.Model):
    status_choices = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=12, choices=status_choices, default='Pending')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    task_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.title


class Subtask(models.Model):
    status_choices = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=12, choices=status_choices, default='Pending')
    due_date = models.DateField()
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')

    def __str__(self):
        return self.title
    
class ActivityLog(models.Model):
    ACTION_CHOICES = (
        ('Task Created', 'Task Created'),
        ('Task Updated', 'Task Updated'),
        ('Task Deleted', 'Task Deleted'),
        # Add more choices for other actions
    )

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.TextField()
    