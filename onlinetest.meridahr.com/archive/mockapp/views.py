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
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponse, redirect

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import requests

def redirect_to_login(request):
    return redirect('login')  


def function(request,phone):#krishna
# Your IPQualityScore API key
    api_key = 'npDpb5niKutZ8vCBXjKoacTZM863Gkaf'
    
    # The mobile number you want to check
    india='+91'
    mobile_number = f'{india}{phone}'

    # The API endpoint
    url = f'https://ipqualityscore.com/api/json/phone/{api_key}/{mobile_number}'

    # Make the API request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Get the network provider information
        network_provider = data.get('carrier', 'Unknown')

        message_coming = data.get('message')
        print(network_provider)
        return HttpResponse(network_provider)
    else:
       return HttpResponse(message_coming)

def loginform(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        print(username,  password)

       
    
        try:
              password=urlsafe_base64_encode(force_bytes(password))
              user = user_register.objects.get(email=username, password=password)
        except user_register.DoesNotExist:
            user = None

        if user is not None:
            # Log the user in and redirect to the dashboard
            #user.loged_in=True
            #user.save()
            #print("user logged in = ",user.loged_in)
            #request.session['register_id']=user.register_id
            #request.session['user_name']=user.name
            #return redirect('dash')
            
            if user.is_active:
                  # Store user's data in session
                  request.session['register_id']=user.register_id
                  request.session['user_name'] = user.name  # Store any other user data you need


                  user.loged_in=True
                  user.save()
                  # Redirect to a success page or dashboard
                  return redirect('dash')
        else:
            # Authentication failed, render the login form with an error message
            return render(request, 'Login copy.html', {'error_message': 'Invalid username or password'})
   
    else:
         registration_success_message = request.session.pop('registration_success_message', None)
      

        
    
         context = {'registration_success_message': registration_success_message}
         return render(request, 'Login copy.html',context)
         
def ForgotPassword(request):#krishna
    if request.method=='POST':
        email=request.POST.get('email')
        try:
            user=user_register.objects.get(email=email)
            
            if user is not None:
                # userid=urlsafe_base64_encode(force_bytes(user.id))
                # return redirect(f"/newpassword/{userid}/")
                verification_url = reverse('new_password', kwargs={ 'uid': urlsafe_base64_encode(force_bytes(user.pk))})

                absolute_verification_url = request.build_absolute_uri(verification_url)
                html_content = render_to_string('hari/email_template2.html', {'verification_url': absolute_verification_url})

                # Create EmailMultiAlternatives object
                subject=f'{user.name} Verify your email'
                msg = EmailMultiAlternatives(
                    subject,
                    body='Please enable HTML to view this message.',
                    from_email='from@example.com',
                    to=[email]
                )
            
                # Attach HTML content
                msg.attach_alternative(html_content, "text/html")

                # Send email
                msg.send()
                return HttpResponse("Please check your email for verification instructions.")
        except:
            
            return HttpResponse('mmdmdlemde')
    return render(request,'hari/email.html')

def CreateNewPsaaword(request,uid):#krishna
    if request.method=="POST":
        New_password = request.POST.get("password")
        confirm_password = request.POST.get("confirmpassword")

        if New_password != confirm_password:
            return HttpResponse('<script>alert("Passwords do not match. Please try again."); window.location.href="/newpassword/{uid}/";</script>')
        else:
            uid = urlsafe_base64_decode(uid).decode()
            user = user_register.objects.get(pk=uid)
            if user:
                # user.is_active = True
                New_password=urlsafe_base64_encode(force_bytes(New_password))
                user.password=New_password
                user.save() 
                return HttpResponse(f'New password updated successfuly <a href="/">login</a>')
    return render(request,'hari/new_password.html')



def ChangePassword(request):#krishna
    if request.method=="POST":
        password=request.POST.get("password")
        New_password = request.POST.get("newpassword")
        confirm_password = request.POST.get("confirmpassword")
        password=urlsafe_base64_encode(force_bytes(password))
        register_id = request.session.get('register_id')
        obj=user_register.objects.get(id=register_id)
    
        if obj.password==password:
            if New_password != confirm_password:
                    return HttpResponse('<script>alert("Passwords do not match. Please try again."); window.location.href="/changepassword";</script>')
            else:
                if obj:
                    New_password=urlsafe_base64_encode(force_bytes(New_password))
                    obj.password=New_password
                    obj.save() 
                    return HttpResponse('<script>alert("password changed successfully");window.location.href="/dashboard";</script>')
        else:
            return HttpResponse('<script>alert("Enter the correct password."); window.location.href="/changepassword";</script>')
    return render(request,'hari/change_password.html')
 
#def signup(request):
   
#   if request.method == 'POST':
#        name = request.POST.get('name')
#        email = request.POST.get('email')
#        phone = request.POST.get('phone')
#        password = request.POST.get('password')

        # Perform any additional validation or checks as needed

        # Create the user
#        user = user_register.objects.create(
#            name=name,
#            email=email,
#            phone=phone,
#            password=password
 #       )

        # Optionally, you can log the user in after registration
        # (you may need to implement your authentication logic)
        # For example:
        # login(request, user)

        
#        request.session['registration_success_message'] = 'Registration successful. You can now log in.'
#        return redirect('login')  # Redirect to the login page after successful registration
#

#   return render(request,'SignUp.html')
   
def signup(request):#krishna
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        print("pasword is password",password)
        confirm_password = request.POST.get("confirmpassword")

        # result=function(f'+91{phone}')

        if password != confirm_password:
            return HttpResponse('<script>alert("Passwords do not match. Please try again."); window.location.href="/register";</script>')

        if user_register.objects.filter(email=email).exists():
            return HttpResponse('<script>alert("Email already exists. Please choose a different email."); window.location.href="/register";</script>')

        obj = user_register.objects.create(name=name, email=email, phone=phone,is_active=False)
        
        
        verification_url = reverse('verify_email', kwargs={ 'uidb64': urlsafe_base64_encode(force_bytes(obj.pk)),'uidb64ps': urlsafe_base64_encode(force_bytes(password))})
        absolute_verification_url = request.build_absolute_uri(verification_url)
        
        
        
        html_content = render_to_string('hari/email_template.html', {'verification_url': absolute_verification_url})

        # Create EmailMultiAlternatives object
        subject=f'{name} Verify your email'
        msg = EmailMultiAlternatives(
            subject,
            body='Please enable HTML to view this message.',
            from_email='from@example.com',
            to=[email]
        )

        # Attach HTML content
        msg.attach_alternative(html_content, "text/html")

        # Send email
        msg.send()

        return HttpResponse("Registered successfully. Please check your email for verification instructions.")
    
    return render(request, "hari/register.html")
    
def verify_email(request, uidb64,uidb64ps):#krishna
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = user_register.objects.get(pk=uid)
        print("verified password is ",uidb64ps)
        if user:
            user.is_active = True
            user.password=uidb64ps
            user.save()
    except (TypeError, ValueError, OverflowError, user_register.DoesNotExist):
        return HttpResponse('Invalid verification link.')
    return HttpResponse('Verified successfuly click here to login<a href="/">login</a>')

def logout(request):
    user=request.session.get('register_id')
    print("djbshvbsvbkhjbfvnabvhv in logout ",user)
    loged_in=user_register.objects.get(register_id=user)
    loged_in.loged_in=False
    loged_in.save()
    return redirect('login')
    
#########################Shuffled##########################

def shuffled_mcq_question(request,subject):
    user=request.session.get('user_name')
    c=0
    print(c)
    loged_in=user_register.objects.get(name=user)
    if loged_in.loged_in==True:
        c+=1
        print("the c value is ",c)
        basic_questions = Mcq_questions.objects.filter(subject__subject=subject, testlevel='basic')
        intermediate_questions = Mcq_questions.objects.filter(subject__subject=subject, testlevel='intermediate')
        advance_questions = Mcq_questions.objects.filter(subject__subject=subject, testlevel='advance')
        
        # Shuffle the questions within each test level
        basic_questions_shuffled = list(basic_questions)
        random.shuffle(basic_questions_shuffled)
        
        intermediate_questions_shuffled = list(intermediate_questions)
        random.shuffle(intermediate_questions_shuffled)
        
        advance_questions_shuffled = list(advance_questions)
        random.shuffle(advance_questions_shuffled)
        
        # Select the desired number of questions from each test level
        num_basic_questions = 5  #implement model
        num_intermediate_questions = 5
        num_advance_questions = 5
        
        selected_basic_questions = basic_questions_shuffled[:num_basic_questions]
        selected_intermediate_questions = intermediate_questions_shuffled[:num_intermediate_questions]
        selected_advance_questions = advance_questions_shuffled[:num_advance_questions]
        
        # Combine the selected questions from all test levels
        combined_questions = selected_basic_questions + selected_intermediate_questions + selected_advance_questions

        total=len(combined_questions)
        print("totalssssss=",total)
        request.session['total']=total
        # Shuffle the combined set of questions
       
        random.shuffle(combined_questions)
        regi = request.session.get('register_id')
        print("cmbined questions=",combined_questions)
        que = {
            'data': combined_questions,
            'subject': subject,
            
            'regi': regi
        }
        
        # Pass the shuffled and selected questions to the HTML template
        context = {'shuffled_questions': combined_questions}
        return render(request, 'shuffle/Questionpaper.html', que)
    
def shuffled_mcq_verify(request,subject,ans,regi):
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
        num_basic_questions = 1  #implement model
        num_intermediate_questions = 1
        num_advance_questions = 1
        total=request.session.get('total')
        print("total= ",total)
        # model = apps.get_model(app_label='mockapp', model_name=subject.capitalize())
        sub=add_subjects.objects.get(subject=subject)
        # model=Mcq_questions.objects.filter(subject=sub.pk)
            
        for i,j in  ans_dict.items():
            try:
            
                query = Q(pk=i, answer=j,subject=sub.pk)

            
                obj = Mcq_questions.objects.get(query)
                

            
                print(f"Correct answer for question ID {i}: {j}")
                print(f"Additional info: {obj.question}")  # Replace with actual field name

                # Incrementing the answered count
                answered_count += 1

            except ObjectDoesNotExist:
            
                print(f"Incorrect answer for question ID {i}: {j}")

                # Incrementing the wrong answers count
                wrong_answers_count += 1

        # calculating the unanswered count
        count_python_q=Mcq_questions.objects.filter(testlevel=testlevel,subject=sub.pk)
        unanswered_count = total - (answered_count+wrong_answers_count)

        # Calculating the marks answered out of the total questions given
        total_questions = total
        marks_info = f"{answered_count} / {total_questions}"

        ur=user_register.objects.get(register_id=regi)
        student_instance = Student_result.objects.create(
        student_id=ur.register_id,
        student_name=ur.name,
        contact_number=ur.phone,
        email=ur.email,
        test_taken=f"{subject} {testlevel}",
        mcq_marks=marks_info,
        
        
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
        return render(request,'shuffle/results2.html',context)
    else:
        return render(request,'404.html')

def shuffled_coding_question(request,subject):
    user=request.session.get('user_name')
    regi=request.session.get('register_id')
   
    loged_in=user_register.objects.get(name=user)
    
    if loged_in.loged_in:
        # Retrieve the user's selected test level
        
        # Retrieve the subject object
        sub = add_subjects.objects.get(subject=subject)
        
        # Retrieve coding questions for each test level
        basic_questions = Coding_Questions.objects.filter(subject__subject=sub, test_level='basic')
        intermediate_questions = Coding_Questions.objects.filter(subject__subject=sub, test_level='intermediate')
        advance_questions = Coding_Questions.objects.filter(subject__subject=sub, test_level='advance')
        
        # Shuffle the questions within each test level
        basic_questions_shuffled = list(basic_questions)
        random.shuffle(basic_questions_shuffled)
        
        intermediate_questions_shuffled = list(intermediate_questions)
        random.shuffle(intermediate_questions_shuffled)
        
        advance_questions_shuffled = list(advance_questions)
        random.shuffle(advance_questions_shuffled)
        
        # Select the desired number of questions from each test level
        num_basic_questions = 5  # Adjust this based on your requirements
        num_intermediate_questions = 5
        num_advance_questions = 5
        
        selected_basic_questions = basic_questions_shuffled[:num_basic_questions]
        selected_intermediate_questions = intermediate_questions_shuffled[:num_intermediate_questions]
        selected_advance_questions = advance_questions_shuffled[:num_advance_questions]
        
        # Combine the selected questions from all test levels
        combined_questions = selected_basic_questions + selected_intermediate_questions + selected_advance_questions

        total = len(combined_questions)
        request.session['total_coding_questions'] = total
        
        # Shuffle the combined set of questions
        random.shuffle(combined_questions)
        
        # Prepare the context to pass to the template
        
        context={"coding_q": combined_questions, 
              "sub": subject,
              
              'register_id':regi
              }
        
        return render(request, 'shuffle/codingquestions2.html', context)
    else:
        return render(request, '404.html')
    
def shuffled_coding_answers(request,subject):
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
    else:
        return render(request,'404.html')

########################Shuffled###############################
from django.http import Http404

def dashboard(request):
    user = request.session.get('user_name')
    print("djbshvbsvbkhjbfvnabvhv  ", user)

    register_id=request.session.get('register_id')


    try:
        loged_in = user_register.objects.get(register_id=register_id)

        if loged_in.loged_in:
            sub = add_subjects.objects.all()
            subjects = {
            'sub': sub,
            'user':user
            }
            if request.method=="POST":
                sub_value=request.POST.get("search")
                if sub_value: 
                        search_val=add_subjects.objects.filter(subject__icontains=sub_value)
                        return render(request,'hari/search1.html',{"search_val":search_val,"user":user})
            print("after login ", user)
            return render(request, 'dashboard.html', subjects)
        else:
            print("no login ", user)
            return render(request, '404.html')

    except user_register.DoesNotExist:
        print(register_id)
        # Handle the case where user_register with the given name does not exist
        return render(request, '404.html')


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

        return render(request,'shuffle/Examlisting2.html',context)
   else:
       return render(request,'404.html')

import random 
def mcq_question(request, subject, testlevel):
    user = request.session.get('user_name')

    loged_in = user_register.objects.get(name=user)
    if loged_in.loged_in == True:
        try:
            sub = add_subjects.objects.get(subject=subject)
            data = Mcq_questions.objects.filter(testlevel=testlevel, subject=sub.pk)
            #random.shuffle(data)
            regi = request.session.get('register_id')
            mcq_allow = QuestionsAllow.objects.filter(Q(tl=testlevel) & Q(sub=sub.pk))
            # sub = ''
            count = ""
            if mcq_allow:
                for i in mcq_allow:
                    # sub += str(i.sub)
                    count += str(i.no_of_questions)
            else:
                count = 0

            c = int(count) + 1

            que = {
                'data': data,
                'subject': subject,
                'testlevel': testlevel,
                'regi': regi,
                "count": c
            }
            if not data.exists():
                return render(request, 'noquestions.html', {'subject': subject.capitalize()})

            print(data)
            return render(request, 'Questionpaper.html', que)
        except LookupError:
            # Handle the case where the model does not exist
            print(f"Model '{subject.capitalize()}' does not exist.")
            return render(request, 'modelnotfound.html', {'subject': subject.capitalize()})
    else:
        return render(request, '404.html')

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
        #model = apps.get_model(app_label='mockapp', model_name=subject.capitalize())
        sub=add_subjects.objects.get(subject=subject)
            
        for i,j in  ans_dict.items():
            try:
            
                query = Q(pk=i, answer=j, testlevel=testlevel,subject=sub.pk)

            
                obj =  Mcq_questions.objects.get(query)
                

            
                print(f"Correct answer for question ID {i}: {j}")
                print(f"Additional info: {obj.question}")  # Replace with actual field name

                # Incrementing the answered count
                answered_count += 1

            except ObjectDoesNotExist:
            
                  print(f"Incorrect answer for question ID {i}: {j}")

                  # Incrementing the wrong answers count
                  wrong_answers_count += 1

        # calculating the unanswered count
        count_python_q=Mcq_questions.objects.filter(testlevel=testlevel,subject=sub.pk)
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
        #random.shuffle(coding_q)
        if not coding_q.exists():
                return render(request, 'noquestions.html', {'subject': subject.capitalize(),'testlevel':testlevel})
        regi=request.session.get('register_id')
        if request.method == "POST":
            
            regi = request.POST.get('regi')
            q_and_a = request.POST.get('jsonData')
            print(q_and_a)

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
            
        coding_allow=CodingQuestionsAllow.objects.filter(Q(test_level=testlevel) & Q(coding_sub=sub.pk))
        count=''
        if coding_allow:
            for i in coding_allow:
                count += str(i.no_of_questions)
        else:
            count = 0
        c = int(count) + 1
        return render(request, "CodingAnswers.html", {"coding_q": coding_q, "sub": subject,'testlevel':testlevel,'register_id':regi,'count':c})

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


