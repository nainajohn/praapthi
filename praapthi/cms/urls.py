from django.conf.urls import url
from django.shortcuts import render, get_object_or_404

from django.views import generic

from . import views

app_name='cms'

urlpatterns = [

    url(r'^$', views.index, name='index'),

	url(r'^register/$', views.lecturer_register, name='lecturer_register'),

	url(r'^register_processor/$', views.lecturer_registerp, name='lecturer_registerp'),

	url(r'^login/$', views.lecturer_login, name='lecturer_login'),

    url(r'^logout/$', views.lecturer_logout, name='lecturer_logout'),

    url(r'^dashboard/$', views.lecturer_dashboard, name='lecturer_dashboard'),

    url(r'^add-course/$', views.add_course, name='add_course'),

    url(r'^delete-course/$', views.delete_course, name='delete_course'),

    url(r'^add-course-session/$', views.add_course_session, name='add_course_session'),

    url(r'^delete-course-session/$', views.delete_course_session, name='delete_course_session'),

    url(r'^add-course-material/$', views.add_course_material, name='add_course_material'),

    url(r'^delete-course-material/$', views.delete_course_material, name='delete_course_material'),

    url(r'^add-institution/$', views.add_institution, name='add_institution'),

    url(r'^delete-institution/$', views.delete_institution, name='delete_institution'),

    url(r'^add-assignment/$', views.add_assignment, name='add_assignment'),

    url(r'^delete-assignment/$', views.delete_assignment, name='delete_assignment'),

#	url(r'^$', views.IndexView.as_view(), name='index')

]