

from django.contrib import admin

from .models import UserProfile,Department,Project,ProjectDispatcher,ProjectUpdate,Forwarder

# Register your models here.



admin.site.register(UserProfile)

admin.site.register(Department)



admin.site.register(Project)

admin.site.register(ProjectDispatcher)

admin.site.register(ProjectUpdate)

admin.site.register(Forwarder)
