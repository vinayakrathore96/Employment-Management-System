
from django import forms


from django.forms import ModelForm

from django.contrib.auth.models import User

from .models import LeaveApp



class LeaveForm(ModelForm):

    leave_date = forms.DateField(required=True)

    class Meta:

        model = LeaveApp

        fields = {

            'subject',

            'leave_date',

            'body',

        }



class LeaveApprovalForm(ModelForm):

    class Meta:

        model = LeaveApp

        fields = {

            'leave_status',

        }
