from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import Http404, HttpResponseRedirect, HttpResponse 
from django.views import generic

from django.template import RequestContext

from django.contrib.auth.models import User
#from lms.models import UserProfile
#from lms.forms import UserForm, UserProfileForm
from lms.models import Lecturer, Course, Institution, Course_created_by, On_course, Course_session, Material, Assignments

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required

import hashlib


def index(request):
   return render(request, 'cms/index.html')

def lecturer_register(request):
    return render(request, 'cms/register.html')

#Register Function for Lecturers
def lecturer_registerp(request):
    if request.method == 'POST': #POST data validation
        first_name = request.POST.get('first_name','')
        last_name = request.POST.get('last_name','')
        email = request.POST.get('email','')
        user_name = request.POST.get('user_name','')
        password = request.POST.get('password','')
        cpassword = request.POST.get('cpassword','')
        country = request.POST.get('country','')
        gender = request.POST.get('gender','')
        conditions = request.POST.get('conditions','')
        profile_image = request.FILES.get('profile_image','') #File Field for uploading profile image

        if password == cpassword:
            password = hashlib.sha512(bytes(password)).hexdigest() #Password Hashing using SHA512 & HashDigest for Hexadecimal Convertion
        else:
            return HttpResponse('Password match error')

        email_check = Lecturer.objects.all().filter(email = email) #Checking for Email 
        user_name_check = Lecturer.objects.all().filter(user_name = user_name) #Checking for User Name

        for x in email_check:
            return HttpResponse('Email Error')

        for y in user_name_check:
            return HttpResponse('User Name Error')

        lecturer_object = Lecturer(profile_image = profile_image,first_name = first_name, last_name = last_name, email = email, user_name = user_name, password = password, country=country, gender = gender, conditions = True)
        lecturer_object.save()

        return HttpResponseRedirect('/cms')    
    else:
        return HttpResponse('Post Data Error')

def lecturer_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        user_id = 0
        user_first_name = ''

        password = hashlib.sha512(bytes(password)).hexdigest()

        user_name_check = Lecturer.objects.all().filter(user_name = user_name)
        user_name_error_flag = True
        for u in user_name_check:
            user_name_error_flag = False
        if (user_name_error_flag):
            return HttpResponse('Invalid User Name')    

        for u in user_name_check:
            if u.password != password:
                return HttpResponse('Password Error')
            user_id = u.id
            user_name = u.user_name
            user_first_name = u.first_name
            user_last_name = u.last_name

        request.session['lecturer_id'] = user_id
        request.session['lecturer_name'] = user_name
        request.session['lecturer_first_name'] = user_first_name
        request.session['lecturer_last_name'] = user_last_name
        request.session['redirect'] = ''

        return HttpResponseRedirect('/cms/dashboard')

    else:
        return HttpResponse('Post Data Error')

def lecturer_logout(request):
    request.session['lecturer_id'] = ''
    request.session['lecturer_name'] = ''
    request.session['lecturer_first_name'] == ''
    request.session['lecturer_last_name'] == ''
    return HttpResponseRedirect('/cms')

def lecturer_dashboard(request):

    #Generating Institution Lists for Forms
    institutions_object = Institution.objects.all()
    institutions = []
    for i in institutions_object:
        institutions.append(i.name)

    #Generating Course Lists for View Course in Dashboard
    course_id_objects = On_course.objects.all().filter(lecturer_id=request.session.get('lecturer_id'))   
    course_objects = []
    for x in course_id_objects:
        temp_obj = Course.objects.get(id=x.course_id_id)
        institution_obj = Institution.objects.get(id=(Course_created_by.objects.get(course_id=x.course_id_id)).institution_id_id)
        temp_obj.institution = institution_obj.name
        temp_obj.crange = range(1,10)
        course_objects.append(temp_obj)   

    #Generating Course Sessions View
    course_session_objects = []
    for x in course_id_objects:
        user_course_sessions = Course_session.objects.all().filter(course_id=x.course_id_id)
        for y in user_course_sessions:
            temp_obj = y
            temp_obj.course = (Course.objects.get(id=y.course_id_id)).name
            course_session_objects.append(temp_obj) 
          
    #Generating Course Materials View
    course_material_objects = []
    for x in course_id_objects:
        user_course_sessions = Material.objects.all().filter(course_id=x.course_id_id)
        for y in user_course_sessions:
            temp_obj = y
            temp_obj.course = (Course.objects.get(id=y.course_id_id)).name
            course_material_objects.append(temp_obj) 

    #Generating Institution List
    course_institution_objects = []
    institution_obj = Institution.objects.all()
    for x in institution_obj:
        temp_obj = x
        course_institution_objects.append(temp_obj)

    #Generating Assignments Materials View
    course_assignment_objects = []
    for x in course_id_objects:
        user_course_assignments = Assignments.objects.all().filter(course_id=x.course_id_id)
        for y in user_course_assignments:
            temp_obj = y
            temp_obj.course = (Course.objects.get(id=y.course_id_id)).name
            course_assignment_objects.append(temp_obj) 


    #Context Variables            
    user = {}
    user['assignments'] = course_assignment_objects
    user['institution_list'] = course_institution_objects
    user['course_materials'] = course_material_objects
    user['course_sessions'] = course_session_objects
    user['view_course'] = course_objects
    user['institutions'] = institutions
    user['id'] = request.session.get('lecturer_id')
    user['name'] = request.session.get('lecturer_name')
    user['first_name'] = request.session.get('lecturer_first_name')
    user['last_name'] = request.session.get('lecturer_last_name')
    return render(request, 'cms/dashboard.html', user)

