import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt


# ---------------- LOAD DATA ----------------

try:
    data = pd.read_csv("food_data.csv")
except:
    messagebox.showerror("Error", "CSV not found")
    exit()


history = []
model = None
cal_per_100g = 0


# ---------------- TRAIN MODEL ----------------

def train_model(cal):
    X = np.array([[10], [50], [100], [200], [300]])
    y = (cal * X) / 100

    m = LinearRegression().fit(X, y)

    return m


# ---------------- PREDICT CALORIES ----------------

def predict():
    global model, cal_per_100g

    try:
        food = food_var.get()
        grams = float(grams_var.get())

        row = data[data["Food"] == food]

        if row.empty or grams <= 0:
            raise ValueError

        cal_per_100g = float(
            row["Calories_per_100g"].values[0]
        )

        model = train_model(cal_per_100g)

        formula = (cal_per_100g * grams) / 100

        ml = model.predict([[grams]])[0][0]

        result_label.config(
            text=f"{ml:.2f} kcal"
        )

        detail_label.config(
            text=f"Formula: ({cal_per_100g} × {grams}) / 100 = {formula:.2f}"
        )

        history.append({
            "Food": food,
            "Grams": grams,
            "Calories": ml
        })

        update_table()

    except:
        messagebox.showerror(
            "Error",
            "Invalid input"
        )


# ---------------- UPDATE HISTORY TABLE ----------------

def update_table():

    tree.delete(*tree.get_children())

    for item in history[-5:]:

        tree.insert(
            "",
            "end",
            values=(
                item["Food"],
                item["Grams"],
                f"{item['Calories']:.1f}"
            )
        )


# ---------------- BAR CHART ----------------

def show_bar():

    if not history:
        messagebox.showinfo(
            "Info",
            "Please make at least one prediction."
        )
        return

    foods = [i["Food"] for i in history]
    cals = [i["Calories"] for i in history]

    plt.figure(figsize=(8, 5))

    plt.bar(foods, cals)

    plt.xlabel("Food")
    plt.ylabel("Calories (kcal)")
    plt.title("Food Calorie Comparison")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


# ---------------- PIE CHART ----------------

def show_pie():

    if not history:
        messagebox.showinfo(
            "Info",
            "Please make at least one prediction."
        )
        return

    foods = [i["Food"] for i in history]
    cals = [i["Calories"] for i in history]

    plt.figure(figsize=(7, 7))

    plt.pie(
        cals,
        labels=foods,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Calorie Contribution by Food")

    plt.tight_layout()
    plt.show()


# ---------------- LINE CHART ----------------

def show_line():

    if not history:
        messagebox.showinfo(
            "Info",
            "Please make at least one prediction."
        )
        return

    grams = [i["Grams"] for i in history]
    cals = [i["Calories"] for i in history]

    plt.figure(figsize=(8, 5))

    plt.plot(
        grams,
        cals,
        marker="o"
    )

    plt.xlabel("Food Quantity (grams)")
    plt.ylabel("Calories (kcal)")
    plt.title("Food Quantity vs Calories")

    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ---------------- SCATTER PLOT ----------------

def show_scatter():

    if not history:
        messagebox.showinfo(
            "Info",
            "Please make at least one prediction."
        )
        return

    grams = [i["Grams"] for i in history]
    cals = [i["Calories"] for i in history]

    plt.figure(figsize=(8, 5))

    plt.scatter(
        grams,
        cals,
        s=80
    )

    plt.xlabel("Food Quantity (grams)")
    plt.ylabel("Calories (kcal)")
    plt.title("Grams vs Calories")

    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ---------------- GUI ----------------

root = tk.Tk()

root.title("Food Calorie Predictor")

root.geometry("500x650")


# Food selection

tk.Label(
    root,
    text="Select Food"
).pack(pady=5)


food_var = tk.StringVar(
    value=data["Food"].iloc[0]
)


food_box = ttk.Combobox(
    root,
    textvariable=food_var,
    values=list(data["Food"]),
    state="readonly"
)

food_box.pack(pady=5)


# Grams input

tk.Label(
    root,
    text="Enter Quantity (grams)"
).pack(pady=5)


grams_var = tk.StringVar(
    value="100"
)


tk.Entry(
    root,
    textvariable=grams_var
).pack(pady=5)


# Predict button

tk.Button(
    root,
    text="Predict",
    command=predict
).pack(pady=10)


# Result

result_label = tk.Label(
    root,
    text="0 kcal",
    font=("Arial", 16, "bold")
)

result_label.pack(pady=5)


# Formula

detail_label = tk.Label(
    root,
    text="Formula: 0"
)

detail_label.pack(pady=5)


# ---------------- HISTORY TABLE ----------------

tk.Label(
    root,
    text="Prediction History",
    font=("Arial", 12, "bold")
).pack(pady=10)


tree = ttk.Treeview(
    root,
    columns=("Food", "Grams", "Calories"),
    show="headings",
    height=5
)


for col in ("Food", "Grams", "Calories"):

    tree.heading(
        col,
        text=col
    )


tree.pack(pady=5)


# ---------------- CHART BUTTONS ----------------

tk.Label(
    root,
    text="Visualizations",
    font=("Arial", 12, "bold")
).pack(pady=10)


tk.Button(
    root,
    text="Bar Chart",
    command=show_bar
).pack(pady=3)


tk.Button(
    root,
    text="Pie Chart",
    command=show_pie
).pack(pady=3)


tk.Button(
    root,
    text="Line Chart",
    command=show_line
).pack(pady=3)


tk.Button(
    root,
    text="Scatter Plot",
    command=show_scatter
).pack(pady=3)


# ---------------- RUN APPLICATION ----------------

root.mainloop()