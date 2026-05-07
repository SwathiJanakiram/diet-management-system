import tkinter as tk
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
import re
import subprocess
from signUp import sign_up_submit
from DietDB import check_login

# Function to switch frames
def show_frame(frame):
    frame.tkraise()

# Function to clear all input fields
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_weight.delete(0, tk.END)
    entry_height.delete(0, tk.END)
    entry_goal_weight.delete(0, tk.END)
    entry_goal_time.delete(0, tk.END)
    activity_var.set("")
    gender_var.set("")

# Function to handle form submission
def submit():
    global name, age, weight, height, goal_weight, goal_time, contact, gender, activity
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    weight = entry_weight.get().strip()
    height = entry_height.get().strip()
    goal_weight = entry_goal_weight.get().strip()
    goal_time = entry_goal_time.get().strip()
    contact = entry_contact.get().strip()
    gender = gender_var.get()
    activity = activity_var.get()
    
    
    if not (name and age and weight and height and goal_weight and goal_time and contact and gender and activity):
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
    try:
        weight = float(weight)
        goal_weight = float(goal_weight)
        goal_time = int(goal_time)

        weight_diff = abs(weight - goal_weight)

        max_realistic_loss = goal_time * 1  # Max 1 kg per week
        min_realistic_loss = goal_time * 0.5  # Min 0.5 kg per week

        if weight_diff > max_realistic_loss:
            messagebox.showerror("Unrealistic Goal", 
                f"Losing {weight_diff:.1f} kg in {goal_time} week(s) is unrealistic.\n"
                "Try setting a more achievable goal (0.5–1 kg per week).")
            return
        elif weight_diff < min_realistic_loss and weight > goal_weight:
            messagebox.showinfo("Note", 
                f"Your goal is very mild.\nConsider setting a slightly more effective goal if you aim to lose weight.")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for weight, goal weight, and goal time.")
    show_frame(password_frame)

def is_strong_password(password):
    if (len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'\d', password) and
        re.search(r'[\W_]', password)):  # \W matches special characters
        return True
    return False

# Function to handle password confirmation
def approvePassword():
    password = pwd_entry.get().strip()
    confirm_password = confirmpwd_entry.get().strip()

    if not password:
        messagebox.showerror("Error", "Password cannot be empty!")
        return
    
    if not is_strong_password(password):
        messagebox.showerror("Error", "Password must be at least 8 characters long and include an uppercase letter, lowercase letter, a number, and a special character.")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match!")
        return
    sign_up_submit(name, age, weight, height, goal_weight, goal_time, contact, gender, activity,password)
    show_frame(login_frame)
    messagebox.showinfo("Success", "UserName :!"+name+contact)

def login_check():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    print(username,password)
    if username=="admin" and password=="1234":
        root.destroy()  # Close the current login window
        subprocess.Popen(["python", "admin.py"])
        return 
    if check_login(username, password):
        root.destroy()  # Close the current login window
        subprocess.Popen(["python", "userProfile.py", username])
        return  # Open userProfile.py with user_id as argument
    else:
        messagebox.showerror("Error", "Username or password do not match!")

# Main window
root = tk.Tk()
root.title("Diet Management")
root.state("zoomed")

# --- Load and Resize Background Image ---
try:
    image_path = r"D:\\Diet Management 2.0\\img4.png"
    original_image = Image.open(image_path)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    resized_image = original_image.resize((screen_width, screen_height), Image.LANCZOS)

    bg_image = ImageTk.PhotoImage(resized_image)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
except Exception as e:
    print(f"Image load failed: {e}")
    root.configure(bg="#F0F0F0")

# --- Frames ---
frame_width = 700
frame_height = 600

home_frame = tk.Frame(root, bg="white", bd=5, relief="ridge")
login_frame = tk.Frame(root, bg="white", bd=5, relief="ridge")
signup_frame = tk.Frame(root, bg="white", bd=5, relief="ridge")
password_frame = tk.Frame(root, bg="white", bd=5, relief="ridge")

for frame in (home_frame, login_frame, signup_frame,password_frame):
    frame.place(relx=0.5, rely=0.5, anchor="center", width=frame_width, height=frame_height)

# --- Function to Add Title to Each Frame ---
def add_title_label(frame,action):
    title_label = tk.Label(frame, text="Diet Management System"+action, font=("Arial", 24, "bold"), fg="#2C3E50", bg="white")
    title_label.pack(pady=10)

# --- Home Frame ---
add_title_label(home_frame,"")

button_frame = tk.Frame(home_frame)
button_frame.pack(pady=100)  # Adjust padding to position frame vertically

# Buttons inside the button_frame
login_button = ttk.Button(button_frame, text="Login", width=30, command=lambda: show_frame(login_frame))
signup_button = ttk.Button(button_frame, text="Sign Up", width=30, command=lambda: show_frame(signup_frame))

login_button.pack(pady=10, padx=20)
signup_button.pack(pady=10)

# --- Login Frame ---
add_title_label(login_frame," - Login")

# Username Label and Entry
username_label = ttk.Label(login_frame, text="Username:", font=("Arial", 14))
username_label.pack(pady=(10, 0))
username_entry = ttk.Entry(login_frame, width=40, font=("Arial", 14))
username_entry.pack(pady=5)
username_entry.insert(0, "")

