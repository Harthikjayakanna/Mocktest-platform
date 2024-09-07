from django.db import models
import uuid

def generate_register_id():
    return 'SLA' + str(uuid.uuid4().hex)[:7].upper()

class user_register(models.Model):
    register_id=models.CharField(max_length=100,default=generate_register_id)
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=11)
    password=models.CharField(max_length=50)
    is_active=models.BooleanField(default=False)
    loged_in=models.BooleanField(default=False)

    def __str__(self):
        return self.name+"    "+self.password












class mcq(models.Model):
    question=models.CharField(max_length=500)
    optionA=models.CharField(max_length=500)
    optionB=models.CharField(max_length=500)
    optionC=models.CharField(max_length=500)
    optionD=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)

    def __str__(self):
        return self.question
    
# class mcq2(models.Model):
#     questions=models.CharField(max_length=500)
#     option1=models.CharField(max_length=500)
#     option2=models.CharField(max_length=500)
#     answers=models.CharField(max_length=500)

#     def __str__(self):
#         return self.questions


testlevel=(
    ('basic','Basic'),
    ('intermediate','Intermediate'),
    ('advance','Advance')
)    
class python(models.Model):
    testlevel = models.CharField(max_length=500,choices=testlevel)
    question=models.CharField(max_length=500,default=None)
    optionA=models.CharField(max_length=500)
    optionB=models.CharField(max_length=500)
    optionC=models.CharField(max_length=500)
    optionD=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    
    def __str__(self):
        return self.testlevel
    
class java(models.Model):
    testlevel = models.CharField(max_length=500,choices=testlevel)
    question=models.CharField(max_length=500,default=None)
    optionA=models.CharField(max_length=500)
    optionB=models.CharField(max_length=500)
    optionC=models.CharField(max_length=500)
    optionD=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    
    def __str__(self):
        return self.testlevel
    
class javascript(models.Model):
    testlevel = models.CharField(max_length=500,choices=testlevel)
    question=models.CharField(max_length=500,default=None)
    optionA=models.CharField(max_length=500)
    optionB=models.CharField(max_length=500)
    optionC=models.CharField(max_length=500)
    optionD=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    
    def __str__(self):
        return self.testlevel
    
class html(models.Model):
    testlevel = models.CharField(max_length=500,choices=testlevel)
    question=models.CharField(max_length=500,default=None)
    optionA=models.CharField(max_length=500)
    optionB=models.CharField(max_length=500)
    optionC=models.CharField(max_length=500)
    optionD=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    
    def __str__(self):
        return self.testlevel
    
class css(models.Model):
    testlevel = models.CharField(max_length=500,choices=testlevel)
    question=models.CharField(max_length=500,default=None)
    optionA=models.CharField(max_length=500)
    optionB=models.CharField(max_length=500)
    optionC=models.CharField(max_length=500)
    optionD=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    
    def __str__(self):
        return self.testlevel
    
class bootstrap(models.Model):
    testlevel = models.CharField(max_length=500,choices=testlevel)
    question=models.CharField(max_length=500,default=None)
    optionA=models.CharField(max_length=500)
    optionB=models.CharField(max_length=500)
    optionC=models.CharField(max_length=500)
    optionD=models.CharField(max_length=500)
    answer=models.CharField(max_length=500)
    
    def __str__(self):
        return self.testlevel
    
course_name=(('python','Python'),
             ('java','Java'),
             ('javascript','JavaScript'),
             ('html','HTML'),
             ('css','CSS'),
             ('bootstrap','Bootstrap'))

class uploaddocument(models.Model):
    course_name=models.CharField(max_length=100,choices=course_name)
    document=models.FileField(upload_to='documents/')




class CodingQuestion(models.Model):
    subject= models.CharField(max_length=200,default=' ',choices=course_name,help_text='Choose Subject.')
    test_level = models.CharField(max_length=200,default=' ',choices=testlevel,blank=True,help_text='Choose test level.')
    question_text = models.TextField(default='',blank=True,help_text='Enter your Question here.')
    code_snippet = models.TextField(default=" ",blank=True,help_text='Enter your Programming answer here.')
    correct_answer = models.TextField(default=' ',blank=True,help_text='Enter your Theory answer here.')

    def __str__(self):
        return self.question_text
    
