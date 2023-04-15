from django.shortcuts import render,redirect,HttpResponse
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from app1.models import Jobseeker,Employeer,User,Qualifications,EmployeerProfile,Verificationdetails,JobseekerProfile,Skills
from app1.models import candidateSkillsandTechnologies,JobapplicationDetails,Interviewscheduling
from django.contrib import messages
from app1.models import Jobdetails,Qualifications,User,ResumeSchema,PayementDetails,CoverLetterDetails
from django.views import generic
from django.urls import reverse
from .models import Qualifications
from django.contrib.auth.decorators import login_required
from taggit.models import Tag, TaggedItem
from django.core.paginator import Paginator
import datetime
from .forms import ProfileForm
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from collections import Counter
from django.conf import settings
from django.http import HttpResponse, Http404
import os
from django.db.models import Q
import json
import PyPDF2
import openai
import spacy
import IPython
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor


openai.api_key = settings.OPENAI_SECRET_KEY
model_engine = "text-davinci-003"

def index(request):
    return render(request,"home.html")

def loginpage(request):
    # if request.user.is_authenticated:
    #     return redirect('loginpage')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)

        if user is not None and user.role == 'EMPLOYEER':
            login(request, user)
            return redirect('employeerpage')
        elif user is not None and user.role == 'JOBSEEKER':
            login(request, user)
            return redirect('candidatepage') 
        elif user is not None and user.role == 'MODERATOR':
            login(request, user)
            return redirect('adminpage') 
        else:
             messages.error(request,"Invalid Credentials" )
             return redirect('loginpage')
    else:
        msg = 'error validating form'
    return render(request,'login.html')
       


def check_username(request):
    User = get_user_model()
    if request.method == 'POST':
        username = request.POST.get('username')
        # Check if the username is available in the database
        if User.objects.filter(username=username).exists():
            # Return 'not available' if the username already exists in the database
            return JsonResponse({'status': 'not available'})
        else:
            # Return 'available' if the username is available
            return JsonResponse({'status': 'available'})

def check_email(request):
    User = get_user_model()
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if the email is available in the database
        if User.objects.filter(email=email).exists():
            # Return 'not available' if the email already exists in the database
            return JsonResponse({'status': 'not available'})
        else:
            # Return 'available' if the email is available
            return JsonResponse({'status': 'available'})

def jsregpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password == cpassword:
            js_user = Jobseeker.objects.create_user(
                username = username,
                email=email,
                password=password,
                )
            js_user.save()
            return redirect('loginpage')
      

       
    return render(request,"jsregistartion.html")

def rregpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password == cpassword:
            r_user = Employeer.objects.create_user(
                username = username,
                email=email,
                password=password,

                )
            r_user.save()
            return redirect('loginpage')

    return render(request,"rregistration.html")

def logout_view(request):
    logout(request)
    return redirect('loginpage')

#Employeer Views 
@login_required(login_url='/login')
def postjob(request):
    userid=request.user.id
    vdetails = Verificationdetails.objects.get(user_id=userid)
    value=vdetails.isverified
    if request.method == 'POST':
        jobtitle= request.POST.get('job_title')
        jobdescription = request.POST.get('job_description')
        email = request.POST.get('contact_email')
        jobtype = request.POST.get('jobtype')
        specialisation= request.POST.get('specialisation')
        experience = request.POST.get('experience')
        salary = request.POST.get('salary')
        vaccancies = request.POST.get('vaccancies')
        qualification=request.POST.get('qualification')
        lastdate = request.POST.get('lastdate')
        
        

        postedjob= Jobdetails(
            job_title=jobtitle,
            job_description=jobdescription,
            contact_email=email,
            job_type=jobtype,
            specialisation=specialisation,
            experience=experience,
            expected_salary=salary,
            vacancies=vaccancies,
            qualification=qualification,
            lastdate=lastdate,

            
            )
        postedjob.cmp_id=request.user

        

        
        postedjob.save()
      
        messages.success(request,"Job is Successfully Posted" )
        return redirect(reverse('managejobs',args=[userid]))
    else:
        pos = Qualifications.objects.all()
        skills=Skills.objects.all()
        current_value = request.user
        user_id=current_value.id
        context ={
        'pos': pos,
        'user_id':user_id,
        'verified':value,
        'skills':skills
        }
        return render(request,'employeer/postjob.html',context)


# Job Post Seeting and Add Qualification

def addqualification(request,id):
    if request.user.is_authenticated:
        userid=request.user.id
        vdetails = Verificationdetails.objects.get(user_id=userid)
        value=vdetails.isverified

        if request.method == 'POST':
            quali =request.POST.get('qualification')

            addedqualification= Qualifications(
                qualification_name=quali,
                )
            addedqualification.cmp_id=request.user
            addedqualification.save()
            messages.success(request,"Qualification is added" )
            return redirect(request.META['HTTP_REFERER'])
        
        
        pos = Qualifications.objects.filter(cmp_id_id=id)
        context ={
            'pos': pos,
            'value':value,
        }
        return render(request,'employeer/addqualification.html',context)
    return redirect('loginpage')

def qualificationdelete(request,id):
        quali = Qualifications.objects.filter(quali_id=id)
        quali.delete()
        return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def qualificationupdate(request,id):
    quali = Qualifications.objects.get(pk=id)
    if request.method == 'POST':
        value =request.POST.get('qualification')
        Qualifications.objects.filter(quali_id=id).update(qualification_name=value)
        value = quali.cmp_id_id
        return redirect(reverse('addqualification',args=[value]))
    else:   
             
        current_value = quali.qualification_name
        return render(request,'employeer/editqualification.html',{
            'detail':quali,'current_value':current_value
    })

# Manage job ,Delete Job ,Update Job


def deletejob(request,id):
        jobs = Jobdetails.objects.filter(job_id=id)
        jobs.delete()
        return redirect(request.META.get('HTTP_REFERER'))




