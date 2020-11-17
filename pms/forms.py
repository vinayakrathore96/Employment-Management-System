
from LoginApp.models import ProjectUpdate, Forwarder, Department, ProjectDispatcher, Project

from django import forms

from django.forms import ModelForm

from .models import Resource



class PostForm(ModelForm):

    outcome = forms.CharField(widget=forms.Textarea, required=False)

    pending = forms.CharField(widget=forms.Textarea, required=False)

    comments = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:

        model = ProjectUpdate

        fields = ['message','outcome','pending','comments' ]



class ForwardForm(ModelForm):

    documents = forms.FileField(required=False)

    class Meta:

        model = Forwarder

        fields = {

            'acceptor_department',

            'documents'

        }



class ProjectForm(ModelForm):

    class Meta:

        model = Project

        fields = {

            'name',

    'description',

        }









class ResourceForm(ModelForm):

    files = forms.FileField(required=False)

    class Meta:

        model = Resource

        fields = '__all__'
