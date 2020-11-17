
from django.shortcuts import render, get_object_or_404,redirect

from LoginApp.models import Project, ProjectDispatcher, ProjectUpdate, Forwarder

from Leave.models import LeaveApp

#validators

def user_is_valid(request, task_pk):

    task = get_object_or_404(ProjectDispatcher, pk=task_pk)

    if user_at_higher_deprtment(request,task.department):

        return True

    if task.department == request.user.profile.department:

        if ((request.user.profile.is_manager) or (request.user.profile in task.employee.all())):

            return True

    return False



def leave_user_is_valid(request, leave_pk):

    leave = get_object_or_404(LeaveApp, pk=leave_pk)

    if user_at_higher_deprtment(request,leave.user.profile.department):

        return True

    if leave.user.profile.department == request.user.profile.department:

        if ((request.user.profile.is_manager) or (request.user.profile == leave.user.profile)):

            return True

    return False





def user_is_manager(request):

    if request.user.profile.is_manager:

        return True

    return False



#admin hierarchy validator



def department_at_higher_deprtment(department_higher, department):

    while(department is not None):

        if department == department_higher:

            return True

        department = department.superdepartment

    return False



def user_at_higher_deprtment(request, department):

    while(department is not None):

        if department == request.user.profile.department:

            return True

        department = department.superdepartment

    return False
