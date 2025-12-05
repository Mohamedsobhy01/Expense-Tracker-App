import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

expenses = []

CURRENCIES = ["USD", "EGP", "EUR", "SAR"]
CATEGORIES = ["Education", "Savings", "Grocery", "Rental", "Gas", "Electricity", "Life Expenses", "Charity"]
PAYMENT_METHODS = ["Paypal", "Cash", "Credit Card"]

def convert_to_usd(amount, currency):
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url)
        data = response.json()
        rate = data["rates"].get(currency)
        if rate is None:
            return None
        return round(amount / rate, 2)
    except Exception as e:
        messagebox.showerror("Error", f"Currency conversion failed!\n{e}")
        return None

def update_total():
    total = sum(exp[-1] for exp in expenses)
    total_label.config(text=f"Total USD: ${total:.2f}")

def clear_inputs():
    amount_entry.delete(0, tk.END)
    currency_box.current(0)
    category_box.current(0)
    payment_box.current(0)
    date_entry.delete(0, tk.END)
    date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))

def add_expense():
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            messagebox.showwarning("Invalid Input", "Amount must be greater than 0!")
            return
    except ValueError:
        messagebox.showwarning("Invalid Input", "Amount must be a number!")
        return

    currency = currency_box.get()
    category = category_box.get()
    payment = payment_box.get()
    date_val = date_entry.get()

    usd_value = convert_to_usd(amount, currency)
    if usd_value is None:
        messagebox.showerror("Error", "Invalid Currency Conversion!")
        return

    expenses.append([amount, currency, category, payment, date_val, usd_value])
    table.insert("", tk.END, values=(amount, currency, category, payment, date_val, usd_value))
    update_total()
    clear_inputs()
    messagebox.showinfo("Success", "Expense added successfully!")

window = tk.Tk()
window.title("Expense Tracker")
window.geometry("950x600")
window.resizable(False, False)

style = ttk.Style(window)
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
style.configure("Treeview", font=("Arial", 10))

input_frame = tk.Frame(window, padx=20, pady=20)
input_frame.pack(fill="x")

table_frame = tk.Frame(window, padx=20, pady=10)
table_frame.pack(fill="both", expand=True)

tk.Label(input_frame, text="Amount:").grid(row=0, column=0, sticky="w", pady=5)
amount_entry = tk.Entry(input_frame, width=20)
amount_entry.grid(row=0, column=1, pady=5)

tk.Label(input_frame, text="Currency:").grid(row=1, column=0, sticky="w", pady=5)
currency_box = ttk.Combobox(input_frame, values=CURRENCIES, state="readonly", width=18)
currency_box.grid(row=1, column=1, pady=5)
currency_box.current(0)

tk.Label(input_frame, text="Category:").grid(row=2, column=0, sticky="w", pady=5)
category_box = ttk.Combobox(input_frame, values=CATEGORIES, state="readonly", width=18)
category_box.grid(row=2, column=1, pady=5)
category_box.current(0)

tk.Label(input_frame, text="Payment Method:").grid(row=3, column=0, sticky="w", pady=5)
payment_box = ttk.Combobox(input_frame, values=PAYMENT_METHODS, state="readonly", width=18)
payment_box.grid(row=3, column=1, pady=5)
payment_box.current(0)

tk.Label(input_frame, text="Date:").grid(row=4, column=0, sticky="w", pady=5)
date_entry = tk.Entry(input_frame, width=20)
date_entry.grid(row=4, column=1, pady=5)
date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))

add_button = tk.Button(input_frame, text="Add Expense", command=add_expense, width=20, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
add_button.grid(row=5, column=0, columnspan=2, pady=15)

total_label = tk.Label(table_frame, text="Total USD: $0.00", font=("Arial", 14, "bold"), pady=10)
total_label.pack(anchor="e")

columns = ("Amount", "Currency", "Category", "Payment Method", "Date", "USD Value")
table = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

for col in columns:
    table.heading(col, text=col)
    table.column(col, anchor="center", width=120)

scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
table.configure(yscroll=scrollbar_y.set)
scrollbar_y.pack(side="right", fill="y")
table.pack(fill="both", expand=True)

window.mainloop()
