import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("400x300")

        # Connect to SQLite database
        self.connection = sqlite3.connect("library.db")
        self.create_tables()

        # Define colors and fonts
        self.bg_color = "#f0f0f0"
        self.button_color = "#3498db"
        self.label_font = ("Helvetica", 16, "bold")
        self.button_font = ("Helvetica", 14, "bold")

        self.current_page = None  # To keep track of the current page
        self.home_page()

    def create_tables(self):
        # Create tables if they don't exist
        with self.connection:
            cursor = self.connection.cursor()

            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    user_name TEXT
                )
            ''')

            # Books table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    book_id TEXT PRIMARY KEY,
                    title TEXT,
                    available BOOLEAN
                )
            ''')

            # BorrowedBooks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS borrowed_books (
                    user_id TEXT,
                    book_id TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (book_id) REFERENCES books(book_id)
                )
            ''')

    def home_page(self):
        if self.current_page:
            self.current_page.destroy()

        self.current_page = tk.Frame(self.root, padx=20, pady=20, bg=self.bg_color)
        self.current_page.pack()

        tk.Label(self.current_page, text="Library Management System", font=self.label_font, bg=self.bg_color).grid(row=0, column=0, pady=10)

        user_button = tk.Button(self.current_page, text="User", command=self.user_login, bg=self.button_color, font=self.button_font)
        user_button.grid(row=1, column=0, pady=5)

        admin_button = tk.Button(self.current_page, text="Admin", command=self.admin_login, bg=self.button_color, font=self.button_font)
        admin_button.grid(row=2, column=0, pady=5)

    def user_login(self):
        if self.current_page:
            self.current_page.destroy()

        self.current_page = tk.Frame(self.root, padx=20, pady=20, bg=self.bg_color)
        self.current_page.pack()

        tk.Label(self.current_page, text="User Page", font=self.label_font, bg=self.bg_color).grid(row=0, column=0, pady=10)
        tk.Button(self.current_page, text="Issue Book", command=self.issue_book, bg=self.button_color, font=self.button_font).grid(row=1, column=0, pady=5)
        tk.Button(self.current_page, text="Return Book", command=self.return_book, bg=self.button_color, font=self.button_font).grid(row=2, column=0, pady=5)
        tk.Button(self.current_page, text="View User Books", command=self.view_user_books, bg=self.button_color, font=self.button_font).grid(row=3, column=0, pady=5)
        tk.Button(self.current_page, text="Home", command=self.home_page, bg=self.button_color, font=self.button_font).grid(row=4, column=0, pady=5)

    def admin_login(self):
        if self.current_page:
            self.current_page.destroy()

        self.current_page = tk.Frame(self.root, padx=20, pady=20, bg=self.bg_color)
        self.current_page.pack()

        tk.Label(self.current_page, text="Admin Page", font=self.label_font, bg=self.bg_color).grid(row=0, column=0, pady=10)
        tk.Button(self.current_page, text="Add User", command=self.add_user, bg=self.button_color, font=self.button_font).grid(row=1, column=0, pady=5)
        tk.Button(self.current_page, text="Remove User", command=self.remove_user, bg=self.button_color, font=self.button_font).grid(row=2, column=0, pady=5)
        tk.Button(self.current_page, text="Add Book", command=self.add_book, bg=self.button_color, font=self.button_font).grid(row=3, column=0, pady=5)
        tk.Button(self.current_page, text="Remove Book", command=self.remove_book, bg=self.button_color, font=self.button_font).grid(row=4, column=0, pady=5)
        tk.Button(self.current_page, text="View User List", command=self.view_user_list, bg=self.button_color, font=self.button_font).grid(row=5, column=0, pady=5)
        tk.Button(self.current_page, text="View Book List", command=self.view_book_list, bg=self.button_color, font=self.button_font).grid(row=6, column=0, pady=5)
        tk.Button(self.current_page, text="View Overdue Books", command=self.view_overdue_books, bg=self.button_color, font=self.button_font).grid(row=7, column=0, pady=5)
        tk.Button(self.current_page, text="Home", command=self.home_page, bg=self.button_color, font=self.button_font).grid(row=8, column=0, pady=5)

    def issue_book(self):
        user_id = simpledialog.askstring("User ID", "Enter User ID:")
        book_id = simpledialog.askstring("Book ID", "Enter Book ID:")

        if user_id and book_id:
            with self.connection:
                cursor = self.connection.cursor()

                # Check if user and book exist
                cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
                user_data = cursor.fetchone()
                cursor.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
                book_data = cursor.fetchone()

                if user_data and book_data:
                    if book_data[2]:  # Check if the book is available
                        # Update borrowed_books table
                        cursor.execute("INSERT INTO borrowed_books (user_id, book_id) VALUES (?, ?)", (user_id, book_id))

                        # Update books table
                        cursor.execute("UPDATE books SET available = 0 WHERE book_id=?", (book_id,))

                        messagebox.showinfo("Issue Book", f"Book '{book_data[1]}' issued to user '{user_data[1]}'")
                    else:
                        messagebox.showwarning("Book Not Available", f"Book '{book_data[1]}' is not available")
                else:
                    messagebox.showerror("Error", "Invalid User ID or Book ID")
        else:
            messagebox.showerror("Error", "User ID and Book ID are required")

    def return_book(self):
        user_id = simpledialog.askstring("User ID", "Enter User ID:")
        book_id = simpledialog.askstring("Book ID", "Enter Book ID:")

        if user_id and book_id:
            with self.connection:
                cursor = self.connection.cursor()

                # Check if user and book exist
                cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
                user_data = cursor.fetchone()
                cursor.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
                book_data = cursor.fetchone()

                if user_data and book_data:
                    cursor.execute("SELECT * FROM borrowed_books WHERE user_id=? AND book_id=?", (user_id, book_id))
                    borrowed_data = cursor.fetchone()

                    if borrowed_data:
                        # Update borrowed_books table
                        cursor.execute("DELETE FROM borrowed_books WHERE user_id=? AND book_id=?", (user_id, book_id))

                        # Update books table
                        cursor.execute("UPDATE books SET available = 1 WHERE book_id=?", (book_id,))

                        messagebox.showinfo("Return Book", f"Book '{book_data[1]}' returned by user '{user_data[1]}'")
                    else:
                        messagebox.showwarning("Invalid Return", f"Book '{book_data[1]}' was not issued to this user")
                else:
                    messagebox.showerror("Error", "Invalid User ID or Book ID")
        else:
            messagebox.showerror("Error", "User ID and Book ID are required")

    def add_user(self):
        user_id = simpledialog.askstring("User ID", "Enter User ID:")
        user_name = simpledialog.askstring("User Name", "Enter User Name:")

        if user_id and user_name:
            with self.connection:
                cursor = self.connection.cursor()

                # Check if user already exists
                cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
                existing_user = cursor.fetchone()

                if not existing_user:
                    # Insert new user
                    cursor.execute("INSERT INTO users (user_id, user_name) VALUES (?, ?)", (user_id, user_name))
                    messagebox.showinfo("User Added", f"User '{user_name}' added successfully")
                else:
                    messagebox.showwarning("User Exists", f"User with ID '{user_id}' already exists")
        else:
            messagebox.showerror("Error", "User ID and User Name are required")

    def remove_user(self):
        user_id = simpledialog.askstring("User ID", "Enter User ID to remove:")

        if user_id:
            with self.connection:
                cursor = self.connection.cursor()

                # Check if user exists
                cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
                existing_user = cursor.fetchone()

                if existing_user:
                    # Remove user
                    cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
                    # Remove user's borrowed books
                    cursor.execute("DELETE FROM borrowed_books WHERE user_id=?", (user_id,))
                    messagebox.showinfo("User Removed", f"User with ID '{user_id}' removed successfully")
                else:
                    messagebox.showwarning("User Not Found", f"User with ID '{user_id}' does not exist")
        else:
            messagebox.showerror("Error", "User ID is required")

    def add_book(self):
        book_id = simpledialog.askstring("Book ID", "Enter Book ID:")
        book_title = simpledialog.askstring("Book Title", "Enter Book Title:")

        if book_id and book_title:
            with self.connection:
                cursor = self.connection.cursor()

                # Check if book already exists
                cursor.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
                existing_book = cursor.fetchone()

                if not existing_book:
                    # Insert new book
                    cursor.execute("INSERT INTO books (book_id, title, available) VALUES (?, ?, ?)", (book_id, book_title, 1))
                    messagebox.showinfo("Book Added", f"Book '{book_title}' added successfully")
                else:
                    messagebox.showwarning("Book Exists", f"Book with ID '{book_id}' already exists")
        else:
            messagebox.showerror("Error", "Book ID and Book Title are required")

    def remove_book(self):
        book_id = simpledialog.askstring("Book ID", "Enter Book ID to remove:")

        if book_id:
            with self.connection:
                cursor = self.connection.cursor()

                # Check if book exists
                cursor.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
                existing_book = cursor.fetchone()

                if existing_book:
                    # Remove book
                    cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
                    # Remove book from borrowed_books
                    cursor.execute("DELETE FROM borrowed_books WHERE book_id=?", (book_id,))
                    messagebox.showinfo("Book Removed", f"Book with ID '{book_id}' removed successfully")
                else:
                    messagebox.showwarning("Book Not Found", f"Book with ID '{book_id}' does not exist")
        else:
            messagebox.showerror("Error", "Book ID is required")

    def view_user_list(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

        user_list = "\n".join([f"User ID: {user[0]}, User Name: {user[1]}" for user in users])
        messagebox.showinfo("User List", f"User List:\n\n{user_list}")

    def view_book_list(self):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()

        book_list = "\n".join([f"Book ID: {book[0]}, Title: {book[1]}, Available: {'Yes' if book[2] else 'No'}" for book in books])
        messagebox.showinfo("Book List", f"Book List:\n\n{book_list}")

    def view_user_books(self):
        user_id = simpledialog.askstring("User ID", "Enter User ID to view books:")

        if user_id:
            with self.connection:
                cursor = self.connection.cursor()

                # Check if user exists
                cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
                existing_user = cursor.fetchone()

                if existing_user:
                    # Retrieve user's borrowed books
                    cursor.execute("SELECT books.title FROM borrowed_books JOIN books ON borrowed_books.book_id = books.book_id WHERE user_id=?", (user_id,))
                    borrowed_books = cursor.fetchall()

                    if borrowed_books:
                        borrowed_books_list = "\n".join([f"Book: {book[0]}" for book in borrowed_books])
                        messagebox.showinfo("Borrowed Books", f"Borrowed Books for User '{existing_user[1]}':\n\n{borrowed_books_list}")
                    else:
                        messagebox.showinfo("No Borrowed Books", f"No books borrowed by User '{existing_user[1]}'")
                else:
                    messagebox.showwarning("User Not Found", f"User with ID '{user_id}' does not exist")
        else:
            messagebox.showerror("Error", "User ID is required")

    def view_overdue_books(self):
        with self.connection:
            cursor = self.connection.cursor()

            # Retrieve overdue books
            cursor.execute("SELECT users.user_id, users.user_name, books.title FROM borrowed_books JOIN users ON borrowed_books.user_id = users.user_id JOIN books ON borrowed_books.book_id = books.book_id WHERE books.available = 0")
            overdue_books = cursor.fetchall()

        if overdue_books:
            overdue_books_list = "\n".join([f"User ID: {book[0]}, User Name: {book[1]}, Book: {book[2]}" for book in overdue_books])
            messagebox.showinfo("Overdue Books", f"Overdue Books:\n\n{overdue_books_list}")
        else:
            messagebox.showinfo("No Overdue Books", "No books are currently overdue")

    def clear_frame(self):
        for widget in self.login_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()


