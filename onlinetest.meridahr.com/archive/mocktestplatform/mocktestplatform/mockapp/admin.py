from django.contrib import admin
from mockapp.models import mcq,html,css,python,java,javascript,bootstrap,uploaddocument,Coding_Questions,student,Student_result
from mockapp.models import *

admin.site.site_header='MY ADMINSTRATION'

# admin.site.register(mcq)
admin.site.register(python)
admin.site.register(java)
admin.site.register(javascript)
admin.site.register(css)
admin.site.register(html)
admin.site.register(bootstrap)
admin.site.register(uploaddocument)
admin.site.register(Coding_Questions) 
admin.site.register(student)
admin.site.register(add_subjects)

admin.site.register(user_register)
#admin.site.register(Student_result)

class Student_result_admin(admin.ModelAdmin):
    list_display = [field.name for field in Student_result._meta.get_fields()]
    search_fields = [field.name for field in Student_result._meta.get_fields()]

class Student_codingresult_admin(admin.ModelAdmin):
    list_display = [field.name for field in Student_coding_result._meta.get_fields()]
    search_fields = [field.name for field in Student_coding_result._meta.get_fields()]

admin.site.register(Student_result, Student_result_admin)
admin.site.register(Student_coding_result,Student_codingresult_admin)

