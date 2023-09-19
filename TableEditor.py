import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from PIL import ImageTk, Image
from tkinter import filedialog
import json

data = open('config.json','r+')
config = json.load(data)

# Create MySQL connection
db_config = {
    'user': config['user'],
    'password': config['password'],
    'host': config['host'],
    'database': config['database']
}
db_conn = mysql.connector.connect(**db_config)
db_cursor = db_conn.cursor()

selected_database = db_config['database']

# Main tkinter window
root = tk.Tk()
root.title("Table Selector")
root.geometry('1280x720')
root.resizable(False,False)

# Background image
background_image = Image.open("images\\TableEditor.png")
background_image = background_image.resize((1280, 720), Image.Resampling.LANCZOS)
background_image = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=background_image)
canvas.image = background_image

table_names = []

def get_table_names():
    global table_names 
    table_list.delete(0, tk.END)

    try:
        db_cursor.execute(f"SHOW TABLES FROM {db_config['database']}")
        tables = db_cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        # Update table list
        for table in table_names:
            table_list.insert(tk.END, table)
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to retrieve tables from database. {error}")

# Create a new table
def create_table():
    new_table = new_table_entry.get()
    
    if new_table == "":
        messagebox.showerror("Error", "Please enter a table name.")
        return
    
    try:
        db_cursor.execute(f"CREATE TABLE {new_table} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), class VARCHAR(255), section VARCHAR(255), image_path VARCHAR(255), votes INT)")
        db_conn.commit()
        
        # Update table list and clear old list
        table_list.insert(tk.END, new_table)
        new_table_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", f"Table {new_table} created successfully.")
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to create table {new_table}. {error}")

# Table selection
def select_table():
    selected_table = table_list.get(tk.ACTIVE)
    """config['table'] = str(selected_table)
    data.seek(0)
    json.dump(config, data, indent=5)
    data.truncate()"""

    try:
        # Retrieve the columns
        db_cursor.execute(f"DESCRIBE {selected_table}")
        columns = db_cursor.fetchall()
        column_names = [column[0] for column in columns]
        
        # Check if selected table has required columns
        if column_names == ['id', 'name', 'class', 'section', 'image_path', 'votes']:
            
            # Clear existing candidate names
            candidate_list.delete(0, tk.END)
            
            # Retrieve candidate names from the selected table
            db_cursor.execute(f"SELECT id, name FROM {selected_table} ORDER BY id")
            candidates = db_cursor.fetchall()
            
            # Insert into candidate list
            for candidate in candidates:
                candidate_list.insert(tk.END, f"{candidate[0]}: {candidate[1]}")
            
        else:
            response = messagebox.askyesno("Error", "The selected table does not match the required structure. Would you like to add the necessary columns?")
            
            if response == 1:
                # Add the necessary columns to the table
                db_cursor.execute(f"ALTER TABLE {selected_table} ADD COLUMN name VARCHAR(255) AFTER id")
                db_cursor.execute(f"ALTER TABLE {selected_table} ADD COLUMN class VARCHAR(255) AFTER name")
                db_cursor.execute(f"ALTER TABLE {selected_table} ADD COLUMN section VARCHAR(255) AFTER class")
                db_cursor.execute(f"ALTER TABLE {selected_table} ADD COLUMN image_path VARCHAR(255) AFTER section")
                db_cursor.execute(f"ALTER TABLE {selected_table} ADD COLUMN votes INT AFTER image_path")
                db_conn.commit()
                
                messagebox.showinfo("Success", "Columns added successfully.")
                
                # Clear existing candidate names
                candidate_list.delete(0, tk.END)
                
                # Retrieve candidate names from the selected table
                db_cursor.execute(f"SELECT id, name FROM {selected_table} ORDER BY id")
                candidates = db_cursor.fetchall()
                
                # Insert into candidate list
                for candidate in candidates:
                    candidate_list.insert(tk.END, f"{candidate[0]}: {candidate[1]}")
                
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to fetch table structure. {error}")

