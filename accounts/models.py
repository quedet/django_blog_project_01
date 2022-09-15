from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    SEXE_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Female'),
        ('O', 'Others')
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    cover_image = models.ImageField(upload_to='users/cover/%Y/%m/%d/', blank=True, default='default/default_background.jpg')
    profile_image = models.ImageField(upload_to='users/profile/%Y/%m/%d/', blank=True, default='default/noimage_profile_men.jpg')
    sexe = models.CharField(max_length=10, choices=SEXE_CHOICES, default='')
    date_of_birth = models.DateField(blank=True, null=True)
    bio = models.TextField(default='', blank=True)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'