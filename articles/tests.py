from django.test import TestCase

# Create your tests here.
from .models import Article
from django.utils.text import slugify
from .utils import slugify_instance_title
from django.core.exceptions import ValidationError


class ArticleTestCase(TestCase):
    def setUp(self):
        self.numbers_of_articles = 500
        for i in range(0, self.numbers_of_articles):
            Article.objects.create(title='Hello world', content='something')

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())
    
    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.numbers_of_articles)

    def test_hello_world_slug(self):
        obj = Article.objects.all().order_by("id").first() 
        title = obj.title
        slug = obj.slug
        slugified_title = slugify(title)
        self.assertEqual(slug, slugified_title) # hello-world

    def test_hello_world_unique_slug(self):
        qs = Article.objects.all().exclude(slug__iexact='hello-world')
        for obj in qs:
            title = obj.title
            slug = obj.slug
            slugified_title = slugify(title)
            self.assertNotEqual(slug, slugified_title)

    def test_slugify_instance_title(self):
        obj = Article.objects.all().last()
        new_slugs = []
        for i in range(0, 25):
            instance = slugify_instance_title(obj, save=False)
            new_slugs.append(instance.slug) # It will create new slug each time
        unique_slugs = list(set(new_slugs))
        self.assertEqual(len(new_slugs), len(unique_slugs))

    def test_slugify_instance_title_redux(self):
        slug_list = Article.objects.all().values_list('slug', flat=True)
        unique_slug_list = list(set(slug_list))
        self.assertEqual(len(slug_list), len(unique_slug_list))

    def test_user_added_slug_unique(self):
        obj = Article.objects.all().last()
        obj.slug = 'hello-world'
        with self.assertRaises(ValidationError):
            obj.full_clean()
            obj.save()

    def test_article_search_manager(self):
        qs = Article.objects.search(query='hello world')
        self.assertEqual(qs.count(), self.numbers_of_articles)
        qs = Article.objects.search(query='hello')
        self.assertEqual(qs.count(), self.numbers_of_articles)
        qs = Article.objects.search(query='something')
        self.assertEqual(qs.count(), self.numbers_of_articles)







