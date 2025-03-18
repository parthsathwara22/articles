from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone


# Create your models here.
from .utils import slugify_instance_title

""" When you change anything here in models.Model make sure to run this command in terminal over and over again 
python manage.py makemigrations 
python manage.py migrate 
"""

User = settings.AUTH_USER_MODEL

class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none() # []
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)

class ArticleManager(models.Manager): # article search view
    
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db) # _db is default database
    
    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Article(models.Model): #every django class inherent from models.Model
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)

    objects = ArticleManager()

    def get_absolute_url(self):
        # return f'/articles/{self.slug}/'
        return reverse("article-detail", kwargs={"slug": self.slug})


    def save(self, *args, **kwargs):
        # obj = Article.objects.get(id=1)
        # set something
        # if self.slug is None:
        #     self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        # obj.save()
        # do another something 

def article_pre_save(sender, instance, *args, **kwagrs):
    # print('pre_save')
    # print(sender, instance)
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(article_pre_save, sender=Article)

def article_post_save(sender, instance, created, *args, **kwagrs):
    # print('post_save')
    # print(args, kwagrs)
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(article_post_save, sender=Article)