# Password Label and Entry
password_label = ttk.Label(login_frame, text="Password:", font=("Arial", 14))
password_label.pack(pady=(10, 0))
password_entry = ttk.Entry(login_frame, width=40, font=("Arial", 14), show="*")
password_entry.pack(pady=5)
password_entry.insert(0, "")


login_submit = ttk.Button(login_frame, text="Login",command=login_check, width=30)
login_submit.pack(pady=20)

back_button = ttk.Button(login_frame, text="Back", width=30, command=lambda: show_frame(home_frame))
back_button.pack(pady=10)

# --- Sign-Up Frame ---
add_title_label(signup_frame," - Sign Up")

form_frame = ttk.Frame(signup_frame, padding="20", style="Card.TFrame")
form_frame.pack(pady=10, padx=135, fill="both", expand=True)

# Apply styles
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("TLabel", font=("Arial", 12), background="white", foreground="#333")
style.configure("TEntry", font=("Arial", 12), padding=5)
style.configure("TCombobox", font=("Arial", 12))
style.configure("Card.TFrame", background="white")

# Form Fields
ttk.Label(form_frame, text="Full Name:").grid(row=1, column=0, sticky="w", pady=5, padx=10)
entry_name = ttk.Entry(form_frame, width=30)
entry_name.grid(row=1, column=1, pady=5)

ttk.Label(form_frame, text="Age:").grid(row=2, column=0, sticky="w", pady=5, padx=10)
entry_age = ttk.Entry(form_frame, width=30)
entry_age.grid(row=2, column=1, pady=5)

ttk.Label(form_frame, text="Gender:").grid(row=3, column=0, sticky="w", pady=5,padx=10)
gender_var = tk.StringVar()
frame_gender = tk.Frame(form_frame, bg="white")
frame_gender.grid(row=3, column=1, pady=5)
tk.Radiobutton(frame_gender, text="Male", variable=gender_var, value="Male", bg="white").pack(side="left")
tk.Radiobutton(frame_gender, text="Female", variable=gender_var, value="Female", bg="white").pack(side="left")

ttk.Label(form_frame, text="Contact Number:").grid(row=4, column=0, sticky="w", pady=5, padx=10)
entry_contact = ttk.Entry(form_frame, width=30)
entry_contact.grid(row=4, column=1, pady=5)

ttk.Label(form_frame, text="Weight (kg):").grid(row=5, column=0, sticky="w", pady=5, padx=10)
entry_weight = ttk.Entry(form_frame, width=30)
entry_weight.grid(row=5, column=1, pady=5)

ttk.Label(form_frame, text="Height (cm):").grid(row=6, column=0, sticky="w", pady=5, padx=10)
entry_height = ttk.Entry(form_frame, width=30)
entry_height.grid(row=6, column=1, pady=5)

ttk.Label(form_frame, text="Goal Weight (kg):").grid(row=7, column=0, sticky="w", pady=5, padx=10)
entry_goal_weight = ttk.Entry(form_frame, width=30)
entry_goal_weight.grid(row=7, column=1, pady=5)

ttk.Label(form_frame, text="Goal Time (weeks):").grid(row=8, column=0, sticky="w", pady=5, padx=10)
entry_goal_time = ttk.Entry(form_frame, width=30)
entry_goal_time.grid(row=8, column=1, pady=5)

ttk.Label(form_frame, text="Activity Level:").grid(row=9, column=0, sticky="w", pady=5,padx=10)
activity_var = tk.StringVar()
activity_dropdown = ttk.Combobox(form_frame, textvariable=activity_var, values=["Sedentary", "Light", "Moderate", "Active", "Very Active"], width=28)
activity_dropdown.grid(row=9, column=1, pady=5)

frame_buttons = tk.Frame(form_frame, bg="white")
frame_buttons.grid(row=10, column=0, columnspan=2, pady=20)

ttk.Button(frame_buttons, text="Submit", command=submit).pack(side="left", padx=10)
ttk.Button(frame_buttons, text="Clear", command=clear_fields).pack(side="left", padx=10)
ttk.Button(frame_buttons, text="Back", command=lambda: show_frame(home_frame)).pack(side="left", padx=10)

#--- Pasword setting---
add_title_label(password_frame," - Password Set")

# Password Label and Entry
pwd_label = ttk.Label(password_frame, text="Password:", font=("Arial", 14))
pwd_label.pack(pady=(10, 0))
pwd_entry = ttk.Entry(password_frame, width=40, font=("Arial", 14), show="*")
pwd_entry.pack(pady=5)
pwd_entry.insert(0, "")

# Confirm Password Label and Entry
confirmpwd_label = ttk.Label(password_frame, text="Confirm Password:", font=("Arial", 14))
confirmpwd_label.pack(pady=(10, 0))
confirmpwd_entry = ttk.Entry(password_frame, width=40, font=("Arial", 14), show="*")
confirmpwd_entry.pack(pady=5)
confirmpwd_entry.insert(0, "")

login_submit = ttk.Button(password_frame, text="Confrim password",command=approvePassword, width=30)
login_submit.pack(pady=20)

show_frame(home_frame)

root.mainloop()