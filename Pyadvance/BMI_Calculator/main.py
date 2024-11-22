import tkinter as tk
from tkinter import ttk
from calculate import calculate_bmi
from ui_helpers import create_spinbox, create_label, create_button

# Tạo cửa sổ chính
window = tk.Tk()
window.title("Tính chỉ số BMI")
window.geometry('400x400')
window.configure(bg='#2c2c2c')  # Màu nền tối

# Tạo Notebook cho các tab Nam/Nữ
tab_control = ttk.Notebook(window)

# Tab 1: Nam
tab1 = ttk.Frame(tab_control, style="TFrame")  # Màu tối
tab_control.add(tab1, text="Nam")

# Tab 2: Nữ
tab2 = ttk.Frame(tab_control, style="TFrame")  # Màu tối
tab_control.add(tab2, text="Nữ")

tab_control.pack(expand=1, fill="both")

# Thiết lập style cho các thành phần
style = ttk.Style()
style.configure("TLabel", background='#2c2c2c', foreground="white", font=("Arial", 12))
style.configure("TButton", background="#ffffff", foreground="black", font=("Arial", 12, "bold"), padding=5)
style.configure("TFrame", background='#2c2c2c')

# Tạo các thành phần giao diện cho Tab 1 (Nam)
create_label(tab1, "Chiều cao (m):", 0, 0)  # Hiển thị Label "Chiều cao"
spin_height_male = create_spinbox(tab1, from_=1.0, to=2.5, increment=0.01, row=0, column=1, width=10)

create_label(tab1, "Cân nặng (kg):", 1, 0)  # Hiển thị Label "Cân nặng"
spin_weight_male = create_spinbox(tab1, from_=30, to=150, increment=0.5, row=1, column=1, width=10)

create_label(tab1, "Tuổi:", 2, 0)  # Hiển thị Label "Tuổi"
spin_age_male = create_spinbox(tab1, from_=1, to=120, increment=1, row=2, column=1, width=10)

lbl_result_male = tk.Label(tab1, text="", font=("Arial", 12, "bold"), fg="#ff0000", bg='#2c2c2c')  # Kết quả BMI màu đỏ
lbl_result_male.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

create_button(tab1, "Tính BMI", lambda: calculate_bmi("Nam", spin_height_male, spin_weight_male, spin_age_male, lbl_result_male), 3, 0)

# Tạo các thành phần giao diện cho Tab 2 (Nữ)
create_label(tab2, "Chiều cao (m):", 0, 0)  # Hiển thị Label "Chiều cao"
spin_height_female = create_spinbox(tab2, from_=1.0, to=2.5, increment=0.01, row=0, column=1, width=10)

create_label(tab2, "Cân nặng (kg):", 1, 0)  # Hiển thị Label "Cân nặng"
spin_weight_female = create_spinbox(tab2, from_=30, to=150, increment=0.5, row=1, column=1, width=10)

create_label(tab2, "Tuổi:", 2, 0)  # Hiển thị Label "Tuổi"
spin_age_female = create_spinbox(tab2, from_=1, to=120, increment=1, row=2, column=1, width=10)

lbl_result_female = tk.Label(tab2, text="", font=("Arial", 12, "bold"), fg="#ff0000", bg='#2c2c2c')  # Kết quả BMI màu đỏ
lbl_result_female.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

create_button(tab2, "Tính BMI", lambda: calculate_bmi("Nữ", spin_height_female, spin_weight_female, spin_age_female, lbl_result_female), 3, 0)

# Bắt đầu vòng lặp sự kiện chính
window.mainloop()