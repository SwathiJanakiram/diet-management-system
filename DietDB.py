import sqlite3

def create_database():
    conn = sqlite3.connect("diet_management_system.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER,
            weight REAL,
            height REAL,
            goal_weight REAL,
            goal_time INTEGER,
            contact TEXT UNIQUE,
            gender TEXT,
            activity REAL,
            password TEXT,
            total_calories REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_calorie_intake (
            user_id TEXT NOT NULL,
            day DATE NOT NULL,
            total_calorie REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            user_id TEXT NOT NULL,
            week_no INTEGER NOT NULL,
            weight REAL NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(name, age, weight, height, goal_weight, goal_time, contact, gender, activity, password, user_id, total_calories):
    conn = sqlite3.connect("diet_management_system.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO Users (user_id, name, age, weight, height, goal_weight, goal_time, contact, gender, activity, password, total_calories)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, name, age, weight, height, goal_weight, goal_time, contact, gender, activity, password, total_calories))
    cursor.execute(
        "INSERT INTO progress (user_id, week_no, weight) VALUES (?, ?, ?)",
        (user_id, 1, weight)
    )

    conn.commit()
    conn.close()

def check_login(username, password):
    conn = sqlite3.connect("diet_management_system.db")  # Ensure correct DB name
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE user_id = ?", (username,))
    user = cursor.fetchone()

    conn.close()
    
    if user:
        stored_password = user[1]  
        print(stored_password)# Fetch password from database
        return stored_password == password  # Ensure direct comparison works

    return False

def user_details(username):
    conn = sqlite3.connect("diet_management_system.db")  # Fixed DB name
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Users WHERE user_id = ?", (username,))
    result = cursor.fetchone()
    
    conn.close()
    return result

def fetch_calorie_data(user_id):
    conn = sqlite3.connect("diet_management_system.db")  # Fixed DB name
    cursor = conn.cursor()
    
    cursor.execute("SELECT day, total_calorie FROM daily_calorie_intake WHERE user_id = ? ORDER BY day", (user_id,))
    data = cursor.fetchall()
    
    conn.close()
    
    if data:
        dates, calories = zip(*data)  # Unpack into two lists
        return list(dates), list(calories)
    else:
        return [], []  

def fetch_progress_data(user_id):
    conn = sqlite3.connect("diet_management_system.db")  # Fixed DB name
    cursor = conn.cursor()
    
    cursor.execute("SELECT week_no, weight FROM progress WHERE user_id = ? ORDER BY week_no", (user_id,))
    data = cursor.fetchall()
    
    conn.close()
    
    if data:
        weeks, weights = zip(*data)  # Unpack into two lists
        return list(weeks), list(weights)
    else:
        return [], []
def update_total_calorie(user_id, day, cal):
    conn = sqlite3.connect("diet_management_system.db")
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE daily_calorie_intake
        SET total_calorie = ?
        WHERE user_id = ? AND day = ?
    ''', (cal, user_id, day))

    conn.commit()
    conn.close()

def insert_total_calorie(user_id, day, cal):
    conn = sqlite3.connect("diet_management_system.db")
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO daily_calorie_intake (user_id, day, total_calorie)
        VALUES (?, ?, ?)
    ''', (user_id, day, cal))

    conn.commit()
    conn.close()

# Function to insert weight data if week does not exist
def insert_weight(user_id, week_update, new_weight, goal_weight, goal_time):
    conn = sqlite3.connect("diet_management_system.db")
    cursor = conn.cursor()
    
    # Insert new record into progress table
    cursor.execute(
        "INSERT INTO progress (user_id, week_no, weight) VALUES (?, ?, ?)",
        (user_id, week_update, new_weight)
    )
    
    # Update user table with latest weight and goals
    cursor.execute(
        "UPDATE Users SET weight = ?, goal_weight = ?, goal_time = ? WHERE user_id = ?",
        (new_weight, goal_weight, goal_time, user_id)
    )
    
    conn.commit()
    conn.close()
    print("New progress record inserted successfully!")

# Function to update weight if week already exists
def update_weight(user_id, week_update, new_weight, goal_weight, goal_time):
    conn = sqlite3.connect("diet_management_system.db")
    cursor = conn.cursor()
    
    # Update progress table for the given week
    cursor.execute(
        "UPDATE progress SET weight = ? WHERE user_id = ? AND week = ?",
        (new_weight, user_id, week_update)
    )
    
    # Update user table with the latest weight and goals
    cursor.execute(
        "UPDATE Users SET weight = ?, goal_weight = ?, goal_time = ? WHERE user_id = ?",
        (new_weight, goal_weight, goal_time, user_id)
    )
    
    conn.commit()
    conn.close()
    print("Progress record updated successfully!")

  
# Example usage
create_database()
