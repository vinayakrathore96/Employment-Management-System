from django.db import models

import datetime

from LoginApp.models import Department,Project

# Create your models here.

class Resource(models.Model):

    title = models.CharField(max_length=100,null=True,blank=True)

    notice = models.TextField(max_length=250,null=True,blank=True)

    files = models.FileField()

    department = models.ForeignKey(Department,on_delete=models.CASCADE)

    date = models.DateTimeField(auto_now=True)
