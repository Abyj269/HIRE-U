# Generated by Django 4.1.1 on 2023-02-28 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_candidateskillsandtechnologies_profile_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseekerprofile',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='fulladdress',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='jobseekerprofile',
            name='state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
