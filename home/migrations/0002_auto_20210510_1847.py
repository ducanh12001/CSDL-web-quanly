# Generated by Django 3.2.1 on 2021-05-10 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='note',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='studentEmail',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
