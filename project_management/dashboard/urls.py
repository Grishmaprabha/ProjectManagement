from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('addproject/', views.add_project, name='addproject'),
    path('updateproject/', views.update_project, name='updateproject'),
    path('deleteproject/', views.delete_project, name='deleteproject'),
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
    
    path('updateprofile/', views.update_profile, name='updateprofile'),
    
    path('activitylog/', views.activitylog, name='activitylog'),
    path('get_prj_data/', views.getprojectdata, name='get_prj_data'),
    
    path('get_list_data/', views.getlistdata, name='get_list_data'),
    path('get_task_data/', views.gettaskdata, name='get_task_data'),
    path('get_subtask_data/', views.getsubtaskdata, name='get_subtask_data'),
    path('get_chart_data/', views.getchartdata, name='get_chart_data'),
    path('get_piechart_data/', views.getpiechartdata, name='get_piechart_data'),
    
    path('get_tooltip_data/', views.gettooltipdata, name='get_tooltip_data'),  
    
    # path('schedule_email_reminder/', views.schedule_email_reminder, name='schedule_email_reminder'),
   
    
]
 