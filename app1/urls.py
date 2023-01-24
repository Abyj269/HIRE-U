from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name='index'),
    path('login',views.loginpage,name='loginpage'),
    path('jobseeker',views.jsregpage,name='jsregpage'),
    path('recruiter',views.rregpage,name='rregpage'),
    path('check_username/', views.check_username, name='check_username'),
    path('check_email/', views.check_email, name='check_email'),
    path('logout', views.logout_view, name='logout'),

#Different User Home Page Urls   
    path('adminpage/', views.adminpage, name='adminpage'),
    path('candidate', views.candidatepage, name='candidatepage'),
    path('employeer', views.employeerpage, name='employeerpage'),


#Employeer Page Urls
    path('postjob', views.postjob, name='postjob'),
    path('addqualification/<int:id>/', views.addqualification, name='addqualification'),
    # path('viewqualifications/<int:id>/', views.viewqualifications,name='viewqualifications'),
    path('qualificationdelete/<int:id>/', views.qualificationdelete,name='qualificationdelete'),
    path('qualificationupdate/<int:id>/', views.qualificationupdate,name='qualificationupdate'),
    path('managejobs/<int:id>/',views.managejobs,name='managejobs'),
    path('delete/<int:id>/',views.deletejob,name='deletejob'),

#Jobseeker Page Urls
    path('editprofile', views.editprofile, name='editprofile'),
    ]