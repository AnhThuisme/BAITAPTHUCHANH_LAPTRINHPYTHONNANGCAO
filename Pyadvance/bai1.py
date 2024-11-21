import tkinter as tk
from tkinter import messagebox, Toplevel

class QuanLySach:
    def __init__(self, master):
        self.master = master
        self.master.title("Quản lý sách")

        # Thiết lập màu sắc và kiểu chữ
        self.bg_color = "#2c3e50"            # Màu nền xanh đậm
        self.entry_bg_color = "#34495e"      # Màu nền cho Entry
        self.entry_text_color = "#ecf0f1"    # Màu chữ trắng cho Entry
        self.button_color = "#e74c3c"        # Màu đỏ cho nút
        self.button_text_color = "#ecf0f1"   # Màu chữ trắng cho nút
        self.label_text_color = "#ecf0f1"    # Màu chữ trắng cho Label
        self.font_title = ("Arial", 14, "bold")
        self.font_label = ("Arial", 12, "bold")
        self.font_entry = ("Arial", 12)
        self.font_button = ("Arial", 12, "bold")

        # Đặt màu nền cho cửa sổ chính
        self.master.configure(bg=self.bg_color)

        # Danh sách sách
        self.danh_sach_sach = []

        # Giao diện
        self.create_widgets()

    def create_widgets(self):
        # Mã sách
        tk.Label(self.master, text="Mã sách:", bg=self.bg_color, fg=self.label_text_color, font=self.font_label).grid(row=0, column=0, pady=5, padx=5, sticky='e')
        self.entry_ma_sach = tk.Entry(self.master, font=self.font_entry, bg=self.entry_bg_color, fg=self.entry_text_color)
        self.entry_ma_sach.grid(row=0, column=1, pady=5, padx=5)

        # Tên sách
        tk.Label(self.master, text="Tên sách:", bg=self.bg_color, fg=self.label_text_color, font=self.font_label).grid(row=1, column=0, pady=5, padx=5, sticky='e')
        self.entry_ten_sach = tk.Entry(self.master, font=self.font_entry, bg=self.entry_bg_color, fg=self.entry_text_color)
        self.entry_ten_sach.grid(row=1, column=1, pady=5, padx=5)

        # Tác giả
        tk.Label(self.master, text="Tác giả:", bg=self.bg_color, fg=self.label_text_color, font=self.font_label).grid(row=2, column=0, pady=5, padx=5, sticky='e')
        self.entry_tac_gia = tk.Entry(self.master, font=self.font_entry, bg=self.entry_bg_color, fg=self.entry_text_color)
        self.entry_tac_gia.grid(row=2, column=1, pady=5, padx=5)

        # Nút Lưu
        tk.Button(self.master, text="Lưu", command=self.luu_sach, bg=self.button_color, fg=self.button_text_color, font=self.font_button).grid(row=3, column=0, columnspan=2, pady=10)

        # Menu bar
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        # Menu để xem danh sách sách
        menu_xem = tk.Menu(menubar, tearoff=0, bg=self.entry_bg_color, fg=self.label_text_color, activebackground=self.button_color, activeforeground=self.button_text_color)
        menubar.add_cascade(label="Thông Báo", menu=menu_xem)
        menu_xem.add_command(label="Danh sách sách đã lưu", command=self.xem_sach)

        # Menu mới để mở cửa sổ danh sách sách
        menu_list = tk.Menu(menubar, tearoff=0, bg=self.entry_bg_color, fg=self.label_text_color, activebackground=self.button_color, activeforeground=self.button_text_color)
        menubar.add_cascade(label="Danh sách", menu=menu_list)
        menu_list.add_command(label="Sách Đã Được Lưu", command=self.mo_cua_so_sach)

    def luu_sach(self):
        ma_sach = self.entry_ma_sach.get()
        ten_sach = self.entry_ten_sach.get()
        tac_gia = self.entry_tac_gia.get()
        if ma_sach and ten_sach and tac_gia:
            # Kiểm tra xem mã sách đã tồn tại chưa
            for sach in self.danh_sach_sach:
                if sach['ma_sach'] == ma_sach:
                    messagebox.showwarning("Cảnh báo", "Mã sách đã tồn tại!")
                    return

            # Thêm sách vào danh sách
            self.danh_sach_sach.append({"ma_sach": ma_sach, "ten_sach": ten_sach, "tac_gia": tac_gia})
            messagebox.showinfo("Thành công", "Lưu sách thành công!")
            self.entry_ma_sach.delete(0, tk.END)
            self.entry_ten_sach.delete(0, tk.END)
            self.entry_tac_gia.delete(0, tk.END)
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")

    def xem_sach(self):
        if not self.danh_sach_sach:
            messagebox.showinfo("Thông tin", "Chưa có sách nào được lưu!")
            return

        # Tạo chuỗi danh sách sách
        danh_sach = ""
        for sach in self.danh_sach_sach:
            danh_sach += f"Mã sách: {sach['ma_sach']}, Tên sách: {sach['ten_sach']}, Tác giả: {sach['tac_gia']}\n"

        # Hiển thị danh sách sách trong một hộp thoại
        messagebox.showinfo("Danh sách sách", danh_sach)

    def mo_cua_so_sach(self):
        # Tạo cửa sổ mới để hiển thị danh sách sách
        new_window = Toplevel(self.master)
        new_window.title("Danh sách sách")
        new_window.configure(bg=self.bg_color)

        if not self.danh_sach_sach:
            tk.Label(new_window, text="Chưa có sách nào được lưu!", bg=self.bg_color, fg=self.label_text_color, font=self.font_label).pack(pady=10)
        else:
            row_num = 0
            # Tạo tiêu đề cột
            tk.Label(new_window, text="Mã sách", bg=self.bg_color, fg=self.label_text_color, font=self.font_title, borderwidth=1, relief="solid", width=20).grid(row=row_num, column=0)
            tk.Label(new_window, text="Tên sách", bg=self.bg_color, fg=self.label_text_color, font=self.font_title, borderwidth=1, relief="solid", width=30).grid(row=row_num, column=1)
            tk.Label(new_window, text="Tác giả", bg=self.bg_color, fg=self.label_text_color, font=self.font_title, borderwidth=1, relief="solid", width=25).grid(row=row_num, column=2)

            # Hiển thị sách
            for sach in self.danh_sach_sach:
                row_num += 1
                tk.Label(new_window, text=sach['ma_sach'], bg=self.bg_color, fg=self.entry_text_color, font=self.font_entry, borderwidth=1, relief="solid", width=20).grid(row=row_num, column=0)
                tk.Label(new_window, text=sach['ten_sach'], bg=self.bg_color, fg=self.entry_text_color, font=self.font_entry, borderwidth=1, relief="solid", width=30).grid(row=row_num, column=1)
                tk.Label(new_window, text=sach['tac_gia'], bg=self.bg_color, fg=self.entry_text_color, font=self.font_entry, borderwidth=1, relief="solid", width=25).grid(row=row_num, column=2)


# Tạo cửa sổ chính
root = tk.Tk()
app = QuanLySach(root)
# Vô hiệu hóa thay đổi kích thước cửa sổ
root.resizable(False, False)

# Chạy chương trình
root.mainloop()