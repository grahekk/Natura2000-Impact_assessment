import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Impact assesment report")
root.geometry('400x300')

# Add a label to the window
label = tk.Label(root, text="Name of the project")
label.pack()

# entry field
txtfld = tk.Entry(root, bd=1)
txtfld.pack()

# shapefile part
label = tk.Label(root, text="Insert shapefile of the project")
label.pack()

# insert shapefile
txtfld = tk.Entry(root, bd=1)
txtfld.pack()

# locate shapefile on the map?
label = tk.Label(root, text="your shapefile is located in:")
label.pack()
# map
label = tk.Label(root, text="OSM map")
label.pack()


def open_window():
    # Create a new window
    new_window = tk.Toplevel(root)
    new_window.title("New Window")
    new_window.geometry('200x200')

    # Add a label to the new window
    label = tk.Label(new_window, text="This is a new window!")
    label.pack()


# Add a button to the window
button = tk.Button(root, text="Open New Window", command=open_window)
button.pack()

button_nature_chapters = tk.Button(root, text="Which chapters are you writting?")
button_nature_chapters.pack()

button_get_db = tk.Button(root, text="Get database for nature chapters")
button_get_db.pack()

variable =  tk.StringVar(root)
OPTIONS = ["Jan","Feb","Mar"]

#variable = tk.StringVar(root)
variable.set(OPTIONS[0]) # default value
w = tk.OptionMenu(root, variable, *OPTIONS)
w.pack()

# Start the main event loop
root.mainloop()