class add_subjects(models.Model):
    
    subject= models.CharField(max_length=200,default=" ")
    sub_image=models.ImageField(upload_to='subject_images/', default=" ")
    def __str__(self):
        return self.subject

class Coding_Questions(models.Model):
    subject= models.ForeignKey(add_subjects,max_length=200,default=' ',on_delete=models.CASCADE,blank=True)
    test_level = models.CharField(max_length=200,default=' ',choices=testlevel,blank=True,help_text='Choose test level.')
    question_text = models.TextField(default='',blank=True,help_text='Enter your Question here.')
    code_snippet = models.TextField(default=" ",blank=True,help_text='Enter your Programming answer here.')
    correct_answer = models.TextField(default=' ',blank=True,help_text='Enter your Theory answer here.')


    def __str__(self):
        return self.question_text
    
class student(models.Model):
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    contact_number  = models.CharField(max_length=250)
    test_choosen = models.CharField(max_length=80,choices=course_name)

    def __str__(self):
        return self.full_name



class Student_result(models.Model):
    student_id = models.CharField(max_length=10,default="....")
    student_name = models.CharField(max_length=200,default="Not entered")
    contact_number = models.CharField(max_length=250,default="not entered")
    email=models.EmailField(default="Not Exist")
    test_taken = models.CharField(max_length=200,default=".....") 
    mcq_marks = models.CharField(max_length=100,default="....") 
   
    submitted_date_time=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.student_name
    
class Student_coding_result(models.Model):
    student_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=250)
    email=models.EmailField()
    subject=models.CharField(max_length=250,default=" ")
    answers=models.TextField(default=" ")
    testlevel = models.CharField(max_length=200) 
    coding_marks = models.CharField(max_length=100)
    submitted_date_time=models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.student_name


class Mcq_questions(models.Model):
    subject= models.ForeignKey(add_subjects,max_length=200,blank=True,on_delete=models.CASCADE)
    
    testlevel = models.CharField(max_length=500,choices=testlevel,blank=True)
    question=models.CharField(max_length=1000,default=None)
    optionA=models.CharField(max_length=1000)
    optionB=models.CharField(max_length=1000)
    optionC=models.CharField(max_length=1000)
    optionD=models.CharField(max_length=1000)
    answer=models.CharField(max_length=1000)


from django.db.models import Q
from django.core.exceptions import ValidationError

class QuestionsAllow(models.Model):
    sub=models.ForeignKey(add_subjects,on_delete=models.CASCADE,blank=False)
    testlevel=(
    ('basic','Basic'),
    ('intermediate','Intermediate'),
    ('advance','Advance')
            )  
    tl=models.CharField(max_length=100,choices=testlevel,default="basic")
    no_of_questions = models.IntegerField(default=0)
    def clean(self):
        # Check if the combination of sub and tl is unique
        if QuestionsAllow.objects.filter(sub=self.sub, tl=self.tl).exists():
            raise ValidationError({'tl': 'A record with this subject and test level already exists.'})


    class Meta:
        # Ensure that the combination of sub and tl is unique
        unique_together = ('sub', 'tl')

    def __str__(self):
        return self.sub.subject+"--->"+self.tl



class CodingQuestionsAllow(models.Model):
    coding_sub=models.ForeignKey(add_subjects,on_delete=models.CASCADE,blank=False)
    testlevel=(
    ('basic','Basic'),
    ('intermediate','Intermediate'),
    ('advance','Advance')
            )  
    test_level=models.CharField(max_length=100,choices=testlevel,default="basic")
    no_of_questions = models.IntegerField(default=0)
    def clean(self):
        # Check if the combination of sub and tl is unique
        if CodingQuestionsAllow.objects.filter(coding_sub=self.coding_sub, test_level=self.test_level).exists():
            raise ValidationError({'test_level': 'A record with this subject and test level already exists.'})


    class Meta:
        # Ensure that the combination of sub and tl is unique
        unique_together = ('coding_sub', 'test_level')

    def __str__(self):
        return self.coding_sub.subject+"--->"+self.test_level

    
