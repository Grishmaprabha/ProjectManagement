from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from account.models import CustomUser
from dashboard.models import Project,List,Task,Subtask,ActivityLog
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse,HttpResponse
from django.core.mail import send_mail
from datetime import datetime, timedelta
import ssl
from django.conf import settings
from celery import shared_task
from datetime import date,datetime, timedelta
from django.core.mail import send_mail
from django.utils import timezone
from celery import shared_task
import smtplib
from email.mime.text import MIMEText
from django.db.models import F,Subquery, OuterRef, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail





# Create your views here.


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
            user_data = request.session.get('user_data')

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
            
            user_id = CustomUser.objects.filter(username=user_data["username"]).values('id')
            user_instance = CustomUser.objects.get(id=user_id[0]['id'])
            
            ActivityLog.objects.create(
                    action='Project Created',
                    user=user_instance,
                    details=f'Project "{title}" created by - {user_data["username"]}.'
                )
            
                        
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
            user_data = request.session.get('user_data')

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
            
            user_id = CustomUser.objects.filter(username=user_data["username"]).values('id')
            user_instance = CustomUser.objects.get(id=user_id[0]['id'])
            
            ActivityLog.objects.create(
                    action='Project Updated',
                    user=user_instance,
                    details=f'Project "{title}" updated by - {user_data["username"]}.'
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
            title = request.POST.get('title')       
            user_data = request.session.get('user_data')

            Project.objects.filter(id=id).delete()  
            
            user_id = CustomUser.objects.filter(username=user_data["username"]).values('id')
            user_instance = CustomUser.objects.get(id=user_id[0]['id'])
            
            ActivityLog.objects.create(
                    action='Project Deleted',
                    user=user_instance,
                    details=f'Project "{title}" deleted by - {user_data["username"]}.'
                )                      
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
        users = project.user.all() 
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
            
            user_data = request.session.get('user_data')
            
            
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
            
            user_id = CustomUser.objects.filter(username=user_data["username"]).values('id')
            user_instance = CustomUser.objects.get(id=user_id[0]['id'])
            
            ActivityLog.objects.create(
                    action='Task Created',
                    user=user_instance,
                    details=f'Task "{title}" created by - {user_data["username"]}.'
                )
                        
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
            user_data = request.session.get('user_data')

            
            if title == '':
                return JsonResponse({'status': '-1' , 'message': 'Title cannot be empty'})
            if list_data == '':
                return JsonResponse({'status': '-1' , 'message': 'List cannot be empty'})
            project_instance = Project.objects.get(id=project)  
            list_instance = List.objects.get(id=list_data) 
            
            Task.objects.filter(id=id).update(title=title,description=description,due_date=duedate,status=status,project=project_instance,task_list=list_instance)            
            
            user_id = CustomUser.objects.filter(username=user_data["username"]).values('id')
            user_instance = CustomUser.objects.get(id=user_id[0]['id'])
            
            ActivityLog.objects.create(
                    action='Task Updated',
                    user=user_instance,
                    details=f'Task "{title}" updated by - {user_data["username"]}.'
                )

                        
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
            title = request.POST.get('title')
            user_data = request.session.get('user_data')
       
            
            Task.objects.filter(id=id).delete()    
            
            user_id = CustomUser.objects.filter(username=user_data["username"]).values('id')
            user_instance = CustomUser.objects.get(id=user_id[0]['id'])
            
            ActivityLog.objects.create(
                    action='Task Deleted',
                    user=user_instance,
                    details=f'Task "{title}" deleted by - {user_data["username"]}.'
                )
                                
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
            user_data = request.session.get('user_data')
            
            if task == '':
                return JsonResponse({'status': '-1' ,'message': ' cannot be empty'}) 
            
            if title == '':
                return JsonResponse({'status': '-2' , 'message': 'Title cannot be empty'})
            
            subtask_name = Subtask.objects.filter(title=title)            
            if subtask_name:
                return JsonResponse({'status': '-3' ,'message': 'Subtask name already exist'}) 
            
            if duedate == '':
                return JsonResponse({'status': '-4' , 'message': 'Due date cannot be empty'})
            
                          
                        
            task_instance = Task.objects.get(id=task)                         
            
            Subtask.objects.create(title=title,description=description,due_date=duedate,status=status,parent_task=task_instance)  
            
            user_id = CustomUser.objects.filter(username=user_data["username"]).values('id')
            user_instance = CustomUser.objects.get(id=user_id[0]['id'])
            
            ActivityLog.objects.create(
                    action='Subtask Created',
                    user=user_instance,
                    details=f'Subtask "{title}" created by - {user_data["username"]}.'
                )
                        
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
            user_data = request.session.get('user_data')
            
            if title == '':
                return JsonResponse({'status': '-1' , 'message': 'Title cannot be empty'})
            
            task_instance = Task.objects.get(id=task)         
            
            Subtask.objects.filter(id=id).update(title=title,description=description,due_date=duedate,status=status,parent_task=task_instance)            
            
            user_id = CustomUser.objects.filter(username=user_data["username"]).values('id')
            user_instance = CustomUser.objects.get(id=user_id[0]['id'])
            
            ActivityLog.objects.create(
                    action='Subtask Updated',
                    user=user_instance,
                    details=f'Subtask "{title}" updated by - {user_data["username"]}.'
                )
                        
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
            title = request.POST.get('title')         
            user_data = request.session.get('user_data')
            Subtask.objects.filter(id=id).delete() 
            
            user_id = CustomUser.objects.filter(username=user_data["username"]).values('id')
            user_instance = CustomUser.objects.get(id=user_id[0]['id'])
            
            ActivityLog.objects.create(
                    action='Subtask Deleted',
                    user=user_instance,
                    details=f'Subtask "{title}" deleted by - {user_data["username"]}.'
                )
                                   
            return JsonResponse({'status': '1' ,'message': 'Data deleted successfully'})
        else:
            return JsonResponse({'status': '-1' , 'message': 'Delete unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})


def update_profile(request):
    try:
        # import pdb;pdb.set_trace();
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
                    user = CustomUser.objects.get(id=id)
                    user.username = username
                    user.email = email
                    user.role = role
                    user.set_password(pwd) 
                    user.save()
                    # CustomUser.objects.filter(id=id).update(username=username,email=email,password=pwd,role=role) 
            else:
                CustomUser.objects.filter(id=id).update(username=username,email=email,role=role)                   
            
                        
            return JsonResponse({'status': '1' ,'message': 'Data updated successfully'})
        else:
            return JsonResponse({'status': '0' , 'message': 'Update unsucessfull'})
    except:
        return JsonResponse({'status': '0' , 'message': 'Some error occured'})
    
def activitylog(request):
    # import pdb;pdb.set_trace();
    user = request.session.get('user_data')
    user_id = CustomUser.objects.filter(username=user['username']).values('id')
    user_projects = Project.objects.filter(user=user_id[0]['id']).values('title')
    all_activity_entries = []
    
    if user_projects:
        for data in user_projects:
            team = Project.objects.filter(title=data['title']).values_list('user')
            
        for item in team:
            user_name = CustomUser.objects.filter(id=item[0]).values('id','username')            
            activity_entries = ActivityLog.objects.filter(user=user_name[0]['id']).order_by('-timestamp')
            all_activity_entries.extend(activity_entries)
    
    page = request.GET.get('page')  
    per_page = 10 
    paginator = Paginator(all_activity_entries, per_page)
    try:
        activity_entries = paginator.page(page)
    except PageNotAnInteger:
        activity_entries = paginator.page(1)
    except EmptyPage:
        activity_entries = paginator.page(paginator.num_pages)      
   
    
    return render(request, 'activity_log.html', {'activity_entries': activity_entries})



@shared_task
def send_email_reminder():
    # import pdb;pdb.set_trace();
    try:        
                
        current_date = datetime.now()
        check_date = current_date + timedelta(days=3)
        recipient_list = []
        tasks_due_soon = Task.objects.filter(due_date__range=[current_date, check_date])
        for task in tasks_due_soon:
            user_data = task.project.user.all().first()
            if user_data:
                task_name = task.title
                recipient_list.append({'name':task_name, 'email':user_data.email})
        print(recipient_list)
        
        subject = "Gentle Reminder"
        
        
        for item in recipient_list:
            user_mail = settings.EMAIL_HOST_USER
            recepient_email = [item['email']]
            message = f"Your task '{item['name']}' is due soon."
            send_mail(subject, message, user_mail, recepient_email,fail_silently=False,)

        return HttpResponse("Email sent successfully!")
    except:
        return HttpResponse("Email sent Unsuccessful!")

send_email_reminder()

# def schedule_email_reminder(request):
#     send_email_reminder.delay()
#     return HttpResponse("Email reminder task scheduled successfully!")



def getprojectdata(request):
    user_data = request.session.get('user_data')
    user_id = CustomUser.objects.filter(username=user_data['username']).values('id')
    # import pdb;pdb.set_trace();
    list_project = Project.objects.filter(user=user_id[0]['id']).order_by('-created_at').values('id','title','description','startdate','enddate','status')
    project_list = list(list_project.values())
    return JsonResponse({'project': project_list})


def getlistdata(request):
    # import pdb;pdb.set_trace();
    user_data = request.session.get('user_data')
    user_id = CustomUser.objects.filter(username=user_data['username']).values('id')
    list_list = List.objects.filter(project__user=user_id[0]['id']).annotate(project_title=F('project__title')).order_by('-created_at').values('id', 'list', 'project_title','project_id')
    list_data = list(list_list.values())
    return JsonResponse({'list_data': list_data})


def gettaskdata(request):
    # import pdb;pdb.set_trace();    
    user_data = request.session.get('user_data')
    user_id = CustomUser.objects.filter(username=user_data['username']).values('id')
    task_data_annotated = Task.objects.filter(project__user=user_id[0]['id']).annotate(project_title=F('project__title')).values('id', 'title', 'description', 'due_date', 'status', 'project_title', 'project__id', 'task_list')
    list_subquery = List.objects.filter(pk=OuterRef('task_list_id')).values('list')[:1]
    combined_task_data = task_data_annotated.annotate(task_list_name=Subquery(list_subquery)).all().order_by('-created_at')
    list_task = list(combined_task_data.values())
    return JsonResponse({'task': list_task})


def getsubtaskdata(request):
    # import pdb;pdb.set_trace();
    user_data = request.session.get('user_data')
    user_id = CustomUser.objects.filter(username=user_data['username']).values('id')
    subtask_data = Subtask.objects.filter(parent_task__project__user=user_id[0]['id']).annotate(task_name=F('parent_task__title')).order_by('-created_at').values('id','title', 'description', 'status', 'due_date', 'parent_task_id','task_name')
    list_subtask = list(subtask_data.values())
    return JsonResponse({'subtask': list_subtask})

def getchartdata(request):
    # import pdb;pdb.set_trace();
    user_data = request.session.get('user_data')
    user_id = CustomUser.objects.filter(username=user_data['username']).values('id')
    pending_list = []
    progress_list = []
    completed_list = []
    
    labels = Project.objects.filter(user=user_id[0]['id']).values('id')
    project_label = list(Project.objects.filter(user=user_id[0]['id']).values_list('title', flat=True))
    
    
    for project in labels:
        pending_data = Task.objects.filter(status='pending', project__user=user_id[0]['id'],project=project['id']).count()
        pending_list.append(pending_data)
        
    for project in labels:
        progress_data = Task.objects.filter(status='inprogress', project__user=user_id[0]['id'],project=project['id']).count()
        progress_list.append(progress_data)
    
    for project in labels:
        completed_data = Task.objects.filter(status='completed', project__user=user_id[0]['id'],project=project['id']).count()
        completed_list.append(completed_data)
    
    
    data = {
        "labels": project_label,
        "pendingData": pending_list,
        "inProgressData": progress_list,
        "completeData": completed_list
    }

    return JsonResponse(data)

def getpiechartdata(request):
    # import pdb;pdb.set_trace();
    user_data = request.session.get('user_data')
    user_id = CustomUser.objects.filter(username=user_data['username']).values('id')
    
    today = date.today()
    three_days_later = today + timedelta(days=3)

    due_task = Task.objects.filter(due_date__gte=today, due_date__lte=three_days_later, project__user=user_id[0]['id']).count()

    other_tasks = Task.objects.filter(Q(due_date__lt=today) | Q(due_date__gt=three_days_later), project__user=user_id[0]['id']).count()
    
    
    data = {
        "due_task": due_task,
        "other_tasks": other_tasks
    }

    return JsonResponse(data)
    
def gettooltipdata(request):
    # import pdb;pdb.set_trace();
    data_received = request.session.get('user_data')
    today = date.today()
    three_days_later = today + timedelta(days=3)
    user_id = CustomUser.objects.filter(username=data_received['username']).values('id')
    total_task_data = Task.objects.filter(project__user=user_id[0]['id']).values('title')
    total_project_data = Project.objects.filter(user=user_id[0]['id']).values('title')
    total_pending_task = Task.objects.filter(status='pending', project__user=user_id[0]['id']).values('title')
    total_due_task = Task.objects.filter(due_date__gte=today, due_date__lte=three_days_later,project__user=user_id[0]['id']).values('title')
    task = []
    project = []
    pending = []
    duetask = []
    for data in total_task_data:
        task.append(data)
    for prj in total_project_data:
        project.append(prj)
    for pend in total_pending_task:
        pending.append(pend)
    for due in total_due_task:
        duetask.append(due)
        
    data = {
        "task": task,
        "project": project,
        "pending": pending,
        "due": duetask
    }
        
    
    return JsonResponse(data, safe=False)


