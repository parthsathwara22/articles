from django.contrib import admin

# Register your models here.
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title'] # using this you can display id and title in admin pannel
    search_fields = ['title', 'content'] #using search fields you can search the title and content

admin.site.register(Article, ArticleAdmin) # To show article in django admin
