import sqlite3

def create_database():
    conn = sqlite3.connect("diet_management_system.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Food (
            food_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            meal_type TEXT NOT NULL,
            measurement TEXT NOT NULL,
            calories INTEGER NOT NULL,
            protein INTEGER NOT NULL,
            carbs INTEGER NOT NULL,
            fiber INTEGER NOT NULL,
            calcium INTEGER NOT NULL,
            key_ingredients TEXT NOT NULL
        )
    ''')
    food_items = [
    ("Oatmeal with Almonds", "Breakfast", "1 bowl", 250, 10, 40, 5, 50, "Oats, Almonds, Milk"),
    ("Scrambled Eggs with Toast", "Breakfast", "2 eggs, 1 slice toast", 320, 18, 25, 2, 70, "Eggs, Bread, Butter"),
    ("Vegetable Poha", "Breakfast", "1 plate", 270, 6, 50, 4, 80, "Flattened Rice, Peas, Carrots"),
    ("Peanut Butter Banana Smoothie", "Breakfast", "1 glass", 350, 12, 55, 3, 100, "Banana, Peanut Butter, Milk"),
    ("Idli with Coconut Chutney", "Breakfast", "2 idlis, chutney", 280, 7, 45, 5, 80, "Rice, Urad Dal, Coconut"),
    ("Boiled Eggs", "Morning Snack", "2 eggs", 140, 12, 1, 0, 50, "Eggs"),
    ("Greek Yogurt with Honey", "Morning Snack", "1 cup", 200, 15, 25, 2, 150, "Greek Yogurt, Honey"),
    ("Handful of Almonds and Walnuts", "Morning Snack", "15 pieces", 180, 6, 8, 4, 100, "Almonds, Walnuts"),
    ("Grilled Chicken Salad", "Lunch", "1 plate", 350, 30, 15, 8, 100, "Chicken, Lettuce, Tomato, Olive Oil"),
    ("Dal and Brown Rice", "Lunch", "1 bowl each", 400, 18, 60, 10, 150, "Lentils, Brown Rice, Ghee"),
    ("Vegetable Roti Wrap", "Lunch", "1 wrap", 380, 12, 55, 8, 120, "Whole Wheat Roti, Vegetables, Paneer"),
    ("Fish Curry with Steamed Rice", "Lunch", "1 plate", 450, 30, 50, 5, 120, "Fish, Rice, Coconut"),
    ("Rajma Chawal", "Lunch", "1 bowl each", 420, 15, 65, 10, 110, "Kidney Beans, Rice, Tomato"),
    ("Fruit Salad", "Evening Snack", "1 bowl", 200, 3, 45, 6, 40, "Apple, Banana, Grapes, Yogurt"),
    ("Vegetable Soup", "Evening Snack", "1 bowl", 180, 5, 30, 6, 90, "Carrots, Beans, Tomato, Corn"),
    ("Bhel Puri", "Evening Snack", "1 plate", 250, 6, 45, 4, 60, "Puffed Rice, Vegetables, Chutneys"),
    ("Masala Roasted Chickpeas", "Evening Snack", "1 cup", 220, 10, 35, 8, 80, "Chickpeas, Spices"),
    ("Steamed Vegetables with Quinoa", "Dinner", "1 plate", 300, 20, 50, 10, 120, "Broccoli, Carrots, Quinoa"),
    ("Paneer Bhurji with Roti", "Dinner", "1 plate", 380, 18, 40, 5, 150, "Paneer, Onion, Tomato, Spices"),
    ("Methi Thepla with Yogurt", "Dinner", "2 theplas", 350, 10, 55, 6, 130, "Whole Wheat, Fenugreek, Yogurt"),
    ("Grilled Fish with Sautéed Vegetables", "Dinner", "1 plate", 400, 35, 20, 5, 160, "Fish, Olive Oil, Vegetables"),
    ("Khichdi with Ghee", "Dinner", "1 bowl", 380, 12, 55, 8, 140, "Rice, Moong Dal, Ghee"),
    ('Chia Pudding with Berries', 'Breakfast', '1 bowl', 280, 8, 42, 10, 120, 'Chia Seeds, Almond Milk, Berries'),
    ('Moong Dal Chilla', 'Breakfast', '2 chillas', 320, 14, 40, 6, 110, 'Moong Dal, Spices, Curd'),
    ('Multigrain Paratha with Curd', 'Breakfast', '1 paratha', 350, 12, 50, 5, 140, 'Whole Wheat, Oats, Curd'),
    ('Cottage Cheese Sandwich', 'Morning Snack', '1 sandwich', 300, 18, 40, 4, 130, 'Paneer, Bread, Butter'),
    ('Sprouts Salad', 'Morning Snack', '1 bowl', 250, 12, 35, 8, 90, 'Mixed Sprouts, Tomato, Lemon'),
    ('Quinoa and Chickpea Bowl', 'Lunch', '1 bowl', 400, 20, 55, 12, 130, 'Quinoa, Chickpeas, Olive Oil'),
    ('Stuffed Capsicum with Rice', 'Lunch', '1 plate', 420, 16, 60, 10, 140, 'Capsicum, Rice, Paneer'),
    ('Spinach and Corn Sandwich', 'Evening Snack', '1 sandwich', 280, 10, 40, 6, 100, 'Spinach, Corn, Bread, Cheese'),
    ('Sweet Potato Chaat', 'Evening Snack', '1 bowl', 300, 5, 50, 8, 90, 'Sweet Potato, Chaat Masala, Lemon'),
    ('Vegetable Stir Fry with Tofu', 'Dinner', '1 plate', 350, 22, 45, 8, 120, 'Tofu, Vegetables, Soy Sauce'),
    ('Lentil Soup with Whole Wheat Bread', 'Dinner', '1 bowl, 1 slice', 380, 18, 50, 10, 110, 'Lentils, Spices, Bread'),
    ('Mushroom and Spinach Pasta', 'Dinner', '1 plate', 450, 20, 60, 6, 150, 'Mushrooms, Spinach, Pasta, Cheese'),
    ('Millet Khichdi', 'Dinner', '1 bowl', 360, 14, 55, 9, 130, 'Millets, Moong Dal, Ghee')
]

    cursor.executemany('''
        INSERT INTO Food (name, meal_type, measurement, calories, protein, carbs, fiber, calcium, key_ingredients)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', food_items)

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Meal (
    meal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_day TEXT NOT NULL,   -- Example: "Monday"
    breakfast INTEGER,        -- Food ID for breakfast
    morning_snack INTEGER,    -- Food ID for morning snack
    lunch INTEGER,            -- Food ID for lunch
    evening_snack INTEGER,    -- Food ID for evening snack
    dinner INTEGER,           -- Food ID for dinner
    FOREIGN KEY (breakfast) REFERENCES Food(food_id),
    FOREIGN KEY (morning_snack) REFERENCES Food(food_id),
    FOREIGN KEY (lunch) REFERENCES Food(food_id),
    FOREIGN KEY (evening_snack) REFERENCES Food(food_id),
    FOREIGN KEY (dinner) REFERENCES Food(food_id)
   )''')
    meal_plan = [
    ("Monday", 1, 2, 3, 4, 5),
    ("Tuesday", 6, 7, 8, 9, 10),
    ("Wednesday", 11, 12, 13, 14, 15),
    ("Thursday", 16, 17, 18, 19, 20),
    ("Friday", 21, 22, 23, 24, 25),
    ("Saturday", 26, 27, 28, 29, 30),
    ("Sunday", 31, 32, 33, 34, 35)
]


    cursor.executemany('''
    INSERT INTO Meal (meal_day, breakfast, morning_snack, lunch, evening_snack, dinner)
    VALUES (?, ?, ?, ?, ?, ?)
''', meal_plan)
    conn.commit()
    conn.close()


def insert_food(name, meal_type, measurement, calories, protein, carbs, fiber, calcium, key_ingredients):
    conn = sqlite3.connect("diet_management_system.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Food (name, meal_type, measurement, calories, protein, carbs, fiber, calcium, key_ingredients)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, meal_type, measurement, calories, protein, carbs, fiber, calcium, key_ingredients))

    conn.commit()
    conn.close()
def get_food_dict():
    """Fetch food items and return a dictionary with name as key and (measurement, calories) as values."""
    conn = sqlite3.connect("diet_management_system.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, measurement, calories FROM Food")
    food_data = cursor.fetchall()  # Returns a list of tuples (name, measurement, calories)

    conn.close()

    # Convert to dictionary {food_name: (measurement, calories)}
    food_dict = {name: (measurement, calories) for name, measurement, calories in food_data}

    return food_dict
create_database()