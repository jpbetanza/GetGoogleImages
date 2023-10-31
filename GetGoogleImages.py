import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
import threading
import searchImages

## App Version 1.0

def validate_numeric_input(P):
    if P == "" or P.isdigit():
        return True
    else:
        return False

def startDownload():
    button.config(state="disabled")
    searchText = input_text.get()

    if searchText == '':
        messagebox.showerror("Input error", "Text input should not be empty")
        button.config(state="active")
        return

    amount = int(input_amount.get())  # Convert to an integer
    label_loading.config(text='Downloading...')

    operation_thread = threading.Thread(target=doThings, args=(searchText, amount))
    operation_thread.start()

def doThings(searchText, amount):
    searchImages.main(searchText, amount)
    app.after(1, operation_completed)

def operation_completed():
    label_loading.config(text='Completed Download')
    button.config(state="active")

app = ThemedTk(theme='breeze')
app.title("GetGoogleImages")

label = ttk.Label(app, text="Hello! Enter the image description you want to search and the amount of images you want to attempt to download")
label.pack(padx=20, pady=15)

label_text = ttk.Label(app, text='Search Text')
label_text.pack()
input_text = ttk.Entry(app, width=40)
input_text.pack(padx=20)

ttk.Frame(app).pack(pady=10)

ttk.Label(app, text='Amount of images').pack()
validate_numeric = app.register(validate_numeric_input)
Var1 = tk.IntVar()
Var1.set(10)
input_amount = ttk.Spinbox(app, from_=10, to=100,textvariable = Var1, width=5, validate="key", validatecommand=(validate_numeric, "%P"))
input_amount.pack(padx=20)

ttk.Frame(app).pack(pady=10)

label_loading = ttk.Label(app, text='')
label_loading.pack(pady=5)

button = ttk.Button(app, text="Download Images", command=startDownload)
button.pack(padx=20)

ttk.Frame(app).pack(pady=15)

app.mainloop()