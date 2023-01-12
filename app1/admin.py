from django.contrib import admin

# Register your models here.

from .models import User,Qualifications

admin.site.register(User)

admin.site.register(Qualifications)
