import tkinter as tk
from tkinter import ttk,messagebox
import sqlite3
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import subprocess
from tkcalendar import Calendar
from DietDB import user_details,fetch_calorie_data,fetch_progress_data,update_total_calorie,insert_total_calorie,insert_weight,update_weight
import matplotlib.pyplot as plt
from FoodDB import get_food_dict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sys
if len(sys.argv) > 1:
    user_id = sys.argv[1]  # Get user_id from command-line argument
else:
    user_id = "Swathi J7899423192"  # Handle missing argument case

print(f"Logged in User ID: {user_id}")

# Root window setup
root = tk.Tk()
root.title("Diet Management System")
root.state("zoomed")  # Full screen for Windows
# root.attributes("-fullscreen", True)  # Full screen for macOS/Linux

# --- Styling ---
BG_COLOR = "#f4f4f4"  
NAV_COLOR = "#0077b6"  
BTN_COLOR = "#0096c7"  
BTN_HOVER = "#48cae4"  
FONT = ("Arial", 12, "bold")

user_id, name, age, weight, height, goal_weight, goal_time, contact, gender, activity, password, total_calories=user_details(user_id)
bmi = weight / (height / 100) ** 2  # Convert height to meters
if bmi < 18.5:
    category = "Underweight"
elif 18.5 <= bmi < 24.9:
    category = "Normal weight"
elif 25 <= bmi < 29.9:
    category = "Overweight"
else:
    category = "Obese"

protein_g = (total_calories * 0.15) / 4 
carbs_g = (total_calories * 0.55) / 4 
fats_g = (total_calories * 0.30) / 9  
fiber_g = total_calories / 100  
calcium_mg = total_calories * 0.5 /1000

# --- Function to Change Frames ---
def show_frame(frame):
    frame.tkraise()

# --- Navigation Bar ---
nav_bar = tk.Frame(root, bg=NAV_COLOR, height=60)
nav_bar.pack(fill="x")

# --- Main Display Area (Expands to full window size) ---
main_display = tk.Frame(root, bg=BG_COLOR)
main_display.pack(fill="both", expand=True)

# Configure main_display to ensure full expansion
main_display.grid_rowconfigure(0, weight=1)
main_display.grid_columnconfigure(0, weight=1)

# --- Create Main Frames ---
frame_dashboard = tk.Frame(main_display, bg="white")
frame_meal_plan = tk.Frame(main_display, bg="white")
frame_calorie_tracker = tk.Frame(main_display, bg="white")
frame_progress = tk.Frame(main_display, bg="white")
frame_food_nutrition = tk.Frame(main_display, bg="white")
def open_plan():
    subprocess.Popen(["python", "mealplan.py"])
# ---- Meal Plan Frame ----
tk.Label(frame_meal_plan, text="Meal Plan5 for a Week", font=("Arial", 18, "bold"), bg="white", fg="black").pack(pady=20)
tk.Label(frame_meal_plan, text="", font=FONT, bg="white").pack()
update_button = tk.Button(frame_meal_plan, text="Check plan", command=open_plan, bg="#0077b6", fg="white", font=("Arial", 10, "bold"))
update_button.pack(pady=10)
frames = [
    frame_dashboard,
    frame_meal_plan,
    frame_calorie_tracker,
    frame_progress,
    frame_food_nutrition,
]

for frame in frames:
    frame.grid(row=0, column=0, sticky="nsew")

# ---- Dashboard Frame ----
tk.Label(frame_dashboard, text="Dashboard", font=("Arial", 18, "bold"), bg="white", fg="black").pack(pady=20)
tk.Label(frame_dashboard, text="Welcome to your Diet Management System!", font=FONT, bg="white").pack()

user_info_frame = tk.Frame(frame_dashboard, bg="white")
user_info_frame.pack(fill="x", padx=20, pady=20)

left_container = tk.Frame(user_info_frame, bg="#e3f2fd", padx=20, pady=20)
left_container.pack(side="left", fill="both", expand=True, padx=10)

right_container = tk.Frame(user_info_frame, bg="#e1f5fe", padx=20, pady=20)
right_container.pack(side="right", fill="both", expand=True, padx=10)

