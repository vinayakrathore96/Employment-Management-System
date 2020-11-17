
from . import views

from django.urls import path, re_path

from django.conf.urls import url

urlpatterns =[

    url(r'^leave/apply/$', views.apply_leave, name='apply_leave'),

    path('', views.leave_home, name='leave_home'),

    url(r'^leave/takeaction/(?P<leave_pk>\d+)/$', views.see_leave, name='see_leave'),

]
