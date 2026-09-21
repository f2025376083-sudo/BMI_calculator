import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt


DB_NAME = "bmi_records.db"


def init_database():
    """Create the BMI database/table if they do not already exist."""
    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    category TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()
    except sqlite3.Error as error:
        messagebox.showerror("Database Error", f"Could not initialize database:\n{error}")


def get_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def calculate_bmi():
    username = name_entry.get().strip()

    if not username:
        messagebox.showwarning("Input Error", "Please enter a user name.")
        return

    try:
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())

        if weight <= 0 or height_cm <= 0:
            raise ValueError

        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)
        category = get_category(bmi)

        result_label.config(
            text=f"BMI: {bmi:.2f}\nCategory: {category}",
            foreground="green" if category == "Normal" else "red"
        )

        try:
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute("""
                    INSERT INTO bmi_records
                    (username, weight, height, bmi, category, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    username, weight, height_cm, bmi, category,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"BMI calculated, but the record could not be saved:\n{error}"
            )

    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Enter positive numbers for weight and height."
        )


def show_history():
    username = name_entry.get().strip()

    if not username:
        messagebox.showwarning("Input Error", "Please enter a user name.")
        return

    try:
        with sqlite3.connect(DB_NAME) as conn:
            rows = conn.execute("""
                SELECT created_at, weight, height, bmi, category
                FROM bmi_records
                WHERE username = ?
                ORDER BY id DESC
            """, (username,)).fetchall()

        history_window = tk.Toplevel(root)
        history_window.title(f"BMI History - {username}")
        history_window.geometry("760x400")

        columns = ("date", "weight", "height", "bmi", "category")
        tree = ttk.Treeview(history_window, columns=columns, show="headings")

        headings = {
            "date": "Date",
            "weight": "Weight (kg)",
            "height": "Height (cm)",
            "bmi": "BMI",
            "category": "Category"
        }

        for col in columns:
            tree.heading(col, text=headings[col])
            tree.column(col, width=130, anchor="center")

        for row in rows:
            tree.insert("", tk.END, values=(
                row[0], f"{row[1]:.2f}", f"{row[2]:.2f}",
                f"{row[3]:.2f}", row[4]
            ))

        tree.pack(fill="both", expand=True, padx=10, pady=10)

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", f"Could not read history:\n{error}")


def show_graph():
    username = name_entry.get().strip()

    if not username:
        messagebox.showwarning("Input Error", "Please enter a user name.")
        return

    try:
        with sqlite3.connect(DB_NAME) as conn:
            rows = conn.execute("""
                SELECT created_at, bmi
                FROM bmi_records
                WHERE username = ?
                ORDER BY id
            """, (username,)).fetchall()

        if not rows:
            messagebox.showinfo(
                "No Data",
                "No BMI records found for this user."
            )
            return

        dates = [row[0] for row in rows]
        bmis = [row[1] for row in rows]

        plt.figure(figsize=(9, 5))
        plt.plot(range(1, len(bmis) + 1), bmis, marker="o")
        plt.axhline(18.5, linestyle="--", label="18.5")
        plt.axhline(25, linestyle="--", label="25")
        plt.axhline(30, linestyle="--", label="30")
        plt.title(f"BMI Trend - {username}")
        plt.xlabel("Record Number")
        plt.ylabel("BMI")
        plt.xticks(range(1, len(bmis) + 1), range(1, len(bmis) + 1))
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    except sqlite3.Error as error:
        messagebox.showerror("Database Error", f"Could not read graph data:\n{error}")
    except Exception as error:
        messagebox.showerror("Graph Error", f"Could not display graph:\n{error}")


def clear_fields():
    name_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_label.config(text="BMI: --\nCategory: --", foreground="black")


# ---------------- GUI ----------------
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("500x560")
root.resizable(False, False)

init_database()

title = tk.Label(
    root,
    text="BMI Calculator",
    font=("Arial", 24, "bold")
)
title.pack(pady=20)

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(frame, text="User Name:", font=("Arial", 12)).grid(
    row=0, column=0, padx=10, pady=10, sticky="e"
)
name_entry = tk.Entry(frame, width=25, font=("Arial", 12))
name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame, text="Weight (kg):", font=("Arial", 12)).grid(
    row=1, column=0, padx=10, pady=10, sticky="e"
)
weight_entry = tk.Entry(frame, width=25, font=("Arial", 12))
weight_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(frame, text="Height (cm):", font=("Arial", 12)).grid(
    row=2, column=0, padx=10, pady=10, sticky="e"
)
height_entry = tk.Entry(frame, width=25, font=("Arial", 12))
height_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Button(
    root, text="Calculate BMI", command=calculate_bmi,
    width=20, font=("Arial", 12, "bold")
).pack(pady=15)

result_label = tk.Label(
    root, text="BMI: --\nCategory: --",
    font=("Arial", 17, "bold")
)
result_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=15)

tk.Button(
    button_frame, text="View History", command=show_history,
    width=15
).grid(row=0, column=0, padx=5, pady=5)

tk.Button(
    button_frame, text="Show Graph", command=show_graph,
    width=15
).grid(row=0, column=1, padx=5, pady=5)

tk.Button(
    button_frame, text="Clear", command=clear_fields,
    width=15
).grid(row=1, column=0, columnspan=2, pady=5)

info = tk.Label(
    root,
    text="Underweight < 18.5   |   Normal 18.5–24.9\n"
         "Overweight 25–29.9   |   Obese ≥ 30",
    font=("Arial", 10)
)
info.pack(pady=15)

root.mainloop()
