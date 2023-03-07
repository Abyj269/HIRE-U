from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        JOBSEEKER = "JOBSEEKER", "jobseeker"
        EMPLOYEER = "EMPLOYEER", "employeer"
        MODERATOR = "MODERATOR", "moderator"

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)



class JobseekerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.JOBSEEKER)


class Jobseeker(User):
    base_role = User.Role.JOBSEEKER
    student = JobseekerManager()
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for students"


@receiver(post_save, sender=Jobseeker)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.role == "JOBSEEKER":
        JobseekerProfile.objects.create(user=instance)


class JobseekerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # jobseeker_id = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(null=True,blank=True,max_length=100)
    last_name = models.CharField(null=True,blank=True,max_length=100)
    phone_number = models.CharField(blank=True, null=True,max_length=15)
    email=models.EmailField(blank=True, null=True,max_length=60)
    highestqualification=models.CharField(blank=True, null=True,max_length=50)
    age=models.IntegerField(blank=True, null=True)
    profile_photo = models.ImageField(null=True,blank=True,upload_to='images/')
    aboutyourself = models.CharField(null=True,blank=True,max_length=600)
    fulladdress= models.CharField(null=True,blank=True,max_length=500)
    # full_address = models.CharField(max_length=255,null=True,blank=True)
    # pincode = models.IntegerField(blank=True, null=True)
    # website_url = models.URLField(blank=True, null=True)
    

    
    def __str__(self):
        return str(self.first_name)


class candidateSkillsandTechnologies(models.Model):
    skill_name = models.CharField(max_length=50,null=True,blank=True)
    profile_id = models.ForeignKey(JobseekerProfile,default=None,on_delete=models.CASCADE)




#Employeer Models

class EmployeerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.EMPLOYEER)


class Employeer(User):

    base_role = User.Role.EMPLOYEER
    employeer = EmployeerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return 



def validate_phone_number(value):
    if not re.match(r'^\d{10}$', value):
        raise ValidationError(_('Invalid phone number format'))

class EmployeerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # employeer_id = models.IntegerField(null=True, blank=True)
    company_name = models.CharField(null=True,blank=True,max_length=100)
    office_location = models.CharField(null=True,blank=True,max_length=100)
    address = models.CharField(max_length=255,null=True,blank=True)
    pincode = models.IntegerField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True,max_length=15,validators=[validate_phone_number])
    company_logo = models.ImageField(null=True,blank=True,upload_to='images/')
    
    

    def __str__(self):
        return str(self.user)
    

class Verificationdetails(models.Model):
    user = models.OneToOneField(User,default=None,on_delete=models.CASCADE)
    buisnesslicence=models.ImageField(null=True,blank=True,upload_to='images/')
    proof_type = models.CharField(null=True,blank=True,max_length=100)
    proof = models.ImageField(null=True,blank=True,upload_to='images/')
    isverified=models.BooleanField('isverified',default=0)

@receiver(post_save, sender=Employeer)
def create_user_profile_and_verification_details(sender, instance, created, **kwargs):
    if created and instance.role == "EMPLOYEER":
        EmployeerProfile.objects.create(user=instance)
        Verificationdetails.objects.create(user=instance)

class Jobdetails(models.Model):
    job_id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=100)
    job_description = models.CharField(max_length=500)
    contact_email = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100)
    specialisation = models.CharField(max_length=100)
    experience = models.IntegerField(blank=True, null=True)
    expected_salary = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    vacancies = models.IntegerField(blank=True, null=True)
    lastdate =  models.DateField()
    cmp_id = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    publisheddate = models.DateTimeField(default=datetime.date.today)
    # cmp_profile = models.ForeignKey(EmployeerProfile,default=None,on_delete=models.CASCADE)

class Qualifications(models.Model): 
    quali_id = models.AutoField(primary_key=True) 
    qualification_name = models.CharField(max_length=100,null=True,blank=True)
    cmp_id = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    status=models.BooleanField('status',default=0)
    
    def __str__(self):
        return self.qualification_name
    
class Skills(models.Model):
    skill_id = models.AutoField(primary_key=True) 
    skill_name = models.CharField(max_length=100,null=True,blank=True)
    emp_profile = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    status=models.BooleanField('status',default=0)
    
    def __str__(self):
        return self.skill_name




#Job application details

class JobapplicationDetails(models.Model):
    application_id = models.AutoField(primary_key=True)
    jobseekerprofile = models.ForeignKey(JobseekerProfile, default=None, on_delete=models.CASCADE)
    job = models.ForeignKey(Jobdetails, default=None, on_delete=models.CASCADE)
    employerprofile = models.ForeignKey(EmployeerProfile, default=None, on_delete=models.CASCADE)
    applicant_resume = models.FileField(null=True, blank=True, upload_to='pdf/')
    application_status = models.BooleanField('status', default=1)
    
    
  
    
    

