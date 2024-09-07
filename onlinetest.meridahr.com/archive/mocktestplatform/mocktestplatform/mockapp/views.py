from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from mockapp.models import *
from mockapp.forms import StudentForm
from mockapp.forms import DocumentForm
from django.core.mail import send_mail
from django.contrib import messages



def main(request):
    return render(request,'first.html')

def mains(request):
    return render(request,'second.html')

def loginform(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        print(username,  password)

       
    
        try:
            user = user_register.objects.get(email=username, password=password)
        except user_register.DoesNotExist:
            user = None

        if user is not None:
            # Log the user in and redirect to the dashboard
            user.loged_in=True
            user.save()
            print("user logged in = ",user.loged_in)
            request.session['register_id']=user.register_id
            request.session['user_name']=user.name
            return redirect('dash')
        else:
            # Authentication failed, render the login form with an error message
            return render(request, 'Login copy.html', {'error_message': 'Invalid username or password'})
   
    else:
         registration_success_message = request.session.pop('registration_success_message', None)
      

        
    # Pass the message to the template context
         context = {'registration_success_message': registration_success_message}
         return render(request, 'Login copy.html',context)
 
def signup(request):
   
   if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # Perform any additional validation or checks as needed

        # Create the user
        user = user_register.objects.create(
            name=name,
            email=email,
            phone=phone,
            password=password
        )

        # Optionally, you can log the user in after registration
        # (you may need to implement your authentication logic)
        # For example:
        # login(request, user)

        
        request.session['registration_success_message'] = 'Registration successful. You can now log in.'
        return redirect('login')  # Redirect to the login page after successful registration


   return render(request,'SignUp.html')

def logout(request):
    user=request.session.get('user_name')
    print("djbshvbsvbkhjbfvnabvhv in logout ",user)
    loged_in=user_register.objects.get(name=user)
    loged_in.loged_in=False
    loged_in.save()
    return redirect('login')
    

def dashboard(request):
    
    user=request.session.get('user_name')
    print("djbshvbsvbkhjbfvnabvhv  ",user)
    loged_in=user_register.objects.get(name=user)
    
    if loged_in.loged_in==True:
        sub=add_subjects.objects.all()
        subjects={
        'sub':sub
        }
        return render(request,'dashboard.html',subjects)
    else:
        return render(request,'404.html')

def subject(request,sub):
   user=request.session.get('user_name')
   print("djbshvbsvbkhjbfvnabvhv  ",user)
   loged_in=user_register.objects.get(name=user)
   if loged_in.loged_in==True:
        s_img=add_subjects.objects.get(subject=sub)
        print("sub image is ",s_img.sub_image)
        context={
            'subject':sub,
            'subject_image':s_img.sub_image,
        }

        return render(request,'Examlisting.html',context)
   else:
       return render(request,'404.html')

from django.apps import apps
def mcq_question(request,subject,testlevel):
    user=request.session.get('user_name')
   
    loged_in=user_register.objects.get(name=user)
    if loged_in.loged_in==True:

        try:
            model = apps.get_model(app_label='mockapp', model_name=subject.capitalize())
            data = model.objects.filter(testlevel=testlevel)
            regi = request.session.get('register_id')
            que = {
                'data': data,
                'subject': subject,
                'testlevel': testlevel,
                'regi': regi
            }
            if not data.exists():
                return render(request, 'noquestions.html', {'subject': subject.capitalize()})


            print(data)
            return render(request, 'Questionpaper.html', que)
        except LookupError:
        # Handle the case where the model does not exist
            print(f"Model '{subject.capitalize()}' does not exist.")
            return render(request,'modelnotfound.html',{'subject':subject.capitalize()})
    else:
        return render(request,'404.html')

def mcq_verify(request,subject,testlevel,ans,regi):
    
    user=request.session.get('user_name')
   
    loged_in=user_register.objects.get(name=user)
    if loged_in.loged_in==True:
        ans_dict = json.loads(ans)
        print("answers= ",ans_dict)
        
        data={
            'subject':subject,
            'testlevel':testlevel,
            'ans':ans_dict
        }


        answered_count = 0
        unanswered_count = 0
        wrong_answers_count = 0
        model = apps.get_model(app_label='mockapp', model_name=subject.capitalize())
        
            
        for i,j in  ans_dict.items():
            try:
            
                query = Q(pk=i, answer=j, testlevel=testlevel)

            
                obj = model.objects.get(query)
                

            
                print(f"Correct answer for question ID {i}: {j}")
                print(f"Additional info: {obj.question}")  # Replace with actual field name

                # Incrementing the answered count
                answered_count += 1

            except model.DoesNotExist:
            
                print(f"Incorrect answer for question ID {i}: {j}")

                # Incrementing the wrong answers count
                wrong_answers_count += 1

        # calculating the unanswered count
        count_python_q=model.objects.filter(testlevel=testlevel)
        unanswered_count = count_python_q.count() - (answered_count+wrong_answers_count)

        # Calculating the marks answered out of the total questions given
        total_questions = count_python_q.count()
        marks_info = f"{answered_count} / {total_questions}"

        ur=user_register.objects.get(register_id=regi)
        student_instance = Student_result.objects.create(
        student_id=ur.register_id,
        student_name=ur.name,
        contact_number=ur.phone,
        email=ur.email,
        test_taken=f"{subject} {testlevel}",
        mcq_marks=marks_info,
        coding_marks="",
        
        )
        send_mail(
            "Test Results",
            f"{ur.name} your {subject} {testlevel} secured marks are {marks_info}",
            'irayya7777@gmail.com',
            [ur.email],
            fail_silently=True,
        )
        # Saving the instance to the database
        student_instance.save() 

        context = {
        'answered_count': answered_count,
        'unanswered_count': unanswered_count,
        'wrong_answers_count':wrong_answers_count,
        }    
        return render(request,'results2.html',context)
    else:
        return render(request,'404.html')



def coding_question(request, subject, testlevel):


    user=request.session.get('user_name')
   
    loged_in=user_register.objects.get(name=user)
    
    if loged_in.loged_in==True:
        print(subject, testlevel)
        sub = add_subjects.objects.get(subject=subject)
        coding_q = Coding_Questions.objects.filter(Q(subject=sub.id) & Q(test_level=testlevel))

        if not coding_q.exists():
                return render(request, 'noquestions.html', {'subject': subject.capitalize(),'testlevel':testlevel})
        regi=request.session.get('register_id')
        if request.method == "POST":
            
            regi = request.POST.get('regi')
            q_and_a = request.POST.get('jsonData')

            # Save data to the database
            ur=user_register.objects.get(register_id=regi)
            result = Student_coding_result.objects.create(
                student_name=ur.name,
                contact_number=ur.phone,
                email=ur.email,
                answers=q_and_a,
                coding_marks="pending",
                subject=subject,
                testlevel=testlevel
            )
            return redirect("/result")
        return render(request, "CodingAnswers.html", {"coding_q": coding_q, "sub": subject,'testlevel':testlevel,'register_id':regi})

    else:
        return render(request,'404.html')





######################################################################
def profile(request):
    return render(request,'profile.html')

def taketest(request):
    return render(request,'taketest.html')

def instructions(request,subject,testlevel):
    content={
        'subject':subject,
        'testlevel':testlevel
    }
    return render(request,'instructions.html',content)

def questions(request,subject,testlevel):
    print(subject,testlevel)
    time_limit = 3600  # 1 hour in seconds
    if subject=='python':
        data=python.objects.filter(testlevel=testlevel)
        que={'data':data,
             'time_limit': time_limit,
             'subject':subject,
             'testlevel':testlevel
             }
        print(data)
        return render(request,'mcq.html',que)
    
    elif subject=='java':
        data=java.objects.filter(testlevel=testlevel)
        que={'data':data,
             'time_limit': time_limit,
             'subject':subject,
             'testlevel':testlevel
             }
        print(data)
        return render(request,'mcq.html',que)
    
    elif subject=='javascript':
        data=javascript.objects.filter(testlevel=testlevel)
        que={'data':data,
             'time_limit': time_limit,
             'subject':subject,
             'testlevel':testlevel
             }
        print(data)
        return render(request,'mcq.html',que)
    
    elif subject=='html':
        data=html.objects.filter(testlevel=testlevel)
        que={'data':data,
             'time_limit': time_limit,
             'subject':subject,
             'testlevel':testlevel}
        print(data)
        return render(request,'mcq.html',que)
    
    elif subject=='css':
        data=css.objects.filter(testlevel=testlevel)
        que={'data':data,
             'time_limit': time_limit,
             'subject':subject,
             'testlevel':testlevel}
        print(data)
        return render(request,'mcq.html',que)
    
    elif subject=='bootstrap':
        data=bootstrap.objects.filter(testlevel=testlevel)
        que={'data':data,
             'time_limit': time_limit,
             'subject':subject,
             'testlevel':testlevel}
        print(data)
        return render(request,'mcq.html',que)

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirecting to a success page.
    else:
        form = DocumentForm()

    documents = uploaddocument.objects.all()  # Retrieving all the uploaded documents.
    return render(request, '.html', {'form': form, 'documents': documents})

import json
from django.db.models import Q

def crossverify(request,subject,testlevel,ans,name,contact_number,email_id):
    print(name,contact_number,email_id)
    ans_dict = json.loads(ans)
    print("answers= ",ans_dict)
    
    data={
        'subject':subject,
        'testlevel':testlevel,
        'ans':ans_dict
    }


    answered_count = 0
    unanswered_count = 0
    wrong_answers_count = 0
    
    if subject=='python':
        
        for i,j in  ans_dict.items():
            try:
           
              query = Q(pk=i, answer=j, testlevel=testlevel)

            
              python_obj = python.objects.get(query)
              

           
              print(f"Correct answer for question ID {i}: {j}")
              print(f"Additional info: {python_obj.question}")  # Replace with actual field name

              # Incrementing the answered count
              answered_count += 1

            except python.DoesNotExist:
            
             print(f"Incorrect answer for question ID {i}: {j}")

             # Incrementing the wrong answers count
             wrong_answers_count += 1

        # calculating the unanswered count
        count_python_q=python.objects.filter(testlevel=testlevel)
        unanswered_count = count_python_q.count() - (answered_count+wrong_answers_count)

        # Calculating the marks answered out of the total questions given
        total_questions = count_python_q.count()
        marks_info = f"{answered_count} / {total_questions}"

        student_instance = Student_result.objects.create(
        student_name=name,
        contact_number=contact_number,
        email=email_id,
        test_taken=f"{subject} {testlevel}",
        mcq_marks=marks_info,
        coding_marks="",
        student_id=""
        )
        send_mail(
           "Test Results",
           f"{name} your {subject} {testlevel} secured marks are {marks_info}",
           'swathipurnima5@gmail.com',
           [email_id],
           fail_silently=True,
        )
        # Saving the instance to the database
        student_instance.save() 
        
        
    elif subject=='javascript':
        for i,j in  ans_dict.items():
            try:
           
              query = Q(pk=i, answer=j, testlevel=testlevel)

            
              javascript_obj = javascript.objects.get(query)

           
              print(f"Correct answer for question ID {i}: {j}")
              print(f"Additional info: {javascript_obj.question}")  # Replace with actual field name

              # Incrementing the answered count
              answered_count += 1

            except javascript.DoesNotExist:
            
             print(f"Incorrect answer for question ID {i}: {j}")   

             # Incrementing the wrong answers count
             wrong_answers_count += 1

        # calculating the unanswered count
        count_javascript_q= javascript.objects.filter(testlevel=testlevel)
        unanswered_count = count_javascript_q.count() - (answered_count+wrong_answers_count) 

        # Calculating the marks answered out of the total questions given
        total_questions = count_javascript_q.count()
        marks_info = f"{answered_count} / {total_questions}"

        student_instance = Student_result.objects.create(
        student_name=name,
        contact_number=contact_number,
        email=email_id,
        test_taken=f"{subject} {testlevel}",
        mcq_marks=marks_info,
        coding_marks="",
        student_id=""
        )
        send_mail(
           "Test Results",
           f"{name} your {subject} {testlevel} secured marks are {marks_info}",
           'swathipurnima5@gmail.com',
           [email_id],
           fail_silently=True,
        )
        # Saving the instance to the database
        student_instance.save() 

    elif subject=='java':
        for i,j in  ans_dict.items():
            try:
           
              query = Q(pk=i, answer=j, testlevel=testlevel)

            
              java_obj = java.objects.get(query)

           
              print(f"Correct answer for question ID {i}: {j}")
              print(f"Additional info: {java_obj.question}")  # Replace with actual field name

              # Incrementing the answered count
              answered_count += 1

            except java.DoesNotExist:
            
             print(f"Incorrect answer for question ID {i}: {j}")    

             # Incrementing the wrong answers count
             wrong_answers_count += 1

        # calculating the unanswered count
        count_java_q= java.objects.filter(testlevel=testlevel)
        unanswered_count = count_java_q.count() - (answered_count+wrong_answers_count) 

        # Calculating the marks answered out of the total questions given
        total_questions = count_java_q.count()
        marks_info = f"{answered_count} / {total_questions}"

        student_instance = Student_result.objects.create(
        student_name=name,
        contact_number=contact_number,
        email=email_id,
        test_taken=f"{subject} {testlevel}",
       mcq_marks=marks_info,
        coding_marks="",
        student_id=""
        )
        send_mail(
           "Test Results",
           f"{name} your {subject} {testlevel} secured marks are {marks_info}",
           'swathipurnima5@gmail.com',
           [email_id],
           fail_silently=True,
        )
        # Saving the instance to the database
        student_instance.save() 

    elif subject=='html':
        for i,j in  ans_dict.items():
            try:
           
              query = Q(pk=i, answer=j, testlevel=testlevel)

            
              html_obj = html.objects.get(query)

           
              print(f"Correct answer for question ID {i}: {j}")
              print(f"Additional info: {html_obj.question}")  # Replace with actual field name

              # Incrementing the answered count
              answered_count += 1

            except html.DoesNotExist:
            
             print(f"Incorrect answer for question ID {i}: {j}")   

             # Incrementing the wrong answers count
             wrong_answers_count += 1

        # calculating the unanswered count
        count_html_q= html.objects.filter(testlevel=testlevel)
        unanswered_count = count_html_q.count() - (answered_count+wrong_answers_count) 

        # Calculating the marks answered out of the total questions given
        total_questions = count_html_q.count()
        marks_info = f"{answered_count} / {total_questions}"

        student_instance = Student_result.objects.create(
        student_name=name,
        contact_number=contact_number,
        email=email_id,
        test_taken=f"{subject} {testlevel}",
        mcq_marks=marks_info,
        coding_marks="",
        student_id=""
        )
        send_mail(
           "Test Results",
           f"{name} your {subject} {testlevel} secured marks are {marks_info}",
           'swathipurnima5@gmail.com',
           [email_id],
           fail_silently=True,
        )
        # Saving the instance to the database
        student_instance.save() 


    elif subject=='css':
        for i,j in  ans_dict.items():
            try:
           
              query = Q(pk=i, answer=j, testlevel=testlevel)

            
              css_obj = css.objects.get(query)

           
              print(f"Correct answer for question ID {i}: {j}")
              print(f"Additional info: {css_obj.question}")  # Replace with actual field name

              # Incrementing the answered count
              answered_count += 1

            except css.DoesNotExist:
            
             print(f"Incorrect answer for question ID {i}: {j}")    

             # Incrementing the wrong answers count
             wrong_answers_count += 1

        # calculating the unanswered count
        count_css_q= css.objects.filter(testlevel=testlevel)
        unanswered_count = count_css_q.count() - (answered_count+wrong_answers_count) 

        # Calculating the marks answered out of the total questions given
        total_questions = count_css_q.count()
        marks_info = f"{answered_count} / {total_questions}"

        student_instance = Student_result.objects.create(
        student_name=name,
        contact_number=contact_number,
        email=email_id,
        test_taken=f"{subject} {testlevel}",
        mcq_marks=marks_info,
        coding_marks="",
        student_id=""
        )
        send_mail(
           "Test Results",
           f"{name} your {subject} {testlevel} secured marks are {marks_info}",
           'swathipurnima5@gmail.com',
           [email_id],
           fail_silently=True,
        )
        # Saving the instance to the database
        student_instance.save() 

    elif subject=='bootstrap':
        for i,j in  ans_dict.items():
            try:
           
              query = Q(pk=i, answer=j, testlevel=testlevel)

            
              bootstrap_obj = bootstrap.objects.get(query)

           
              print(f"Correct answer for question ID {i}: {j}")
              print(f"Additional info: {bootstrap_obj.question}")  # Replace with actual field name

              # Incrementing the answered count
              answered_count += 1

            except bootstrap.DoesNotExist:
            
             print(f"Incorrect answer for question ID {i}: {j}")  

             # Incrementing the wrong answers count
             wrong_answers_count += 1

        # calculating the unanswered count
        count_bootstrap_q= bootstrap.objects.filter(testlevel=testlevel)
        unanswered_count = count_bootstrap_q.count() - (answered_count+wrong_answers_count) 

         # Calculating the marks answered out of the total questions given
        total_questions = count_bootstrap_q.count()
        marks_info = f"{answered_count} / {total_questions}"

        student_instance = Student_result.objects.create(
        student_name=name,
        contact_number=contact_number,
        email=email_id,
        test_taken=f"{subject} {testlevel}",
        mcq_marks=marks_info,
        coding_marks="",
        student_id=""
        )
        send_mail(
           "Test Results",
           f"{name} your {subject} {testlevel} secured marks are {marks_info}",
           'swathipurnima5@gmail.com',
           [email_id],
           fail_silently=True,
        )
        # Saving the instance to the database
        student_instance.save() 

    # Rendering the results in the template or modify as needed.
    context = {
       'answered_count': answered_count,
       'unanswered_count': unanswered_count,
       'wrong_answers_count':wrong_answers_count,
    }    
    return render(request,'results2.html',context)


def coding(request):
   obj=Coding_Questions.objects.all()
   basic_dic={}
   intermediate_dic={}
   advance_dic={}
   for i in obj:
      if i.test_level=="basic":
         basic_dic[i.subject.subject]=i.test_level
      elif i.test_level=="intermediate":
         intermediate_dic[i.subject.subject]=i.test_level
      else:
         advance_dic[i.subject.subject]=i.test_level

   data={
      "basic_dic":basic_dic,
      "intermediate_dic":intermediate_dic,
      "advance_dic":advance_dic
   }
   return render(request, 'coding.html',data)


def c_question(request, subject, testlevel):
    print(subject, testlevel)
    sub = add_subjects.objects.get(subject=subject)
    coding_q = Coding_Questions.objects.filter(Q(subject=sub.id) & Q(test_level=testlevel))

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        q_and_a = request.POST.get('jsonData')

        # Save data to the database
        result = Student_coding_result.objects.create(
            student_name=name,
            contact_number=phone,
            email=email,
            answers=q_and_a,
            coding_marks="pending",
            subject=subject,
            testlevel=testlevel
        )
        return redirect("/result")
    return render(request, "coding_test.html", {"coding_q": coding_q, "sub": subject})

def student_registration(request):
    if request.method == 'POST':
        print("student")
        form = StudentForm(request.POST)
        if form.is_valid():
            print("valid form")
            form.save()
            return redirect('dash') 
        else:
            # Print form errors to the console for debugging
            print(form.errors)
    else:
        form = StudentForm()

        return render(request, 'student_registration.html', {'form': form})

def student_results_view(request):
    student_results = Student_result.objects.all()

    email_subject = 'Student Results'
    email_message = 'Please find attached the latest student results.'

    recipients = ['recipient@example.com']

    email_template = render(request, 'student_results.html', {'student_results': student_results})
    email_content = email_template.content()

    # Sending email
    send_mail(
        email_subject,
        email_message,
        'sender@example.com',  # sender email
        recipients,
        html_message=email_content,
    )

    return render(request, 'student_results.html', {'student_results': student_results})


def result(request):

   return render(request,'result.html')


