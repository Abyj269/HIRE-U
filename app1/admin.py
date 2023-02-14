from django.contrib import admin

# Register your models here.

from .models import User,Qualifications,EmployeerProfile,Verificationdetails

admin.site.register(User)
admin.site.register(EmployeerProfile)
admin.site.register(Qualifications)
admin.site.register(Verificationdetails)
