from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .fields import OrderField

# Create your models here.
class Topic(models.Model):
    slug = models.SlugField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=False)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
    
    
class Post(models.Model):
    slug = models.SlugField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_posts')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    
    overview = models.TextField(default='')
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
class ItemBase(models.Model):
    author = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.title
    
class Text(ItemBase):
    content = models.TextField()
    
class File(ItemBase):
    file = models.FileField(upload_to='files')
    
class Image(ItemBase):
    file = models.FileField(upload_to='images')
    
class Video(ItemBase):
    url = models.URLField()
    
class Content(models.Model):
    post = models.ForeignKey(Post, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('text', 'video', 'image', 'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['post'])