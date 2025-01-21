import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

# File to store the budget data
DATA_FILE = "budget_data.csv"
DEFAULT_CATEGORIES = [
    "Groceries", "Online Orders", "Restaurants & Coffee Shops",
    "Electronics", "Subscriptions", "Rent", "Internet",
    "Cell Phone", "Total"
]

# Check if data file exists, create if not
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Category", "Amount"])
    df.to_csv(DATA_FILE, index=False)

# BudgetTrackerApp class
class BudgetTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("800x600")

        # Load data
        self.data = pd.read_csv(DATA_FILE, parse_dates=["Date"])
        self.categories = list(DEFAULT_CATEGORIES)

        # Build GUI
        self.build_gui()

    def build_gui(self):
        # Title
        title = tk.Label(self.root, text="Budget Tracker", font=("Arial", 20, "bold"))
        title.pack(pady=10)

        # Add expense frame
        add_frame = tk.LabelFrame(self.root, text="Add Expense", padx=10, pady=10)
        add_frame.pack(pady=10, fill="x")

        tk.Label(add_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.category_var = tk.StringVar(value=self.categories[0])
        self.category_menu = ttk.Combobox(add_frame, textvariable=self.category_var, values=self.categories, state="readonly")
        self.category_menu.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_frame, text="Amount:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.amount_entry = tk.Entry(add_frame)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(add_frame, text="Add Expense", command=self.add_expense).grid(row=0, column=4, padx=5, pady=5)

        # Add new category frame
        category_frame = tk.LabelFrame(self.root, text="Add New Category", padx=10, pady=10)
        category_frame.pack(pady=10, fill="x")

        tk.Label(category_frame, text="Category Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.new_category_entry = tk.Entry(category_frame)
        self.new_category_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(category_frame, text="Add Category", command=self.add_category).grid(row=0, column=2, padx=5, pady=5)

        # View expenses frame
        view_frame = tk.LabelFrame(self.root, text="View Expenses", padx=10, pady=10)
        view_frame.pack(pady=10, fill="x")

        tk.Button(view_frame, text="View Weekly Expenses", command=self.view_weekly).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(view_frame, text="View Monthly Expenses", command=self.view_monthly).grid(row=0, column=1, padx=5, pady=5)

        # Exit button
        tk.Button(self.root, text="Exit", command=self.root.quit, bg="red", fg="white").pack(pady=10)

    def add_expense(self):
        try:
            category = self.category_var.get()
            amount = float(self.amount_entry.get())
            date = datetime.now()

            new_entry = {"Date": date, "Category": category, "Amount": amount}
            self.data = pd.concat([self.data, pd.DataFrame([new_entry])])
            self.data.to_csv(DATA_FILE, index=False)

            messagebox.showinfo("Success", "Expense added successfully!")
            self.amount_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")

    def add_category(self):
        new_category = self.new_category_entry.get().strip()
        if new_category and new_category not in self.categories:
            self.categories.append(new_category)
            self.category_menu["values"] = self.categories
            messagebox.showinfo("Success", f"Category '{new_category}' added successfully!")
            self.new_category_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid or duplicate category name!")

    def view_weekly(self):
        self.show_expenses("weekly")

    def view_monthly(self):
        self.show_expenses("monthly")

    def show_expenses(self, period):
        if period == "weekly":
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            title = f"Weekly Expenses ({start_date.strftime('%m/%d/%Y')} - {end_date.strftime('%m/%d/%Y')})"
        else:  # monthly
            end_date = datetime.now()
            start_date = end_date.replace(day=1)  # Start of the current month
            title = f"Monthly Expenses ({start_date.strftime('%m/%Y')})"

        # Filter data for the specified date range
        filtered_data = self.data[(self.data["Date"] >= start_date) & (self.data["Date"] <= end_date)]
        summary = filtered_data.groupby("Category")["Amount"].sum()

        # Add total expenses as a new bar
        total_expenses = summary.sum()
        summary["Total"] = total_expenses

        self.plot_expenses(title, summary)

    def plot_expenses(self, title, summary):
        # Create a bar plot of expenses with total included
        plt.figure(figsize=(10, 6))
        colors = sns.color_palette("tab10", len(summary))
        bars = summary.plot(kind="bar", color=colors, edgecolor="black")

        plt.title(title, fontsize=16)
        plt.ylabel("Amount ($)", fontsize=12)
        plt.xlabel("Category", fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.tight_layout()

        # Add numerical labels on top of each bar
        for i, value in enumerate(summary):
            plt.text(i, value + (value * 0.01), f"${value:.2f}", ha='center', va='bottom', fontsize=10)

        plt.show()



if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()
