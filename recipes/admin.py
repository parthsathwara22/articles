from django.contrib import admin
from django.contrib.auth import get_user_model
# Register your models here.
from .models import Recipe, RecipeIngredient

User = get_user_model
# admin.site.unregister(User)

# admin.site.register(RecipeIngredient)

# class RecipeInline(admin.StackedInline):
#     model = Recipe
#     extra = 0

# class UserAdmin(admin.ModelAdmin):
#     inlines = [RecipeInline]
#     list_display = ['username']

# admin.site.register(User, UserAdmin)

class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0
    readonly_fields = ['quantity_as_float']
    # fields = ['name', 'quantity', 'unit', 'directions']


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['name', 'user']
    readonly_fields = ['timestamp', 'updated']
    raw_id_fields = ['user']

admin.site.register(Recipe, RecipeAdmin)