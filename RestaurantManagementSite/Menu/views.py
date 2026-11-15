from django.shortcuts import render, HttpResponse
import json

# Create your views here.
def index(request):
    # Request object taken as a parameter will allow us to access things like query parameters and the body of different requests that are
    # being sent to this function 
    return HttpResponse("See Recipes")

    #return render(request, "recipe.html") # render the template, only works if templates are inside directory

def recipe_detail(request):
    with open('Menu/Recipes.json') as json_file:
        data = json.load(json_file)
    recipes = data['recipe']
    context = {"recipes": recipes}
    return render(request, "Menu/recipe.html", context)