# Individual User Details
user_details_list = [
    ("Name", name),
    ("Age", age),
    ("Height", f"{height} cm"),
    ("Weight", f"{weight} kg"),
    ("Goal Weight", f"{goal_weight} kg"),
    ("Goal Time", f"{goal_time} weeks"),
    ("BMI", f"{bmi:.2f}"),
    ("Category", category)
]
for label, value in user_details_list:
    tk.Label(left_container, text=f"{label}: {value}", font=("Arial", 12), bg="#e3f2fd", relief="groove", padx=10, pady=5).pack(fill="x", pady=2)

# Individual Nutrients Breakdown
nutrients_list = [
    ("Total Calories", f"{total_calories} kcal"),
    ("Protein", f"{protein_g:.1f} g"),
    ("Carbs", f"{carbs_g:.1f} g"),
    ("Fats", f"{fats_g:.1f} g"),
    ("Fiber", f"{fiber_g:.1f} g"),
    ("Calcium", f"{calcium_mg:.1f} g")
]
for label, value in nutrients_list:
    tk.Label(right_container, text=f"{label}: {value}", font=("Arial", 12), bg="#e1f5fe", relief="groove", padx=10, pady=5).pack(fill="x", pady=2)

# Pie Chart
fig, ax = plt.subplots(figsize=(3, 3))
labels = ["Protein", "Carbs", "Fiber", "Fats", "Calcium"]
values = [protein_g, carbs_g, fiber_g, fats_g,  calcium_mg]
ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0'])
ax.set_title("Nutrient Breakdown")
canvas = FigureCanvasTkAgg(fig, master=right_container)
canvas.get_tk_widget().pack()



# ---- Calorie Tracker Frame ----
tk.Label(frame_calorie_tracker, text="Calorie Tracker", font=("Arial", 18, "bold"), bg="white", fg="black").pack(pady=20)
tk.Label(frame_calorie_tracker, text="Track your calorie intake.", font=FONT, bg="white").pack()
left_frame = tk.Frame(frame_calorie_tracker, bg="#e3f2fd", padx=20, pady=20)
left_frame.pack(side="left", fill="both", expand=True, padx=10)


# Daily Calorie Intake Graph
fig, ax = plt.subplots(figsize=(5,3))
dates,calories=fetch_calorie_data(user_id)
ax.plot(dates, calories, marker='o', linestyle='-')
ax.set_title("Daily Calorie Intake")
ax.set_xlabel("Date")
ax.set_ylabel("Calories (kcal)")
canvas = FigureCanvasTkAgg(fig, master=left_frame)
canvas.get_tk_widget().pack()

# Calendar for Date Selection
tk.Label(left_frame, text="Select Date", font=("Arial", 12), bg="#e3f2fd").pack(pady=5)
cal = Calendar(left_frame, selectmode='day', year=2025, month=4, day=1)
cal.pack(pady=5)

tk.Label(left_frame, text="Enter Calorie Intake", font=("Arial", 12), bg="#e3f2fd").pack(pady=5)
calorie_entry = tk.Entry(left_frame)
calorie_entry.pack(pady=5)

def update_calorie():
    selected_date = cal.get_date()  # Get selected date as string (e.g., '04/01/2025')
    selected_date = datetime.strptime(selected_date, "%m/%d/%y")  # Convert to datetime object
    tomorrow = datetime.today() + timedelta(days=1)  # Get tomorrow's date

    if selected_date >= tomorrow:
        tk.messagebox.showerror("Input Error", "Please select date is in the past or today.")
        return
    new_calorie = calorie_entry.get()
    selected_date = cal.get_date()
    if new_calorie.isdigit():
        dates,calories=fetch_calorie_data(user_id)
        if selected_date in dates:
            update_total_calorie(user_id,selected_date,new_calorie)
        else:
            insert_total_calorie(user_id,selected_date,new_calorie)
            
        dates,calories=fetch_calorie_data(user_id)
        ax.clear()
        ax.plot(dates, calories, marker='o', linestyle='-')
        ax.set_title("Daily Calorie Intake")
        ax.set_xlabel("Date")
        ax.set_ylabel("Calories (kcal)")
        canvas.draw()

