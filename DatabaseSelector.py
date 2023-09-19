import tkinter as tk
import mysql.connector
import json

data = open('config.json','r+')
config = json.load(data)

mydb = mysql.connector.connect(
    user = config['user'],
    password = config['password'],
    host =  config['host']
)

window = tk.Tk()
window.title("Database Selector")
window.geometry("500x550")

def select_database():
    selected_item = database_listbox.get(tk.ACTIVE)
    output_label["text"] = f"Selected database: {selected_item}"

def create_database():
    new_database = new_database_entry.get()
    if new_database:
        mycursor = mydb.cursor()
        mycursor.execute(f"CREATE DATABASE {new_database}")
        database_listbox.insert(tk.END, new_database)
        output_label["text"] = f"Database created: {new_database}"
        new_database_entry.delete(0, tk.END)

# Retrieve current databases
mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")
databases = mycursor.fetchall()

sd_label = tk.Label(window, text="Select a database to proceed:", font=("Arial", 14))
sd_label.pack(pady=10, padx=10, anchor="nw")

current_databases_label = tk.Label(window, text="Current databases", font=("Arial", 14))
current_databases_label.pack(pady=5)

database_listbox = tk.Listbox(window, height=10, width=40)
for database in databases:
    database_listbox.insert(tk.END, database[0])
database_listbox.pack(pady=5)

select_button = tk.Button(window, text="Select", command=select_database, width=20)
select_button.pack()

output_label = tk.Label(window, text="", font=("Arial", 14), pady=20)
output_label.pack()

create_database_label = tk.Label(window, text="Or create a new database:", font=("Arial", 14))
create_database_label.pack(pady=10, padx=10, anchor="nw")

new_database_label = tk.Label(window, text="New Database Name", font=("Arial", 14))
new_database_label.pack()

new_database_entry = tk.Entry(window, font=("Arial", 14), width=20)
new_database_entry.pack()

create_button = tk.Button(window, text="Create", command=create_database, width=20)
create_button.pack(pady=20)

# Center all the elements
window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry(f"{width}x{height}+{x}+{y}")

window.mainloop()
