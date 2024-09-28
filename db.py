import sqlite3

conn = sqlite3.connect('calories.db', check_same_thread=False)
c = conn.cursor()

# Create a table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    calories INTEGER NOT NULL
)
''')
conn.commit()

# Function to add a meal
def add_meal(name, calories):
    c.execute('INSERT INTO meals (name, calories) VALUES (?, ?)', (name, calories))
    conn.commit()
    return f"Added meal: {name} with {calories} calories."

# Function to get total calories consumed
def get_total_calories():
    c.execute('SELECT SUM(calories) FROM meals')
    total = c.fetchone()[0]
    if total:
        return f"Total calories consumed: {total} calories."
    else:
        return "No meals added yet."

# Function to list all meals
def list_meals():
    c.execute('SELECT name, calories FROM meals')
    meals = c.fetchall()
    if meals:
        meal_list = "Meals added:\n"
        for meal in meals:
            meal_list += f"{meal[0]}: {meal[1]} calories\n"
        return meal_list
    else:
        return "No meals added yet."