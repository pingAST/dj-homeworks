from django.http import HttpResponse
from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },

}


def recipe_view(request, recipe):
    servings = int(request.GET.get('servings', 1))
    recipe_data = DATA.get(recipe, {})

    if recipe_data:
        updated_recipe = {ingredient: amount * servings for ingredient, amount in recipe_data.items()}
        context = {'recipe': updated_recipe}
        return render(request, 'calculator/index.html', context)
    else:
        return HttpResponse('Рецепт не найден')

