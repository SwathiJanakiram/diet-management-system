import sqlite3
import tkinter as tk
from tkinter import ttk

# Function to fetch meal plan and food details
def fetch_meal_details(meal_day):
    conn = sqlite3.connect("diet_management_system.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT M.breakfast, M.morning_snack, M.lunch, M.evening_snack, M.dinner
        FROM Meal M WHERE M.meal_day = ?
    ''', (meal_day,))
    meal_ids = cursor.fetchone()

    if not meal_ids:
        conn.close()
        return []

    food_details = []
    for idx, food_id in enumerate(meal_ids):
        if food_id:
            cursor.execute('''
                SELECT name, measurement, calories, protein, carbs, fiber, calcium, key_ingredients
                FROM Food WHERE food_id = ?
            ''', (food_id,))
            food_details.append((idx, cursor.fetchone()))

    conn.close()
    return food_details

# Function to display meal details
def display_meal_details(event):
    selected_item = tree.focus()
    if not selected_item:
        return

    meal_day = tree.item(selected_item, 'values')[0]
    meal_details = fetch_meal_details(meal_day)

    # Clear previous details
    for widget in details_top_frame.winfo_children():
        widget.destroy()
    for widget in nutrition_frame.winfo_children():
        widget.destroy()

    if not meal_details:
        return

    tk.Label(details_top_frame, text=f"Meal Details for {meal_day}", font=("Arial", 16, "bold", "underline"), bg="#f2f2f2", fg="#333").pack(anchor="w", pady=(10, 5))

    # Meal Time and Food Item Treeview
    columns = ("Meal Time", "Food Item")
    meal_tree = ttk.Treeview(details_top_frame, columns=columns, show='headings', height=5, style="Details.Treeview")
    meal_tree.heading("Meal Time", text="Meal Time")
    meal_tree.heading("Food Item", text="Food Item")
    meal_tree.column("Meal Time", anchor="center", width=150)
    meal_tree.column("Food Item", anchor="w", width=300)
    meal_tree.pack(fill="both", expand=True, pady=(5, 10))

    # Add meal details to treeview
    for meal_idx, meal_data in meal_details:
        if meal_data:
            name, measurement, calories, protein, carbs, fiber, calcium, key_ingredients = meal_data
            meal_tree.insert("", tk.END, values=(['Breakfast', 'Morning Snack', 'Lunch', 'Evening Snack', 'Dinner'][meal_idx], name))

    # Section for detailed nutritional info
    tk.Label(nutrition_frame, text="Nutritional Information:", font=("Arial", 14, "bold"), bg="#f2f2f2", fg="#333").pack(anchor='w', pady=(10, 5))
    for meal_idx, meal_data in meal_details:
        if meal_data:
            name, measurement, calories, protein, carbs, fiber, calcium, key_ingredients = meal_data
            meal_label = tk.Label(nutrition_frame, text=f"{['Breakfast', 'Morning Snack', 'Lunch', 'Evening Snack', 'Dinner'][meal_idx]}: {name} ({measurement})", font=("Arial", 12, "bold"), bg="#f2f2f2", fg="#555")
            meal_label.pack(anchor='w', pady=(5, 2))

            details_text = f"Calories: {calories} kcal | Protein: {protein}g | Carbs: {carbs}g | Fiber: {fiber}g | Calcium: {calcium}mg\nIngredients: {key_ingredients}"
            detail_label = tk.Label(nutrition_frame, text=details_text, font=("Arial", 10), justify='left', wraplength=600, bg="#f2f2f2", fg="#777")
            detail_label.pack(anchor='w', pady=(2, 5))


# Initialize main window
root = tk.Tk()
root.title("Meal Plan Management")
root.state("zoomed")
root.configure(bg="#e0f7fa")  # Light blue background for the main window

# Modern styling
style = ttk.Style()

# Configure the main Treeview style
style.configure("Treeview", font=("Segoe UI", 11), rowheight=35, background="#f9f9f9", fieldbackground="#f9f9f9", borderwidth=1, relief="solid")
style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"), background="##80deea", foreground="white", padding=(5, 5))
style.map("Treeview", background=[("selected", "#b2ebf2")])

# Configure the details Treeview style
style.configure("Details.Treeview", font=("Calibri", 10), rowheight=25, background="#ffffff", fieldbackground="#ffffff", borderwidth=1, relief="solid")
style.configure("Details.Treeview.Heading", font=("Calibri", 11, "bold"), background="#80deea", foreground="white", padding=(3, 3))
style.map("Details.Treeview", background=[("selected", "#80deea")])

# Style for labels
label_font = ("Arial", 11)
root.option_add("*Label.Font", label_font)

# Main frame
main_frame = tk.Frame(root, bg="#e0f7fa", padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# Treeview frame (left side)
tree_frame = tk.Frame(main_frame, bg="#e0f7fa")
tree_frame.pack(side="left", fill="y", padx=(0, 20))

# Treeview widget
tree = ttk.Treeview(tree_frame, columns=("Day",), show="headings", height=10, style="Treeview")
tree.heading("Day", text="Meal Plan Day")
tree.column("Day", anchor="center", width=180)

# Adding data to Treeview
conn = sqlite3.connect("diet_management_system.db")
cursor = conn.cursor()
cursor.execute("SELECT meal_day FROM Meal")
meal_days = cursor.fetchall()
conn.close()

for meal in meal_days:
    tree.insert("", "end", values=meal)

tree.bind("<ButtonRelease-1>", display_meal_details)
tree.pack(fill="y", expand=True)

# Scrollbar for the treeview
tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview, style="TScrollbar")
tree.configure(yscrollcommand=tree_scrollbar.set)
tree_scrollbar.pack(side="right", fill="y")

# Details frame (right side)
details_frame = tk.Frame(main_frame, bg="#f2f2f2", padx=15, pady=15, borderwidth=2, relief="groove")
details_frame.pack(side="right", fill="both", expand=True)

# Top part of the details frame
details_top_frame = tk.Frame(details_frame, bg="#f2f2f2")
details_top_frame.pack(fill="x")

# Separator
separator = ttk.Separator(details_frame, orient="horizontal")
separator.pack(fill="x", pady=10)

# Bottom part of the details frame
nutrition_canvas = tk.Canvas(details_frame, bg="#f2f2f2", highlightthickness=0)
nutrition_canvas.pack(side="left", fill="both", expand=True)

nutrition_scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=nutrition_canvas.yview, style="TScrollbar")
nutrition_scrollbar.pack(side="right", fill="y")

nutrition_canvas.configure(yscrollcommand=nutrition_scrollbar.set)
nutrition_canvas.bind('<Configure>', lambda e: nutrition_canvas.configure(scrollregion = nutrition_canvas.bbox("all")))

nutrition_frame = tk.Frame(nutrition_canvas, bg="#f2f2f2", padx=10, pady=10)
nutrition_canvas.create_window((0, 0), window=nutrition_frame, anchor="nw")

# Custom scrollbar style (optional)
style.configure("TScrollbar", background="#80cbc4", arrowcolor="#4db6ac")
style.map("TScrollbar", background=[("active", "#4db6ac"), ("!active", "#80cbc4")])

root.mainloop()