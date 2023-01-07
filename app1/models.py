from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db import models



class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        JOBSEEKER = "JOBSEEKER", "jobseeker"
        EMPLOYEER = "EMPLOYEER", "employeer"

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


# @receiver(post_save, sender=Jobseeker)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "JOBSEEKER":
#         JobseekerProfile.objects.create(user=instance)


# class JobseekerProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     jobseeker_id = models.IntegerField(null=True, blank=True)


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


# class EmployeerProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     employeer_id = models.IntegerField(null=True, blank=True)


# @receiver(post_save, sender=Employeer)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "EMPLOYEER":
#         EmployeerProfile.objects.create(user=instance)


