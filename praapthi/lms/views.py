from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import Http404, HttpResponseRedirect, HttpResponse 
from django.views import generic

from django.template import RequestContext

from django.contrib.auth.models import User
#from lms.models import UserProfile
#from lms.forms import UserForm, UserProfileForm
from lms.models import Student, Course, Enrolled_course, Material, Assignments, Student_results, Enrolled_course

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required

import hashlib

import time, datetime



def index(request):
    return render(request, 'lms/index.html')


def register(request):
    return render(request, 'lms/register.html')

def registerp(request):

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

        email_check = Student.objects.all().filter(email = email) #Checking for Email 
        user_name_check = Student.objects.all().filter(user_name = user_name) #Checking for User Name

        for x in email_check:
            return HttpResponse('Email Error')

        for y in user_name_check:
            return HttpResponse('User Name Error')

        student_object = Student(profile_image = profile_image,first_name = first_name, last_name = last_name, email = email, user_name = user_name, password = password, country=country, gender = gender, conditions = True)
        student_object.save()

        return HttpResponseRedirect('/cms')  
    else:
        return HttpResponse('Post Data Error')

#def image_upload(request):

def student_login(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        user_id = 0
        user_first_name = ''

        password = hashlib.sha512(bytes(password)).hexdigest()

        user_name_check = Student.objects.all().filter(user_name = user_name)
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

        request.session['user_id'] = user_id
        request.session['user_name'] = user_name
        request.session['user_first_name'] = user_first_name
        request.session['user_last_name'] = user_last_name
        request.session['redirect'] = ''

        return HttpResponseRedirect('/lms/dashboard')

    else:
        return HttpResponse('Post Data Error')

def student_logout(request):
    request.session['user_id'] = ''
    request.session['user_name'] = ''
    request.session['user_first_name'] == ''
    request.session['user_last_name'] == ''
    return HttpResponseRedirect('/lms')


def student_profile(request):
    return HttpResponse('Profile')



def student_dashboard(request):

    #Generating all course list
    course_objects = Course.objects.all()
    course_list = []
    for x in course_objects:
        temp_obj = x
        course_list.append(temp_obj)

    #Generating Enrolled Course List
    enrolled_course_objects = Enrolled_course.objects.all().filter(student_id=request.session.get('user_id'))
    enrolled_course_list = []
    for x in enrolled_course_objects:
        temp_obj = Course.objects.get(id=x.course_session_id_id)
        enrolled_course_list.append(temp_obj)



    user = {}
    user['enrolled_course_list'] = enrolled_course_list
    user['course_list'] = course_list
    user['id'] = request.session.get('user_id')
    user['name'] = request.session.get('user_name')
    user['first_name'] = request.session.get('user_first_name')
    user['last_name'] = request.session.get('user_last_name')
    return render(request, 'lms/dashboard.html', user)







"""  
        registered = False
        if request.method == 'POST':
                uform = UserForm(data = request.POST)
                pform = UserProfileForm(data = request.POST)
                if uform.is_valid() and pform.is_valid():
                        user = uform.save()
                        # form brings back a plain text string, not an encrypted password
                        pw = user.password
                        # thus we need to use set password to encrypt the password string
                        user.set_password(pw)
                        user.save()
                        profile = pform.save(commit = False)
                        profile.user = user
                        profile.save()
                        save_file(request.FILES['picture'], user.username)
                        registered = True
                else:
                        print uform.errors, pform.errors
        else:
                uform = UserForm()
                pform = UserProfileForm()

        return render(request, 'lms/register.html', {'uform': uform, 'pform': pform, 'registered': registered })

def save_file(file,  user_name, path='profile_pics/'):
        filename = user_name + '.jpg'
        fd = open('%s/%s' % (settings.MEDIA_ROOT, str(path) + str(filename)), 'wb' )
        for chunk in file.chunks():
                fd.write(chunk)
        fd.close()


def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None:
              if user.is_active:
                  login(request, user)
                  # Redirect to index page.
                  return HttpResponse("Success.")
              else:
                  # Return a 'disabled account' error message
                  return HttpResponse("You're account is disabled.")
          else:
              # Return an 'invalid login' error message.
              print  "invalid login details " + username + " " + password
              return render(request, 'lms/login.html', {}, context)
    else:
        # the login is a  GET request, so just show the user the login form.
        return render(request, 'lms/login.html', {}, context)


def custom(request):
        if not request.user.is_authenticated():
                return HttpResponseRedirect('/lms/login/')
        else:
        
	return HttpResponse('Rango says: since you are an authenticated user you can view this restricted page.')
"""

def student_enroll_course(request):

    if request.method == 'POST': #POST data validation
        enroll_course_id = request.POST.get('enroll_course_id','')
        enroll_student_id = request.session.get('user_id')
        enroll_date = '2017-04-26'
        enroll_grade = 0

        course_enroll_obj = Enrolled_course()
        course_enroll_obj.student_id = Student.objects.get(id=enroll_student_id)
        course_enroll_obj.course_session_id = Course.objects.get(id=enroll_course_id)
        course_enroll_obj.enrollment_date = enroll_date
        course_enroll_obj.grade = enroll_grade
        course_enroll_obj.save()
        #course_enroll_obj.course_id = Course.objects.get(id=session_course)
        #course_enroll_obj.start_date = session_start
        #course_enroll_obj.end_date = session_end
        #course_enroll_obj.save()

        return HttpResponse("Course Enrollment completed Successfully")
    else:
        return HttpResponse("Post Data Error")


def student_course_access(request):

    course_id = request.GET.get('course_id')

    #Generate Course Material List
    course_materials = Material.objects.all().filter(course_id=course_id)
    material_list = []
    for x in course_materials:
        temp_obj = x
        material_list.append(temp_obj)

    #Generate Course Assignement Lists
    course_assignments = Assignments.objects.all().filter(course_id=course_id)
    assignment_list = []
    for x in course_assignments:
        temp_obj = x
        assignment_list.append(temp_obj)


    user = {}
    user['course_id'] = course_id
    user['assignment_list'] = assignment_list
    user['material_list'] = material_list
    user['id'] = request.session.get('user_id')
    user['name'] = request.session.get('user_name')
    user['first_name'] = request.session.get('user_first_name')
    user['last_name'] = request.session.get('user_last_name')
 

    return render(request, 'lms/course-access.html', user)



def student_assignment_submission(request):

    assignment_id = request.POST.get('assignment_id')
    course_id = request.POST.get('course_id')



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

    assignment_object = Assignments.objects.get(id=assignment_id)

    score = 0

    if int(a1) == assignment_object.a1:
        score = score + 10
    if int(a2) == assignment_object.a2:
        score = score + 10
    if int(a3) == assignment_object.a3:
        score = score + 10
    if int(a4) == assignment_object.a4:
        score = score + 10
    if int(a5) == assignment_object.a5:
        score = score + 10
    if int(a6) == assignment_object.a6:
        score = score + 10
    if int(a7) == assignment_object.a7:
        score = score + 10
    if int(a8) == assignment_object.a8:
        score = score + 10
    if int(a9) == assignment_object.a9:
        score = score + 10
    if int(a10) == assignment_object.a10:
        score = score + 10

    enrolled_course = Enrolled_course.objects.get(student_id=request.session.get('user_id'), course_session_id=course_id)
    student_result_object = Student_results()
    student_result_object.assignment_id = assignment_object
    student_result_object.enrolled_course_id = enrolled_course
    student_result_object.score = score
    student_result_object.save()



    return HttpResponse("Assignment Submitted Succesfully")












