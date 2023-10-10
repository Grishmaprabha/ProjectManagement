from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from account.models import CustomUser
from dashboard.models import Project,List,Task,Subtask
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse,HttpResponse
from django.core.mail import send_mail
from datetime import datetime, timedelta
import ssl

from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.utils import timezone
# from project_management.settings import EMAIL_HOST_USER

import smtplib
from email.mime.text import MIMEText


from django.core.mail import send_mail






# Create your views here.

# def view_project(request):
#     import pdb;pdb.set_trace();
#     list_data = Project.objects.all()
#     return render(request, 'home.html',  {'list_data':list_data})


def add_project(request):
    # import pdb;pdb.set_trace();
    try:
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            startdate = request.POST.get('stardate')
            enddate = request.POST.get('enddate')
            status = request.POST.get('status')
            checkedValues = request.POST.getlist('checkedValues[]')
            
            if title == '':
                return JsonResponse({'status': '-1' , 'message': 'Title cannot be empty'})
            prj_name = Project.objects.filter(title=title)
            if prj_name:
                return JsonResponse({'status': '-2' ,'message': 'Title already exist'}) 
            
            current_date = datetime.now().date()
            formatted_date = current_date.strftime('%Y-%m-%d')
            
            if startdate == '':
                startdate = formatted_date
            if enddate == '':
                enddate = formatted_date  
                
            if enddate < startdate:
                return JsonResponse({'status': '-3' , 'message': 'End date cannot be earlier than the start date'})               
                        
            
            project = Project.objects.create(title=title,
                                            description=description,
                                            startdate=startdate,
                                            enddate=enddate,
                                            status=status)
            project.user.set(checkedValues)
            
                        
            return JsonResponse({'status': '1' ,'message': 'Data saved successfully'})
        else:
            return JsonResponse({'status': '2' , 'message': 'Data save unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    


def update_project(request):
    try:
        # import pdb;pdb.set_trace();
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            startdate = request.POST.get('stardate')
            enddate = request.POST.get('enddate')
            status = request.POST.get('status')
            checkedValues = request.POST.getlist('checkedValues[]')
            id = request.POST.get('id')
            
            if title == '':
                return JsonResponse({'status': '-1' , 'message': 'Title cannot be empty'})
         
            
            current_date = datetime.now().date()
            formatted_date = current_date.strftime('%Y-%m-%d')
            
            if startdate == '':
                startdate = formatted_date
            if enddate == '':
                enddate = formatted_date  
            
            if enddate < startdate:
                return JsonResponse({'status': '-2' , 'message': 'Title cannot be empty'})   
            
            project = Project.objects.filter(id=id).update(
                                                    title=title,
                                                    description=description,
                                                    startdate=startdate,
                                                    enddate=enddate,
                                                    status=status
                                                )

            project = Project.objects.get(id=id)
            project.user.set(checkedValues)
            
                        
            return JsonResponse({'status': '1' ,'message': 'Data updated successfully'})
        else:
            return JsonResponse({'status': '-1' , 'message': 'Update unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    

def delete_project(request):
    try:
        # import pdb;pdb.set_trace();
        if request.method == 'POST':
            id = request.POST.get('id')         
            
            Project.objects.filter(id=id).delete()                        
            return JsonResponse({'status': '1' ,'message': 'Data deleted successfully'})
        else:
            return JsonResponse({'status': '-1' , 'message': 'Delete unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    
def update_table(request):
    # import pdb;pdb.set_trace()
    try:
        updated_list = Project.objects.all().values('id','title','description','startdate','enddate','status','user')
        return JsonResponse({'data':updated_list})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    
def update_data(request):
    try:
        # import pdb;pdb.set_trace();
        id = request.POST.get('id')
        project = Project.objects.get(id=id)
        users = project.user.all()  # Retrieve all associated users
        user_ids = [user.id for user in users]
        print(user_ids)
        return JsonResponse({'status': '1' , 'users':user_ids})          
        
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    


def add_list(request):
    # import pdb;pdb.set_trace();
    try:
        if request.method == 'POST':
            project = request.POST.get('project')
            list_data = request.POST.get('list')
            
            
            if list_data == '' or project == ' ':
                return JsonResponse({'status': '-1' , 'message': 'List/Project cannot be empty'})
            list_chk = List.objects.filter(list=list_data)
            if list_chk:
                return JsonResponse({'status': '-2' ,'message': 'List name already exist'})
            
            project_instance = Project.objects.get(id=project)                          
            
            List.objects.create(list=list_data,project=project_instance)            
                        
            return JsonResponse({'status': '1' ,'message': 'Data saved successfully'})
        else:
            return JsonResponse({'status': '2' , 'message': 'Data save unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})

def update_list(request):
    try:
        # import pdb;pdb.set_trace();
        if request.method == 'POST':
            list_data = request.POST.get('list')
            project = request.POST.get('project')
            id = request.POST.get('id')
            
            if list_data == '':
                return JsonResponse({'status': '-1' , 'message': 'List cannot be empty'})
            
            project_instance = Project.objects.get(id=project)                          
            
            List.objects.filter(id=id).update(list=list_data,project=project_instance)            
            
                        
            return JsonResponse({'status': '1' ,'message': 'Data updated successfully'})
        else:
            return JsonResponse({'status': '-1' , 'message': 'Update unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    

def delete_list(request):
    try:
        # import pdb;pdb.set_trace();
        if request.method == 'POST':
            id = request.POST.get('id')         
            
            List.objects.filter(id=id).delete()                        
            return JsonResponse({'status': '1' ,'message': 'Data deleted successfully'})
        else:
            return JsonResponse({'status': '-1' , 'message': 'Delete unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
   
def get_list(request):
    # import pdb;pdb.set_trace();
    try:
        val = request.GET.get('prj_id')
        data = List.objects.filter(project=val).values('id','list')    
        data_list = list(data)     
        return JsonResponse({ 'data': data_list})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
        
    

def add_task(request):
    # import pdb;pdb.set_trace();
    try:
        if request.method == 'POST':
            project = request.POST.get('project')
            list_data = request.POST.get('list')
            title = request.POST.get('title')
            description = request.POST.get('description')
            duedate = request.POST.get('duedate')
            status = request.POST.get('status')
            
            if project == '':
                return JsonResponse({'status': '-1' , 'message': 'Project cannot be empty'})
            task_name = Task.objects.filter(title=title)
            if task_name:
                return JsonResponse({'status': '-2' ,'message': 'List name already exist'}) 
            
            if duedate == '':
                return JsonResponse({'status': '-3' , 'message': 'Due date cannot be empty'})
            if title == '':
                return JsonResponse({'status': '-4' , 'message': 'Title cannot be empty'})
                          
                        
            project_instance = Project.objects.get(id=project)  
            list_instance = List.objects.get(id=list_data)                        
            
            Task.objects.create(title=title,description=description,due_date=duedate,status=status,project=project_instance,task_list=list_instance)  
            
                        
            return JsonResponse({'status': '1' ,'message': 'Data saved successfully'})
        else:
            return JsonResponse({'status': '2' , 'message': 'Data save unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    

    
def updatelist_data(request):
    try:
        # import pdb;pdb.set_trace();
        id = request.POST.get('id')
        task = Task.objects.filter(id=id).values('task_list')
        print(task)
        task = task[0]['task_list']
        # list_data = List.objects.get(id=task).list
        list_data = List.objects.filter(id=task).values('id','list')
        return JsonResponse({'status': '1' , 'task':list_data[0],'task_id':task})          
        
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    
    

def update_task(request):
    try:
        # import pdb;pdb.set_trace();
        if request.method == 'POST':
            project = request.POST.get('project')
            list_data = request.POST.get('list')
            title = request.POST.get('title')
            description = request.POST.get('description')
            duedate = request.POST.get('duedate')
            status = request.POST.get('status')
            id = request.POST.get('id')
            
            if title == '':
                return JsonResponse({'status': '-1' , 'message': 'Title cannot be empty'})
            if list_data == '':
                return JsonResponse({'status': '-1' , 'message': 'List cannot be empty'})
            project_instance = Project.objects.get(id=project)  
            list_instance = List.objects.get(id=list_data) 
            
            Task.objects.filter(id=id).update(title=title,description=description,due_date=duedate,status=status,project=project_instance,task_list=list_instance)            
            
                        
            return JsonResponse({'status': '1' ,'message': 'Data updated successfully'})
        else:
            return JsonResponse({'status': '-1' , 'message': 'Update unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    

def delete_task(request):
    try:
        # import pdb;pdb.set_trace();
        if request.method == 'POST':
            id = request.POST.get('id')         
            
            Task.objects.filter(id=id).delete()                        
            return JsonResponse({'status': '1' ,'message': 'Data deleted successfully'})
        else:
            return JsonResponse({'status': '-1' , 'message': 'Delete unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    
    
def add_subtask(request):
    # import pdb;pdb.set_trace();
    try:
        if request.method == 'POST':
            task = request.POST.get('task')
            title = request.POST.get('title')
            description = request.POST.get('description')
            duedate = request.POST.get('duedate')
            status = request.POST.get('status')
            
            if task == '':
                return JsonResponse({'status': '-1' ,'message': ' cannot be empty'}) 
            
            if title == '':
                return JsonResponse({'status': '-2' , 'message': 'Title cannot be empty'})
            
            subtask_name = Subtask.objects.filter(title=title)            
            if subtask_name:
                return JsonResponse({'status': '-3' ,'message': 'List name already exist'}) 
            
            if duedate == '':
                return JsonResponse({'status': '-4' , 'message': 'Due date cannot be empty'})
            
                          
                        
            task_instance = Task.objects.get(id=task)                         
            
            Subtask.objects.create(title=title,description=description,due_date=duedate,status=status,parent_task=task_instance)  
            
                        
            return JsonResponse({'status': '1' ,'message': 'Data saved successfully'})
        else:
            return JsonResponse({'status': '2' , 'message': 'Data save unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    
def update_subtask(request):
    try:
        # import pdb;pdb.set_trace();
        if request.method == 'POST':
            task = request.POST.get('task')
            title = request.POST.get('title')
            description = request.POST.get('description')
            duedate = request.POST.get('duedate')
            status = request.POST.get('status')
            id = request.POST.get('id')
            
            if title == '':
                return JsonResponse({'status': '-1' , 'message': 'Title cannot be empty'})
            
            task_instance = Task.objects.get(id=task)         
            
            Subtask.objects.filter(id=id).update(title=title,description=description,due_date=duedate,status=status,parent_task=task_instance)            
            
                        
            return JsonResponse({'status': '1' ,'message': 'Data updated successfully'})
        else:
            return JsonResponse({'status': '-1' , 'message': 'Update unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    
def delete_subtask(request):
    try:
        # import pdb;pdb.set_trace();
        if request.method == 'POST':
            id = request.POST.get('id')         
            
            Subtask.objects.filter(id=id).delete()                        
            return JsonResponse({'status': '1' ,'message': 'Data deleted successfully'})
        else:
            return JsonResponse({'status': '-1' , 'message': 'Delete unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})


def update_profile(request):
    try:
        import pdb;pdb.set_trace();
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            role = request.POST.get('role')
            id = request.POST.get('id')
            pwd = request.POST.get('pwd')
            cnfpwd = request.POST.get('cnfpwd')
            
            if username == '':
                return JsonResponse({'status': '-1' , 'message': 'Username cannot be empty'})
            
            if email == '':
                return JsonResponse({'status': '-2' , 'message': 'Email cannot be empty'})
            
            if role == '':
                return JsonResponse({'status': '-3' , 'message': 'Role cannot be empty'})
            
            new_user = CustomUser.objects.filter(username=username).values('id')
            if new_user:
                if new_user[0]['id'] != int(id):
                    return JsonResponse({'status': '-4' , 'message': 'Username alraedy exist'})                                      
            
             
            
            if pwd:
                if pwd != cnfpwd:
                    return JsonResponse({'status': '-5' ,'message': 'password should be same'})
                else:
                    CustomUser.objects.filter(id=id).update(username=username,email=email,password=pwd,role=role) 
            else:
                CustomUser.objects.filter(id=id).update(username=username,email=email,role=role)                   
            
                        
            return JsonResponse({'status': '1' ,'message': 'Data updated successfully'})
        else:
            return JsonResponse({'status': '0' , 'message': 'Update unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    


# @login_required
def send_email_reminder():
    # import pdb;pdb.set_trace();
    try:
        
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
                
        current_date = datetime.now()
        check_date = current_date + timedelta(days=3)
        recipient_list = []
        tasks_due_soon = Task.objects.filter(due_date=check_date)
        for task in tasks_due_soon:
            user_data = task.project.user.all().first()
            if user_data:
                task_name = task.title
                recipient_list.append({'name':task_name, 'email':user_data.email})
        print(recipient_list)
        
        subject = "Gentle Reminder"
        
        
        for item in recipient_list:
            user_email = item['email']
            message = f"Your task '{item['name']}' is due soon."
            send_mail(subject, message, 'greeshma150295@gmail.com', [user_email])

        return HttpResponse("Email sent successfully!")
    except:
        return HttpResponse("Email sent Unsuccessful!")

# send_email_reminder()


 