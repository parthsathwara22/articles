from django import forms
from .models import Article 


class ArticleForm(forms.ModelForm): #ModelAdmin uses ModelForm by default, when you register your model
    class Meta: #Meta is describing others parts of model form class 
        model = Article
        fields = ['title', 'content']

    def clean(self):
        data = self.cleaned_data
        title = data.get("title")
        if title:
            qs = Article.objects.filter(title__iexact=title) #This type of query will filter down our entire database for particular string that coming in here
            if qs.exists():
                self.add_error("title", f"\"{title}\" is already in use. Please pick another title.") 
        return data 

class ArticleFormOld(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    # def clean_title(self):
    #     cleaned_data = self.cleaned_data #dictionary
    #     print("cleaned_data", cleaned_data)
    #     title = cleaned_data.get('title')
    #     if title.lower().strip() == "the office":
    #         raise forms.ValidationError("This Title is taken.")
    #     print("title", title)
    #     return title

    def clean(self):
        cleaned_data = self.cleaned_data 
        print("all data", cleaned_data)
        title = cleaned_data.get('title')
        content = cleaned_data.get("content")
        if title.lower().strip() == "the office":
            self.add_error('title', 'This Title is taken.')
            # raise forms.ValidationError("This Title is taken.")
        if "office" in content or "office" in title.lower():
            self.add_error('content', "Office can't be in content")
            raise forms.ValidationError("Office is not allowed")
        return cleaned_data