# View candidate information
def view_information():
    selected_table = table_list.get(tk.ACTIVE)
    selected_candidate = candidate_list.get(tk.ACTIVE)
    
    # Get candidate id
    selected_candidate_id = int(selected_candidate.split(":")[0].strip())
    
    try:
        # Fetch candidate details from the selected table
        db_cursor.execute(f"SELECT * FROM {selected_table} WHERE id = {selected_candidate_id}")
        candidate_info = db_cursor.fetchone()
        
        # Display candidate information
        info_text.config(state=tk.NORMAL)
        info_text.delete(1.0, tk.END)
        info_text.insert(tk.END, f"Candidate ID: {candidate_info[0]}\n")
        info_text.insert(tk.END, f"Name: {candidate_info[1]}\n")
        info_text.insert(tk.END, f"Class: {candidate_info[2]}\n")
        info_text.insert(tk.END, f"Section: {candidate_info[3]}\n")
        
        # Display candidate image
        image_path = candidate_info[4]
        if image_path:
            try:
                img = Image.open(image_path)
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                image_label.config(image=img)
                image_label.image = img
            except IOError:
                messagebox.showerror("Error", "Failed to load candidate image.")
                img = Image.open("images\\placeholder.png")
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                image_label.config(image=img)
                image_label.image = img
        else:
            messagebox.showwarning("Warning", "No image available for the candidate.")
            img = Image.open("images\\placeholder.png")
            img = img.resize((200, 200), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(img)
            image_label.config(image=img)
            image_label.image = img
        
        info_text.config(state=tk.DISABLED)
        
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to fetch candidate information. {error}")

# Create new candidate with default values
def create_new_candidate():
    selected_table = table_list.get(tk.ACTIVE)
    
    try:
        db_cursor.execute(f"INSERT INTO {selected_table} (name, class, section, image_path, votes) VALUES ('New Candidate', 'Class', 'Section', 'images\\placeholder.png', 0)")
        db_conn.commit()
        
        # Clear existing candidate names
        candidate_list.delete(0, tk.END)
        
        # Retrieve candidate names from selected table
        db_cursor.execute(f"SELECT id, name FROM {selected_table} ORDER BY id")
        candidates = db_cursor.fetchall()
        
        # Update the candidate list
        for candidate in candidates:
            candidate_list.insert(tk.END, f"{candidate[0]}: {candidate[1]}")
        
        messagebox.showinfo("Success", "New candidate created successfully.")
        
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to create new candidate. {error}")

# Edit candidate information
def edit_information():
    selected_table = table_list.get(tk.ACTIVE)
    selected_candidate = candidate_list.get(tk.ACTIVE)
    
    # Get candidate ID
    selected_candidate_id = int(selected_candidate.split(":")[0].strip())
    
    try:
        db_cursor.execute(f"SELECT * FROM {selected_table} WHERE id = {selected_candidate_id}")
        candidate_info = db_cursor.fetchone()
        
        # New window
        edit_window = tk.Toplevel(root)
        edit_window.geometry('200x250')
        edit_window.title("Edit Candidate Information")
        
        # Name
        name_label = tk.Label(edit_window, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(edit_window)
        name_entry.insert(tk.END, candidate_info[1])
        name_entry.pack()
        
        # Class
        class_label = tk.Label(edit_window, text="Class:")
        class_label.pack()
        class_entry = tk.Entry(edit_window)
        class_entry.insert(tk.END, candidate_info[2])
        class_entry.pack()
        
        # Section
        section_label = tk.Label(edit_window, text="Section:")
        section_label.pack()
        section_entry = tk.Entry(edit_window)
        section_entry.insert(tk.END, candidate_info[3])
        section_entry.pack()
        
        # Image Path
        def select_image():
            file_path = filedialog.askopenfilename(filetypes=[("JPEG Images", "*.jpg"), ("PNG Images", "*.png")])
            image_path_entry.delete(0, tk.END)
            image_path_entry.insert(tk.END, file_path)

        image_path_label = tk.Label(edit_window, text="Image Path:")
        image_path_label.pack()
        image_path_entry = tk.Entry(edit_window)
        image_path_entry.insert(tk.END, candidate_info[4])
        image_path_entry.pack()
        select_image_button = tk.Button(edit_window, text="Select Image", command=select_image)
        select_image_button.pack()
        
        # Update button
        def update_candidate():
            new_name = name_entry.get()
            new_class = class_entry.get()
            new_section = section_entry.get()
            new_image_path = image_path_entry.get()
            
            try:
                db_cursor.execute(f"UPDATE {selected_table} SET name = '{new_name}', class = '{new_class}', section = '{new_section}', image_path = '{new_image_path}' WHERE id = {selected_candidate_id}")
                db_conn.commit()
                
                # Refresh candidate list
                select_table()
                edit_window.destroy()
                
                messagebox.showinfo("Success", "Candidate information updated successfully.")
                
            except mysql.connector.Error as error:
                messagebox.showerror("Error", f"Failed to update candidate information. {error}")
        
        update_button = tk.Button(edit_window, text="Update", command=update_candidate)
        update_button.pack()
        
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to fetch candidate information. {error}")

# Create GUI elements
title = canvas.create_text(640,30,text = f"Editing: {selected_database}", anchor= tk.CENTER, font=('Helvetica 20 bold'), fill='white')

table_list = tk.Listbox(canvas, selectmode=tk.SINGLE)
table_list.configure(fg='#ffffff', font=('Helvetica 8 bold'), background='#333333', width=58, height=28, bd= 0, highlightthickness=0, relief='flat')
table_list_window = canvas.create_window(50, 123, anchor=tk.NW, window=table_list )
get_table_names()

new_table_entry = tk.Entry(canvas)
new_table_entry.configure(fg='black', bg='#ffffff', font=('Helvetica 14 bold'), borderwidth=0, highlightthickness=0, relief='flat', width=22)
new_table_entry_window = canvas.create_window(44, 650, anchor=tk.NW, window=new_table_entry )
new_table_entry.insert(0,'Create new post')

create_table_button = tk.Button(canvas, text="Create", command=create_table)
create_table_button.configure(fg='#ffffff', font=('Helvetica 14 bold'), background='#333333', activebackground='#333333', activeforeground='#4b4b4b', borderwidth=0, relief='flat')
create_table_button_window = canvas.create_window(325, 646, anchor=tk.NW, window=create_table_button )

select_table_button = tk.Button(canvas, text="View Candidates", command=select_table)
select_table_button.configure(fg='#ffffff', font=('Helvetica 14 bold'), background='#333333', activebackground='#333333', activeforeground='#4b4b4b', borderwidth=0, relief='flat')
select_table_button_window = canvas.create_window(150, 585, anchor=tk.NW, window=select_table_button )

candidate_list = tk.Listbox(canvas, selectmode=tk.SINGLE)
candidate_list.configure(fg='#ffffff', font=('Helvetica 14 bold'), background='#333333', width=33, height=16, bd= 0, highlightthickness=0, relief='flat')
candidate_list_window = canvas.create_window(458, 123, anchor=tk.NW, window=candidate_list )

view_info_button = tk.Button(canvas, text="View Information", command=view_information)
view_info_button.configure(fg='#ffffff', font=('Helvetica 14 bold'), background='#333333', activebackground='#333333', activeforeground='#4b4b4b', borderwidth=0, relief='flat')
view_info_button_window = canvas.create_window(560, 585, anchor=tk.NW, window=view_info_button )

info_text = tk.Text(canvas, height=10, width=50)
info_text.configure(fg='#ffffff', font=('Helvetica 13 bold'), background='#333333', width=40, height=13, bd= 0, highlightthickness=0, relief='flat')
info_text_window = canvas.create_window(870, 424, anchor=tk.NW, window=info_text )
info_text.config(state=tk.DISABLED)

image_label = tk.Label(canvas)
image_label.configure(background='#333333',borderwidth=0)
image_label_window = canvas.create_window(950, 180, anchor=tk.NW, window=image_label)

create_new_button = tk.Button(canvas, text="Create New Candidate", command=create_new_candidate)
create_new_button.configure(fg='#ffffff', font=('Helvetica 14 bold'), background='#333333', activebackground='#333333', activeforeground='#4b4b4b', borderwidth=0, relief='flat')
create_new_button_window = canvas.create_window(530, 525, anchor=tk.NW, window=create_new_button )

edit_button = tk.Button(canvas, text="Edit Candidate Information", command=edit_information,)
edit_button.configure(fg='#ffffff', font=('Helvetica 14 bold'), background='#333333', activebackground='#333333', activeforeground='#4b4b4b', borderwidth=0, relief='flat')
edit_button_window = canvas.create_window(520, 646, anchor=tk.NW, window=edit_button )

root.mainloop()
