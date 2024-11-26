import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime, timedelta

# File to store library data
DATA_FILE = r"C:\Users\omara\OneDrive\Desktop\AutoCAD\library_data.json"

# Initialize library data
library_data = {
    "books": [],
    "borrowed_books": [],
    "students": []  # Add a list to track students
}

# Load data from file
def load_data():
    global library_data
    try:
        with open(DATA_FILE, "r") as file:
            library_data = json.load(file)
            if "students" not in library_data:
                library_data["students"] = []  # Ensure the students key exists
    except FileNotFoundError:
        save_data()

# Save data to file
def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(library_data, file, indent=4)

# Add a book to the library
def add_book():
    title = title_entry.get()
    author = author_entry.get()
    year = year_entry.get()

    if not title or not author or not year:
        messagebox.showerror("Error", "All fields are required!")
        return

    library_data["books"].append({"title": title, "author": author, "year": year, "available": True})
    save_data()
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Book added successfully!")
    refresh_books()

# Refresh the list of books
def refresh_books():
    for row in books_tree.get_children():
        books_tree.delete(row)

    for book in library_data["books"]:
        books_tree.insert("", tk.END, values=(book["title"], book["author"], book["year"], "Yes" if book["available"] else "No"))

# Refresh the list of borrowed books
def refresh_borrowed_books():
    for row in borrowed_books_tree.get_children():
        borrowed_books_tree.delete(row)

    for borrowed_book in library_data["borrowed_books"]:
        borrowed_books_tree.insert("", tk.END, values=(borrowed_book["book"]["title"], borrowed_book["borrower"], borrowed_book["due_date"]))

# Borrow a book
def borrow_book():
    selected = books_tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a book!")
        return

    index = books_tree.index(selected[0])
    book = library_data["books"][index]

    if not book["available"]:
        messagebox.showerror("Error", "Book is not available!")
        return

    borrower = borrower_entry.get()
    days = days_entry.get()

    if not borrower or not days:
        messagebox.showerror("Error", "Borrower and days are required!")
        return

    book["available"] = False
    due_date = (datetime.now() + timedelta(days=int(days))).strftime("%Y-%m-%d")
    library_data["borrowed_books"].append({"book": book, "borrower": borrower, "due_date": due_date})
    save_data()
    borrower_entry.delete(0, tk.END)
    days_entry.delete(0, tk.END)
    refresh_books()
    refresh_borrowed_books()
    messagebox.showinfo("Success", "Book borrowed successfully!")

# Return a book
def return_book():
    selected = books_tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a book!")
        return

    index = books_tree.index(selected[0])
    book = library_data["books"][index]

    if book["available"]:
        messagebox.showerror("Error", "Book is already available!")
        return

    book["available"] = True
    library_data["borrowed_books"] = [b for b in library_data["borrowed_books"] if b["book"]["title"] != book["title"]]
    save_data()
    refresh_books()
    refresh_borrowed_books()
    messagebox.showinfo("Success", "Book returned successfully!")

# Delete a book
def delete_book():
    selected = books_tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a book!")
        return

    index = books_tree.index(selected[0])
    book = library_data["books"][index]

    if book["available"]:
        messagebox.showerror("Error", "Only borrowed books can be deleted!")
        return

    library_data["books"].pop(index)
    library_data["borrowed_books"] = [b for b in library_data["borrowed_books"] if b["book"]["title"] != book["title"]]
    save_data()
    refresh_books()
    refresh_borrowed_books()
    messagebox.showinfo("Success", "Book deleted successfully!")

# Check overdue books
def check_overdue():
    overdue_books = [b for b in library_data["borrowed_books"] if datetime.strptime(b["due_date"], "%Y-%m-%d") < datetime.now()]
    if overdue_books:
        overdue_list = "\n".join([f"{b['book']['title']} (Borrower: {b['borrower']}, Due Date: {b['due_date']})" for b in overdue_books])
        messagebox.showinfo("Overdue Books", f"Overdue books:\n\n{overdue_list}")
    else:
        messagebox.showinfo("Overdue Books", "No overdue books!")

# Search for books by title or author
def search_books():
    query = search_entry.get().lower()
    for row in books_tree.get_children():
        books_tree.delete(row)

    for book in library_data["books"]:
        if query in book["title"].lower() or query in book["author"].lower():
            books_tree.insert("", tk.END, values=(book["title"], book["author"], book["year"], "Yes" if book["available"] else "No"))

# Add a student to the library system
def add_student():
    student_name = student_name_entry.get()
    student_id = student_id_entry.get()

    if not student_name or not student_id:
        messagebox.showerror("Error", "All fields are required!")
        return

    library_data["students"].append({"name": student_name, "id": student_id})
    save_data()
    student_name_entry.delete(0, tk.END)
    student_id_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Student added successfully!")
    refresh_students()

# Refresh the list of students
def refresh_students():
    for row in students_tree.get_children():
        students_tree.delete(row)

    for student in library_data["students"]:
        students_tree.insert("", tk.END, values=(student["name"], student["id"]))

# Initialize the GUI
root = tk.Tk()
root.title("Library Management System")
root.geometry("1024x768")  # Adjusted screen size
root.configure(bg="#f0f8ff")
root.iconbitmap(r"C:\Users\omara\OneDrive\Desktop\AutoCAD\download.ico")  # Add this line to set the logo

# Add a canvas and a scrollbar to the main window
main_frame = tk.Frame(root, bg="#f0f8ff")
main_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(main_frame, bg="#f0f8ff")
scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

