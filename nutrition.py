import requests
from config import edamam_app_id, edamam_app_key

# Function to get calorie information from Edamam API
def get_calories_from_api(food_item):
    url = f"https://api.edamam.com/api/food-database/v2/parser"
    params = {
        'app_id': edamam_app_id,
        'app_key': edamam_app_key,
        'ingr': food_item,
        'nutrition-type': 'cooking'
    }
    response = requests.get(url, params=params)
    data = response.json()

    try:
        # Extract calories from the API response
        calories = data['parsed'][0]['food']['nutrients']['ENERC_KCAL']
        return calories
    except (IndexError, KeyError):
        return None