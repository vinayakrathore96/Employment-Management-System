from django.shortcuts import render,redirect

from django.contrib.auth.models import auth

from django.contrib import messages

from django import forms

from .models import UserProfile

from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm

from .forms import RegistrationForm,EditProfileForm,EditUserProfileForm

from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required

#from django.http import HttpResponse

from django.contrib.auth.models import User

from django.shortcuts import render, get_object_or_404





# Create your views here.

def login(request):

    if request.method == 'POST':

        emp_username=request.POST['username']

        emp_password=request.POST['pswd']



        user=auth.authenticate(username = emp_username,password = emp_password)



        if user is not None:

            auth.login(request,user)

            print('success')

            return redirect('home')

        else:

            #messages.error(request,'invalid credentials')

            return redirect('/')



    return render(request,'Login.html')





@login_required

def home(request):

    return render(request,'homepage.html')



@login_required()

def logout(request):

    auth.logout(request)

    return redirect('/')





@login_required

def change_password(request):

    if request.method == 'POST':

        form = PasswordChangeForm(data = request.POST, user = request.user)



        if form.is_valid():

            form.save()

            update_session_auth_hash(request, form.user)

            messages.info(request, 'Password Changed Successfully')

            return redirect('change_password')

        else:

            messages.error(request, 'Password Changing Failed')

            return redirect('change_password')

    else :

        form = PasswordChangeForm(user = request.user)

        args = {'form' : form}



        return render(request,'change_password.html',args)





@login_required

def edit_profile(request):

    if request.method == 'POST':

        form = EditUserProfileForm(request.POST, instance = request.user)

        profile_form = EditProfileForm(

            request.POST,

            request.FILES,

            instance=request.user.profile

        )



        if form.is_valid() and profile_form.is_valid():

            user_form = form.save()

            custom_form = profile_form.save(False)

            custom_form.user=user_form

            user_form.save()

            custom_form.save()

            messages.info(request, 'Changes Saved')

            return redirect('profile')

    else:

        form = EditUserProfileForm(instance = request.user)

        profile_form = EditProfileForm(instance = request.user.profile)



        args = {}

        args['form'] = form

        args['profile_form'] = profile_form

        return render(request,'edit_profile.html',args)





@login_required

def profile(request):

    args = {'user' : request.user,'userprofile' : request.user.profile}

    return render(request,'profile.html',args)







def register(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            details = form.save(commit=False)

            details.is_active = False

            details.save()

            return redirect('/')

        else:

            messages.error(request,'Please Enter correct Details. Make sure your password is strong. Make Sure email or username is not  registered')            

    form = RegistrationForm()

    args = {'form' : form}

    return render(request,'register.html',args)

           


def employees_list(request):

    lists = User.objects.all()



    return render(request, 'employee_list.html', {'lists': lists})





def deactivate_user(request):

    print('Helll')

    if request.method == 'POST':

        employees_id = request.POST.getlist('employees')

        print(employees_id)

        for id in employees_id:

            user = get_object_or_404(User,id=id)

            user.is_active = False

            user.save()

    return redirect('employees_list')
