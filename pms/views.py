from django.shortcuts import render


import datetime;

from LoginApp.models import Project, ProjectDispatcher, ProjectUpdate, Forwarder ,UserProfile

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect

from django.db.models import Count

from .forms import *

from .validators import department_at_higher_deprtment,user_at_higher_deprtment,user_is_manager,user_is_valid

from django.contrib.auth.models import User

# Create your views here.

@login_required

def project_home(request, special=-1):

    if request.user.profile.is_super_manager:

        tasks = None

        departments = Department.objects.all()

        for department in departments:

            if user_at_higher_deprtment(request, department):

                if tasks is None:

                    tasks = ProjectDispatcher.objects.filter(department=department)

                    continue

                tasks = tasks.union(ProjectDispatcher.objects.filter(department=department))

        if int(special) == 1:

            return render(request, 'see_requests.html', {'tasks': tasks})

        return render(request, 'user_task.html', {'tasks': tasks})



    if request.user.profile.is_manager:

        tasks = ProjectDispatcher.objects.filter(department=request.user.profile.department)

        if int(special) == 1:

            return render(request, 'see_requests.html', {'tasks': tasks})

        return render(request, 'user_task.html', {'tasks': tasks})

    else:

        tasks = ProjectDispatcher.objects.filter(employee=request.user.profile)

        if int(special) == 1:

            return render(request, 'see_requests.html', {'tasks': tasks})

        return render(request, 'user_task.html', {'tasks': tasks})





@login_required

def project_updates(request, task_pk):

    if not user_is_valid(request, task_pk):

        return redirect('project')

    if request.method == 'POST':

        date = request.POST['date']

        dateday = datetime.datetime.strptime(date, '%Y-%m-%d')

        dateday = dateday.date

        task = get_object_or_404(ProjectDispatcher, pk=task_pk)

    else:

        dateday = datetime.date.today()

        date = datetime.datetime.strptime(str(dateday), '%Y-%m-%d').strftime('%Y-%m-%d')

        task = get_object_or_404(ProjectDispatcher, pk=task_pk)

    return render(request, 'project_updates.html', {'task': task, 'date': date, 'dateday': dateday})





@login_required

def new_update(request, task_pk, adstr=''):

    if not user_is_valid(request, task_pk):

        return redirect('project')

    task = get_object_or_404(ProjectDispatcher, pk=task_pk)

    project = task.project

    if request.method == 'POST':

        return_to_forward = None

        form = PostForm(request.POST)

        form2 = ForwardForm(request.POST)

        stamp = datetime.datetime.now().time()

        stamp = str(stamp.hour) + ':' + str(stamp.minute) + ':' + str(stamp.second)

        if form.is_valid():

            updated_today = ProjectUpdate.objects.filter(created_at__date=datetime.date.today(),

                                                         created_by=request.user.profile, project=project).exists()

            post = form.save(commit=False)

            post.message = stamp + ':' + adstr + post.message

            post.topic = task.project

            post.project = task.project

            post.created_by = request.user.profile

            if not updated_today:

                post.save()

                return_to_forward = post

            else:

                update_today = ProjectUpdate.objects.get(created_at__date=datetime.date.today(),

                                                         created_by=request.user.profile, project=project)

                update_today.message = update_today.message + '\n\t' + post.message

                update_today.save()

                return_to_forward = update_today



        if form2.is_valid():

            return return_to_forward

        else:

            return redirect('project_updates', task_pk=task_pk)

    else:

        form = PostForm()

    return render(request, 'new_update.html', {'task': task, 'form': form})





@login_required

def new_forward_request(request, project_pk, task_pk):

    if not user_is_valid(request, task_pk):

        return redirect('project')

    task = get_object_or_404(ProjectDispatcher, pk=task_pk)

    if request.method == 'POST':

        form = ForwardForm(request.POST, request.FILES)

        form2 = PostForm(request.POST)

        adstr = 'FORWARD UPDATE ------> '



        if form.is_valid() and form2.is_valid():

            post = form.save(commit=False)

            post.created_by = request.user.profile

            post.task = task

            post.update = new_update(request, task_pk=task_pk, adstr=adstr)

            post.requesting_department = task.project.current_department

            if request.user.profile.is_manager:

                post.request_manager_approval = 0

            post.save()

            task.current_forwarder = post

            task.request_forward = True

            task.save()

            return redirect('project_updates', task_pk=task_pk)

    else:

        form = ForwardForm()

        form2 = PostForm()

    return render(request, 'new_forward.html', {'task': task, 'form': form, 'form2': form2})





@login_required

def cancel_forward_request(request, project_pk, task_pk):  # Might go wrong

    task = get_object_or_404(ProjectDispatcher, pk=task_pk)

    if not user_is_valid(request, task_pk):

        if not (

                task.current_forwarder.request_manager_approval == 0 and request.user.profile.department == task.current_forwarder.acceptor_department):

            return redirect('project')

    task.request_forward = False

    if request.user.profile.is_manager:

        task.current_forwarder.request_manager_approval = 1

        if (request.user.profile.department == task.current_forwarder.acceptor_department) or user_at_higher_deprtment(

                request, task.current_forwarder.acceptor_department):

            print("I ama manadfasd")

            task.current_forwarder.acceptor_manager_approval = 1

        task.current_forwarder.save()

    task.save()

    return redirect('project_updates', task_pk=task_pk)





@login_required

