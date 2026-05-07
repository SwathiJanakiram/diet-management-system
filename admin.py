import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def fetch_users():
    conn = sqlite3.connect("diet_management_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    conn.close()
    print("Fetched Users:", users)  # Debugging line
    return users
def on_tree_select(event):
    selected_item = tree.selection()
    if not selected_item:
        return
    user_data = tree.item(selected_item)['values']
    entry_name.delete(0, tk.END)
    entry_name.insert(0, user_data[1])
    entry_age.delete(0, tk.END)
    entry_age.insert(0, user_data[2])
    entry_weight.delete(0, tk.END)
    entry_weight.insert(0, user_data[3])
    entry_height.delete(0, tk.END)
    entry_height.insert(0, user_data[4])
    entry_goal_weight.delete(0, tk.END)
    entry_goal_weight.insert(0, user_data[5])
    entry_goal_time.delete(0, tk.END)
    entry_goal_time.insert(0, user_data[6])
    entry_contact.delete(0, tk.END)
    entry_contact.insert(0, user_data[7])
    gender_var.set(user_data[8])
    activity_var.set(user_data[9])
    entry_password.delete(0, tk.END)
    entry_password.insert(0, user_data[10])
    entry_calories.delete(0, tk.END)
    entry_calories.insert(0, user_data[11])
def validate(name, age, weight, height, goal_weight, goal_time, contact, gender, activity,password,total):
    if not (name and age and weight and height and goal_weight and goal_time and contact and gender and activity and password and total):
        messagebox.showerror("Error", "All fields are required!")
        return
    
    if not age.isdigit() or int(age) <= 0:
        messagebox.showerror("Error", "Age must be a positive number!")
        return
    
    if not weight.isdigit() or int(weight) <= 0 or int(weight) > 300:
        messagebox.showerror("Error", "Enter a realistic weight (1-300 kg)!")
        return
    
    if not height.isdigit() or int(height) <= 50 or int(height) > 250:
        messagebox.showerror("Error", "Enter a realistic height (50-250 cm)!")
        return
    
    if not goal_weight.isdigit() or int(goal_weight) < 0 or int(goal_weight) > 300:
        messagebox.showerror("Error", "Goal weight must be between 0-300 kg!")
        return
    
    if not goal_time.isdigit() or int(goal_time) < 0:
        messagebox.showerror("Error", "Goal time must be a positive number or zero!")
        return
    
    if not (contact.isdigit() and len(contact) == 10):
        messagebox.showerror("Error", "Contact number must be exactly 10 digits!")
        return
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_weight.delete(0, tk.END)
    entry_height.delete(0, tk.END)
    entry_goal_weight.delete(0, tk.END)
    entry_goal_time.delete(0, tk.END)
    activity_var.set("")
    gender_var.set("")
def add_user():
    name = entry_name.get()
    age = entry_age.get()
    weight = entry_weight.get()
    height = entry_height.get()
    goal_weight = entry_goal_weight.get()
    goal_time = entry_goal_time.get()
    contact = entry_contact.get()
    gender = gender_var.get()
    activity = activity_var.get()
    password = entry_password.get()
    total_calories = entry_calories.get()
    validate(name, age, weight, height, goal_weight, goal_time, contact, gender, activity,password,total_calories)
    try:
        weight = float(weight)
        height = float(height)
        age = int(age)
        goal_weight = float(goal_weight)
        goal_time = int(goal_time)
        total_calories=float(total_calories)
        conn = sqlite3.connect("diet_management_system.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Users (name, age, weight, height, goal_weight, goal_time, contact, gender, activity, password, total_calories)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, weight, height, goal_weight, goal_time, contact, gender, activity, password, total_calories))
        conn.commit()
        conn.close()
        refresh_users()
        messagebox.showinfo("Success", "User added successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Contact must be unique!")

def delete_user():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a user to delete!")
        return
    user_id = tree.item(selected_item)['values'][0]
    conn = sqlite3.connect("diet_management_system.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Users WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
    refresh_users()
    clear_fields()
    messagebox.showinfo("Success", "User deleted successfully!")

def update_user():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a user to update!")
        return
    user_id = tree.item(selected_item)['values'][0]
    name = entry_name.get()
    age = entry_age.get()
    weight = entry_weight.get()
    height = entry_height.get()
    goal_weight = entry_goal_weight.get()
    goal_time = entry_goal_time.get()
    contact = entry_contact.get()
    gender = gender_var.get()
    activity = activity_var.get()
    password = entry_password.get()
    total_calories = entry_calories.get()
    conn = sqlite3.connect("diet_management_system.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Users SET name=?, age=?, weight=?, height=?, goal_weight=?, goal_time=?, contact=?, gender=?, activity=?, password=?, total_calories=?
        WHERE user_id=?
    ''', (name, age, weight, height, goal_weight, goal_time, contact, gender, activity, password, total_calories, user_id))
    conn.commit()
    conn.close()
    refresh_users()
    messagebox.showinfo("Success", "User updated successfully!")

def refresh_users():
    for row in tree.get_children():
        tree.delete(row)
    for user in fetch_users():
        tree.insert("", "end", values=user)

def show_frame(frame):
    frame.tkraise()

root = tk.Tk()
root.title("Admin Panel")
root.geometry("1000x600")
root.configure(bg="#f0f0f0")

main_container = tk.Frame(root, bg="#ffffff", padx=10, pady=10)
main_container.pack(fill="both", expand=True)

nav_frame = tk.Frame(main_container, width=220, bg="#2c3e50")
nav_frame.pack(side="left", fill="y")

tk.Label(nav_frame, text="Admin Panel", fg="#ecf0f1", bg="#2c3e50", font=("Arial", 18, "bold")).pack(pady=20)

nav_buttons = [
    ("User Management", lambda: show_frame(frame_users))
]

for text, command in nav_buttons:
    tk.Button(nav_frame, text=text, command=command, width=20, pady=10, bg="#34495e", fg="#ecf0f1", font=("Arial", 12), relief="flat").pack(pady=5)

content_frame = tk.Frame(main_container, bg="#ecf0f1")
content_frame.pack(side="right", fill="both", expand=True)

frame_users = tk.Frame(content_frame, bg="#ffffff", padx=20, pady=20)
frame_users.grid(row=0, column=0, sticky="nsew")
tk.Label(frame_users, text="User Management", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=10)

tree = ttk.Treeview(frame_users, columns=("ID", "Name", "Age", "Weight", "Height", "Goal Weight", "Goal Time", "Contact", "Gender", "Activity", "Calories"), show="headings")
for col in ("ID", "Name", "Age", "Weight", "Height", "Goal Weight", "Goal Time", "Contact", "Gender", "Activity", "Calories"):
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")
tree.pack(fill="both", expand=True, padx=10, pady=10)
tree.bind("<ButtonRelease-1>", on_tree_select)
refresh_users()
entry_frame = tk.Frame(frame_users, bg="#ffffff")
entry_frame.pack(pady=10, fill="x")
labels = ["Name", "Age", "Weight", "Height", "Goal Weight", "Goal Time", "Contact", "Gender", "Activity", "Password", "Calories"]
entries = {}

for label in labels:
    row = tk.Frame(entry_frame, bg="#ffffff")
    row.pack(fill="x", pady=2)
    tk.Label(row, text=label, bg="#ffffff", width=15, anchor="w").pack(side="left")
    if label in ["Gender", "Activity"]:
        var = tk.StringVar()
        combobox = ttk.Combobox(row, textvariable=var, values=["Male", "Female", "Other"] if label == "Gender" else ["Sedentary", "Lightly active", "Moderately active", "Very active"])
        combobox.pack(side="right", fill="x", expand=True)
        entries[label] = var
    else:
        entry = tk.Entry(row, width=40)
        entry.pack(side="right", fill="x", expand=True)
        entries[label] = entry

entry_name, entry_age, entry_weight, entry_height, entry_goal_weight, entry_goal_time, entry_contact, gender_var, activity_var, entry_password, entry_calories = (
    entries["Name"], entries["Age"], entries["Weight"], entries["Height"],
    entries["Goal Weight"], entries["Goal Time"], entries["Contact"],
    entries["Gender"], entries["Activity"], entries["Password"], entries["Calories"]
)
tk.Button(frame_users, text="Add", command=add_user, bg="#27ae60", fg="white").pack(side="left", padx=5)
tk.Button(frame_users, text="Delete", command=delete_user, bg="#c0392b", fg="white").pack(side="left", padx=5)
tk.Button(frame_users, text="Update", command=update_user, bg="#f39c12", fg="white").pack(side="left", padx=5)

show_frame(frame_users)
root.mainloop()
