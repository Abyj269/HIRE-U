from django.shortcuts import render,redirect,HttpResponse
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from app1.models import Jobseeker,Employeer,User
from django.contrib import messages
from app1.models import Jobdetails,Qualifications

def index(request):
    return render(request,"home.html")

def loginpage(request):
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


def postjob(request):
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
    
    return render(request,'employeer/postjob.html')



def addqualification(request):
    if request.method == 'POST':
        quali =request.POST.get('qualification')

        addedqualification= Qualifications(
            qualification_name=quali,
            )
        addedqualification.cmp_id=request.user
        addedqualification.save()
        return redirect('addqualification')
    
   
    pos = Qualifications.objects.all()
    context ={
        'pos': pos
    }
    return render(request,'employeer/addqualification.html',context)


    
    














def adminpage(request):
    return render(request,'admin.html')

def candidatepage(request):
    return render(request,'jobseeker/profile.html')

def employeerpage(request):
    return render(request,'employeer/home.html')