second_frame = tk.Frame(canvas, bg="#f0f8ff")

canvas.create_window((0, 0), window=second_frame, anchor="nw")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

second_frame.bind("<Configure>", on_configure)

# Enable mousewheel scrolling
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Add Student Section
tk.Label(second_frame, text="Add Student", bg="#f0f8ff", font=("Arial", 16, "bold")).pack(pady=10)
student_frame = tk.Frame(second_frame, bg="#f0f8ff")
student_frame.pack()

tk.Label(student_frame, text="Student Name:", bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5)
student_name_entry = tk.Entry(student_frame)
student_name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(student_frame, text="Student ID:", bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5)
student_id_entry = tk.Entry(student_frame)
student_id_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(student_frame, text="Add Student", command=add_student, bg="#008080", fg="white").grid(row=2, columnspan=2, pady=10)

# Students List Section
tk.Label(second_frame, text="Students List", bg="#f0f8ff", font=("Arial", 16, "bold")).pack(pady=10)
students_frame = tk.Frame(second_frame, bg="#f0f8ff")
students_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
students_scrollbar = tk.Scrollbar(students_frame, orient=tk.VERTICAL)
students_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
student_columns = ("Name", "ID")
students_tree = ttk.Treeview(students_frame, columns=student_columns, show="headings", yscrollcommand=students_scrollbar.set)
students_scrollbar.config(command=students_tree.yview)
for col in student_columns:
    students_tree.heading(col, text=col)
students_tree.pack(fill=tk.BOTH, expand=True)

# Add Book Section
tk.Label(second_frame, text="Add Book", bg="#f0f8ff", font=("Arial", 16, "bold")).pack(pady=10)
add_frame = tk.Frame(second_frame, bg="#f0f8ff")
add_frame.pack()

tk.Label(add_frame, text="Title:", bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5)
title_entry = tk.Entry(add_frame)
title_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(add_frame, text="Author:", bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5)
author_entry = tk.Entry(add_frame)
author_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(add_frame, text="Year:", bg="#f0f8ff").grid(row=2, column=0, padx=5, pady=5)
year_entry = tk.Entry(add_frame)
year_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Button(add_frame, text="Add Book", command=add_book, bg="#008080", fg="white").grid(row=3, columnspan=2, pady=10)

# Books List Section
tk.Label(second_frame, text="Books List", bg="#f0f8ff", font=("Arial", 16, "bold")).pack(pady=10)
books_frame = tk.Frame(second_frame, bg="#f0f8ff")
books_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
books_scrollbar = tk.Scrollbar(books_frame, orient=tk.VERTICAL)
books_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
columns = ("Title", "Author", "Year", "Available")
books_tree = ttk.Treeview(books_frame, columns=columns, show="headings", yscrollcommand=books_scrollbar.set)
books_scrollbar.config(command=books_tree.yview)
for col in columns:
    books_tree.heading(col, text=col)
books_tree.pack(fill=tk.BOTH, expand=True)

# Borrowed Books List Section
tk.Label(second_frame, text="Borrowed Books", bg="#f0f8ff", font=("Arial", 16, "bold")).pack(pady=10)
borrowed_frame = tk.Frame(second_frame, bg="#f0f8ff")
borrowed_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
borrowed_scrollbar = tk.Scrollbar(borrowed_frame, orient=tk.VERTICAL)
borrowed_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
borrowed_columns = ("Title", "Borrower", "Due Date")
borrowed_books_tree = ttk.Treeview(borrowed_frame, columns=borrowed_columns, show="headings", yscrollcommand=borrowed_scrollbar.set)
borrowed_scrollbar.config(command=borrowed_books_tree.yview)
for col in borrowed_columns:
    borrowed_books_tree.heading(col, text=col)
borrowed_books_tree.pack(fill=tk.BOTH, expand=True)

# Search Section
tk.Label(second_frame, text="Search Books", bg="#f0f8ff", font=("Arial", 16, "bold")).pack(pady=10)
search_frame = tk.Frame(second_frame, bg="#f0f8ff")
search_frame.pack()

tk.Label(search_frame, text="Search:", bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5)
search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Button(search_frame, text="Search", command=search_books, bg="#008080", fg="white").grid(row=0, column=2, padx=5, pady=5)

# Borrow/Return/Delete Section
borrow_frame = tk.Frame(second_frame, bg="#f0f8ff")
borrow_frame.pack(pady=10)

tk.Label(borrow_frame, text="Borrower:", bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5)
borrower_entry = tk.Entry(borrow_frame)
borrower_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(borrow_frame, text="Days:", bg="#f0f8ff").grid(row=1, column=0, padx=5, pady=5)
days_entry = tk.Entry(borrow_frame)
days_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(borrow_frame, text="Borrow Book", command=borrow_book, bg="#008080", fg="white").grid(row=2, column=0, pady=10)
tk.Button(borrow_frame, text="Return Book", command=return_book, bg="#008080", fg="white").grid(row=2, column=1, pady=10)
tk.Button(borrow_frame, text="Delete Book", command=delete_book, bg="#ff4500", fg="white").grid(row=2, column=2, pady=10)

# Overdue Books Button
tk.Button(second_frame, text="Check Overdue Books", command=check_overdue, bg="#dc143c", fg="white").pack(pady=10)

# Initialize the data and refresh the GUI
load_data()
refresh_books()
refresh_borrowed_books()
refresh_students()  # Refresh the students list

# Run the GUI loop
root.mainloop()
