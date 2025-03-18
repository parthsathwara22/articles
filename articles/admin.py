from django.contrib import admin

# Register your models here.
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug','timestamp', 'updated'] # using this you can display id and title in admin pannel
    search_fields = ['title', 'content'] #using search fields you can search the title and content
    raw_id_fields = ['user'] # you can select user if there are mutiple of them

admin.site.register(Article, ArticleAdmin) # To show article in django admin
