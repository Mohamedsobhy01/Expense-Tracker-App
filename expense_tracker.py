import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

expenses = []

def convert_to_usd(amount, currency) : 
    url ="https://open.er-api.com/v6/latest/USD"
    response = requests.get(url)
    data = response.json()

    rate = data["rates"].get(currency, None)

    if rate is None :
        return None
    
    usd_value = amount / rate 
    return usd_value

def update_total() :
    total = sum(x[-1] for x in expenses)
    total_label.config(text= f"Total USD = {round(total, 2)}")

def add_expense() :
    try :
        amount = float(amount_entry.get())
    except :
        messagebox.showwarning("Invalid Input", "Amount must be a number!")
        return

    if amount <= 0 :
        messagebox.showwarning("Invalid Input", "Amount must be > 0!")
        return
    
    currency = currency_box.get()
    category = category_box.get()
    payment = payment_box.get()
    date_val = date_entry.get()

    usd_value = convert_to_usd(amount, currency)

    if usd_value is None :
        result_label.config(text= "Invalid Currency Conversion!", fg="red")
        return

    expenses.append([amount, currency, category, payment, date_val, usd_value]) 

    table.insert("",tk.END, values=(amount, currency, category, payment, date_val, round(usd_value, 2)))

    update_total()

    result_label.config(text= "Expense Added Successfully!", fg="green")
        
window = tk.Tk()
window.title("Expense Tracker")
window.geometry = ("900x600")

tk.Label(window, text="Amount").grid(row= 0, column= 0, padx= 5, pady= 5)
amount_entry = tk.Entry(window)
amount_entry.grid(row= 0, column= 1)

tk.Label(window, text= "Currency").grid(row= 1, column= 0, padx= 5, pady= 5)
currency_box = ttk.Combobox(window, values=["USD", "EGP", "EUR", "SAR"])
currency_box.grid(row= 1, column= 1)
currency_box.current(0)

tk.Label(window, text= "Category").grid(row= 2, column= 0, padx= 5, pady= 5)
category_box = ttk.Combobox(window, values=["Education", "Savings", "Grocery", "Rental", "Gas", "Electricity", "Life Expenses", "Charity"])
category_box.grid(row= 2, column= 1)
category_box.current(0)

tk.Label(window, text= "Payment Method").grid(row= 3, column= 0, padx= 5, pady= 5)
payment_box = ttk.Combobox(window, values=["Paypal", "Cash", "Credit Card"])
payment_box.grid(row= 3, column= 1)
payment_box.current(0)

tk.Label(window, text= "Date").grid(row= 4, column= 0, padx= 5, pady= 5)
date_entry = tk.Entry(window)
date_entry.grid(row= 4, column= 1)
date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))

expense_button = tk.Button(window, text= "Add Expense", command= add_expense, width= 20)
expense_button.grid(row= 5, column= 1, pady= 10)

result_label = tk.Label(window, text="")
result_label.grid(row= 6, column= 1)

columns = ("Amount", "Currency", "Category", "Payment Method")
table = ttk.Treeview(window, columns= columns, show= "headings")

for col in columns :
    table.heading(col, text= col)

table.grid(row= 7, column= 0, columnspan= 2, padx= 20)

total_label = tk.Label(window, text= "Total USD", font=("Arial", 14, "bold"))
total_label.grid(row= 8, column= 0, sticky="W", padx= 20, pady= 20)

window.mainloop()