update_button = tk.Button(left_frame, text="Update", command=update_calorie, bg="#0077b6", fg="white", font=("Arial", 10, "bold"))
update_button.pack(pady=10)

# Right Frame for Calorie Calculator
right_frame = tk.Frame(frame_calorie_tracker, bg="#e1f5fe", padx=20, pady=20)
right_frame.pack(side="right", fill="both", expand=True, padx=10)

tk.Label(right_frame, text="Calorie Calculator", font=("Arial", 14, "bold"), bg="#e1f5fe").pack(pady=5)

food_items = get_food_dict()
selected_food = tk.StringVar()
tk.Label(right_frame, text="Select Item", font=("Arial", 12), bg="#e1f5fe").pack(pady=5)
food_dropdown = ttk.Combobox(right_frame, textvariable=selected_food, values=list(food_items.keys()))
food_dropdown.pack(pady=5)

tk.Label(right_frame, text="Quantity(Serving)", font=("Arial", 12), bg="#e1f5fe").pack(pady=5)
quantity_entry = tk.Entry(right_frame)
quantity_entry.pack(pady=5)

item_list = []
calculated_calories = tk.Label(right_frame, text="Total Calories: 0 kcal", font=("Arial", 12, "bold"), bg="#e1f5fe")
calculated_calories.pack(pady=10)

food_listbox = tk.Listbox(right_frame, height=10, width=40)
food_listbox.pack(pady=5)
def calculate_nutrients():
    food = selected_food.get()
    quantity = quantity_entry.get()

    if not food:
        tk.messagebox.showerror("Input Error", "Please select a food item.")
        return
    if not quantity.isdigit() or int(quantity) <= 0:
        tk.messagebox.showerror("Input Error", "Please enter a valid positive quantity.")
        return

    quantity = int(quantity)

    if food in food_items:
        measurement, default_calories = food_items[food]  # Get default measurement and calories

        # Extract the numeric value from the measurement (e.g., "100g" -> 100)
        measurement_value = ''.join(filter(str.isdigit, measurement))
        measurement_value = int(measurement_value) if measurement_value else 1  # Avoid division by zero

        # Adjust calories based on the input quantity
        total_cal = (default_calories / measurement_value) * quantity

        item_list.append((food, quantity, round(total_cal)))  # Round to avoid decimals
        food_listbox.insert(tk.END, f"{food} ({quantity}g) - {round(total_cal)} kcal")
        update_total_calories()

def update_total_calories():
    total_cal = sum(item[2] for item in item_list)
    calculated_calories.config(text=f"Total Calories: {total_cal} kcal")
    calorie_entry.delete(0, tk.END)
    calorie_entry.insert(0, str(total_cal))

def remove_selected_item():
    selected = food_listbox.curselection()
    if selected:
        index = selected[0]
        del item_list[index]
        food_listbox.delete(index)
        update_total_calories()

def clear_all_items():
    item_list.clear()
    food_listbox.delete(0, tk.END)
    update_total_calories()

tk.Button(right_frame, text="Add Item", command=calculate_nutrients, bg="#0096c7", fg="white", font=("Arial", 10, "bold")).pack(pady=5)
tk.Button(right_frame, text="Remove Selected", command=remove_selected_item, bg="#ff6b6b", fg="white", font=("Arial", 10, "bold")).pack(pady=5)
tk.Button(right_frame, text="Clear All", command=clear_all_items, bg="#ffa502", fg="white", font=("Arial", 10, "bold")).pack(pady=5)
# ---- Progress Frame ----
tk.Label(frame_progress, text="Progress", font=("Arial", 18, "bold"), bg="white", fg="black").pack(pady=20)
tk.Label(frame_progress, text="Monitor your health progress.", font=FONT, bg="white").pack()


progress_left_frame = tk.Frame(frame_progress, bg="#e3f2fd", padx=20, pady=20)
progress_left_frame.pack(side="left", fill="both", expand=True, padx=10)

tk.Label(progress_left_frame, text="Weight Progress", font=("Arial", 14, "bold"), bg="#e3f2fd").pack(pady=5)

