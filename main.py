import sqlite3
import tkinter as tk
from tkinter import messagebox

from PIL import Image
from customtkinter import *

import Capture_Image
import Recognize
import Train_Image
import check_camera


# Function to initialize the login window
def initialize_login():
    login_window = CTk()
    login_window.geometry("500x500")
    login_window.title("Login Form")

    # Database connection
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Ensure the users table exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()

    def login():
        entered_username = user_entry.get()
        entered_password = user_pass.get()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (entered_username, entered_password))
        result = cursor.fetchone()

        if result:
            tk.messagebox.showinfo(title="Login Successful", message="You have logged in Successfully")
            login_window.destroy()
            initialize_main_app()
        else:
            tk.messagebox.showerror(title="Login Failed", message="Invalid Username and password")

    def open_registration_window():
        registration_window = CTkToplevel(login_window)
        registration_window.title("Register New User")

        lblUsername = CTkLabel(registration_window, text="Username:")
        lblUsername.pack()
        entUsername = CTkEntry(registration_window)
        entUsername.pack()

        lblPassword = CTkLabel(registration_window, text="Password:")
        lblPassword.pack()
        entPassword = CTkEntry(registration_window, show="*")
        entPassword.pack()

        inner_btnRegister = CTkButton(registration_window, text="Register",
                                      command=lambda: register_user(entUsername, entPassword))
        inner_btnRegister.pack()

    def register_user(username_entry, password_entry):
        username = username_entry.get()
        password = password_entry.get()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        if result:
            tk.messagebox.showerror("Error", "Username already exists.")
            return

        cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
        conn.commit()

        tk.messagebox.showinfo("Success", "New user registered successfully.")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

    label = CTkLabel(login_window, text="Login Page", font=("Helvetica", 16))
    label.pack(pady=20)

    frame = CTkFrame(master=login_window)
    frame.pack(pady=20, padx=40, fill='both', expand=True)

    label = CTkLabel(master=frame, text='Please Enter Your Login details')
    label.pack(pady=12, padx=10)

    user_entry = CTkEntry(master=frame, placeholder_text="Username")
    user_entry.pack(pady=12, padx=10)

    user_pass = CTkEntry(master=frame, placeholder_text="Password", show="*")
    user_pass.pack(pady=12, padx=10)

    button = CTkButton(master=frame, text='Login', command=login)
    button.pack(pady=12, padx=10)

    btnRegister = CTkButton(master=frame, text="Register", command=open_registration_window)
    btnRegister.pack(pady=12, padx=10)

    checkbox = CTkCheckBox(master=frame, text='Remember Me')
    checkbox.pack(pady=12, padx=10)

    login_window.mainloop()


def initialize_main_app():
    root = CTk()
    root.geometry("1280x720")
    root.title("Face Recognition Attendance System Neoscape University")
    root.configure(bg='royalblue')

    def check_camera_command():
        check_camera.camera()

    def capture_faces_command():
        def submit_details():
            reg_number = reg_entry.get()
            full_name = full_name_entry.get()
            if not reg_number or not full_name:
                messagebox.showerror("Error", "Both fields are required.")
                return

            Capture_Image.capture_images(reg_number, full_name)
            detail_window.destroy()
            start_capture_button.configure(state=NORMAL)  # Enable the Start Capture button

        def cancel_details():
            detail_window.destroy()

        detail_window = CTkToplevel(root)
        detail_window.title("Enter Details")
        detail_window.grab_set()  # Prevents clicking outside the window to close it

        CTkLabel(detail_window, text="Registration Number").grid(row=0, column=0, padx=10, pady=10)
        CTkLabel(detail_window, text="Full Name").grid(row=1, column=0, padx=10, pady=10)

        reg_entry = CTkEntry(detail_window)
        full_name_entry = CTkEntry(detail_window)

        reg_entry.grid(row=0, column=1, padx=10, pady=10)
        full_name_entry.grid(row=1, column=1, padx=10, pady=10)

        submit_button = CTkButton(detail_window, text="Submit", command=submit_details)
        submit_button.grid(row=2, column=0, pady=10)

        cancel_button = CTkButton(detail_window, text="Cancel", command=cancel_details)
        cancel_button.grid(row=2, column=1, pady=10)

    def train_images_command():
        Train_Image.TrainImages()

    def recognize_faces_command():
        Recognize.recognize_attendance()

    def quit_command():
        root.destroy()

    def clear_screen():
        for widget in root.winfo_children():
            widget.destroy()

    def create_menu():
        clear_screen()

        menu_frame = CTkFrame(root, width=1080, height=720)
        menu_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        CTkLabel(menu_frame, text="Facial Recognition Attendance System Neoscape University",
                 font=("Helvetica", 16)).pack()

        camera_icon_image = Image.open('Icons/action-camera.png')
        capture_icon_image = Image.open('Icons/face-detection.png')
        Train_icon_image = Image.open("Icons/train.png")
        Recognition_icon_image = Image.open("Icons/clipboard.png")

        camera_icon = CTkImage(dark_image=camera_icon_image, light_image=camera_icon_image, size=(16, 16))
        capture_icon = CTkImage(dark_image=capture_icon_image, light_image=capture_icon_image, size=(16, 16))
        Train_icon = CTkImage(dark_image=Train_icon_image, light_image=Train_icon_image, size=(16, 16))
        Recognizer_icon = CTkImage(dark_image=Recognition_icon_image, light_image=Recognition_icon_image, size=(16, 16))

        options = [
            ("Check Camera", check_camera_command, 'lightblue', camera_icon),
            ("Capture Faces", capture_faces_command, 'royalblue', capture_icon),
            ("Train Images", train_images_command, 'lightgray', Train_icon),
            ("Recognition & Attendance", recognize_faces_command, 'lightgreen', Recognizer_icon),
            ("Quit", quit_command, 'lightcoral', None)
        ]

        for text, command, color, icon in options:
            button = CTkButton(
                menu_frame,
                text=text,
                command=command,
                fg_color=color,
                text_color='black',
                image=icon,
                compound='left'
            )
            button.pack(pady=10)

            # Initialize the Start Capture button as disabled
        global start_capture_button
        start_capture_button = CTkButton(menu_frame, text="Start Capture", fg_color='orange', text_color='white',
                                         state=DISABLED)
        start_capture_button.pack(pady=20)

    set_appearance_mode("dark")
    set_default_color_theme("blue")

    root.update_idletasks()
    create_menu()

    root.mainloop()


initialize_login()