def approve_forward_request(request, project_pk, task_pk):  # Might go wrong

    task = get_object_or_404(ProjectDispatcher, pk=task_pk)

    if not user_is_valid(request, task_pk):

        if not (

                task.current_forwarder.request_manager_approval == 0 and request.user.profile.department == task.current_forwarder.acceptor_department):

            return redirect('project')

    if request.user.profile.is_manager:

        task.current_forwarder.request_manager_approval = 0

        if request.user.profile.department == task.current_forwarder.acceptor_department:

            task.current_forwarder.acceptor_manager_approval = 0

            task.forward = True

            task.project.current_department = task.current_forwarder.acceptor_department

            if request.user.profile.is_super_manager:

                task.project.has_completed = True

                task.project.completion_time = datetime.datetime.now()

                task.project.save()

            task.project.save()

        task.current_forwarder.save()

        task.save()

        if request.user.profile.department == task.current_forwarder.acceptor_department:

            if not request.user.profile.is_super_manager:

                employees = User.objects.all()

                return render(request, 'project_dispatch_forward.html',

                              {'employees': employees, 'project': task.project})

    return redirect('project_updates', task_pk=task_pk)





@login_required

def see_request(request, project_pk, task_pk):

    task = get_object_or_404(ProjectDispatcher, pk=task_pk)

    return render(request, 'see_request.html', {'task': task})





@login_required

def new_project(request):

    if not user_is_manager(request):

        return redirect('project')

    if request.method == 'POST':

        form = ProjectForm(request.POST)

        deadline = request.POST['deadline']

        post = form.save(commit=False)

        post.deadline = deadline

        post.current_department = request.user.profile.department

        post.starter = request.user.profile

        post.save()

        new_project_dispatcher(request, project_id=post.id)

        return redirect('project')

    form = ProjectForm()

    employees = User.objects.all()

    return render(request, 'new_project.html', {'form': form, 'employees': employees})





def new_project_dispatcher(request, project_id=None, task_pk=None):

    if not user_is_manager(request):

        return redirect('project')

    if task_pk is not None:

        if not user_is_valid(request, task_pk):

            return redirect('project')

    if request.method == 'POST':

        if not task_pk is None:

            task = get_object_or_404(ProjectDispatcher, pk=task_pk)

        else:

            task = ProjectDispatcher()

            task.project = get_object_or_404(Project, pk=project_id)

        if not request.user.profile.is_super_manager:

            employees = request.POST.getlist('employees')

            task.department = request.user.profile.department

        else:

            username = request.POST['department-assigned']

            employee = get_object_or_404(User, username=username)

            task.department = employee.profile.department

        task.task_deadline = request.POST['userdeadline']

        task.save()

        if not request.user.profile.is_super_manager:

            new_employee_list = []

            for employee in employees:

                emp_obj = get_object_or_404(User, username=employee)

                new_employee_list.append(emp_obj.profile)

            new_employee_list = set(new_employee_list)

            new_employee_list = new_employee_list.union([request.user.profile])

            task.employee.set(new_employee_list)

            task.project.has_started = True

            task.project.save()

            task.save()

        else:

            task.employee.set([employee.profile])

            task.save()

        return redirect('project')

    task = get_object_or_404(ProjectDispatcher, pk=task_pk)

    employees = User.objects.all()

    return render(request, 'project_dispatcher.html', {'employees': employees, 'task': task})





@login_required

def see_accepting_requests(request):

    if request.user.profile.is_manager:

        forward_requests = None

        departments = Department.objects.all()

        for department in departments:

            if user_at_higher_deprtment(request, department):

                if forward_requests is None:

                    forward_requests = Forwarder.objects.filter(acceptor_department=department,

                                                                request_manager_approval=0, acceptor_manager_approval=3)

                    continue

                forward_requests = forward_requests.union(

                    Forwarder.objects.filter(acceptor_department=department, request_manager_approval=0,

                                             acceptor_manager_approval=3))

        return render(request, 'see_pending_accepts.html', {'forward_requests': forward_requests})

    return redirect('project')





@login_required

def see_completed_projects(request):

    user_dept = request.user.profile.department

    projects = Project.objects.filter(has_completed=True)

    departments = Department.objects.all()

    completed_projects = None

    for project in projects:

        if department_at_higher_deprtment(user_dept,

                                          project.current_department):  # department_at_higher_deprtment(project.current_department, user_dept)

            if completed_projects is None:

                completed_projects = [project]

                completed_projects = set(completed_projects)

            else:

                completed_projects = completed_projects.union([project])

    return render(request, 'completed_projects.html', {'projects': completed_projects})





def new_shared_resource(request):

    if request.user.is_superuser:

        if request.method == 'POST':

            form = ResourceForm(request.POST,request.FILES)

            if form.is_valid():

                resource_form = form.save()

                return redirect('shared_resource')

        else :

            form = ResourceForm()



            args = {'form': form }

            return render(request,'add_resource.html',args)

    elif request.user.profile.is_manager:

        if request.method == 'POST':

            form = ResourceForm(request.POST,request.FILES)

            if form.is_valid():

                resource_form = form.save(False)

                resource_form.department = request.user.profile.department

                resource_form.save()

                return redirect('shared_resource')

        else :

            form = ResourceForm()



            args = {'form': form }

            return render(request,'add_resource.html',args)





def shared_resource(request):

    resources = Resource.objects.filter(department=request.user.profile.department).order_by('-date')

    print(resources)

    return render(request,'resource.html',{'resources': resources})



# Create your views here.
