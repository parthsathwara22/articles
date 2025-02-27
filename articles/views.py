from django.contrib.auth.decorators import login_required # If user is not login it will redirect to login page
from django.shortcuts import render

from .models import Article #import model data here
from articles.forms import ArticleForm
# try:
#     from articles.forms import ArticleForm
#     print("Import successful!")
# except ImportError as e:
#     print(f"ImportError: {e}")


# Create your views here.
def article_search_view(request):
    query_dict = request.GET
    
    try:
        query = int(query_dict.get("q"))
    except:
        query = None
    article_obj = None 
    if query is not None:
        article_obj = Article.objects.get(id=query)

    context = {
        "object": article_obj,

    }
    return render(request, "articles/search.html", context= context) 

@login_required
def article_create_view(request): 
    form = ArticleForm(request.POST or None)
    # print(dir(form))
    context = {
        "form": form
    }
   
    if form.is_valid():
        article_object = form.save() #Now form itself is model class, .save() method works on ModelForm
        context['form'] = ArticleForm()
    return render(request, "articles/create.html", context= context)

# def article_create_view(request): 
#     form = ArticleForm()
#     # print(dir(form))
#     context = {
#         "form": form
#     }
#     if request.method == "POST":
#         form = ArticleForm(request.POST)
#         context['form'] = form
#         if form.is_valid():
#             title = form.cleaned_data.get("title")
#             content = form.cleaned_data.get("content")
#             article_object = Article.objects.create(title= title, content= content)
#             context['object'] = article_object
#             # context['content'] = content
#             context['created'] = True
#     return render(request, "articles/create.html", context= context)

def article_detail_view(request, id=None): 
    article_obj = None
    if id is not None:
        article_obj = Article.objects.get(id=id)
    context = {
        "object": article_obj,
    }
    return render(request, "articles/detail.html", context= context) #use for handle list's urls