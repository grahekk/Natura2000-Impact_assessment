import time
import tkinter as tk
from tkinter import ttk, filedialog

# Create the main window
root = tk.Tk()
root.title("Impact assesment report")
root.geometry('600x700')

# Add a label to the window
label = tk.Label(root, text="Name of the project")
label.pack(side="top", padx=10, pady=10)

# entry field
txtfld = tk.Entry(root, bd=1)
txtfld.pack()

# Type of the project
label = tk.Label(root, text="Type of the project")
label.pack(side="top", padx=10, pady=10)

# option menu for type
variable = tk.StringVar(root)
OPTIONS = ["OPP", "PUO", "SPUO"]
variable.set(OPTIONS[0])  # default value
option_menu = tk.OptionMenu(root, variable, *OPTIONS)
option_menu.pack()

# shapefile part
label = tk.Label(root, text="Insert shapefile of the project")
label.pack(side="top", padx=10, pady=10)

# insert shapefile

def select_file(self):
    filename = filedialog.askopenfilename()
    self.log.insert("end", f"Selected file: {filename}\n")

    self.file_button = tk.Button(self, text="Select File", command=self.select_file)
    self.file_button.pack(side="trop", padx=10, pady=10)

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


label = tk.Label(root, text="Which chapters are you writting in EIA?")
label.pack(side="top", padx=10, pady=10)


# chapters window
def open_new_window():
    # Create a new window
    new_window = tk.Toplevel(root)
    new_window.title("Chapters check")
    # checkboxes for chapters
    c1 = tk.Checkbutton(new_window, text='Nature', onvalue=1, offvalue=0).pack()
    c2 = tk.Checkbutton(new_window, text='Geology', onvalue=1, offvalue=0).pack()
    c1 = tk.Checkbutton(new_window, text='Landscape', onvalue=1, offvalue=0).pack()
    c2 = tk.Checkbutton(new_window, text='Forestry', onvalue=1, offvalue=0).pack()
    c2 = tk.Checkbutton(new_window, text='Hunting', onvalue=1, offvalue=0).pack()
    c2 = tk.Checkbutton(new_window, text='Traffic', onvalue=1, offvalue=0).pack()
    c2 = tk.Checkbutton(new_window, text='Climate', onvalue=1, offvalue=0).pack()
    c2 = tk.Checkbutton(new_window, text='Otpad', onvalue=1, offvalue=0).pack()


open_window_button = tk.Button(root, text="Check chapters", command=open_new_window)
open_window_button.pack()

button_get_db = tk.Button(root, text="Check available databases")
button_get_db.pack()


def open_window():
    # Create a new window
    new_window = tk.Toplevel(root)
    new_window.title("New Window")
    new_window.geometry('200x200')

    # Add a label to the new window
    label = tk.Label(new_window, text="This is a new window!")
    label.pack()


# Add a button that opens new window
button = tk.Button(root, text="Options", command=open_window)
button.pack()


class StatusBar(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        # self.label = tk.Label(self, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        # self.label.pack(fill=tk.X)

    def create_widgets(self):
        # create status bar label
        self.status_bar = tk.Label(self, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # create button
        self.button = tk.Button(self, text="Click me!", command=self.button_click)
        self.button.pack()

    def button_click(self):
        # change status bar text to "Loading"
        self.status_bar.config(text="Loading...")

        # wait for one second
        time.sleep(1)

        # change status bar text back to "Ready"
        self.status_bar.config(text="Ready")

# add status bar widget
status_bar = StatusBar(root)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)


class message_log(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.log_label = tk.Label(self, text="Message Log")
        self.log_label.pack(side="top", padx=10, pady=10)

        self.log = tk.Text(self, height=10, width=50)
        self.log.pack()

        self.file_button = tk.Button(self, text="Select File", command=self.select_file)
        self.file_button.pack(side="left", padx=10, pady=10)

        self.subtract_button = tk.Button(self, text="Subtract", command=self.subtract)
        self.subtract_button.pack(side="left")

        self.quit_button = tk.Button(self, text="Quit", command=self.master.destroy)
        self.quit_button.pack(side="right")

    def select_file(self):
        filename = filedialog.askopenfilename()
        self.log.insert("end", f"Selected file: {filename}\n")

    def subtract(self):
        a = 10
        b = 5
        result = a - b
        self.log.insert("end", f"{a} - {b} = {result}\n")

message_log = message_log(root)
#status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# reporting button in the end
button_get_db = tk.Button(root, text="Create report!")
button_get_db.pack()

# Start the main event loop
root.mainloop()
