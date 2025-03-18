from django.contrib.auth.decorators import login_required # If user is not login it will redirect to login page

from django.shortcuts import render, redirect
# from django.db.models import Q
from .models import Article #import model data here
from articles.forms import ArticleForm
from django.http import Http404

# Create your views here.

def article_search_view(request):
    query = request.GET.get("q")
    # qs = Article.objects.all() 
    # if query is not None:
        # lookups = Q(title__icontains=query) | Q(content__icontains=query)
        # qs = Article.objects.filter(lookups)
    qs = Article.objects.search(query=query)
    context = {
        "object_list": qs,

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
        return redirect(article_object.get_absolute_url())
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

def article_detail_view(request, slug=None): 
    article_obj = None
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
        except:
            raise Http404
    context = {
        "object": article_obj,
    }
    return render(request, "articles/detail.html", context= context) #use for handle list's urls