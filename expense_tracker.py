import tkinter as tk
from tkinter import messagebox
import os

FILE_NAME = "expenses.txt"

def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        return [line.strip().split("|") for line in f.readlines()]

def save_expenses():
    with open(FILE_NAME, "w") as f:
        for exp in expenses:
            f.write("|".join(exp) + "\n")

def refresh_listbox():
    listbox.delete(0, tk.END)
    total = 0.0
    for amount, category, note in expenses:
        listbox.insert(tk.END, f"${amount} | {category} | {note}")
        total += float(amount)
    total_label.config(text=f"Total: ${total:.2f}")

def add_expense():
    amount = amount_entry.get().strip()
    category = category_entry.get().strip()
    note = note_entry.get().strip()

    if not amount or not category:
        messagebox.showwarning("Warning", "Amount and Category are required")
        return

    try:
        float(amount)
    except ValueError:
        messagebox.showwarning("Warning", "Amount must be a number")
        return

    expenses.append([amount, category, note])
    save_expenses()
    refresh_listbox()

    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    note_entry.delete(0, tk.END)

def delete_expense():
    try:
        index = listbox.curselection()[0]
        expenses.pop(index)
        save_expenses()
        refresh_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Select an expense to delete")

# --- GUI Setup ---
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("500x450")
root.resizable(False, False)

expenses = load_expenses()

# --- Input Fields ---
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Amount ($)").grid(row=0, column=0, padx=5)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=0, column=1)

tk.Label(frame, text="Category").grid(row=1, column=0, padx=5)
category_entry = tk.Entry(frame)
category_entry.grid(row=1, column=1)

tk.Label(frame, text="Note").grid(row=2, column=0, padx=5)
note_entry = tk.Entry(frame)
note_entry.grid(row=2, column=1)

add_button = tk.Button(frame, text="Add Expense", width=20, command=add_expense)
add_button.grid(row=3, columnspan=2, pady=10)

# --- Expense List ---
listbox = tk.Listbox(root, width=60, height=10)
listbox.pack(pady=10)

delete_button = tk.Button(root, text="Delete Selected Expense", command=delete_expense)
delete_button.pack()

# --- Total ---
total_label = tk.Label(root, text="Total: $0.00", font=("Arial", 12, "bold"))
total_label.pack(pady=10)

refresh_listbox()
root.mainloop()
