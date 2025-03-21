from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import RecipeIngredient, Recipe
from django.core.exceptions import ValidationError
# Create your tests here.

User = get_user_model()

class UserTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('abc', password='xyz')

    def test_user_pw(self):
        checked = self.user_a.check_password("xyz")
        self.assertTrue(checked)

class RecipeTestCase(TestCase):
    def setUp(self):
        self.user_a = User.objects.create_user('parth', password='123')
        self.recipe_a = Recipe.objects.create(
            name='Panner Tikka Masala', 
            user=self.user_a
        )

        self.recipe_b = Recipe.objects.create(
            name='Panner Butter Masala', 
            user=self.user_a
        )

        self.recipe_ingridient_a = RecipeIngredient.objects.create(
            recipe=self.recipe_a, 
            name='Panner', 
            quantity='1/2', 
            unit='kg'
        )

        self.recipe_ingridient_b = RecipeIngredient.objects.create(
            recipe=self.recipe_a, 
            name='Panner', 
            quantity='sscsd', 
            unit='kg'
        )


    def test_user_count(self):
        qs = User.objects.all()
        self.assertEqual(qs.count(), 1)

    def test_user_recipe_reverse_count(self):
        user = self.user_a
        qs = user.recipe_set.all()
        # print(qs)
        self.assertEqual(qs.count(), 2)
    
    def test_user_recipe_forward_count(self):
        user = self.user_a
        qs = Recipe.objects.filter(user=user)
        # print(qs)
        self.assertEqual(qs.count(), 2)

    def test_recipe_ingredient_reverse_count(self):
        recipe = self.recipe_a
        qs = recipe.recipeingredient_set.all()
        # print(qs)
        self.assertEqual(qs.count(), 2)

    def test_recipe_ingredient_count(self):
        recipe = self.recipe_a
        qs = RecipeIngredient.objects.filter(recipe=recipe)
        # print(qs)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation(self):
        user = self.user_a
        qs = RecipeIngredient.objects.filter(recipe__user=user)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation_reverse(self):
        user = self.user_a
        recipeingredient_ids = list(user.recipe_set.all().values_list('recipeingredient__id', flat=True))
        # print(recipeingredient_ids)
        qs = RecipeIngredient.objects.filter(id__in=recipeingredient_ids)
        self.assertEqual(qs.count(), 2)

    def test_user_two_level_relation_via_recipes(self):
        user = self.user_a
        ids = user.recipe_set.all().values_list("id", flat=True)
        qs = RecipeIngredient.objects.filter(recipe__id__in=ids)
        self.assertEqual(qs.count(), 2) 

    def test_unit_measure_validation(self):
        invalid_unit = 'kg'
        ingredient = RecipeIngredient(
            name='New',
            quantity= 10,
            recipe=self.recipe_a,
            unit=invalid_unit
        )
        ingredient.full_clean() 

    def test_unit_measure_validation_error(self):
        invalid_units = ['nada', 'assvbnn']
        for unit in invalid_units:
            with self.assertRaises(ValidationError):
                ingredient = RecipeIngredient(
                    name='New',
                    quantity= 10,
                    recipe=self.recipe_a,
                    unit=unit
                )
                ingredient.full_clean() 

    def test_quantity_as_float(self):
        self.assertIsNotNone(self.recipe_ingridient_a.quantity_as_float)
        self.assertIsNone(self.recipe_ingridient_b.quantity_as_float)


