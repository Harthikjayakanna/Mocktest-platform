from django.contrib import admin
from mockapp.models import mcq,html,css,python,java,javascript,bootstrap,uploaddocument,Coding_Questions,student,Student_result
from mockapp.models import *

admin.site.site_header='MY ADMINSTRATION'

from .forms import *

class QuestionsAllowAdmin(admin.ModelAdmin):
    form = QuestionsAllowForm
    list_filter=["sub"]

admin.site.register(QuestionsAllow, QuestionsAllowAdmin)

class codingQuestionsAllowAdmin(admin.ModelAdmin):
    form = CodingQuestionsAllowForm
    list_filter=["coding_sub"]

admin.site.register(CodingQuestionsAllow, codingQuestionsAllowAdmin)  
    

    
admin.site.register(Coding_Questions) 

class McqQuestionsAdmin(admin.ModelAdmin):
      list_display = ['subject','testlevel','question']
      search_fields = ['testlevel']
      list_filter = ('subject', 'testlevel')
admin.site.register(Mcq_questions,McqQuestionsAdmin)

admin.site.register(add_subjects)
admin.site.register(user_register)


class Student_result_admin(admin.ModelAdmin):
    list_display = [field.name for field in Student_result._meta.get_fields()]
    search_fields = [field.name for field in Student_result._meta.get_fields()]

class Student_codingresult_admin(admin.ModelAdmin):
    list_display = [field.name for field in Student_coding_result._meta.get_fields()]
    search_fields = [field.name for field in Student_coding_result._meta.get_fields()]

admin.site.register(Student_result, Student_result_admin)
admin.site.register(Student_coding_result,Student_codingresult_admin)


    


