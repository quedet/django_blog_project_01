from django.contrib import admin

from article.models import Post, Topic
# Register your models here.

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created', 'updated']