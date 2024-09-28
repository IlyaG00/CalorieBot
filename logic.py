import telebot
from config import bot_key
from db import create_table, add_meal, get_total_calories, list_meals
from nutrition import get_calories_from_api
from recipe import get_meal_suggestions

bot = telebot.TeleBot(bot_key)

# Handle the '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Calorie Counter Bot!\nUse /add to add meals, /total to view total calories, /list to list all meals, and /suggest to get meal options based on ingredients.")

# Handle the '/add' command
@bot.message_handler(commands=['add'])
def add_meal_handler(message):
    try:
        msg = bot.reply_to(message, "Please enter the meal name (e.g., 'apple', 'pizza')")
        bot.register_next_step_handler(msg, process_food_search_step)
    except Exception as e:
        bot.reply_to(message, "Something went wrong. Please try again.")

# Process the meal name and calculate calories
def process_food_search_step(message):
    try:
        food_item = message.text.strip()
        calories = get_calories_from_api(food_item)
        if calories is not None:
            response = add_meal(food_item, calories)
            bot.reply_to(message, f"{response} (Found {calories} calories)")
        else:
            bot.reply_to(message, "Sorry, I couldn't find the calorie information for that item.")
    except Exception as e:
        bot.reply_to(message, "An error occurred. Please try again later.")

# Handle the '/total' command
@bot.message_handler(commands=['total'])
def total_calories_handler(message):
    total_calories = get_total_calories()
    bot.reply_to(message, total_calories)

# Handle the '/list' command
@bot.message_handler(commands=['list'])
def list_meals_handler(message):
    meals = list_meals()
    bot.reply_to(message, meals)

# Handle the '/suggest' command
@bot.message_handler(commands=['suggest'])
def suggest_meals_handler(message):
    try:
        msg = bot.reply_to(message, "Please enter a fruit or vegetable (e.g., 'apple', 'carrot')")
        bot.register_next_step_handler(msg, process_suggestion_step)
    except Exception as e:
        bot.reply_to(message, "Something went wrong. Please try again.")

# Process the ingredient input and suggest meals
def process_suggestion_step(message):
    try:
        ingredient = message.text.strip()
        suggestions = get_meal_suggestions(ingredient)
        bot.reply_to(message, f"Here are some meal options with {ingredient}:\n{suggestions}")
    except Exception as e:
        bot.reply_to(message, "Sorry, I couldn't find any meal suggestions for that ingredient.")

# Start the bot
if __name__ == "__main__":
    bot.polling()