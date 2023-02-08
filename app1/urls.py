from django.urls import path
from . import views



urlpatterns = [
    path('',views.index, name='index'),
    path('login/',views.loginpage,name='loginpage'),
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
    path('deletejob/<int:id>/',views.deletejob,name='deletejob'),
    path('changestatus/<int:id>/',views.changestatus,name='changestatus'),
    path('editjob/<int:id>/',views.editjob,name='editjob'),
    path('editprofile/<int:id>/',views.editemployeerprofile,name='editemployeerprofile'),


#Moderator Page URLS

    path('employerslist', views.employerslist, name='employerslist'),
    path('jobseekerslist', views.jobseekerslist, name='jobseekerslist'),



#Jobseeker Page Urls
    path('editprofile', views.editprofile, name='editprofile'),
    ]
 