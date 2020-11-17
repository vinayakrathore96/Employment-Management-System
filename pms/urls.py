
from django.urls import path, re_path

from django.conf.urls import url

from . import views

from django.contrib.auth import views as auth_views



urlpatterns =[

    path('', views.project_home,name='project'),

    path('shared_resource/',views.shared_resource,name='shared_resource'),

    path('new_shared_resource/',views.new_shared_resource,name='new_shared_resource'),

    url(r'^project/new/$', views.new_project, name='new_project'),

    url(r'^project/completed_projects/$', views.see_completed_projects, name='see_completed_projects'),

    url(r'^project/dispatch/update/(?P<project_id>\d+)/$', views.new_project_dispatcher, name='update_dispatch'),

    url(r'^project/dispatch/new/(?P<task_pk>\d+)/$', views.new_project_dispatcher, name='new_dispatch'),

    url(r'^project/(?P<task_pk>\d+)/$', views.project_updates, name='project_updates'),

    url(r'^requests/(?P<special>\d+)/$', views.project_home, name='pending_requests'),

    url(r'^accepts/$', views.see_accepting_requests, name='accepting_requests'),

    url(r'^requests/(?P<project_pk>\d+)/(?P<task_pk>\d+)/$', views.see_request, name='see_request'),

    url(r'^project/(?P<task_pk>\d+)/new/$', views.new_update, name='new_update'),

    url(r'^project/(?P<project_pk>\d+)/(?P<task_pk>\d+)/$', views.new_forward_request, name='forward_request'),

    url(r'^project/(?P<project_pk>\d+)/cancelrequest/(?P<task_pk>\d+)/$', views.cancel_forward_request,

        name='cancel_forward_request'),

    url(r'^project/(?P<project_pk>\d+)/approverequest/(?P<task_pk>\d+)/$', views.approve_forward_request,

        name='approve_forward_request')

]
