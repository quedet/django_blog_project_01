# Generated by Django 4.1.1 on 2022-09-14 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sexe',
            field=models.CharField(choices=[('M', 'Masculin'), ('F', 'Female'), ('O', 'Others')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='cover_image',
            field=models.ImageField(blank=True, default='default/default_background.jpg', upload_to='users/cover/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='default/noimage_profile_men.jpg', upload_to='users/profile/%Y/%m/%d/'),
        ),
    ]
