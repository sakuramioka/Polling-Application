import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel
from tkinter import Message
import mysql.connector
from PIL import Image, ImageTk
import os
import json

# Read from config
data = open('config.json','r+')
config = json.load(data)

buttons = []
existing_elements = []
posts = config['posts']
postindex = 0
user_has_voted = False
message_display_time = 1000


# Connect to MySQL database
db = mysql.connector.connect(
    host=config['host'],
    user=config['user'],
    password=config['password'],
    database=config['database']
)

# Retrieve candidate information
def get_candidates():
    global number_of_candidates
    cursor = db.cursor()
    cursor.execute(f"SELECT id, name, class, section, image_path, votes FROM {posts[postindex]}")
    candidates = cursor.fetchall()
    cursor.close()
    number_of_candidates = len(candidates)
    return candidates

def info(title, msg, display_time):
    global posts
    global postindex

    top = Toplevel(root)
    top.geometry('400x100')
    top.title(title)
    # top.overrideredirect(True)
    
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()
    
    x = int((screen_width / 2) - (400 / 2))
    y = int((screen_height / 2) - (100 / 2))
    
    top.geometry(f"{400}x{100}+{x}+{y}")
    top.configure(background= '#333333')

    
    Message(top, text=msg, padx=0, pady=100, justify="center" ,font=("Century Gothic","15" ,"bold"), bg = '#333333', fg= '#ffffff').pack()

    
    top.after(display_time*1000, top.destroy)
    postindex = postindex+1
    root.after(display_time*1000, lambda: generate_list())

        

# Vote button
def vote(candidate_id):

    global user_has_voted
    global postindex
    global buttons 

    cursor = db.cursor()
    cursor.execute(f"UPDATE {posts[postindex]} SET votes = votes + 1 WHERE id = {candidate_id}")
    db.commit()
    cursor.execute("SELECT name FROM {} WHERE id = %s".format(posts[postindex]), (candidate_id,))
    name = cursor.fetchall()
    name = name[0][0]
    cursor.close()
    for button in buttons:
        button['state'] = tk.DISABLED

    if not len(posts)-1 == postindex:     
        info("Voted has been casted!", f"You voted for: {name}", 1)
        user_has_voted = True
    else:
        info("Voting finished!", f"You voted for: {name}\n \nThank you for voting!", 3)

def replace_characters(string):
    string = string.replace("_"," ")
    string = string.replace("  "," - ")
    string = string.upper()
    return string

# Exit button
def exit_app():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()




# Main window
index = 1
x_spacing = 70
y_spacing = 5
y_pad = (200, 5)
root = tk.Tk()
root.title("Voting")
# root.geometry('1366x768')

root.configure(bg="#000000")
root.attributes('-fullscreen', True)
root.wm_attributes('-transparentcolor', '#ab23ff')

# Background image
background_image = Image.open("images\\bg.png")
background_image = background_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()),
                                           Image.Resampling.LANCZOS)
background_image = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
canvas.pack(fill="both", expand=True)  # Fill and expand the canvas to fit the window

canvas.create_image(0, 0, anchor="nw", image=background_image)
canvas.image = background_image

# Get candidates
# candidates = get_candidates()

# Create temporary grid
row = 0
col = 0
frame_width = root.winfo_screenwidth()
frame_height = root.winfo_screenheight()
canvas_width = 5 * (frame_width + x_spacing) + x_spacing
canvas_height = 2 * (frame_height + y_spacing) + y_spacing
canvas_x = (root.winfo_screenwidth() - canvas_width) // 2
canvas_y = (root.winfo_screenheight() - canvas_height) // 2
canvas.configure(width=canvas_width, height=canvas_height)
canvas.pack_propagate(0)

