from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

# Create your models here.


"""

class UserProfile(models.Model):
    # One to One field
    user = models.OneToOneField(User)
    # Custom Fields
    country = models.CharField(max_length=20)
    gender = models.CharField(max_length=6)
    conditions = models.BooleanField()
    profile_image = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='imgs', blank=True)

    def __unicode__(self):
            return self.user.username
"""

class Student(models.Model):
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=40)
	email = models.CharField(max_length=40, default='India')
	user_name = models.CharField(max_length=10)
	password = models.CharField(max_length=130)
	country = models.CharField(max_length=20, default='India')
	gender = models.CharField(max_length=10, null=True)
	profile_image = models.ImageField(upload_to='lms/profile_pics/', default='lms/profile_pics/dummy.jpg')
	conditions = models.BooleanField(default=True)
     
class Course(models.Model):
	name = models.CharField(max_length=20)
	description = models.TextField()
	min_grade = models.DecimalField(decimal_places=2,max_digits=5)
	course_category = models.CharField(max_length=20, null=True)
	is_active = models.BooleanField()
	course_schedules = models.DecimalField(decimal_places=2,max_digits=5,blank=True)
	course_icon = models.ImageField(upload_to='cms/course_icon/', default='cms/course_icon/dummy.jpg')
	course_banner = models.ImageField(upload_to='cms/course_banner/', default='cms/course_banner/dummy.jpg')


class Institution(models.Model):
	name = models.CharField(max_length=20)
	location = models.CharField(max_length=20)

class Lecturer(models.Model):
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=40)
	email = models.CharField(max_length=40, default='India')
	user_name = models.CharField(max_length=10, default="user_name")
	password = models.CharField(max_length=130, default="password")
	country = models.CharField(max_length=20, default='India')
	gender = models.CharField(max_length=10, null=True)
	profile_image = models.ImageField(upload_to='cms/profile_pics/', default='cms/profile_pics/dummy.jpg')
	conditions = models.BooleanField(default=True)

class On_course(models.Model):
	lecturer_id = models.ForeignKey(Lecturer, on_delete = models.CASCADE)
	course_id = models.ForeignKey(Course, on_delete = models.CASCADE)

class Course_created_by(models.Model):
	institution_id = models.ForeignKey(Institution, on_delete = models.CASCADE, null=True)
	course_id = models.ForeignKey(Course, on_delete = models.CASCADE)


class Chapter(models.Model):
	course_id = models.ForeignKey(Course, on_delete = models.CASCADE)
	chapter_no = models.IntegerField()
	description = models.TextField()

class Course_session(models.Model):
	course_id = models.ForeignKey(Course, on_delete = models.CASCADE)
	start_date = models.DateField()
	end_date = models.DateField()


class Status(models.Model):
	status_name = models.CharField(max_length=20)

class Enrolled_course(models.Model):
	student_id = models.ForeignKey(Student, on_delete = models.CASCADE)
	course_session_id = models.ForeignKey(Course, on_delete = models.CASCADE)
	enrollment_date = models.DateField()
	grade = models.DecimalField(decimal_places=2,max_digits=2, null=True)
	#certificate_ID = models.TextField(max_length=20)
	#certificate_location = models.TextField(max_length=20)

class Material_type(models.Model):
	type_name = models.CharField(max_length=30)

class Material(models.Model):
	course_id = models.ForeignKey(Course, on_delete = models.CASCADE, null=True)
	week = models.DecimalField(decimal_places=0, max_digits=2, null=True)
	material_link = models.TextField(null=True)
	material_text = models.TextField(null=True)

"""class Assignments(models.Model):
	course_id = models.ForeignKey(Course, on_delete = models.CASCADE, null=True)
	week = models.DecimalField(decimal_places=0, max_digits=2, null=True)
	material_link = models.TextField(null=True)
	material_text = models.TextField(null=True)"""

class Assignments(models.Model):
	course_id = models.ForeignKey(Course, on_delete = models.CASCADE, null=True)
	week = models.DecimalField(decimal_places=0, max_digits=2, null=True)
	q1 = models.TextField(null=True)
	a1 = models.DecimalField(decimal_places=0, max_digits=1, null=True)
	q2 = models.TextField(null=True)
	a2 = models.DecimalField(decimal_places=0, max_digits=1, null=True)
	q3 = models.TextField(null=True)
	a3 = models.DecimalField(decimal_places=0, max_digits=1, null=True)
	q4 = models.TextField(null=True)
	a4 = models.DecimalField(decimal_places=0, max_digits=1, null=True)
	q5 = models.TextField(null=True)
	a5 = models.DecimalField(decimal_places=0, max_digits=1, null=True)
	q6 = models.TextField(null=True)
	a6 = models.DecimalField(decimal_places=0, max_digits=1, null=True)
	q7 = models.TextField(null=True)
	a7 = models.DecimalField(decimal_places=0, max_digits=1, null=True)
	q8 = models.TextField(null=True)
	a8 = models.DecimalField(decimal_places=0, max_digits=1, null=True)
	q9 = models.TextField(null=True)
	a9 = models.DecimalField(decimal_places=0, max_digits=1, null=True)
	q10 = models.TextField(null=True)
	a10 = models.DecimalField(decimal_places=0, max_digits=1, null=True)


class Student_results(models.Model):
	assignment_id = models.ForeignKey(Assignments, on_delete = models.CASCADE, null=True)
	enrolled_course_id = models.ForeignKey(Enrolled_course, on_delete = models.CASCADE, null=True)
	#attempt = models.IntegerField()
	#attempt_link = models.TextField()
	#started = models.DateTimeField()
	#ended = models.DateTimeField()
	score = models.IntegerField()

