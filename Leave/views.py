from django.shortcuts import render

from LoginApp.models import *

from pms.validators import *

from .forms import *

from .models import LeaveApp

from django.contrib.auth.decorators import login_required





# Create your views here.

@login_required

def apply_leave(request):

    if request.method == 'POST':

        form = LeaveForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)

            post.user = request.user

            post.save()

            return redirect('leave_home')

    form = LeaveForm()

    return render(request, 'leaveform.html', {'form': form})





@login_required

def see_leave(request, leave_pk):

    if not leave_user_is_valid(request, leave_pk):

        return redirect('leave_home')

    leave = get_object_or_404(LeaveApp, pk=leave_pk)

    if request.method == 'POST':

        form = LeaveApprovalForm(request.POST)

        print(form.is_valid())

        if form.is_valid():

            post = form.save(commit=False)

            leave.leave_status = post.leave_status

            leave.save()

        return redirect('leave_home')



    form = None

    if not leave.user == request.user:

        form = LeaveApprovalForm()

    return render(request, 'see_leave.html', {'leave': leave, 'form': form})





@login_required

def leave_home(request):

    print('in here')

    if request.user.profile.is_super_manager:

        print('in is_super_manager')

        leaves_to_render = None

        leaves = LeaveApp.objects.all()

        for leave in leaves:

            if user_at_higher_deprtment(request, leave.user.profile.department):

                if leaves_to_render is None:

                    leaves_to_render = [leave]

                    leaves_to_render = set(leaves_to_render)

                    continue

                leaves_to_render = leaves_to_render.union([leave])

        return render(request, 'see_leaves.html', {'leaves': leaves_to_render})



    if request.user.profile.is_manager:

        print('in is_manager')

        leaves = LeaveApp.objects.all()

        leaves_to_render = None

        for leave in leaves:

            if leave.user.profile.department == request.user.profile.department:

                if leaves_to_render is None:

                    print(leaves)

                    leaves_to_render = [leave]

                    leaves_to_render = set(leaves_to_render)

                    continue

                leaves_to_render = leaves_to_render.union([leave])

        return render(request, 'see_leaves.html', {'leaves': leaves_to_render})





    else:

        print('in normal user')

        leaves = LeaveApp.objects.all()

        leaves_to_render = None

        for leave in leaves:

            if leave.user == request.user:

                if leaves_to_render is None:

                    leaves_to_render = [leave]

                    leaves_to_render = set(leaves_to_render)

                    continue

                leaves_to_render = leaves_to_render.union([leave])

        return render(request, 'see_leaves.html', {'leaves': leaves_to_render})

# Create your views here.