# Job  Setting and Add Skills

def addskills(request,id):
    if request.user.is_authenticated:
        userid=request.user.id
        vdetails = Verificationdetails.objects.get(user_id=userid)
        value=vdetails.isverified

        if request.method == 'POST':
            skill =request.POST.get('skills')
            value =EmployeerProfile.objects.get(user_id=userid)
            addedskills= Skills(
                skill_name=skill
                )
            addedskills.emp_profile_id=userid
            addedskills.save()
            messages.success(request,"Skill is added" )
            return redirect(request.META['HTTP_REFERER'])
        
        
        pos = Skills.objects.filter(emp_profile_id=id)
        context ={
            'pos': pos,
            'value':value,
        }
        return render(request,'employeer/addskill.html',context)
    return redirect('loginpage')

def skilldelete(request,id):
        skill = Skills.objects.filter(skill_id=id)
        skill.delete()
        return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login')
def skillupdate(request,id):
    skill = Skills.objects.get(pk=id)
    if request.method == 'POST':
        value =request.POST.get('skills')
        Skills.objects.filter(skill_id=id).update(skill_name=value)
        value =skill.emp_profile_id
        return redirect(reverse('addskills',args=[value]))
    else:   
             
        current_value = skill.skill_name
        return render(request,'employeer/editskill.html',{
            'detail':skill,'current_value':current_value
    })









def managejobs(request ,id):
    if request.user.is_authenticated:
        pos = Jobdetails.objects.filter(cmp_id_id=id)
        if request.method =='POST':
            searched = request.POST['searched']
            jobs=Jobdetails.objects.filter(job_title__contains=searched)
            context={
                'searched':searched,
                'jobs':jobs,
            }
            return render(request,'employeer/managejobs.html',context) 
        
        else:
            context ={
                'pos': pos,
                'id':id
            }
            return render(request,'employeer/managejobs.html',context) 
    return redirect('loginpage')





@login_required(login_url='/login')
def editjob(request,id):
    jb = Jobdetails.objects.get(pk=id)
    idvalue= request.user
    allqualifications = Qualifications.objects.filter(cmp_id_id=idvalue)
    if request.method == 'POST':
        jobtitle= request.POST.get('job_title')
        jobdescription = request.POST.get('job_description')
        email = request.POST.get('contact_email')
        jobtype = request.POST.get('jobtype')
        specialisation= request.POST.get('specialisation')
        experience = request.POST.get('experience')
        salary = request.POST.get('salary')
        vaccancies = request.POST.get('vaccancies')
        qualification=request.POST.get('qualification')
        lastdate = request.POST.get('lastdate')
        Jobdetails.objects.filter(job_id=id).update(
            job_title=jobtitle,
            job_description=jobdescription,
            contact_email=email,
            job_type=jobtype,
            specialisation=specialisation,
            experience=experience,
            expected_salary=salary,
            vacancies=vaccancies,
            qualification=qualification,
            lastdate=lastdate,)
        value = jb.cmp_id_id
        return redirect(reverse('managejobs',args=[value]))
    else:  

        jobtitle = jb.job_title
        jobdescription = jb.job_description
        email = jb.contact_email
        jobtype = jb.job_type
        specialisation=jb.specialisation
        experience=jb.experience
        salary=jb.expected_salary
        vaccancies=jb.vacancies
        qualification=jb.qualification
        lastdate=jb.lastdate

        context={
            'detail':jb,
            'jobtitle': jobtitle,
            'jobdescription':jobdescription,
            'email':email,
            'jobtype':jobtype,
            'specialisation':specialisation,
            'experience':experience,
            'salary':salary,
            'vaccancies':vaccancies,
            'qualification':qualification,
            'lastdate':lastdate,
            'qualificationdetails':allqualifications
        }
        return render(request,'employeer/editjob.html',context)

# Change Status
def changestatus(request,id):
    quali = Qualifications.objects.get(quali_id=id)
    status_value = quali.status
    if status_value == 0:
        quali.status=1
        quali.save()
    else:
        quali.status=0
        quali.save()
        
    return redirect(request.META.get('HTTP_REFERER'))


def changeskillstatus(request,id):
    skill = Skills.objects.get(skill_id=id)
    status_value = skill.status
    if status_value == 0:
        skill.status=1
        skill.save()
    else:
        skill.status=0
        skill.save()
        
    return redirect(request.META.get('HTTP_REFERER'))

   


# class QualificationDelete(generic.DeleteView):
#     model=Qualifications
#     template_name= 'addqualifications.html'
#     success_url=reverse_lazy('employeer/addqualifications/<int:id>')

def editemployeerprofile(request,id):
    if request.user.is_authenticated:
        details = EmployeerProfile.objects.get(user_id=id)
        if request.method == 'POST':
            company_name= request.POST.get('Company-Name')
            office_location = request.POST.get('Office-Location')
            address = request.POST.get('Address')
            pincode = request.POST.get('Pincode')
            website_url= request.POST.get('Website-URL')
            phone_number = request.POST.get('Phoneno')
            company_logo = request.FILES.get('logo')
            EmployeerProfile.objects.filter(user_id=id).update(
            company_name = company_name,
            office_location = office_location,
            address = address,
            pincode = pincode,
            website_url = website_url,
            phone_number = phone_number,
            )
            if details.company_logo and company_logo:
                    details.company_logo.delete()
            if company_logo:
                details.company_logo = company_logo
                details.save()

            return redirect('employeerpage')
        else: 
            company_name= details.company_name
            office_location = details.office_location
            address = details.address
            pincode = details.pincode
            website_url=details.website_url
            phone_number = details.phone_number
            company_logo= details.company_logo
            context={
                "company_name":company_name,
                "office_location":office_location,
                "address":address,
                "pincode":pincode,
                "website_url":website_url,
                "phone_number":phone_number,
                "company_logo":company_logo,
            }
            return render(request,'employeer/editprofile.html',context)

    return redirect('loginpage')



