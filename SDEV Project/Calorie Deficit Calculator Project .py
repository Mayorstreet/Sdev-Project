import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk

# Activity level multipliers
activity_levels = {
    "Sedentary (little to no exercise)": 1.2,
    "Lightly Active (1-3 days per week)": 1.375,
    "Moderately Active (3-5 days per week)": 1.55,
    "Very Active (6-7 days per week)": 1.725,
    "Super Active (athlete level)": 1.9
}

# Convert height from feet/inches to cm
def convert_height(feet, inches):
    return (feet * 12 + inches) * 2.54  # Convert total inches to cm

# Convert weight from pounds to kg
def convert_weight(pounds):
    return pounds * 0.453592  # Convert lbs to kg

# Function to calculate TDEE, deficits, and surpluses
def calculate_tdee():
    try:
        weight_lbs = float(weight_entry.get())
        feet = int(feet_entry.get())
        inches = int(inches_entry.get())
        age = int(age_entry.get())
        gender = gender_var.get()
        activity_multiplier = activity_levels[activity_var.get()]

        weight_kg = convert_weight(weight_lbs)
        height_cm = convert_height(feet, inches)

        # Mifflin-St Jeor Equation
        if gender == "Male":
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

        tdee = bmr * activity_multiplier

        # Deficit for weight loss
        deficits = {
            "Lose 0.5 lb/week": tdee - 250,
            "Lose 1 lb/week": tdee - 500,
            "Lose 1.5 lb/week": tdee - 750,
            "Lose 2 lb/week": tdee - 1000
        }

        # Surplus for weight gain
        surpluses = {
            "Gain 0.5 lb/week": tdee + 250,
            "Gain 1 lb/week": tdee + 500,
            "Gain 1.5 lb/week": tdee + 750,
            "Gain 2 lb/week": tdee + 1000
        }

        display_results(tdee, deficits, surpluses)

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# Function to display results in a second window
def display_results(tdee, deficits, surpluses):
    result_window = Toplevel(root)
    result_window.title("Calorie Calculator Results")
    result_window.geometry("400x400")
    result_window.configure(bg="#ADD8E6")

    tk.Label(result_window, text=f"Your TDEE: {int(tdee)} cal/day", font=("Arial", 12), bg="#ADD8E6").pack(pady=10)

    # Display weight loss deficits
    tk.Label(result_window, text="Caloric Intake for Weight Loss:", font=("Arial", 10, "bold"), bg="#ADD8E6").pack()
    for rate, cals in deficits.items():
        tk.Label(result_window, text=f"{rate}: {int(cals)} cal/day", font=("Arial", 10), bg="#ADD8E6").pack()

    # Spacer
    tk.Label(result_window, text="", bg="#ADD8E6").pack()

    # Display weight gain surpluses
    tk.Label(result_window, text="Caloric Intake for Weight Gain:", font=("Arial", 10, "bold"), bg="#ADD8E6").pack()
    for rate, cals in surpluses.items():
        tk.Label(result_window, text=f"{rate}: {int(cals)} cal/day", font=("Arial", 10), bg="#ADD8E6").pack()

    tk.Button(result_window, text="Close", command=result_window.destroy).pack(pady=10)

# Function to exit application
def exit_app():
    root.quit()

# Main GUI Window
root = tk.Tk()
root.title("Calorie Calculator")
root.geometry("500x600")
root.configure(bg="#ADD8E6")

# Center frame to hold all widgets
frame = tk.Frame(root, bg="#ADD8E6")
frame.pack(expand=True)

# Load images
scale_img = Image.open("weight scale.png").resize((100, 100))
scale_photo = ImageTk.PhotoImage(scale_img)

activity_img = Image.open("activity_levels.png").resize((100, 100))
activity_photo = ImageTk.PhotoImage(activity_img)

# Labels
tk.Label(frame, text="Calorie Calculator", font=("Arial", 14), bg="#ADD8E6").pack(pady=5)
tk.Label(frame, image=scale_photo, text="Track Your Calories", compound="top", bg="#ADD8E6").pack()

tk.Label(frame, text="Enter Your Weight (lbs):", font=("Arial", 12), bg="#ADD8E6").pack()
weight_entry = tk.Entry(frame)
weight_entry.pack()

tk.Label(frame, text="Enter Your Height:", font=("Arial", 12), bg="#ADD8E6").pack()
height_frame = tk.Frame(frame, bg="#ADD8E6")
height_frame.pack()

feet_entry = tk.Entry(height_frame, width=5)
feet_entry.pack(side=tk.LEFT, padx=5)
tk.Label(height_frame, text="feet", bg="#ADD8E6").pack(side=tk.LEFT)

inches_entry = tk.Entry(height_frame, width=5)
inches_entry.pack(side=tk.LEFT, padx=5)
tk.Label(height_frame, text="inches", bg="#ADD8E6").pack(side=tk.LEFT)

tk.Label(frame, text="Enter Your Age:", font=("Arial", 12), bg="#ADD8E6").pack()
age_entry = tk.Entry(frame)
age_entry.pack()

tk.Label(frame, text="Select Gender:", font=("Arial", 12), bg="#ADD8E6").pack()
gender_var = tk.StringVar(value="Male")
tk.OptionMenu(frame, gender_var, "Male", "Female").pack()

tk.Label(frame, text="Select Activity Level:", font=("Arial", 12), bg="#ADD8E6").pack()
activity_var = tk.StringVar(value="Sedentary (little to no exercise)")
tk.OptionMenu(frame, activity_var, *activity_levels.keys()).pack()

# Buttons
tk.Button(frame, text="Calculate Calories", command=calculate_tdee).pack(pady=10)
tk.Button(frame, text="Exit", command=exit_app).pack(pady=5)

# Activity image
tk.Label(frame, image=activity_photo, text="Activity Levels", compound="top", bg="#ADD8E6").pack(pady=10)

# Run the application
root.mainloop()
