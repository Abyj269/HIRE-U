# Generated by Django 4.1.1 on 2023-02-16 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_remove_jobdetails_cmp_profile_jobdetails_cmp_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('skill_id', models.AutoField(primary_key=True, serialize=False)),
                ('skill_name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=0, verbose_name='status')),
                ('emp_profile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app1.employeerprofile')),
            ],
        ),
    ]
