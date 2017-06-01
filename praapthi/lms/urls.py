from django.conf.urls import url
from django.shortcuts import render, get_object_or_404

from django.views import generic

from . import views

app_name='lms'
urlpatterns = [

    url(r'^$', views.index, name='index'),

    url(r'^register/$', views.register, name='register'),

    url(r'^register_processor/$', views.registerp, name='registerp'),

    url(r'^login/$', views.student_login, name='login'),

    url(r'^logout/$', views.student_logout, name='logout'),

    url(r'^profile/$', views.student_profile, name='profile'),

    url(r'^dashboard/$', views.student_dashboard, name='dashboard'),

    url(r'^enroll-course/$', views.student_enroll_course, name='enroll_course'),

    url(r'^course-access/$', views.student_course_access, name='course_access'),

    url(r'^assignment-submission/$', views.student_assignment_submission, name='assignment_submission'),



    #url(r'^custom/$', views.custom, name='custom'),

    #url(r'^logout/$', views.user_logout, name='logout'),

#	url(r'^$', views.IndexView.as_view(), name='index')

]