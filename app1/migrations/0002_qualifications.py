# Generated by Django 4.1.1 on 2023-01-10 05:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qualifications',
            fields=[
                ('quali_id', models.AutoField(primary_key=True, serialize=False)),
                ('qualification_name', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=0, verbose_name='status')),
                ('cmp_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]