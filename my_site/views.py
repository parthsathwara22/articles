#it's use for html web page
from django.http import HttpResponse
import random 
from articles.models import Article # This import article data into views
from django.template.loader import render_to_string #This import html file into views 


# Model View Template (MVT)
def home_view(requests, *args, **kwargs):

    '''take in response(django sends requests)
    Return html as response'''

    name = "Parth" #hard coded
    random_id = random.randint(1, 3) #pseudo random
    
    #from database
    article_obj = Article.objects.get(id=random_id) 
    article_queryset = Article.objects.all()
    # my_list = article_list #[102, 23, 450, 32, 59] 
    # my_list_str = ""
    #for x in my_list:
        #my_list_str += f"<li>number is {x}</li>"

    context = {
        "object_list": article_queryset,
        "title": article_obj.title,
        "id": article_obj.id,
        "content": article_obj.content,

    }
    # django templates
    
    #f= open("my-template.html", 'r')
    #string = f.read()
    html_string = render_to_string("home-view.html", context= context)
    #html_string = '''<h1>Hi! {title} ({id})</h1> <p>{content}</p>'''.format(**context)
    return HttpResponse(html_string)
