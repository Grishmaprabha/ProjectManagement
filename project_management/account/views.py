

from django.shortcuts import render, redirect
# from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from account.models import CustomUser
from django.db.models import F,Subquery, OuterRef
from dashboard.models import Project,List,Task,Subtask
from django.contrib.auth.decorators import login_required
import json
from datetime import date, timedelta

# Create your views here.


def index(request):
    return render(request, 'index.html')

@login_required
def home(request):
    # import pdb;pdb.set_trace();
    sort_by = request.GET.get('sort_by')
    status_filter = request.GET.get('status')
    keyword = request.GET.get('keyword')
    data_received = request.session.get('user_data')
    user_profile = CustomUser.objects.filter(username=data_received['username']).values('id','username','email','role')
    user_data = CustomUser.objects.all().values_list('id','username')
    list_data = Project.objects.all().order_by('-created_at').values('id','title','description','startdate','enddate','status')
    datalist_list = List.objects.all().annotate(project_title=F('project__title')).order_by('-created_at').values('id', 'list', 'project_title','project_id')
    user_id = CustomUser.objects.filter(username=data_received['username']).values('id')
    project_user = Project.objects.filter(user=user_id[0]['id']).values('id','title')
    task_data_annotated = Task.objects.annotate(project_title=F('project__title')).values('id', 'title', 'description', 'due_date', 'status', 'project_title', 'project__id', 'task_list')
    list_subquery = List.objects.filter(pk=OuterRef('task_list_id')).values('list')[:1]
    combined_task_data = task_data_annotated.annotate(task_list_name=Subquery(list_subquery)).all().order_by('-created_at')
    if status_filter:
        combined_task_data = combined_task_data.filter(status=status_filter)
    if keyword:
        combined_task_data = combined_task_data.filter(title__icontains=keyword)
    if sort_by == 'due_date':
        combined_task_data = combined_task_data.order_by('due_date')
    elif sort_by == 'priority':
        combined_task_data = combined_task_data.order_by('priority_field')
    elif sort_by == 'alphabetical':
        combined_task_data = combined_task_data.order_by('title')
        
    # subtask = Subtask.objects.all().values('title','description','status','due_date','parent_task')
    subtask = Subtask.objects.annotate(task_name=F('parent_task__title')).order_by('-created_at').values('id','title', 'description', 'status', 'due_date', 'parent_task_id','task_name')   
    user_subtasks = Subtask.objects.annotate(task_name=F('parent_task__title')).filter(parent_task__project__user=user_id[0]['id']).order_by('-created_at').values('id','title', 'description', 'status', 'due_date', 'parent_task_id','task_name')   

    
    total_project = Project.objects.filter(user=user_id[0]['id']).count()
    pending_tasks = Task.objects.filter(status='pending', project__user=user_id[0]['id']).count()

    # import pdb;pdb.set_trace();
    today = date.today()
    three_days_later = today + timedelta(days=3)

    # Perform the query to get tasks with due dates within the next 3 days
    due_task = Task.objects.filter(due_date__gte=today, due_date__lte=three_days_later,project__user=user_id[0]['id']).count()
    
    total_task = Task.objects.filter(project__user=user_id[0]['id']).count()


    return render(request, 'home.html', {'dataReceived': data_received,'user_data':user_data,'list_data':list_data,'list':datalist_list,'projects':project_user,'task_data':combined_task_data,'subtask':user_subtasks,'profile':user_profile,'prj_count':total_project,'pending_tasks':pending_tasks,'due_task':due_task,'total_task':total_task})


def register(request):
    # import pdb; pdb.set_trace();
    msg = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')
        
        if password1 != password2:
            msg = 'password should be same'
            return render(request,'register.html', {'msg': msg})         
        elif username =='':
            msg = 'Username cannot be null'
            return render(request,'register.html', {'msg': msg})
        elif email == '':
            msg = 'Email cannot be null'
            return render(request,'register.html', {'msg': msg})
        elif password1 == '' or password2 == '':
            msg = 'password cannot be null'
            return render(request,'register.html', {'msg': msg}) 
        elif username:
            new_user = CustomUser.objects.filter(username=username)
            if new_user:
                msg = "user name already exist"
                return render(request,'register.html', {'msg': msg})
            else:
                my_user = CustomUser.objects.create_user(username=username,email=email,password=password1,role=role)
                my_user.save()
                return redirect('login')
    return render(request,'register.html', {'msg': msg})
    
            


def login_view(request):
    # import pdb; pdb.set_trace();
    msg = None
    data ={}
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            data['username'] = username
            user_role =  CustomUser.objects.filter(username=username).values('role')
            data['role'] = user_role[0]['role']
            # return render(request , 'home.html', {'data': data })
            request.session['user_data'] = {'username': username, 'role': user_role[0]['role']}
            return redirect('home')
        else:
            msg = "Username or password is incorrect"
            return render(request, 'login.html', {'msg': msg})
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