def previewjob(request,id):
    if request.user.is_authenticated:
      jobdetails = Jobdetails.objects.get(job_id=id)  
      userid = request.user 
      details= EmployeerProfile.objects.get(user_id=userid)

      jobtitle=jobdetails.job_title
      clogo = details.company_logo
      type= jobdetails.job_type
      jobid = jobdetails.job_id
      context={
          "job_title":jobtitle,
          "c_logo":clogo,
          "type":type,
          "id":jobid,
      }


      return render(request,'employeer/jobpreview.html',context)

    return redirect('loginpage')


def jobdetails(request,id):
    if request.user.is_authenticated:

        jobdetails = Jobdetails.objects.get(job_id=id)  
        userid = request.user 
        details= EmployeerProfile.objects.get(user_id=userid)
        jobtitle=jobdetails.job_title
        clogo = details.company_logo
        type= jobdetails.job_type
        description = jobdetails.job_description
        lastdate=jobdetails.lastdate
        specialisation = jobdetails.specialisation
        location = details.office_location
        salary = jobdetails.expected_salary
        experience= jobdetails.experience
        vaccancies = jobdetails.vacancies
        qualification = jobdetails.qualification
       
        context={
            "job_title":jobtitle,
            "c_logo":clogo,
            "type":type,
            "description":description,
            "lastdate":lastdate,
            "specialisation":specialisation,
            "location":location,
            "salary":salary,
            "experience":experience,
            "vaccancies":vaccancies,
            "qualification":qualification,
        }



        return render(request,'employeer/jobpreviewdetail.html',context)
    return redirect('loginpage')

def profileverify(request):
     if request.user.is_authenticated:
        if request.method == 'POST':
            userid=request.user.id  
            # # all=Verificationdetails.objects.all()
            # # for i in all:
            # #  if userid == i.user_id:
            # #     messages.warning(request,"Verification Details is Already Added" )
            #     return redirect(request.META['HTTP_REFERER'])
            bc=Verificationdetails.objects.get(user_id=userid)
            buisness_license = request.FILES.get('buisness-license')
            prooftype = request.POST.get('recruiter-id')
            proof = request.FILES.get('fileupload')

            if bc.buisnesslicence and buisness_license:
                bc.buisnesslicence.delete()
            if buisness_license:
                bc.buisnesslicence = buisness_license
                bc.save()


            if bc.proof and proof:
                bc.proof.delete()
            if proof:
                bc.proof = proof
                bc.save()
           
            
            return redirect('employeerpage')
             
        else:
            return render(request,'employeer/verifyprofile.html')
     return redirect('loginpage')


def alljobapplicants(request):
    if request.user.is_authenticated:
        
        user_id=request.user.id
        emp_profile_details=EmployeerProfile.objects.get(user_id=user_id)
        emp_profile_id=emp_profile_details.id

        applicationdetails=JobapplicationDetails.objects.filter(employerprofile_id=emp_profile_id)
        jobdetails=Jobdetails.objects.all()
        profiledetails=JobseekerProfile.objects.all()
        context={

            "applicationdetails":applicationdetails,
            "jobdetails":jobdetails,
            "profiledetails":profiledetails,
        }
        return render(request, 'employeer/alljobapplicants.html',context)
    return redirect('loginpage')

def applicantdetails(request,id,id2):
    if request.user.is_authenticated:
        profiledetails=JobseekerProfile.objects.get(id=id)
        applicationdetails=JobapplicationDetails.objects.get(application_id=id2)
        jobdetails=Jobdetails.objects.all()
        # image_path = os.path.join(settings.MEDIA_ROOT, profiledetails.profile_photo.name)
        scheduledetails=Interviewscheduling.objects.filter(application_id=id2)
        context={
            "profilelogo":profiledetails.profile_photo,
            "profileid":id,
            "firstname":profiledetails.first_name,
            "lastname":profiledetails.last_name,
            "email":profiledetails.email,
            "phone":profiledetails.phone_number,
            "age":profiledetails.age,
            "qualification":profiledetails.highestqualification,
            "fulladdress":profiledetails.fulladdress,
            # "resume":resume_pdf,
            "applictiondetails":applicationdetails,
            "jobdetails":jobdetails,
            "jobid": applicationdetails.job_id,
            "appid":applicationdetails.application_id,
            "scheduledetails":scheduledetails,
          
        }
        return render(request, 'employeer/applicantdetails.html',context)
    return redirect('loginpage')

def chatbox(request,id):
    if request.user.is_authenticated:
        userid=request.user.id
        empprofile=EmployeerProfile.objects.get(user_id=userid)
        profiledetails=JobseekerProfile.objects.get(id=id)
        context={
            "profilelogo":profiledetails.profile_photo,
            "profileid":id,
            "firstname":profiledetails.first_name,
            "lastname":profiledetails.last_name,
            "loggeduserid":userid,
            "senttouserid":profiledetails.user_id,
            "empprofiledetails":empprofile,

        }

        return render(request, 'employeer/chatbox.html',context)
    return redirect('loginpage')




def showpdf(request, id):
    applicationdetails = JobapplicationDetails.objects.get(application_id=id)
    pdf_path = os.path.join(settings.MEDIA_ROOT, applicationdetails.applicant_resume.name)
        
    with open(pdf_path, 'rb') as pdf_file:
        resume_pdf = HttpResponse(pdf_file.read(), content_type='application/pdf')
        resume_pdf['Content-Disposition'] = f'filename="{applicationdetails.applicant_resume.name}"'
    
    return resume_pdf

