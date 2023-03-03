from django.shortcuts import render,redirect,HttpResponse
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from app1.models import Jobseeker,Employeer,User,Qualifications,EmployeerProfile,Verificationdetails,JobseekerProfile,Skills
from app1.models import candidateSkillsandTechnologies
from django.contrib import messages
from app1.models import Jobdetails,Qualifications,User
from django.views import generic
from django.urls import reverse
from .models import Qualifications
from django.contrib.auth.decorators import login_required
from taggit.models import Tag, TaggedItem
from django.core.paginator import Paginator

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
        return redirect('postjob')
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

            p = Paginator(sorted_jobs,3)
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
            details =Jobdetails.objects.get(job_id=id)
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





    





#To render different User Home pages

def adminpage(request):

    jobseekercount = JobseekerProfile.objects.all().count()
    actualcount=jobseekercount-1
    employeercount = EmployeerProfile.objects.all().count()
    context={
    'employeercount':employeercount,
    'jobseekercount':actualcount,
    }

    return render(request,'moderator/admin.html',context)




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


