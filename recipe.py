import requests
from config import spoonacular_key

def get_meal_suggestions(ingredient):
    url = f"https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        'apiKey': spoonacular_key,
        'ingredients': ingredient,
        'number': 5  # Number of suggestions you want to return
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data:
        suggestions = []
        for recipe in data:
            title = recipe.get('title', 'Unknown recipe')
            link = f"https://spoonacular.com/recipes/{title.replace(' ', '-').lower()}-{recipe['id']}"
            suggestions.append(f"{title}: {link}")
        return "\n".join(suggestions)
    else:
        return "No meal suggestions found."