def alljobsposted(request):
    if request.user.is_authenticated:

        userdetails =request.user.id;
        jobdetails = Jobdetails.objects.filter(cmp_id_id=userdetails)
        # sample=[jobdetails.job_id,]
        sample = []
        for jobdetail in jobdetails:
            sample.append(jobdetail.job_id)

        empprofileid = EmployeerProfile.objects.get(user_id=userdetails)
        allapplicants =JobapplicationDetails.objects.filter(employerprofile_id=empprofileid).values_list("job_id",flat=True)
        # counts=dict(Counter(allapplicants))
        #print(type(counts))
        counts={'a':1,'b':2}
       
        context={
            "jobdetails":jobdetails,
            "counts":counts,
           
        }
        return render(request,"employeer/alljobsposted.html",context)
    return redirect('loginpage')











def specificapplicant(request,id):
    if request.user.is_authenticated:
            nlp = spacy.load("en_core_web_sm")
            skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
            empid=request.user.id
            empprofile=EmployeerProfile.objects.get(user_id=empid)
            applicationdetails = JobapplicationDetails.objects.filter(job_id=id, employerprofile_id=empprofile.id)
            jobdetails = Jobdetails.objects.get(job_id=id)
            title=jobdetails.job_title
            description=jobdetails.job_description
            specialisation=jobdetails.specialisation
            skill_expected=title + description + specialisation
            #print(skill_expected)
            if applicationdetails.exists():
                applicants = {}

                annotation2 = skill_extractor.annotate(skill_expected)
                expectedskills =annotation2['results']
                expectedskills.keys()
                        
                fullmatch1 = expectedskills['full_matches']
                ngrams_scored1 = expectedskills['ngram_scored']
                a_key1 = "doc_node_value"

                f_docnodevalues1 = [a_dict1[a_key1] for a_dict1 in fullmatch1]
                n_docnodevalues1 = [a_dict1[a_key1] for a_dict1 in ngrams_scored1]

                requiredskills = f_docnodevalues1 + n_docnodevalues1
                sanitized_values = list(set(requiredskills)) 


                for application in applicationdetails:
                    jobseeker_id = application.jobseekerprofile_id
                    applicant_resume = application.applicant_resume
                    resume_path = application.applicant_resume.path
                    application_id = application.application_id


                    with open(resume_path, 'rb') as filehandle:
                        pdfReader = PyPDF2.PdfReader(filehandle)
                        pagehandle = pdfReader.pages[0]
                        text = pagehandle.extract_text()
                        text = text.replace('o','')
                        text = text.replace('|','')

                        annotations = skill_extractor.annotate(text)
                        allresult =annotations['results']
                        allresult.keys()
                        
                        fullmatches = allresult['full_matches']
                        ngrams_scored = allresult['ngram_scored']
                        a_key = "doc_node_value"

                        f_docnodevalues = [a_dict[a_key] for a_dict in fullmatches]
                        n_docnodevalues = [a_dict[a_key] for a_dict in ngrams_scored]

                        all_doc_node_values = f_docnodevalues + n_docnodevalues
                        cleaned_values = list(set(all_doc_node_values)) 

                        scraped_data = [' '.join(cleaned_values)]
                        cv = [' '.join(sanitized_values)]
                        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
                        tfidf_jobid = tfidf_vectorizer.fit_transform(scraped_data)
                        user_tfidf = tfidf_vectorizer.transform(cv)
                        cos_similarity_tfidf = cosine_similarity(user_tfidf, tfidf_jobid)
                        similarity_score = round(np.max(cos_similarity_tfidf), 2)
                        



                    applicants[jobseeker_id] = {'ExtractedSkill': cleaned_values,'Requiredskill':sanitized_values,'Similarity Scores':similarity_score, 'application_id': application_id}
                    sorted_applicants = sorted(applicants.items(), key=lambda x: x[1]['Similarity Scores'], reverse=True)

                    # Assign rank to each applicant
                    ranked_applicants = []
                    rank = 1
                    for i, (jobseeker_id, application_details) in enumerate(sorted_applicants):
                        application_details['rank'] = rank
                        ranked_applicants.append((jobseeker_id, application_details))
                        if i < len(sorted_applicants) - 1 and application_details['Similarity Scores'] != sorted_applicants[i+1][1]['Similarity Scores']:
                            rank += 1

                print(ranked_applicants)
                #print(applicants)
            jobseeker=JobseekerProfile.objects.all()
            
            context={
                "applicantdetails":applicationdetails,
                "jobdetails":jobdetails,
                "employerprofile":empprofile,
                "jobseeker":jobseeker,
                "ranked_applicants": ranked_applicants,
            }


            return render(request,"employeer/specificapplicant.html",context)
    else:
        return redirect('loginpage')


