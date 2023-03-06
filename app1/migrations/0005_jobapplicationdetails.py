# Generated by Django 4.1.1 on 2023-03-05 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_remove_jobseekerprofile_country_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobapplicationDetails',
            fields=[
                ('application_id', models.AutoField(primary_key=True, serialize=False)),
                ('applicant_resume', models.FileField(blank=True, null=True, upload_to='pdf_files/')),
                ('application_status', models.BooleanField(default=1, verbose_name='status')),
                ('job_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app1.jobdetails')),
                ('jobseekerprofile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app1.jobseekerprofile')),
            ],
        ),
    ]