def add_course(request):

    if request.method == 'POST': #POST data validation
        course_name = request.POST.get('course_name','')
        course_institution = request.POST.get('course_institution')
        course_category = request.POST.get('course_category','')
        course_desc = request.POST.get('course_desc','')
        minimum_percent = request.POST.get('minimum_percent','')
        course_schedules = request.POST.get('course_schedules','')
        is_active = request.POST.get('is_active','')
        icon_image = request.FILES.get('icon_image','') #File Field for uploading profile image
        banner_image = request.FILES.get('banner_image','') #File Field for uploading profile image

        course_name_check = Course.objects.all().filter(name=course_name) #Checking for Course Name 
        for x in course_name_check:
            return HttpResponse('Course Name Error')

        institution_id = Institution()
        course_id = Course()

        course_object = Course(name=course_name, description=course_desc, min_grade=minimum_percent, is_active=is_active, course_schedules=course_schedules, course_icon= icon_image, course_banner= banner_image, course_category=course_category)
        course_object.save()

        #Course Created By ::::
        course_created_by_object = Course_created_by()

        course_created_by_object.course_id = course_object
        course_created_by_object.institution_id = Institution.objects.get(name=course_institution)

        course_created_by_object.save()

        #On_course Object
        on_course_object = On_course()

        on_course_object.lecturer_id = Lecturer.objects.get(id=request.session.get('lecturer_id'))
        on_course_object.course_id = course_object

        on_course_object.save()

        return HttpResponse("Course Creation Success")


def delete_course(request):
    if request.method == 'POST':
        delete_course_id = request.POST.get('delete_course_id')
        Course.objects.filter(id=delete_course_id).delete()
        return HttpResponse("Deleted Successfully")
    else: 
        return HttpResponse("Post data Error")


def add_course_session(request):

    if request.method == 'POST': #POST data validation
        session_course = request.POST.get('session_course','')
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end','')

        course_session_obj = Course_session()
        course_session_obj.course_id = Course.objects.get(id=session_course)
        course_session_obj.start_date = session_start
        course_session_obj.end_date = session_end
        course_session_obj.save()

        return HttpResponse("Course Session Creation Success")
    else:
        return HttpResponse("Post Data Error")


def delete_course_session(request):
    if request.method == 'POST':
        delete_course_session_id = request.POST.get('delete_course_session_id')
        Course_session.objects.filter(id=delete_course_session_id).delete()
        return HttpResponse("Course Session Deleted Successfully")
    else: 
        return HttpResponse("Post data Error")


def add_course_material(request):
    if request.method == 'POST': #POST data validation
        course_material = request.POST.get('course_material','')
        course_week = request.POST.get('course_week')
        course_link = request.POST.get('course_link','')
        course_text = request.POST.get('course_text','')

        course_material_obj = Material()
        course_material_obj.course_id = Course.objects.get(id=course_material)
        course_material_obj.week = course_week
        course_material_obj.material_link = course_link
        course_material_obj.material_text = course_text
        course_material_obj.save()

        return HttpResponse("Course Material Creation Success")
    else:
        return HttpResponse("Post Data Error")



