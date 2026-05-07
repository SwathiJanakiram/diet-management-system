import tkinter as tk
from tkinter import ttk, messagebox
from DietDB import add_user
# BMR Calculation Functions
def calculate_bmr(gender, weight, height, age):
    if gender.lower() == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == "female":
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:
        return False

def adjust_bmr_for_activity(bmr, activity_level):
    activity_factors = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9,
    }
    return bmr * activity_factors.get(activity_level, 1.2)

def calculate_daily_calories(gender, weight, height, age, goal_weight, weeks, activity_level):
    bmr = calculate_bmr(gender, weight, height, age)
    adjusted_bmr = adjust_bmr_for_activity(bmr, activity_level)
    weight_difference = goal_weight - weight    
    total_calorie_change = weight_difference * 7700  
    daily_calorie_change = total_calorie_change / (weeks * 7)  
    return round(adjusted_bmr + daily_calorie_change, 2)

# Macronutrient Breakdown
def calculate_macronutrients(total_calories):
    protein = round(total_calories * 0.3 / 4, 2)
    carbs = round(total_calories * 0.5 / 4, 2)
    fats = round(total_calories * 0.2 / 9, 2)
    fiber = round(total_calories * 0.05 / 4, 2)
    other_nutrients = round(total_calories * 0.05 / 4, 2)
    return carbs, protein, fiber, fats, other_nutrients

# Submit function
def sign_up_submit(name, age, weight, height, goal_weight, goal_time, contact, gender, activity,password):
     weight = float(weight)
     height = float(height)
     age = int(age)
     goal_weight = float(goal_weight)
     goal_time = int(goal_time)
     total_calories = calculate_daily_calories(gender,weight,height,age,goal_weight,goal_time,activity)
     userid=name+contact
     add_user(name, age, weight, height, goal_weight, goal_time, contact, gender, activity,password,userid,total_calories)

