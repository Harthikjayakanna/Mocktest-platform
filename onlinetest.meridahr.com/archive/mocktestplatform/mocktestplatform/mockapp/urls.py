from django.contrib import admin
from django.urls import path
from mockapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('main',views.main,name='main'),
    # path('mains',views.mains,name='mains'),
    path('loginform',views.loginform,name='login'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logout,name='logoutt'),
    path('dashboard',views.dashboard,name= 'dash'),
    path("subject/<sub>",views.subject,name="subject"),
    path('mcq_question/<subject>/<testlevel>',views.mcq_question,name="mcq_question"),
    path('mcq_verify/<subject>/<testlevel>/<ans>/<regi>',views.mcq_verify,name='mcq_verify'),
    path('coding/<subject>/<testlevel>',views.coding_question,name='coding'),



    path('profile',views.profile,name='prof'),
    path('taketest',views.taketest,name='test'),
    path('instructions/<subject>/<testlevel>',views.instructions,name='instruct'),
    path('mcq2/<subject>/<testlevel>',views.questions,name='mcq2'),
    path('submitted/<subject>/<testlevel>/<ans>/<name>/<contact_number>/<email_id>',views.crossverify,name='submitted'),
    # path('code', views.coding, name='coding'),
    path('student_registration/', views.student_registration, name='student_registration'),
    path('codes/<subject>/<testlevel>',views.c_question,name='codes'),
    path("result",views.result)
    

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)