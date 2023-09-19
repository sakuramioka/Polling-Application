import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import json

# Read from config
data = open('config.json','r+')
config = json.load(data)

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        return connection
    except mysql.connector.Error as error:
        print("Error while connecting to MySQL:", error)

def retrieve_tables():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor]
        cursor.close()
        connection.close()
        return tables

def retrieve_candidates():
    selected_table = tables_combobox.get()
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT ID, Name, Class, Section, Votes FROM {selected_table} ORDER BY Votes DESC")
        candidates = cursor.fetchall()
        cursor.close()
        connection.close()
        return candidates

def reset_all_votes():
    confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to reset all election votes?")
    if confirmed:
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor(buffered=True)
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor]
            for table in tables:
                cursor.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' AND COLUMN_NAME = 'Votes'")
                if cursor.fetchone():
                    cursor.execute(f"UPDATE {table} SET Votes = 0")
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success", "All election votes have been reset to 0.")

def reset_post_votes():
    confirmed = messagebox.askyesno("Confirmation", "Are you sure you want to reset the votes for this post?")
    if confirmed:
        selected_table = tables_combobox.get()
        connection = connect_to_database()     
        if connection:
            cursor = connection.cursor(buffered=True)
            cursor.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{selected_table}' AND COLUMN_NAME = 'Votes'")
            if cursor.fetchone():
                cursor.execute(f"UPDATE {selected_table} SET Votes = 0")
                connection.commit()
                cursor.close()
                connection.close()
                messagebox.showinfo("Success", f"Votes for the table '{selected_table}' have been reset to 0.")
            else:
                messagebox.showwarning("Column Not Found", f"The 'Votes' column does not exist in the table '{selected_table}'.")

def calculate_total_votes():
    selected_table = tables_combobox.get()
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT SUM(Votes) FROM {selected_table}")
        total_votes = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        if total_votes is not None:
            total_votes_label.configure(text=f"Total votes: {total_votes}")
        else:
            total_votes_label.configure(text="Total votes: 0")

window = tk.Tk()
window.title("Candidate Information")
window.geometry("600x420")

tables_combobox = ttk.Combobox(window, state="readonly")
tables_combobox.pack()

tables = retrieve_tables()
if tables:
    tables_combobox["values"] = tables

def results():
    candidates = retrieve_candidates()
    if candidates:
        for child in treeview.get_children():
            treeview.delete(child)

        for candidate in candidates:
            treeview.insert("", "end", values=candidate)
        calculate_total_votes()

display_button = tk.Button(window, text="View Results", command=results, background="#90EE90", font=("Helvetica", "10", "bold"))
display_button.pack(pady=10)

treeview = ttk.Treeview(window, columns=("ID", "Name", "Class", "Section", "Votes"))
treeview.heading("#0", text="Table", anchor="center")
treeview.heading("ID", text="ID", anchor="center")
treeview.heading("Name", text="Name", anchor="center")
treeview.heading("Class", text="Class", anchor="center")
treeview.heading("Section", text="Section", anchor="center")
treeview.heading("Votes", text="Votes", anchor="center")

# Config columns
treeview.column("#0", width=0, stretch=tk.NO)
treeview.column("ID", width=10)
treeview.column("Name", width=200)
treeview.column("Class", width=50)
treeview.column("Section", width=50)
treeview.column("Votes", width=50)

treeview.pack()

total_votes_label = tk.Label(window, text="Total votes: 0")
total_votes_label.pack()

reset_post_button = tk.Button(window, text="Reset post votes", command=reset_post_votes, background="#DC0C37", fg="white", font=("Arial", "10", "bold"))
reset_post_button.pack(pady=10)

reset_all_button = tk.Button(window, text="Reset all election votes", command=reset_all_votes, background="#DC0C37", fg="white", font=("Arial", "10", "bold"))
reset_all_button.pack(pady=10)

window.mainloop()
