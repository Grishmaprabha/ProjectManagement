from django.db import models
from account.models import CustomUser
from django.utils import timezone

# Create your models here.

class Project(models.Model):

    title = models.CharField(max_length=100,null=False)
    description = models.TextField(blank=True)
    startdate = models.DateField()
    enddate = models.DateField()    
    status = models.CharField(max_length=12, default='Pending')
    user = models.ManyToManyField(CustomUser, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
    


class List(models.Model):
    list = models.CharField(max_length=250)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='lists')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.title
    

class Task(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=12,  default='Pending')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    task_list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.title


class Subtask(models.Model):
    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=12, default='Pending')
    due_date = models.DateField()
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.title
    
class ActivityLog(models.Model):
    
    action = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True,)
    details = models.TextField()
    