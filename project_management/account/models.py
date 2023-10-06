from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class CustomUser(AbstractUser):
    role_choice = (
        ('mngr', 'Manager'),
        ('user', 'User')
    )
    role = models.CharField(max_length=20, choices=role_choice, default='user')

    def __str__(self):
        return self.username



class User(AbstractUser):
    is_admin = models.BooleanField('Is admin', default=False)
    is_user = models.BooleanField('Is user', default=False)
    is_mngr = models.BooleanField('Is manager', default=False)
    
    # Defined related_nameto avoid clashes in groups and user_permissions
    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users')
    

    


