from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('addproject/', views.add_project, name='addproject'),
    path('updateproject/', views.update_project, name='updateproject'),
    path('deleteproject/', views.delete_project, name='deleteproject'),
    path('updatetable/', views.update_table, name='updatetable'),
    path('getupdatedata/', views.update_data, name='getupdatedata'),
    
    path('addlist/', views.add_list, name='addlist'),
    path('updatelist/', views.update_list, name='updatelist'),
    path('deletelist/', views.delete_list, name='deletelist'),
    
    path('getlist/', views.get_list, name='getlist'),
    path('addtask/', views.add_task, name='addtask'),
    path('getupdatelistdata/', views.updatelist_data, name='getupdatelistdata'),
    path('updatetask/', views.update_task, name='updatetask'),
    path('deletetask/', views.delete_task, name='deletetask'),
    
    path('addsubtask/', views.add_subtask, name='addsubtask'),
    path('updatesubtask/', views.update_subtask, name='updatesubtask'),    
    path('deletesubtask/', views.delete_subtask, name='deletesubtask'),
    
    
    
    
    
]
    # path('', views.index, name= 'index'),
    # path('login/', views.login_view, name='login'),
    # path('register/', views.register, name='register'),
    # path('logout/', views.logout_view, name='logout'),
    # path('home/', views.home, name='home'),
 