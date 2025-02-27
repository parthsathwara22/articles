from django.db import models

# Create your models here.

""" When you change anything here make sure to run this command in terminal over and over again 
python manage.py makemigration
python manage.py migrate """

class Article(models.Model): #every django class inherent from models.Model
    title = models.TextField()
    content = models.TextField()