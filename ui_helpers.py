import tkinter as tk

def create_spinbox(parent, from_, to, increment, row, column, width=10):
    spinbox = tk.Spinbox(parent, from_=from_, to=to, increment=increment, width=width, font=("Arial", 12))
    spinbox.grid(row=row, column=column, padx=10, pady=10)
    return spinbox

def create_label(parent, text, row, column, columnspan=1, fg_color='#ffffff'):
    label = tk.Label(parent, text=text, font=("Arial", 12, "bold"), fg=fg_color, bg='#2c2c2c')  # Màu nền tối
    label.grid(row=row, column=column, padx=10, pady=10, columnspan=columnspan)
    return label

def create_button(parent, text, command, row, column):
    button = tk.Button(parent, text=text, command=command, bg="#ffffff", fg="black", font=("Arial", 14, "bold"), relief="solid")
    button.grid(row=row, column=column, columnspan=2, pady=10)
    return button