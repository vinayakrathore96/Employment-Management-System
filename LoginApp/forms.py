
from django.contrib.auth.forms import UserCreationForm

from django import forms

from django.contrib.auth.models import User

from .models import UserProfile

from django.forms import ModelForm



class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)



    class Meta:

        model = User

        fields = {

            'username',

            'first_name',

            'last_name',

            'email',

            'password1',

            'password2'

        }

    def save(self, commit=True):

        user = super(RegistrationForm,self).save(commit=False)

        user.first_name = self.cleaned_data['first_name']

        user.last_name = self.cleaned_data['last_name']

        user.email = self.cleaned_data['email']



        if commit :

            user.save()



        return user







class EditUserProfileForm(ModelForm):

    class Meta:

        model = User

        fields = {

            'email',

            'username',

            'first_name',

            'last_name'

        }



class EditProfileForm(ModelForm):

    class Meta:

        model = UserProfile

        fields = {

            'contact_number',

            'fathers_name',

            'date_of_birth',

            'address',

            'image',

            'aadhar_number',

            'pan_number',

            'education'



        }
