import random
from django.utils.text import slugify


def slugify_instance_title(instance, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else: 
        slug = slugify(instance.title)
    Klass = instance.__class__ # It's another way to access the class of the instance  
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id) #This exclude id in instance of slug
    if qs.exists():
        # auto generate new slug
        random_int = random.randint(100_000, 25_500_000)
        slug = f"{slug}-{random_int}"
        return slugify_instance_title(instance, save=save, new_slug=slug)
    instance.slug = slug
    if save:
        instance.save()
    return instance