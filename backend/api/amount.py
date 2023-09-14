from django.db import models
from rest_framework import serializers

class Ingredient(models.Model):
    name = models.CharField(max_length = 20)
    recipes = models.ManyToManyField('Recipe', through = 'RecipeIngredient')

class Recipe(models.Model):
    name = models.CharField(max_length = 20)

class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey('Ingredient')
    recipe = models.ForeignKey('Recipe')
    amount = models.DateTimeField()


serializers.py:
ДобавляемСериалайзер:
class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field(source='recipe.id')
    name = serializers.Field(source='recipe.name')
    class Meta:
        model = RecipeIngredient

        fields = ('id', 'name', 'amount', )

class IngredientSerializer(serializers.ModelSerializer):
    recipes = RecipeIngredientSerializer(source='RecipeIngredient_set', many=True) # Добавили строку
    class Meta:
        model = Ingredient

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe






views.py:

class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

Требуется:
{
   'id' : 2,
   'name' : 'some ingredient',
   'recipes' : [
      {
         'id' : 55,
         'name' : 'recipe 1'
         'amount' : 34151564
      },
      {
         'id' : 56,
         'name' : 'recipe 2'
         'amount' : 11200299
      }
   ]
}