def addscheduleinterview(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        duration = data.get('duration')
        interviewtype = data.get('interviewType')
        timeanddate = data.get('timeAndDate')
        applicationid = data.get('applicationId')
        jobid = data.get('jobid')
        existing_interview = Interviewscheduling.objects.filter(
            application_id=applicationid,
            interview_timeanddate=timeanddate
        ).exists()
        if existing_interview:
            return JsonResponse({'status': 'Interview already scheduled for this application'})
        try:
            interviewdetails = Interviewscheduling(
                time_duration=duration,
                interview_type=interviewtype,
                interview_timeanddate=timeanddate,
                application_id=applicationid,
                job_id=jobid,
            )
            interviewdetails.save()
            return JsonResponse({'status': 'Success'})
        except:
            return JsonResponse({'status': 'Invalid'})
    else:
        return HttpResponse("Invalid request method")





def rescheduleinterview(request,id):
   
    if request.method == 'POST':
        duration = request.POST.get('duration')
        interviewtype = request.POST.get('interviewtype')
        timeanddate = request.POST.get('timeanddate')
        Interviewscheduling.objects.filter(interview_id=id).update(
            time_duration=duration,
            interview_type=interviewtype,
            interview_timeanddate=timeanddate,
            )
    else:
        interviewscheduling=Interviewscheduling.objects.get(interview_id=id)
        context={
            "timeduration":interviewscheduling.time_duration,
            "interviewtype":interviewscheduling.interview_type,
            "timeanddate":interviewscheduling.interview_timeanddate,
        }
    return JsonResponse(context)

    
       

   








# Jobseeker Views

@login_required(login_url='/login')
def candidatepage(request):
    if request.user.is_authenticated:
        return render(request,'jobseeker/home.html')
    return redirect('loginpage')

# def joblisting(request):

#     userid=request.user.id
#     jobseekerprofile=JobseekerProfile.objects.get(user_id=userid)
#     profile_id=jobseekerprofile.id  
#     jobseekerskills = candidateSkillsandTechnologies.objects.get(id=profile_id)
#     jobseeker_skills =jobseekerskills.skill_name
#     jobseeker_skill_list=[s.strip() for s in jobseeker_skills.split(',')] 
#     if request.user.is_authenticated:
#         if request.method =='POST':
#             searched = request.POST['searched']
#             jobs=Jobdetails.objects.filter(job_title__contains=searched)
#             profiledetails=EmployeerProfile.objects.all()
#             context={
#                 'searched':searched,
#                 'jobs':jobs,
#                 'profiledetails':profiledetails,
#             }
#             return render(request,'jobseeker/jobs.html',context) 
#         else:
#             allspecialisations = Jobdetails.objects.values_list('specialisation', flat=True)
#             matching_skills = []

#             skills = Skills.objects.all()
#             for skill in skills:
#                 for specialisation in allspecialisations:
#                     if skill.skill_id == specialisation:
#                         matching_skills.append(skill.skill_name)

#             jobdetails = Jobdetails.objects.all()
#             profiledetails=EmployeerProfile.objects.all()
#             context={
#                     "jobdetails":jobdetails,
#                     "profiledetails":profiledetails,
#             }



          
#             return render(request,'jobseeker/jobs.html',context)

            
#     return redirect('loginpage')
"""
def joblisting(request):
    if request.user.is_authenticated:
        

        userid = request.user.id
        jobseekerprofile = JobseekerProfile.objects.get(user_id=userid)
        profile_id = jobseekerprofile.id  

        try:
            jobseekerskills = candidateSkillsandTechnologies.objects.get(id=profile_id)
            jobseeker_skills = jobseekerskills.skill_name
            jobseeker_skill_list = [s.strip() for s in jobseeker_skills.split(',')]
        except candidateSkillsandTechnologies.DoesNotExist:
            jobseeker_skill_list = []

        # jobseekerskills = candidateSkillsandTechnologies.objects.get(id=profile_id)
        # jobseeker_skills = jobseekerskills.skill_name
        # jobseeker_skill_list = [s.strip() for s in jobseeker_skills.split(',')] 

        if request.method == 'POST':
            searched = request.POST['searched']
            jobs = Jobdetails.objects.filter(job_title__contains=searched)
            profiledetails = EmployeerProfile.objects.all()
            context = {
                'searched': searched,
                'jobs': jobs,
                'profiledetails': profiledetails,
            }
            return render(request, 'jobseeker/jobs.html', context) 
        else:
            job_details_dict = {}
            jobdetails=Jobdetails.objects.all()
           

            for job in jobdetails:
                job_skills = [s.strip() for s in job.specialisation.split(',')]
                matching_skills = set(job_skills) & set(jobseeker_skill_list)
                matching_score = len(matching_skills) / len(job_skills) * 100 if job_skills else 0
                job_details_dict[job] = matching_score
            sorted_job_details = sorted(job_details_dict.items(), key=lambda x: x[1], reverse=True)
            sorted_jobs = [job for job, _ in sorted_job_details]

            p = Paginator(sorted_jobs,4)
            page=request.GET.get('page')
            jos=p.get_page(page)

            profiledetails = EmployeerProfile.objects.all()
            context = {
                'jobdetails': jos,
                'profiledetails': profiledetails,
                'pages':jos
            }
            return render(request, 'jobseeker/jobs.html', context)
    else:
        return redirect('loginpage')
"""


def joblisting(request):
    if request.user.is_authenticated:
        userid = request.user.id
        jobseekerprofile = JobseekerProfile.objects.get(user_id=userid)
        profile_id = jobseekerprofile.id  

        try:
            jobseekerskills = candidateSkillsandTechnologies.objects.get(id=profile_id)
            jobseeker_skills = jobseekerskills.skill_name
            jobseeker_skill_list = [s.strip() for s in jobseeker_skills.split(',')]
        except candidateSkillsandTechnologies.DoesNotExist:
            jobseeker_skill_list = []

        if request.method == 'POST':
            searched = request.POST['searched']
            jobs = Jobdetails.objects.filter(job_title__contains=searched)
            profiledetails = EmployeerProfile.objects.all()
            context = {
                'searched': searched,
                'jobs': jobs,
                'profiledetails': profiledetails,
            }
            return render(request, 'jobseeker/jobs.html', context) 
        else:
            applied_jobs = JobapplicationDetails.objects.filter(jobseekerprofile=jobseekerprofile).values_list('job_id', flat=True)
            jobdetails = Jobdetails.objects.exclude(job_id__in=applied_jobs)

            job_details_dict = {}
            for job in jobdetails:
                job_skills = [s.strip() for s in job.specialisation.split(',')]
                matching_skills = set(job_skills) & set(jobseeker_skill_list)
                matching_score = len(matching_skills) / len(job_skills) * 100 if job_skills else 0
                job_details_dict[job] = matching_score
            sorted_job_details = sorted(job_details_dict.items(), key=lambda x: x[1], reverse=True)
            sorted_jobs = [job for job, _ in sorted_job_details]

            p = Paginator(sorted_jobs,4)
            page=request.GET.get('page')
            jos=p.get_page(page)

            profiledetails = EmployeerProfile.objects.all()
            context = {
                'jobdetails': jos,
                'profiledetails': profiledetails,
                'pages':jos
            }
            return render(request, 'jobseeker/jobs.html', context)
    else:
        return redirect('loginpage')
















def jobsindetail(request,id):
    if request.user.is_authenticated:
        userid= request.user.id
        jobseekerprofie=JobseekerProfile.objects.get(user_id=userid)
        details =Jobdetails.objects.get(job_id=id)
        empprofileid=details.cmp_id
        empprofile=EmployeerProfile.objects.get(user_id=empprofileid)
        jobid=details.job_id
        jobseekerprofie_id=jobseekerprofie.id
        if request.method == 'POST':
            cv=request.FILES.get('resume')
            # jobid=request.POST.get('job_id')
            jobapplicaion= JobapplicationDetails(
                applicant_resume=cv,
                jobseekerprofile_id=jobseekerprofie_id,
                job_id=jobid,
                employerprofile_id=empprofile.id
                )          
            jobapplicaion.save()
            return redirect(reverse('jobsindetail',args=[jobid]))
        else:
            
            applied = False
            if  JobapplicationDetails.objects.all() is not None:
                try:
                    applicationdetails=JobapplicationDetails.objects.get(jobseekerprofile_id=jobseekerprofie_id,job_id=jobid)
                    applied=True
                except JobapplicationDetails.DoesNotExist:
                    pass

            profiledetails=EmployeerProfile.objects.all()
            publisheddate=details.publisheddate
            formatDate = publisheddate.strftime("%d-%b-%y")
            context ={
                "job_title":details.job_title,
                "type": details.job_type,
                "description":details.job_description,
                "lastdate":details.lastdate,
                "specialisation":details.specialisation,
                "salary":details.expected_salary,
                "experience":details.experience,
                "vaccancies":details.vacancies,
                "qualification":details.qualification,
                "company_id":details.cmp_id_id,
                "profiledetails":profiledetails,
                "publisheddate":formatDate,
                "jobid":details.job_id,
                "applied":applied,
            }

            return render(request,'jobseeker/jobdetails.html',context)
            
    return redirect('loginpage')



def editprofile(request):
    if request.user.is_authenticated:
        userid=request.user.id
        jobseek=JobseekerProfile.objects.get(user_id=userid)

        jobseekprofile_id=jobseek.id 
        profileidexist = None
        # profileidexist = candidateSkillsandTechnologies.objects.get(profile_id_id=jobseekprofile_id)

        email =request.user.email
        
       

        if request.method == 'POST':
            profile_photo = request.FILES.get('customFile')
            first_name = request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            phone=request.POST.get('phone')
            highestqualification= request.POST.get('highestqualification')
            age=request.POST.get('age')
            aboutyourself=request.POST.get('aboutyourself')
            fulladdress=request.POST.get('fulladdress')
            skills=request.POST.get('skills')

            JobseekerProfile.objects.filter(user_id=userid).update(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone,
                email=email,
                highestqualification=highestqualification,
                age=age,
                aboutyourself=aboutyourself,
                fulladdress=fulladdress
                )

            if jobseek.profile_photo and profile_photo:
                jobseek.profile_photo.delete()
            if profile_photo:
                jobseek.profile_photo =profile_photo
                jobseek.save()

            candidateSkillsandTechnologies.objects.update_or_create(
                profile_id_id=jobseekprofile_id,
                defaults={
                    'skill_name': skills
                }
                )
            
        
            return redirect(editprofile)
            
        
        else:
            if jobseekprofile_id is not None:
                try:
                    profileidexist = candidateSkillsandTechnologies.objects.get(profile_id_id=jobseekprofile_id)
                except candidateSkillsandTechnologies.DoesNotExist:
                    pass
            # for tag in taggeditem:
            #     print(tag.tag.name)
            context={
            "profile_photo":jobseek.profile_photo,
            "first_name":jobseek.first_name,
            "last_name":jobseek.last_name,
            "phone":jobseek.phone_number,
            "email":jobseek.email,
            "highestqualification":jobseek.highestqualification,
            "age":jobseek.age,
            "aboutyourself":jobseek.aboutyourself,
            "fulladdress":jobseek.fulladdress,
            "skills":profileidexist.skill_name if profileidexist is not None else None,
            }
            return render(request,'jobseeker/jobseekerprofile.html',context)
    else:
        return redirect('loginpage')

def appliedjobs(request):
    userid=request.user.id
    profileid=JobseekerProfile.objects.get(user_id=userid)
    appliedjobs = JobapplicationDetails.objects.filter(jobseekerprofile_id=profileid)



    jobdetails=Jobdetails.objects.all()
    empprofiledetails = EmployeerProfile.objects.all()
    context={
        "appliedjobs":appliedjobs,
        "jobdetails":jobdetails,
        "employerprofile":empprofiledetails, 
        
    }

    return render(request,'jobseeker/appliedjobs.html',context)

def appliedjobstatus(request,id):
    user_id = request.user.id
    profile = JobseekerProfile.objects.get(user_id=user_id)
    profile_id=profile.id
    jobdetails=Jobdetails.objects.get(job_id=id)
    job_applications = JobapplicationDetails.objects.get(jobseekerprofile_id=profile_id,job_id=id)
 
    employerid=jobdetails.cmp_id_id
    employeedetails=EmployeerProfile.objects.all()
    
    context = {
        "job_details": jobdetails,
        "type":jobdetails.job_type,
        "job_title":jobdetails.job_title,
        "job_applications": job_applications,
        "employeedetails":employeedetails,
        "employerid":employerid,
       
    
    }

    return render(request, 'jobseeker/appliedjobstatus.html', context)

def jobseekerchatbox(request,id):
        userid=request.user.id
        jobprofile=JobseekerProfile.objects.get(user_id=userid)
        empprofiledetails=EmployeerProfile.objects.get(id=id)
        context={
            "profilelogo":jobprofile.profile_photo,
            "profileid":id,
            "companyname":empprofiledetails.company_name,
            "companyphoto":empprofiledetails.company_logo,
            "loggeduserid":userid,
            "senttouserid":empprofiledetails.user_id,
            "jobprofile":jobprofile,
        }

        return render(request,'jobseeker/jobseekerchatbox.html',context) 


def resumebuilderhomepage(request):
    return render(request,"jobseeker/resumebldrhomepage.html")




### Currently Payemnt Not Integrated


razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
def payementpage(request):
    userid=request.user.id
    profiledetails=JobseekerProfile.objects.get(user_id=userid)
    payementdetails=PayementDetails.objects.get(profile_id=userid)
    profile_id=profiledetails.id
    if (payementdetails.paid==1):
        return redirect('resumebuilderhomepage')
    else:
        amount=30000
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        response_payment=client.order.create(dict(amount=amount,currency='INR',payment_capture=1))
        order_id=response_payment['id']
        context={
            'amount':amount,
            'api_key':settings.RAZOR_KEY_ID,
            'order_id':order_id,
            'username': profiledetails.first_name,
            'profileid':profile_id,
            'userid':userid
        }
        print(response_payment)
        return render(request,'jobseeker/payementpage.html',context)


def verifypayment(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        amount=request.POST.get('amount')
        amount=int(amount)/100
        username= request.POST.get('username')
        userid=request.POST.get('userid')
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        try:
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            client.utility.verify_payment_signature(params_dict)
            PayementDetails.objects.filter(profile_id=userid).update(
                user_name=username,
                order_id=razorpay_order_id,
                productname="Resume Builder",
                amount=amount,
                razorpay_payment_id=razorpay_payment_id,
                paid=1,
                )
                
            return JsonResponse({'status': 'Success'})
        except:
            return  JsonResponse({'status': 'Verification failed'})
           # return HttpResponse("Payment verification failed")
    else:
        return HttpResponse("Invalid request method")


    

@csrf_exempt
def success(request):
    return render(request,"success.html")


    
def notifications(request):

    userid=request.user.id
    jobseekerprofile=JobseekerProfile.objects.get(user_id=userid)
    applicationdetails=JobapplicationDetails.objects.filter(jobseekerprofile_id=jobseekerprofile.id)

    
    application_ids = [app.application_id for app in applicationdetails]

   

    interviewscheduling = Interviewscheduling.objects.filter(application_id__in=application_ids)

    job_ids=[job.job_id for job in interviewscheduling]

    jobdetails=Jobdetails.objects.all()

    context={
        "applicationdetails":  applicationdetails,
        "interviewscheduling":interviewscheduling,
        "jobdetails":jobdetails,
        "jobids":job_ids,
    }


    return render(request,"jobseeker/notifications.html",context) 




########End of Payment Code


def premiumservices(request):
    return render(request,'jobseeker/premiumsevices.html') 

def resumebuilderform(request):
    context = {'YEAR_CHOICES': [(year, year) for year in range(1900, 2100)]}
    userid=request.user.id
    profileid=JobseekerProfile.objects.get(user_id=userid)
    resumetitle=request.POST.get('resumetitle')  
    name = request.POST.get('name')    
    careerobjective = request.POST.get('careerobjective') 
    address = request.POST.get('address')    
    phonenumber = request.POST.get('phonenumber') 
    email = request.POST.get('email')    
    skills= request.POST.get('skills') 
    projecttitle=request.POST.get('projecttitle') 
    projectdescription=request.POST.get('projectdescription') 
    profilepic = request.FILES.get('profilepic')
    collegename=request.POST.get('collegename') 
    coursename=request.POST.get('coursename') 
    passingyear = request.POST.get('passingyear')

    twelthschoolname=request.POST.get('schoolname') 
    twelthmarks=request.POST.get('hssmarks') 
    twelthpassingyear = request.POST.get('yearcompletion')

    tenthschoolname=request.POST.get('hsschoolname') 
    tenthmarks=request.POST.get('tenthmarks') 
    tenthpassingyear = request.POST.get('tenthpassingyear')

    if request.method == 'POST':
        resumedetails=ResumeSchema(
            resumetitle=resumetitle,
            seekername=name,
            careerobjective=careerobjective,    
            address=address,
            phonenumber=phonenumber,
            email=email,
            skills=skills,
            projecttitle=projecttitle,
            projectdescription=projectdescription,
            profilepicture=profilepic,
            collegename=collegename,
            coursename=coursename,
            passingyear=passingyear,
            hssname=twelthschoolname,
            hssyear=twelthpassingyear,
            hssmarks=twelthmarks,
            tenthschoolname=tenthschoolname,
            tenthpassyear=tenthpassingyear,
            tenthmarks=tenthmarks,
            jprofile_id=profileid.id
        )
        resumedetails.save()
        value=ResumeSchema.objects.get(resume_id=resumedetails.pk)
        messages.success(request,"Resume Created")
        return redirect(reverse('resumepreview',args=[value.resume_id]))
   

        # return render(request, 'jobseeker/resumebuilderform.html',context)
    # else:
       
    return render (request, 'jobseeker/resumebuilderform.html',context)

def resumepreview(request, id): #show resume of requested id
    userid=request.user.id
    profileid=JobseekerProfile.objects.get(user_id=userid)
    allresumes = ResumeSchema.objects.get(jprofile_id=profileid.id,resume_id=id)
    context={
        "allresumes":allresumes
    }
    return render(request, 'jobseeker/resumepreview.html',context)

def deleteresume(request,id):
    userid=request.user.id
    profileid=JobseekerProfile.objects.get(user_id=userid)
    allresumes = ResumeSchema.objects.get(jprofile_id=profileid.id,resume_id=id)
    allresumes.delete()
    return redirect(request.META.get('HTTP_REFERER'))
    

def resumelist(request): #show resume of requested id
    userid=request.user.id
    profileid=JobseekerProfile.objects.get(user_id=userid)
    allresumes = ResumeSchema.objects.filter(jprofile_id=profileid.id)
    context={
        "allresumes":allresumes
    }
    return render(request,'jobseeker/resumelist.html',context)

def userpaymentdetails(request):

    userid=request.user.id
    # userpayementdetails=PayementDetails.objects.filter(profile_id=userid)
    query = Q(razorpay_payment_id__isnull=False) & Q(order_id__isnull=False) & Q(profile_id=userid)
    userpayementdetails = PayementDetails.objects.filter(query)
    context={
        "userpayementdetails":userpayementdetails
    }
    
    return render(request,'jobseeker/userpaymentdetails.html',context)


def coverletterhomepage(request):
    return render(request,"jobseeker/coverletterhomepage.html")



def coverletterform(request):
    userid=request.user.id
    profileid=JobseekerProfile.objects.get(user_id=userid)
    coverlettertitle=request.POST.get('covertitle')  
    candidatename = request.POST.get('name')    
    role_you_apply = request.POST.get('designation') 
    company_apply = request.POST.get('companyname')    
    skills= request.POST.get('skills') 


    prompt = f"Generate cover letter for applicant name {candidatename} and I am applying for the position of {role_you_apply} at {company_apply}. I have experience in {skills}."
    response = openai.Completion.create(
        model="text-davinci-003", 
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024
        )
    completion_text = response.choices[0].text
    print(completion_text)
    if request.method == 'POST':
            letterdetails=CoverLetterDetails(
            coverlettertitle=coverlettertitle,
            profile_id=  profileid.id,
            coverletter=completion_text,
            )
            letterdetails.save()
            # value=CoverLetterDetails.objects.get(coverletter_id=letterdetails.pk)
            # return redirect(reverse('resumepreview',args=[value.coverletter_id]))
           
    return render(request,"jobseeker/coverletterform.html")


def allcoverletter(request):
    userid=request.user.id
    profileid=JobseekerProfile.objects.get(user_id=userid)
    coverletters=CoverLetterDetails.objects.filter(profile_id=profileid.id)
    context={
        "coverletters":coverletters
    }
    return render(request,"jobseeker/allcoverletters.html",context)


def coverletterpreview(request,id):
    userid=request.user.id
    profileid=JobseekerProfile.objects.get(user_id=userid)
    coverletters=CoverLetterDetails.objects.get(coverletter_id=id)
    context={
        "coverletters":coverletters
    }

    return render(request,"jobseeker/coverletterpreview.html",context)



#To render different User Home pages

def adminpage(request):
    if request.user.is_authenticated:
        jobseekercount = JobseekerProfile.objects.all().count()
        actualcount=jobseekercount-1
        employeercount = EmployeerProfile.objects.all().count()
        context={
        'employeercount':employeercount,
        'jobseekercount':actualcount,
        }

        return render(request,'moderator/admin.html',context)
    else:
        return redirect('loginpage')



@login_required(login_url='/login')
def employeerpage(request):

    id = request.user
    postedjobcount = Jobdetails.objects.filter(cmp_id_id=id).count()
    context={
    'postedjobcount':postedjobcount
    }

    return render(request,'employeer/home.html',context)





# Admin Pages


def employerslist(request):
    employees = User.objects.filter(role="EMPLOYEER").select_related('employeerprofile','verificationdetails')
    context={
        "employees":employees,
    }
    return render(request,'moderator/employerslist.html',context) 

def jobseekerslist(request):
    seekers = User.objects.filter(role="JOBSEEKER")
    context={
        "seekers":seekers
    }
    return render(request,'moderator/jobseekerslist.html',context) 


def employerdetails(request,id):
    if request.user.is_authenticated:

        profiledetails = EmployeerProfile.objects.get(user_id=id)
        verificationdetails = Verificationdetails.objects.get(user_id=id)
        userdetails = User.objects.get(id=id)
        context = {
           
            'company_name':profiledetails.company_name,
            'officelocation':profiledetails.office_location,
            'phonenumber':profiledetails.phone_number,
            'address':profiledetails.address,
            'pincode':profiledetails.pincode,
            'websiteurl':profiledetails.website_url,
            'prooftype':verificationdetails.proof_type,
            'proof':verificationdetails.proof,
            'buisnesslicense':verificationdetails.buisnesslicence,
            'email':userdetails.email,
            'username':userdetails.username,
            'companylogo':profiledetails.company_logo,
            'status':verificationdetails.isverified,
            'id':userdetails.id
        }


        return render(request,'moderator/employeerdetails.html',context)
    return redirect('loginpage')


def accept(request,id):
    xy = Verificationdetails.objects.get(user_id=id)
    status_value = xy.isverified
    if status_value == 0:
        xy.isverified=1
        xy.save()
    
    return redirect(request.META.get('HTTP_REFERER'))

def reject(request,id):
    xy = Verificationdetails.objects.get(user_id=id)
    status_value = xy.isverified
    if status_value == 1:
        xy.isverified=0
        xy.save()

    return redirect(request.META.get('HTTP_REFERER'))



def allpayements(request):

    query = Q(razorpay_payment_id__isnull=False) & Q(order_id__isnull=False)
    results = PayementDetails.objects.filter(query)
    context={
        "results":results
    }
    return render(request,'moderator/allpayements.html',context)

def statistics(request):
    return render(request,'moderator/statisticshome.html')


def reports(request):
    return render(request,'moderator/reportshome.html')




