from flask import Flask, render_template, redirect, url_for, request, session, flash
import psycopg2
from psycopg2 import sql
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Thay bằng một chuỗi bí mật

# Thông tin kết nối cơ sở dữ liệu
DB_NAME = 'Library_db'  # Thay đổi tên cơ sở dữ liệu nếu cần
DB_USER = 'postgres'     # Thay bằng tên người dùng PostgreSQL của bạn
DB_PASSWORD = 'anhthu'   # Thay bằng mật khẩu PostgreSQL của bạn
DB_HOST = 'localhost'
DB_PORT = '5432'
TABLE_NAME = 'books'     # Thay đổi tên bảng nếu cần

# Thông tin đăng nhập (có thể thay đổi hoặc lấy từ cơ sở dữ liệu)
USERNAME = 'admin'
PASSWORD = 'admin'

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD ,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
        return None

def is_logged_in():
    return session.get('logged_in')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash("Vui lòng đăng nhập để truy cập trang này.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.context_processor
def inject_current_year():
    import datetime
    return {'current_year': datetime.datetime.utcnow().year, 'is_logged_in': is_logged_in}

@app.route('/', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('main_menu'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Kiểm tra tên đăng nhập và mật khẩu
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('main_menu'))
        else:
            flash("Tên đăng nhập hoặc mật khẩu không đúng!", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Bạn đã đăng xuất.", "info")
    return redirect(url_for('login'))

@app.route('/main_menu')
@login_required
def main_menu():
    conn = get_connection()
    books = []
    if conn:
        try:
            cur = conn.cursor()
            query = sql.SQL("SELECT isbn, title, author, year, genre FROM {}").format(sql.Identifier(TABLE_NAME))
            cur.execute(query)
            books = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
            flash(f"Không thể tải dữ liệu: {e}", "danger")
    else:
        flash("Không thể kết nối cơ sở dữ liệu.", "danger")
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        isbn = request.form.get('isbn').strip()
        title = request.form.get('title').strip()
        author = request.form.get('author').strip()
        publisher = request.form.get('publisher').strip()
        year = request.form.get('year').strip()
        genre = request.form.get('genre').strip()

        if all([isbn, title, author, publisher, year, genre]):
            try:
                conn = get_connection()
                cur = conn.cursor()
                query = sql.SQL("INSERT INTO {} (isbn, title, author, publisher, year, genre) VALUES (%s, %s, %s, %s, %s, %s)").format(sql.Identifier(TABLE_NAME))
                cur.execute(query, (isbn, title, author, publisher, year, genre))
                conn.commit()
                cur.close()
                conn.close()
                flash("Thêm sách thành công!", "success")
                return redirect(url_for('main_menu'))
            except Exception as e:
                flash(f"Không thể thêm sách: {e}", "danger")
        else:
            flash("Vui lòng nhập đầy đủ thông tin!", "warning")
    return render_template('add_book.html')

@app.route('/edit_book/<isbn>', methods=['GET', 'POST'])
@login_required
def edit_book(isbn):
    conn = get_connection()
    book = None
    if conn:
        try:
            cur = conn.cursor()
            query = sql.SQL("SELECT isbn, title, author, publisher, year, genre FROM {} WHERE isbn = %s").format(sql.Identifier(TABLE_NAME))
            cur.execute(query, (isbn,))
            row = cur.fetchone()
            if row:
                book = {
                    'isbn': row[0],
                    'title': row[1],
                    'author': row[2],
                    'publisher': row[3],
                    'year': row[4],
                    'genre': row[5]
                }
            cur.close()
            conn.close()
        except Exception as e:
            flash(f"Không thể tải dữ liệu sách: {e}", "danger")
    else:
        flash("Không thể kết nối cơ sở dữ liệu.", "danger")

    if not book:
        flash("Không tìm thấy sách.", "danger")
        return redirect(url_for('main_menu'))

    if request.method == 'POST':
        title = request.form.get('title').strip()
        author = request.form.get('author').strip()
        publisher = request.form.get('publisher').strip()
        year = request.form.get('year').strip()
        genre = request.form.get('genre').strip()

        if any([title, author, publisher, year, genre]):
            try:
                conn = get_connection()
                cur = conn.cursor()
                if title:
                    cur.execute(sql.SQL("UPDATE {} SET title = %s WHERE isbn = %s").format(sql.Identifier(TABLE_NAME)), (title, isbn))
                if author:
                    cur.execute(sql.SQL("UPDATE {} SET author = %s WHERE isbn = %s").format(sql.Identifier(TABLE_NAME)), (author, isbn))
                if publisher:
                    cur.execute(sql.SQL("UPDATE {} SET publisher = %s WHERE isbn = %s").format(sql.Identifier(TABLE_NAME)), (publisher, isbn))
                if year:
                    cur.execute(sql.SQL("UPDATE {} SET year = %s WHERE isbn = %s").format(sql.Identifier(TABLE_NAME)), (year, isbn))
                if genre:
                    cur.execute(sql.SQL("UPDATE {} SET genre = %s WHERE isbn = %s").format(sql.Identifier(TABLE_NAME)), (genre, isbn))
                conn.commit()
                cur.close()
                conn.close()
                flash("Cập nhật sách thành công!", "success")
                return redirect(url_for('main_menu'))
            except Exception as e:
                flash(f"Không thể cập nhật sách: {e}", "danger")
        else:
            flash("Vui lòng nhập ít nhất một thông tin để cập nhật!", "warning")
    return render_template('edit_book.html', book=book)

@app.route('/delete_book/<isbn>', methods=['POST'])
@login_required
def delete_book(isbn):
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = sql.SQL("DELETE FROM {} WHERE isbn = %s").format(sql.Identifier(TABLE_NAME))
        cur.execute(query, (isbn,))
        conn.commit()
        cur.close()
        conn.close()
        flash("Xóa sách thành công!", "success")
    except Exception as e:
        flash(f"Không thể xóa sách: {e}", "danger")
    return redirect(url_for('main_menu'))

@app.route('/search_book', methods=['GET', 'POST'])
@login_required
def search_book():
    if request.method == 'POST':
        search_field = request.form.get('search_field')
        search_value = request.form.get('search_value').strip()
        if search_value:
            try:
                conn = get_connection()
                cur = conn.cursor()
                query = sql.SQL("SELECT isbn, title, author, year, genre FROM {} WHERE {} ILIKE %s").format(
                    sql.Identifier(TABLE_NAME),
                    sql.Identifier(search_field)
                )
                cur.execute(query, ('%' + search_value + '%',))
                books = cur.fetchall()
                cur.close()
                conn.close()
                if books:
                    return render_template('search_results.html', books=books)
                else:
                    flash("Không tìm thấy sách.", "info")
                    return redirect(url_for('main_menu'))
            except Exception as e:
                flash(f"Không thể tìm kiếm sách: {e}", "danger")
        else:
            flash("Vui lòng nhập giá trị tìm kiếm!", "warning")
    return render_template('search_book.html')

if __name__ == '__main__':
    app.run(debug=True)