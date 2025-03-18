from django.db import models
from django.conf import settings

from .utils import number_str_to_float
from .validators import validate_unit_of_measure

# Create your models here.
"""
- User
    - Ingrediants
    - Recipes
        - Ingrediants
        - Directions for Ingrediants
"""

class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    # ingredients = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=220)
    quantity = models.CharField(max_length=50) # 1, 1/2
    quantity_as_float = models.FloatField(blank=True, null=True)
    
    unit = models.CharField(max_length=50, validators=[validate_unit_of_measure]) # gram, kg, etc.
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True) 

    def save(self, *args, **kwagrs):
        qty = self.quantity
        qty_as_float, qty_as_float_success = number_str_to_float(qty)
        if qty_as_float_success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None
        super().save(*args, **kwagrs)

# class MyUser_Ingredient(models.Model):



