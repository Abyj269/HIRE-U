from django.contrib import admin

# Register your models here.

from .models import User,Qualifications,EmployeerProfile,Verificationdetails,Jobdetails,JobseekerProfile,candidateSkillsandTechnologies
from .models import JobapplicationDetails
from taggit.models import Tag

admin.site.register(User)
admin.site.register(EmployeerProfile)
admin.site.register(Qualifications)
admin.site.register(Verificationdetails)
admin.site.register(Jobdetails)

admin.site.register(JobseekerProfile)
admin.site.register(candidateSkillsandTechnologies)

admin.site.register(JobapplicationDetails)

