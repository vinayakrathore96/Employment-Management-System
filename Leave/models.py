from django.db import models


from LoginApp.models import UserProfile

from django.contrib.auth.models import User, AbstractBaseUser

# Create your models here.

class LeaveApp(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    subject = models.CharField(max_length=100)

    body = models.TextField(max_length=2000)

    LEAVE_APPROVED = 0

    LEAVE_REJECTED = 1

    UNSEEN = 3

    STATUS_CHOICES = [(LEAVE_APPROVED, 'Approve'), (LEAVE_REJECTED, 'Reject'), (UNSEEN, 'Unseen')]

    leave_status = models.IntegerField(choices=STATUS_CHOICES, default=UNSEEN)

    leave_date = models.DateField(null = True)

    date_applied = models.DateTimeField( auto_now_add=True)

# Create your models here.