# Weight Progress Graph
fig_progress, ax_progress = plt.subplots(figsize=(5,3))
weeks,weights=fetch_progress_data(user_id)
ax_progress.plot(weeks, weights, marker='o', linestyle='-')
ax_progress.set_title("Weight Progress Over Weeks")
ax_progress.set_xlabel("Week")
ax_progress.set_ylabel("Weight (kg)")
canvas_progress = FigureCanvasTkAgg(fig_progress, master=progress_left_frame)
canvas_progress.get_tk_widget().pack()

# Update Progress Section
progress_right_frame = tk.Frame(frame_progress, bg="#e1f5fe", padx=20, pady=20)
progress_right_frame.pack(side="right", fill="both", expand=True, padx=10)

tk.Label(progress_right_frame, text="Update Progress", font=("Arial", 14, "bold"), bg="#e1f5fe").pack(pady=5)

tk.Label(progress_right_frame, text="Week", font=("Arial", 12), bg="#e1f5fe").pack(pady=5)
current_week_entry = tk.Entry(progress_right_frame)
current_week_entry.pack(pady=5)

tk.Label(progress_right_frame, text="Current Weight (kg)", font=("Arial", 12), bg="#e1f5fe").pack(pady=5)
current_weight_entry = tk.Entry(progress_right_frame)
current_weight_entry.pack(pady=5)

tk.Label(progress_right_frame, text="Goal Weight (kg)", font=("Arial", 12), bg="#e1f5fe").pack(pady=5)
goal_weight_entry = tk.Entry(progress_right_frame)
goal_weight_entry.pack(pady=5)

tk.Label(progress_right_frame, text="Goal Time (weeks)", font=("Arial", 12), bg="#e1f5fe").pack(pady=5)
goal_time_entry = tk.Entry(progress_right_frame)
goal_time_entry.pack(pady=5)

def update_progress():
    new_weight = float(current_weight_entry.get())
    goal_weight= float(goal_weight_entry.get())
    goal_time=int(goal_time_entry.get())
    week_update=int(current_week_entry.get())
    
    if new_weight:
        weeks,weights=fetch_progress_data(user_id)
        if week_update in weeks:
            update_weight(user_id,week_update,new_weight,goal_weight,goal_time)
        elif week_update >max(weeks)+1:
             messagebox.showerror("Error", "Previous weeks not filled or only for these weeks!")
        else:
            insert_weight(user_id,week_update,new_weight,goal_weight,goal_time)
        ax_progress.clear()
        weeks,weights=fetch_progress_data(user_id)
        ax_progress.plot(weeks, weights, marker='o', linestyle='-')
        ax_progress.set_title("Weight Progress Over Weeks")
        ax_progress.set_xlabel("Week")
        ax_progress.set_ylabel("Weight (kg)")
        canvas_progress.draw()
    else:
        messagebox.showerror("Error", "Posivite Weight!")

update_button = tk.Button(progress_right_frame, text="Update", command=update_progress, bg="#0077b6", fg="white", font=("Arial", 10, "bold"))
update_button.pack(pady=10)

# ---- Food Nutrition Frame ----
tk.Label(frame_food_nutrition, text="Food Nutrition Guide", font=("Arial", 18, "bold"), bg="white").pack(pady=10)
frame_top = tk.Frame(frame_food_nutrition, bg="white")
frame_top.pack(fill="both", expand=True)

frame_bottom = tk.Frame(frame_food_nutrition, bg="white")
frame_bottom.pack(fill="both", expand=True, pady=10)

frame_left = tk.Frame(frame_top, bg="white")
frame_right = tk.Frame(frame_top, bg="white")
frame_left.pack(side="left", expand=True, fill="both", padx=10)
frame_right.pack(side="right", expand=True, fill="both", padx=10)

