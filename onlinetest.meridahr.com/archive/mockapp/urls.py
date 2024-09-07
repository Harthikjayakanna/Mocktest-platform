from django.contrib import admin
from django.urls import path,re_path
from mockapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('main',views.main,name='main'),
    # path('mains',views.mains,name='mains'),
    path('',views.loginform,name='login'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logout,name='logoutt'),
    path('dashboard',views.dashboard,name= 'dash'),
    path("subject/<sub>",views.subject,name="subject"),
    path('mcq_question/<subject>/<testlevel>',views.mcq_question,name="mcq_question"),
    path('mcq_verify/<subject>/<testlevel>/<ans>/<regi>',views.mcq_verify,name='mcq_verify'),
    path('coding/<subject>/<testlevel>',views.coding_question,name='coding'),
    path("result",views.result),
    
    path("register",views.signup,name="register"),
    # path('verify-email/<uidb64>/<uid64ps>/',views.verify_email, name='verify_email'),
    path('verify-email/<str:uidb64>/<str:uidb64ps>/', views.verify_email, name='verify_email'),
    #path("login/",views.login),
    path("logout",views.logout,name='logout'),
    # path("dashboard",sectiondata),
    path("forgotpass",views.ForgotPassword),
    path('newpassword/<str:uid>/',views.CreateNewPsaaword , name='new_password'),
    path('changepassword',views.ChangePassword,name='changepassword'),
    path('number/<int:phone>',views.function),
    # path("newpassword/<int:uid>",CreateNewPsaaword),
    
    ###################shuffled##################
    
    path('shuffled/<subject>',views.shuffled_mcq_question,name='shuffled_mcq_question'),
    path('shuffled_mcq_verify/<subject>/<ans>/<regi>',views.shuffled_mcq_verify,name='shuffled_mcq_verify'),

    path('shuffled_coding_question/<subject>',views.shuffled_coding_question,name='shuffled_coding_question'),
    path('shuffled_coding_answers/<subject>',views.shuffled_coding_answers,name='shuffled_coding_answers'),
    ##################shuffled################
    
	#re_path(r'^.*$', views.redirect_to_login),


    #path('profile',views.profile,name='prof'),
    #path('taketest',views.taketest,name='test'),
    #path('instructions/<subject>/<testlevel>',views.instructions,name='instruct'),
    #path('mcq2/<subject>/<testlevel>',views.questions,name='mcq2'),
    #path('submitted/<subject>/<testlevel>/<ans>/<name>/<contact_number>/<email_id>',views.crossverify,name='submitted'),
    # path('code', views.coding, name='coding'),
    #path('student_registration/', views.student_registration, name='student_registration'),
    #path('codes/<subject>/<testlevel>',views.c_question,name='codes'),
    
    

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)