# Top image
top_image_width = 784
top_image_height = 120
top_image_path = "images\\top_image.png"
top_image = Image.open(top_image_path)
top_image = top_image.resize((784, 120), Image.Resampling.LANCZOS)
top_image = ImageTk.PhotoImage(top_image)
canvas.create_image((root.winfo_screenwidth() - top_image_width) // 2, y_spacing+10, image=top_image, anchor=tk.NW)

def generate_list():
    global number_of_candidates
    global user_has_voted
    global postindex
    global existing_elements
    global row
    global col
    global x_spacing
    global y_pad 
    global buttons 

    try:
        posts[postindex]
    except IndexError:
        postindex = 0

    user_has_voted = False
    col = 0
    row = 0
    # Clear all elements
    for element in existing_elements:
        element.destroy()
    try:
        canvas.delete("names")
    except Exception:
        pass
    existing_elements.clear()
    buttons.clear()

    candidates = get_candidates()

    if number_of_candidates >= 6:
        canvas.create_text((root.winfo_screenwidth()) // 2, y_spacing + 160, text=f"{replace_characters(posts[postindex])} ({postindex+1}/{len(posts)})", fill='white',
                    font=('Century Gothic', '25',), anchor=tk.N, tags=("names",))
    else:
        canvas.create_text((root.winfo_screenwidth()) // 2, y_spacing + 260, text=f"{replace_characters(posts[postindex])} ({postindex+1}/{len(posts)})", fill='white',
                    font=('Century Gothic', '25'), anchor=tk.N, tags=("names",))
        
    if number_of_candidates <= 5:    
        candidates_per_row = number_of_candidates
    else:
        candidates_per_row = 5

    initial_x_spacing = ((root.winfo_screenwidth()/2) - (((candidates_per_row * (160) + ((candidates_per_row - 1) * (150))))/2), 70)
    final_x_spacing = (70,70)
    
    if number_of_candidates <= 5:
        y_pad = (350, 5)
    else:
        y_pad = (250, 5)

    for candidate in candidates:
        global image

        if candidates.index(candidate) == 0 or candidates.index(candidate) == 5:
            x_spacing = initial_x_spacing
        else:
            x_spacing = final_x_spacing

        # Load and resize candidate's image
        if os.path.isfile(candidate[4]):
            image = Image.open(candidate[4])
            image = image.resize((160, 160), Image.Resampling.LANCZOS)
        else:
            image = Image.open("images\\placeholder.png")
            image = image.resize((160, 160), Image.Resampling.LANCZOS)

        # Create a label for candidate's image
        image = ImageTk.PhotoImage(image)
        image_label = tk.Label(canvas, image=image, bg="#f0f0f0")
        image_label.image = image
        image_label.grid(row=row, column=col, padx=x_spacing, pady=y_pad, sticky="n")
        existing_elements.append(image_label)

        # Label for candidate's name
        name_label = tk.Label(canvas, text=f"{candidate[1]}", bg="#000000", fg="#000000", font=("Arial", 14))
        name_label.grid(row=row + 2, column=col, padx=x_spacing, sticky="n")

        # Load and resize vote button image
        vote_button_image_path = "images\\Vote_Button.png"
        vote_button_image = Image.open(vote_button_image_path)
        vote_button_image = vote_button_image.resize((100, 35), Image.Resampling.LANCZOS)
        vote_button_image = ImageTk.PhotoImage(vote_button_image)

        # Create the image button for voting
        vote_button = tk.Button(canvas, image=vote_button_image,
                                command=lambda candidate_id=candidate[0]: vote(candidate_id),
                                bg="#f0f0f0", bd=0, highlightthickness= 0)
        vote_button.image = vote_button_image
        vote_button.grid(row=row + 5, column=col, padx=x_spacing, pady=(40, 0), sticky="n")
        existing_elements.append(vote_button)
        buttons.append(vote_button)

        root.update()

        for x in [name_label]:
            x_pos = x.winfo_x() + x.winfo_width() // 2
            #        if index <= 3:
            #            x_pos = x_pos - 25
            #            index = index+1
            y_pos = x.winfo_y() + x.winfo_height() // 2
            if x == name_label:
                canvas.create_text(x_pos, y_pos, text=f"{candidate[1].upper()}", fill="#ffffff",
                                                       font=("Arial", 14), tags=("names",))

        for element in [name_label]:
            element.destroy()


        # Adjust column and row positions
        col = col + 1
        if col > 4:
            col = 0
            row = row + 6
            y_pad = (70, 5)

generate_list()

def switch_category(event):
    global postindex

    if event.keysym == "Right":
        postindex = postindex + 1
        generate_list()
"""    elif event.keysym == "Left":
        postindex = postindex - 1
        if postindex == 0:
            postindex == len(posts)-1 """

"""def mouse_wheel_binding(event):
    global postindex
    if event.delta < 0 and user_has_voted == True: 
        postindex = postindex + 1
        generate_list()
    elif event.delta > 0 and user_has_voted == True:
        postindex = postindex - 1
        generate_list()"""

root.bind("<Right>", switch_category)
root.bind("<Left>", switch_category)
# root.bind("<MouseWheel>", mouse_wheel_binding)

# Exit button
exit_button = tk.Button(root, text="Exit", command=exit_app, bg="#f44336", fg="#ffffff", font=("Arial", 14, "bold"), relief='flat')
exit_button.place(x=root.winfo_screenwidth() - 90, y=10, width=80, height=30)

root.mainloop()