nutrition_info = {
    "Carb-rich Foods": "Essential for energy. Examples: Rice, Pasta, Bread, Potatoes, Oats, Bananas, Sweet Corn, Quinoa, Barley.",
    "Fiber-rich Foods": "Supports digestion and heart health. Examples: Beans, Lentils, Broccoli, Apples, Whole Grains, Chia Seeds, Almonds, Carrots.",
    "Micro-nutrient Rich Foods": "Vital for immune function and overall well-being. Examples: Nuts, Seeds, Leafy Greens, Fish, Dairy, Mushrooms, Seaweed, Shellfish.",
    "Vitamin-rich Foods": "Boosts immune system and cell function. Examples: Citrus Fruits, Carrots, Peppers, Eggs, Fish, Spinach, Tomatoes, Berries, Avocado.",
    "Iron-rich Foods": "Prevents anemia and enhances oxygen transport. Examples: Red Meat, Spinach, Pumpkin Seeds, Chickpeas, Tofu, Dark Chocolate, Quinoa.",
    "Calcium-rich Foods": "Strengthens bones and teeth. Examples: Milk, Cheese, Yogurt, Almonds, Sardines, Kale, Fortified Soy Milk.",
    "Protein-rich Foods": "Builds and repairs tissues. Examples: Chicken, Eggs, Lentils, Chickpeas, Tofu, Fish, Greek Yogurt, Nuts.",
    "Healthy Fats": "Supports brain and heart health. Examples: Olive Oil, Avocados, Nuts, Fatty Fish, Dark Chocolate, Chia Seeds.",
    "Hydration & Water-rich Foods": "Keeps the body hydrated and aids metabolism. Examples: Cucumber, Watermelon, Celery, Tomatoes, Oranges, Lettuce, Strawberries.",
    "Probiotic Foods": "Promotes gut health and digestion. Examples: Yogurt, Kimchi, Sauerkraut, Kefir, Miso, Pickles, Kombucha."
}

columns = list(nutrition_info.keys())
half = len(columns) // 2

def create_nutrition_section(parent, title, content):
    frame = tk.Frame(parent, bg="#e3f2fd", padx=20, pady=10)
    frame.pack(fill="x", padx=10, pady=5)
    tk.Label(frame, text=title, font=("Arial", 14, "bold"), bg="#e3f2fd").pack(anchor="w")
    tk.Label(frame, text=content, font=("Arial", 12), bg="#e3f2fd", wraplength=500, justify="left").pack(anchor="w", padx=10)

for i, title in enumerate(columns):
    content = nutrition_info[title]
    if i < half:
        create_nutrition_section(frame_left, title, content)
    else:
        create_nutrition_section(frame_right, title, content)


# Basic Health Guidelines
tk.Label(frame_bottom, text="Basic Health Guidelines", font=("Arial", 18, "bold"), bg="white").pack(pady=10)
guidelines = """1. Stay hydrated with at least 8 glasses of water daily.
2. Eat a balanced diet including proteins, carbs, fats, and fiber.
3. Exercise at least 30 minutes a day.
4. Get 7-9 hours of sleep per night.
5. Reduce processed and sugary foods.
6. Manage stress with relaxation techniques.
7. Maintain a strong gut with probiotic-rich foods.
8. Eat mindfully and avoid overeating.
9. Maintain a healthy weight and BMI.
10. Consult a doctor for personalized diet plans."""
tk.Label(frame_bottom, text=guidelines, font=("Arial", 14), bg="white", wraplength=700, justify="left").pack(pady=5)



# --- Button Hover Effect ---
def on_enter(e):
    e.widget.config(bg=BTN_HOVER)

def on_leave(e):
    e.widget.config(bg=BTN_COLOR)

# --- Navigation Buttons ---
buttons = [
    ("Dashboard", frame_dashboard),
    ("Meal Plan", frame_meal_plan),
    ("Calorie Tracker", frame_calorie_tracker),
    ("Progress", frame_progress),
    ("Food Nutrition", frame_food_nutrition),
]

for idx, (text, frame) in enumerate(buttons):
    btn = tk.Button(nav_bar, text=text, font=FONT, bg=BTN_COLOR, fg="white",
                    activebackground=BTN_HOVER, relief="flat",
                    command=lambda f=frame: show_frame(f))
    btn.pack(side="left", padx=15, pady=10)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Start with Dashboard visible
frame_dashboard.tkraise()

root.update_idletasks()

root.mainloop()
