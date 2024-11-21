import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
import psycopg2
from psycopg2 import sql

class LibraryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quản lý thư viện")

        # Thông tin kết nối cơ sở dữ liệu
        self.db_name = 'Library_db'   # Thay đổi tên cơ sở dữ liệu
        self.user = 'postgres'
        self.password = 'anhthu'  # Thay bằng mật khẩu của bạn
        self.host = 'localhost'
        self.port = '5432'
        self.table_name = 'books'     # Thay đổi tên bảng

        # Tạo menu bar và nút đăng xuất
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        account_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tài khoản", menu=account_menu)
        account_menu.add_command(label="Đăng xuất", command=self.confirm_logout)

        # Tạo giao diện đăng nhập
        self.create_login_widgets()

    def create_login_widgets(self):
        self.login_frame = tk.Frame(self.master)
        self.login_frame.pack(pady=10)

        tk.Label(self.login_frame, text="Tên đăng nhập:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_username = tk.Entry(self.login_frame)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_password = tk.Entry(self.login_frame, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.login_frame, text="Đăng nhập", command=self.login).grid(row=2, columnspan=2, pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Kiểm tra tên đăng nhập và mật khẩu
        if username == self.user and password == self.password:
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            self.login_frame.pack_forget()  # Ẩn khung đăng nhập
            self.show_main_menu()  # Hiển thị giao diện chính của thư viện
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")

    def show_main_menu(self):
        # Khung hiển thị danh sách sách
        self.display_books()

        # Khung chứa các nút chức năng nằm ngang bên dưới bảng
        self.functions_frame = tk.Frame(self.master, padx=10, pady=10)
        self.functions_frame.pack(pady=10)

        # Thêm các nút chức năng theo chiều ngang
        tk.Button(self.functions_frame, text="Thêm sách", command=self.open_add_book_window, width=15).grid(row=0, column=0, padx=5)
        tk.Button(self.functions_frame, text="Sửa thông tin sách", command=self.open_edit_book_window, width=15).grid(row=0, column=1, padx=5)
        tk.Button(self.functions_frame, text="Xóa sách", command=self.open_delete_book_window, width=15).grid(row=0, column=2, padx=5)
        tk.Button(self.functions_frame, text="Tìm kiếm sách", command=self.open_search_book_window, width=15).grid(row=0, column=3, padx=5)

    def display_books(self):
        # Tạo khung cho Treeview
        self.tree_frame = tk.Frame(self.master)
        self.tree_frame.pack(pady=10)

        # Tạo bảng Treeview để hiển thị thông tin sách
        self.tree = ttk.Treeview(self.tree_frame, columns=("ISBN", "Tên sách", "Tác giả", "Năm xuất bản", "Thể loại"), show="headings")
        self.tree.heading("ISBN", text="ISBN")
        self.tree.heading("Tên sách", text="Tên sách")
        self.tree.heading("Tác giả", text="Tác giả")
        self.tree.heading("Năm xuất bản", text="Năm xuất bản")
        self.tree.heading("Thể loại", text="Thể loại")

        # Thiết lập kích thước các cột và canh chỉnh
        self.tree.column("ISBN", width=100, anchor="center")
        self.tree.column("Tên sách", width=200, anchor="center")
        self.tree.column("Tác giả", width=150, anchor="center")
        self.tree.column("Năm xuất bản", width=100, anchor="center")
        self.tree.column("Thể loại", width=120, anchor="center")

        # Thêm Treeview vào giao diện
        self.tree.pack()

        # Gọi hàm load dữ liệu từ cơ sở dữ liệu
        self.load_data()

    def load_data(self):
        # Hàm load dữ liệu từ cơ sở dữ liệu và hiển thị trong Treeview
        try:
            conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            cur = conn.cursor()
            query = sql.SQL("SELECT isbn, title, author, year, genre FROM {}").format(sql.Identifier(self.table_name))
            cur.execute(query)
            rows = cur.fetchall()

            # Xóa dữ liệu cũ trong Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Thêm dữ liệu vào Treeview
            for row in rows:
                self.tree.insert("", "end", values=row)

            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")

    def confirm_logout(self):
        # Xác nhận đăng xuất
        response = messagebox.askyesno("Đăng xuất", "Bạn có muốn đăng xuất tài khoản không?")
        if response:
            self.logout()

    def logout(self):
        # Xóa giao diện chính và hiển thị lại giao diện đăng nhập
        self.tree_frame.pack_forget()
        self.functions_frame.pack_forget()
        self.create_login_widgets()

    def open_add_book_window(self):
        self.add_book_window = Toplevel(self.master)
        self.add_book_window.title("Thêm sách")

        tk.Label(self.add_book_window, text="ISBN:").grid(row=0, column=0)
        self.entry_isbn = tk.Entry(self.add_book_window)
        self.entry_isbn.grid(row=0, column=1)

        tk.Label(self.add_book_window, text="Tên sách:").grid(row=1, column=0)
        self.entry_title = tk.Entry(self.add_book_window)
        self.entry_title.grid(row=1, column=1)

        tk.Label(self.add_book_window, text="Tác giả:").grid(row=2, column=0)
        self.entry_author = tk.Entry(self.add_book_window)
        self.entry_author.grid(row=2, column=1)

        tk.Label(self.add_book_window, text="Nhà xuất bản:").grid(row=3, column=0)
        self.entry_publisher = tk.Entry(self.add_book_window)
        self.entry_publisher.grid(row=3, column=1)

        tk.Label(self.add_book_window, text="Năm xuất bản:").grid(row=4, column=0)
        self.entry_year = tk.Entry(self.add_book_window)
        self.entry_year.grid(row=4, column=1)

        tk.Label(self.add_book_window, text="Thể loại:").grid(row=5, column=0)
        self.entry_genre = tk.Entry(self.add_book_window)
        self.entry_genre.grid(row=5, column=1)

        tk.Button(self.add_book_window, text="Thêm sách", command=self.add_book).grid(row=6, column=0, columnspan=2)

    def add_book(self):
        # Hàm thêm sách vào cơ sở dữ liệu
        isbn = self.entry_isbn.get()
        title = self.entry_title.get()
        author = self.entry_author.get()
        publisher = self.entry_publisher.get()
        year = self.entry_year.get()
        genre = self.entry_genre.get()

        if all([isbn, title, author, publisher, year, genre]):
            try:
                conn = psycopg2.connect(
                    dbname=self.db_name,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                cur = conn.cursor()
                query = sql.SQL("INSERT INTO {} (isbn, title, author, publisher, year, genre) VALUES (%s, %s, %s, %s, %s, %s)").format(sql.Identifier(self.table_name))
                cur.execute(query, (isbn, title, author, publisher, year, genre))
                conn.commit()
                conn.close()
                self.load_data()  # Tải lại dữ liệu sau khi thêm
                messagebox.showinfo("Thành công", "Thêm sách thành công!")
                self.add_book_window.destroy()  # Đóng cửa sổ sau khi thêm
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể thêm sách: {e}")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")

    def open_edit_book_window(self):
        self.edit_book_window = Toplevel(self.master)
        self.edit_book_window.title("Sửa thông tin sách")

        tk.Label(self.edit_book_window, text="ISBN:").grid(row=0, column=0)
        self.entry_edit_isbn = tk.Entry(self.edit_book_window)
        self.entry_edit_isbn.grid(row=0, column=1)

        tk.Label(self.edit_book_window, text="Tên sách mới:").grid(row=1, column=0)
        self.entry_edit_title = tk.Entry(self.edit_book_window)
        self.entry_edit_title.grid(row=1, column=1)

        tk.Label(self.edit_book_window, text="Tác giả mới:").grid(row=2, column=0)
        self.entry_edit_author = tk.Entry(self.edit_book_window)
        self.entry_edit_author.grid(row=2, column=1)

        tk.Label(self.edit_book_window, text="Nhà xuất bản mới:").grid(row=3, column=0)
        self.entry_edit_publisher = tk.Entry(self.edit_book_window)
        self.entry_edit_publisher.grid(row=3, column=1)

        tk.Label(self.edit_book_window, text="Năm xuất bản mới:").grid(row=4, column=0)
        self.entry_edit_year = tk.Entry(self.edit_book_window)
        self.entry_edit_year.grid(row=4, column=1)

        tk.Label(self.edit_book_window, text="Thể loại mới:").grid(row=5, column=0)
        self.entry_edit_genre = tk.Entry(self.edit_book_window)
        self.entry_edit_genre.grid(row=5, column=1)

        tk.Button(self.edit_book_window, text="Cập nhật sách", command=self.update_book).grid(row=6, column=0, columnspan=2)

    def update_book(self):
        isbn = self.entry_edit_isbn.get()
        title = self.entry_edit_title.get()
        author = self.entry_edit_author.get()
        publisher = self.entry_edit_publisher.get()
        year = self.entry_edit_year.get()
        genre = self.entry_edit_genre.get()

        if isbn and (title or author or publisher or year or genre):
            try:
                conn = psycopg2.connect(
                    dbname=self.db_name,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                cur = conn.cursor()

                # Cập nhật các trường có giá trị mới
                if title:
                    cur.execute(sql.SQL("UPDATE {} SET title = %s WHERE isbn = %s").format(sql.Identifier(self.table_name)), (title, isbn))
                if author:
                    cur.execute(sql.SQL("UPDATE {} SET author = %s WHERE isbn = %s").format(sql.Identifier(self.table_name)), (author, isbn))
                if publisher:
                    cur.execute(sql.SQL("UPDATE {} SET publisher = %s WHERE isbn = %s").format(sql.Identifier(self.table_name)), (publisher, isbn))
                if year:
                    cur.execute(sql.SQL("UPDATE {} SET year = %s WHERE isbn = %s").format(sql.Identifier(self.table_name)), (year, isbn))
                if genre:
                    cur.execute(sql.SQL("UPDATE {} SET genre = %s WHERE isbn = %s").format(sql.Identifier(self.table_name)), (genre, isbn))

                conn.commit()
                conn.close()
                self.load_data()  # Tải lại dữ liệu sau khi cập nhật
                messagebox.showinfo("Thành công", "Cập nhật sách thành công!")
                self.edit_book_window.destroy()  # Đóng cửa sổ sau khi cập nhật
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể cập nhật sách: {e}")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ISBN và ít nhất một thông tin cần cập nhật!")

    def open_delete_book_window(self):
        self.delete_book_window = Toplevel(self.master)
        self.delete_book_window.title("Xóa sách")

        tk.Label(self.delete_book_window, text="ISBN:").grid(row=0, column=0)
        self.entry_delete_isbn = tk.Entry(self.delete_book_window)
        self.entry_delete_isbn.grid(row=0, column=1)

        tk.Button(self.delete_book_window, text="Xóa sách", command=self.delete_book).grid(row=1, column=0, columnspan=2)

    def delete_book(self):
        isbn = self.entry_delete_isbn.get()

        if isbn:
            try:
                conn = psycopg2.connect(
                    dbname=self.db_name,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                cur = conn.cursor()
                query = sql.SQL("DELETE FROM {} WHERE isbn = %s").format(sql.Identifier(self.table_name))
                cur.execute(query, (isbn,))
                conn.commit()
                conn.close()
                self.load_data()  # Tải lại dữ liệu sau khi xóa
                messagebox.showinfo("Thành công", "Xóa sách thành công!")
                self.delete_book_window.destroy()  # Đóng cửa sổ sau khi xóa
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa sách: {e}")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ISBN cần xóa!")

    def open_search_book_window(self):
        self.search_book_window = Toplevel(self.master)
        self.search_book_window.title("Tìm kiếm sách")

        tk.Label(self.search_book_window, text="Tìm kiếm theo:").grid(row=0, column=0)
        self.search_option = tk.StringVar(value="title")
        options = ["isbn", "title", "author", "publisher", "year", "genre"]
        tk.OptionMenu(self.search_book_window, self.search_option, *options).grid(row=0, column=1)

        tk.Label(self.search_book_window, text="Giá trị tìm kiếm:").grid(row=1, column=0)
        self.entry_search_value = tk.Entry(self.search_book_window)
        self.entry_search_value.grid(row=1, column=1)

        tk.Button(self.search_book_window, text="Tìm kiếm", command=self.search_book).grid(row=2, column=0, columnspan=2)

    def search_book(self):
        search_field = self.search_option.get()
        search_value = self.entry_search_value.get()

        if search_value:
            try:
                conn = psycopg2.connect(
                    dbname=self.db_name,
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    port=self.port
                )
                cur = conn.cursor()
                query = sql.SQL("SELECT isbn, title, author, year, genre FROM {} WHERE {} ILIKE %s").format(
                    sql.Identifier(self.table_name),
                    sql.Identifier(search_field)
                )
                cur.execute(query, ('%' + search_value + '%',))
                rows = cur.fetchall()
                conn.close()

                # Xóa dữ liệu cũ trong Treeview
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Hiển thị kết quả tìm kiếm
                for row in rows:
                    self.tree.insert("", "end", values=row)

                if not rows:
                    messagebox.showinfo("Thông tin", "Không tìm thấy sách.")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tìm kiếm sách: {e}")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập giá trị tìm kiếm!")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()