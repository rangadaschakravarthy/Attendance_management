import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime, timedelta, timezone
db = mysql.connector.connect(host='localhost', user='root', passwd='Anurag@123', database='info')
cursor = db.cursor()
def mark_attendance(username):
    mark_window = tk.Toplevel()
    mark_window.title("Mark Attendance")
    mark_window.geometry("300x200")
    label_student_id = tk.Label(mark_window, text="Student ID:")
    label_student_id.grid(row=0, column=0)
    entry_student_id = tk.Entry(mark_window)
    entry_student_id.grid(row=0, column=1)
    label_subject = tk.Label(mark_window, text="Subject:")
    label_subject.grid(row=1, column=0)
    subjects = ["Mathematics", "Python", "Linux","Statistics"]
    subject_var = tk.StringVar(mark_window)
    subject_var.set(subjects[0])  # Default subject
    subject_dropdown = tk.OptionMenu(mark_window, subject_var, *subjects)
    subject_dropdown.grid(row=1, column=1)
    label_attendance = tk.Label(mark_window, text="Attendance Status:")
    label_attendance.grid(row=2, column=0)
    attendance_var = tk.StringVar(mark_window)
    attendance_var.set("Present")
    attendance_dropdown = tk.OptionMenu(mark_window, attendance_var, "Present", "Absent")
    attendance_dropdown.grid(row=2, column=1)
    button_submit = tk.Button(mark_window, text="Submit", command=lambda: submit_attendance(username, entry_student_id.get(), subject_var.get(), attendance_var.get()))
    button_submit.grid(row=3, column=0, columnspan=2, pady=10)
def submit_attendance(faculty_username, student_id, subject, attendance):
    try:
        current_date = datetime.now(timezone(timedelta(hours=5, minutes=30))) 
        formatted_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO attendance (username, student_id, subject, attendance, date) VALUES (%s, %s, %s, %s, %s)",(faculty_username, student_id, subject, attendance, formatted_date))
        db.commit()
        messagebox.showinfo("Success", "Attendance marked successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
def view_attendance(username):
    view_window = tk.Toplevel()
    view_window.title("View Attendance")
    view_window.geometry("300x200")
    label_student_id = tk.Label(view_window, text="Student ID:")
    label_student_id.grid(row=0, column=0)
    entry_student_id = tk.Entry(view_window)
    entry_student_id.grid(row=0, column=1)
    button_submit = tk.Button(view_window, text="Submit", command=lambda: display_attendance(entry_student_id.get()))
    button_submit.grid(row=1, column=0, columnspan=2, pady=10)
def display_attendance(student_id):
    cursor.execute("SELECT subject, attendance, date FROM attendance WHERE student_id=%s", (student_id,))
    attendance_data = cursor.fetchall()
    if not attendance_data:
        messagebox.showinfo("No Data", "No attendance data available for this student")
        return
    attendance_text = "Subject\t\tAttendance\t\tDate\n"
    for subject, attendance, date in attendance_data:
        attendance_text += f"{subject}\t\t{attendance}\t\t{date}\n"
    messagebox.showinfo("Attendance Data", attendance_text)
def reset_password(username):
    reset_password_window = tk.Toplevel()
    reset_password_window.title("Reset Password")
    reset_password_window.geometry("250x150")
    label_new_password = tk.Label(reset_password_window, text="New Password:")
    label_new_password.grid(row=0, column=0)
    entry_new_password = tk.Entry(reset_password_window, show="*")
    entry_new_password.grid(row=0, column=1)
    button_update_password = tk.Button(reset_password_window, text="Update Password", command=lambda: update_password(username, entry_new_password.get()))
    button_update_password.grid(row=1, column=0, columnspan=2, pady=10)
def update_password(username, new_password):
    try:
        cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_password, username))
        db.commit()
        messagebox.showinfo("Reset Password", "Password updated successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
def change_password(username):
    change_password_window = tk.Toplevel()
    change_password_window.title("Change Password")
    change_password_window.geometry("250x150")
    label_new_password = tk.Label(change_password_window, text="New Password:")
    label_new_password.grid(row=0, column=0)
    entry_new_password = tk.Entry(change_password_window, show="*")
    entry_new_password.grid(row=0, column=1)
    button_update_password = tk.Button(change_password_window, text="Update Password", command=lambda: update_password(username, entry_new_password.get()))
    button_update_password.grid(row=1, column=0, columnspan=2, pady=10)
def faculty_login(username):
    faculty_root = tk.Toplevel()
    faculty_root.title("Faculty Homepage")
    faculty_root.geometry("300x300")
    button_mark_attendance = tk.Button(faculty_root, text="Mark Attendance", command=lambda: mark_attendance(username))
    button_mark_attendance.pack(pady=10)
    button_reset_password = tk.Button(faculty_root, text="Reset Password", command=lambda: reset_password(username))
    button_reset_password.pack(pady=10)
def student_login(username):
    student_root = tk.Toplevel()
    student_root.title("Student Homepage")
    student_root.geometry("300x300")
    button_view_attendance = tk.Button(student_root, text="View Attendance", command=lambda: view_attendance(username))
    button_view_attendance.pack(pady=10)
    button_reset_password = tk.Button(student_root, text="Reset Password", command=lambda: reset_password(username))
    button_reset_password.pack(pady=10)
def login():
    username = entry_username.get()
    password = entry_password.get()

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login Successful", f"Welcome {username}!")
        role = user[3]
        if role == "faculty":
            faculty_login(username)
        elif role == "student":
            student_login(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
root = tk.Tk()
root.title("Attendance Management System")
root.geometry("400x400")
label_username = tk.Label(root, text="Username:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()
label_password = tk.Label(root, text="Password:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()
button_login = tk.Button(root, text="Login", command=login)
button_login.pack()
root.mainloop()