def delete_course_material(request):
    if request.method == 'POST':
        delete_course_material_id = request.POST.get('delete_course_material_id')
        Material.objects.filter(id=delete_course_material_id).delete()
        return HttpResponse("Course Material Deleted Successfully")
    else: 
        return HttpResponse("Post data Error")



def add_institution(request):
    if request.method == 'POST': #POST data validation
        institution_name = request.POST.get('institution_name','')
        institution_location = request.POST.get('institution_location','')
  
        institution_name_check = Institution.objects.all().filter(name=institution_name) #Checking for Course Name 
        for x in institution_name_check:
            return HttpResponse('Institution Name Error')


        institution_object = Institution(name=institution_name, location=institution_location)
        institution_object.save()

        return HttpResponse("Institution Success")

        """
        if password == cpassword:
            password = hashlib.sha512(bytes(password)).hexdigest() #Password Hashing using SHA512 & HashDigest for Hexadecimal Convertion
        else:
            return HttpResponse('Password match error')

        email_check = Lecturer.objects.all().filter(email = email) #Checking for Email 
        user_name_check = Lecturer.objects.all().filter(user_name = user_name) #Checking for User Name

        for x in email_check:
            return HttpResponse('Email Error')

        for y in user_name_check:
            return HttpResponse('User Name Error')

        lecturer_object = Lecturer(profile_image = profile_image,first_name = first_name, last_name = last_name, email = email, user_name = user_name, password = password, country=country, gender = gender, conditions = True)
        lecturer_object.save()

        return HttpResponseRedirect('/cms')    """
    else:
        return HttpResponse('Post Data Error')


def delete_institution(request):
    if request.method == 'POST':
        delete_institution_id = request.POST.get('course_institution_id')
        Institution.objects.filter(id=delete_institution_id).delete()
        return HttpResponse("Institution Deleted Successfully")
    else: 
        return HttpResponse("Post data Error")


def add_assignment(request):
    if request.method == 'POST': #POST data validation
        assignment_course = request.POST.get('assignment_course','')
        assignment_week = request.POST.get('assignment_week')
        q1 = request.POST.get('q1','')
        q2 = request.POST.get('q2','')
        q3 = request.POST.get('q3','')
        q4 = request.POST.get('q4','')
        q5 = request.POST.get('q5','')
        q6 = request.POST.get('q6','')
        q7 = request.POST.get('q7','')
        q8 = request.POST.get('q8','')
        q9 = request.POST.get('q9','')
        q10 = request.POST.get('q10','')
        a1 = request.POST.get('a1','')
        a2 = request.POST.get('a2','')
        a3 = request.POST.get('a3','')
        a4 = request.POST.get('a4','')
        a5 = request.POST.get('a5','')
        a6 = request.POST.get('a6','')
        a7 = request.POST.get('a7','')
        a8 = request.POST.get('a8','')
        a9 = request.POST.get('a9','')
        a10 = request.POST.get('a10','')

        course_assignment_obj = Assignments()
        course_assignment_obj.course_id = Course.objects.get(id=assignment_course)
        course_assignment_obj.week = assignment_week
        course_assignment_obj.q1 = q1
        course_assignment_obj.q2 = q2
        course_assignment_obj.q3 = q3
        course_assignment_obj.q4 = q4
        course_assignment_obj.q5 = q5
        course_assignment_obj.q6 = q6
        course_assignment_obj.q7 = q7
        course_assignment_obj.q8 = q8
        course_assignment_obj.q9 = q9
        course_assignment_obj.q10 = q10
        course_assignment_obj.a1 = int(a1)
        course_assignment_obj.a2 = int(a2)
        course_assignment_obj.a3 = int(a3)
        course_assignment_obj.a4 = int(a4)
        course_assignment_obj.a5 = int(a5)
        course_assignment_obj.a6 = int(a6)
        course_assignment_obj.a7 = int(a7)
        course_assignment_obj.a8 = int(a8)
        course_assignment_obj.a9 = int(a9)
        course_assignment_obj.a10 = int(a10)
        course_assignment_obj.save()

        return HttpResponse("Assignment Created Successfully")
    else:
        return HttpResponse("Post Data Error")



def delete_assignment(request):
    if request.method == 'POST':
        delete_course_assignment_id = request.POST.get('delete_course_assignment_id')
        Assignments.objects.filter(id=delete_course_assignment_id).delete()
        return HttpResponse("Assignment Deleted Successfully")
    else: 
        return HttpResponse("Post data Error")



