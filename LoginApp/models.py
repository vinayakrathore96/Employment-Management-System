from django.db import models

from phone_field import PhoneField

from django.contrib.auth.models import User, AbstractBaseUser

from . import models as mdl

from django.db.models.signals import post_save





# Create your models here.





class Department(models.Model):

    name = models.CharField(max_length=30)

    superdepartment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,

                                        related_name='sub_department')



    def __str__(self):

        return self.name





'''class SuperDepartment(models.Model):

    name = models.CharField(max_length=30)

    def __str__(self):

        return self.name'''





class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1, related_name='profile')

    contact_number = PhoneField(help_text='Employee Contact Number', blank=True, null=True)

    fathers_name = models.CharField(max_length=30, blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)

    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)

    is_manager = models.BooleanField(default=False)

    is_super_manager = models.BooleanField(default=False)

    address = models.TextField(max_length=250, blank=True, null=True)

    image = models.ImageField(upload_to='Employee_Image', blank=True, null=True)

    aadhar_number = models.ImageField(upload_to='Employee_aadhar', blank=True, null=True)

    pan_number = models.ImageField(upload_to='Employee_pancard', blank=True, null=True)

    education = models.TextField(max_length=250, blank=True, null=True)

    salary = models.IntegerField(default=0, blank=True, null=True)



    def __str__(self):

        return self.user.username  # +' ----> '+ self.department.name





def create_profile(sender, **kwargs):

    if kwargs['created']:

        user_profile = UserProfile.objects.create(user=kwargs['instance'])





post_save.connect(create_profile, sender=User)





class Project(models.Model):

    name = models.CharField(max_length=50, blank=True, null=True)

    starter = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='starter')

    current_department = models.ForeignKey(Department, on_delete=models.CASCADE)

    description = models.TextField(max_length=300, blank=True, null=True)

    date_created = models.DateTimeField(auto_now=True)

    has_started = models.BooleanField(default=False)

    has_completed = models.BooleanField(default=False)

    completion_time = models.DateTimeField(blank=True, null=True)

    deadline = models.DateTimeField()



    def __str__(self):

        return self.name





class ProjectDispatcher(models.Model):

    employee = models.ManyToManyField(UserProfile, related_name='dispatch')

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='dispatch')

    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)

    date_created = models.DateTimeField(auto_now=True)

    request_forward = models.BooleanField(default=False)

    forward = models.BooleanField(default=False)

    current_forwarder = models.ForeignKey('Forwarder', on_delete=models.CASCADE, blank=True, null=True)

    task_deadline = models.DateTimeField()



    def __str__(self):

        return self.project.name





class ProjectUpdate(models.Model):

    message = models.TextField(max_length=4000, null=True)

    outcome = models.TextField(max_length=4000, null=True)

    pending = models.TextField(max_length=4000, null=True)

    comments = models.TextField(max_length=4000, null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='update')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(null=True)

    created_by = models.ForeignKey(UserProfile, related_name='update', on_delete=models.CASCADE)

    updated_by = models.ForeignKey(UserProfile, null=True, related_name='+', on_delete=models.CASCADE)



    def __str__(self):

        return self.project.name





'''class UserDept(models.Model):

    employee = models.OneToOneField(UserProfile,on_delete=models.CASCADE, related_name = 'dept')

    department =  models.ForeignKey(Department,on_delete=models.CASCADE)

    def __str__(self):

        return self.department.name+'\t------>\t'+ self.employee.user.username'''





class Forwarder(models.Model):

    created_by = models.ForeignKey(UserProfile, related_name='requester', on_delete=models.CASCADE)

    task = models.ForeignKey(ProjectDispatcher, on_delete=models.CASCADE, related_name='assignement')

    requesting_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='requester')

    acceptor_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='acceptor')

    update = models.ForeignKey(ProjectUpdate, on_delete=models.CASCADE, related_name='forwarder', blank=True, null=True)

    Approval = [(0, 'Approve'), (1, 'Reject'), (3, 'Unseen')]

    request_manager_approval = models.IntegerField(choices=Approval, default=3)

    acceptor_manager_approval = models.IntegerField(choices=Approval, default=3)

    documents = models.FileField(blank=True, null=True)
