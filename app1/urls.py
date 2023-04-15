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
    path('addskills/<int:id>/', views.addskills, name='addskills'),

    # path('viewqualifications/<int:id>/', views.viewqualifications,name='viewqualifications'),
    path('qualificationdelete/<int:id>/', views.qualificationdelete,name='qualificationdelete'),
    path('qualificationupdate/<int:id>/', views.qualificationupdate,name='qualificationupdate'),


    path('skilldelete/<int:id>/', views.skilldelete,name='skilldelete'),
    path('skillupdate/<int:id>/', views.skillupdate,name='skillupdate'),

    path('managejobs/<int:id>/',views.managejobs,name='managejobs'),




    
    path('deletejob/<int:id>/',views.deletejob,name='deletejob'),
    path('editjob/<int:id>/',views.editjob,name='editjob'),
    path('previewjob/<int:id>/',views.previewjob,name='previewjob'),
    path('jobdetails/<int:id>/',views.jobdetails,name='jobdetails'),

    path('changestatus/<int:id>',views.changestatus, name='changestatus'),
    path('changeskillstatus/<int:id>',views.changeskillstatus, name='changeskillstatus'),


    path('editprofile/<int:id>/',views.editemployeerprofile,name='editemployeerprofile'),
    path('profileverify/',views.profileverify,name='profileverify'),
    path('employeer/alljobapplicants/',views.alljobapplicants,name='alljobapplicants'),
    path('employeer/applicantdetails/<int:id>/<int:id2>',views.applicantdetails,name='applicantdetails'),
    path('add/showpdf/<int:id>/',views.showpdf,name='showpdf'),
    path('chatbox/<int:id>/',views.chatbox,name='chatbox'),

    path('alljobsposted/',views.alljobsposted,name='alljobsposted'),
    path('specificapplicant/<int:id>/',views.specificapplicant,name='specificapplicant'),
    path('addscheduleinterview/', views.addscheduleinterview, name='addscheduleinterview'),
    path('rescheduleinterview/<int:id>/', views.rescheduleinterview, name='rescheduleinterview'),
#Moderator Page URLS

    path('employerslist', views.employerslist, name='employerslist'),
    path('jobseekerslist', views.jobseekerslist, name='jobseekerslist'),
    path('employerdetails/<int:id>/', views.employerdetails, name='employerdetails'),
    path('accept/<int:id>/', views.accept, name='accept'),
    path('reject/<int:id>/', views.reject, name='reject'),
    path('allpayements', views.allpayements, name='allpayements'),
    path('statistics', views.statistics, name='statistics'),
    path('reports', views.reports, name='reports'),


#Jobseeker Page Urls
    path('editprofile', views.editprofile, name='editprofile'),
    path('joblisting', views.joblisting, name='joblisting'),
    path('jobdetails/<int:id>', views.jobsindetail, name='jobsindetail'),
    path('appliedjobs', views.appliedjobs, name='appliedjobs'),
    path('appliedjobstatus/<int:id>/', views.appliedjobstatus, name='appliedjobstatus'),
    path('jobseekerchatbox/<int:id>/', views.jobseekerchatbox, name='jobseekerchatbox'),
    path('premiumservices', views.premiumservices, name='premiumservices'),
    path('resumebuilderform/', views.resumebuilderform, name='resumebuilderform'),
    path('resumepreview/<int:id>/', views.resumepreview, name='resumepreview'),
   
    path('resumebuilderhomepage/', views.resumebuilderhomepage, name='resumebuilderhomepage'),
    path('resumelist/', views.resumelist, name='resumelist'),
    path('deleteresume/<int:id>/', views.deleteresume, name='deleteresume'),
    # path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('payementpage/', views.payementpage, name='payementpage'),
    path('verifypayment/', views.verifypayment, name='verifypayment'),
    path('userpaymentdetails/', views.userpaymentdetails, name='userpaymentdetails'),

    path('coverletterhomepage/', views.coverletterhomepage, name='coverletterhomepage'),
    path('coverletterform/',views.coverletterform,name='coverletterform'),
    path('allcoverletter/',views.allcoverletter,name='allcoverletter'),
    path('coverletterpreview/<int:id>/',views.coverletterpreview,name='coverletterpreview'),
    path('notifications/',views.notifications,name='notifications'),
     ]
 