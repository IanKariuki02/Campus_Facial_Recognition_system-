from tkinter import *
from PIL import Image, ImageTk
from student import Student
from face_recognition import Face_Recognition
from train import Train
from attendance import Attendance
from data_visualization import DataVisualization
from help import Help
import pyttsx3
import sqlite3
import tkinter
from tkinter import ttk
from tkinter import messagebox
import os
import re

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 is for female voice and 0 is for male voice


def main():
    win = Tk()
    app = login_window(win)
    win.mainloop()


# Function to speak the provided query
def speak_va(transcribed_query):
    engine.say(transcribed_query)
    engine.runAndWait()


# Database connection and table creation
conn = sqlite3.connect('neoscapedb.sqlite')
cursor = conn.cursor()

# Create login_user table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS login_user (
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT NOT NULL PRIMARY KEY,
                    securityQ TEXT NOT NULL,
                    securityA TEXT NOT NULL
                )''')
conn.commit()

conn.close()


class login_window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")

        # Background Image
        self.bg = ImageTk.PhotoImage(file="Images/re2.jpg")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, width=1466, height=850)

        # Frame for login interface
        frame = Frame(self.root, bg="Green")
        frame.place(x=610, y=170, width=340, height=450)

        # Logo Image
        img1 = Image.open("img/2.jpg")
        img1 = img1.resize((100, 100), Image.LANCZOS)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        lblimg1 = Label(image=self.photoimage1, bg="black", borderwidth=0)
        lblimg1.place(x=730, y=175, width=100, height=100)

        # Title "Get Started"
        get_str = Label(frame, text="Get Started", font=("times new roman", 20, "bold"), bg="Green", fg="orange")
        get_str.place(x=100, y=100)

        # Username Label and Entry
        username_lbl = Label(frame, text="Username", font=("times new roman", 15, "bold"), bg="green", fg="orange")
        username_lbl.place(x=65, y=152)
        self.txtuser = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.txtuser.place(x=40, y=180, width=270)

        # Password Label and Entry
        password_lbl = Label(frame, text="Password", font=("times new roman", 15, "bold"), bg="green", fg="orange")
        password_lbl.place(x=65, y=225)
        self.txtpass = ttk.Entry(frame, show="*", font=("times new roman", 15, "bold"))
        self.txtpass.place(x=40, y=250, width=270)

        # Login Button
        loginbtn = Button(frame, command=self.login, text="Login", font=("times new roman", 15, "bold"), bd=3,
                          relief=RIDGE, bg="red", fg="orange")
        loginbtn.place(x=110, y=300, width=120, height=35)

        # Register Button
        registerbtn = Button(frame, text="New User Register", command=self.register_window,
                             font=("times new roman", 10, "bold"), borderwidth=0, bg="green", fg="orange",
                             activebackground="black")
        registerbtn.place(x=15, y=350, width=160)

        # Forgot Password Button
        forgetbtn = Button(frame, text="Forgot Password", command=self.forgot_password_window,
                           font=("times new roman", 10, "bold"), borderwidth=0, bg="green", fg="orange",
                           activebackground="black")
        forgetbtn.place(x=10, y=370, width=160)

    def register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = Register(self.new_window)

    def login(self):
        if self.txtuser.get() == "" or self.txtpass.get() == "":
            messagebox.showerror("Error", "all fields are required")
        else:
            conn = sqlite3.connect('neoscapedb.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM login_user WHERE email=? AND password=?",
                           (self.txtuser.get(), self.txtpass.get()))
            row = cursor.fetchone()
            if row is None:
                speak_va("Invalid username and password!")
                messagebox.showerror("Error", "Invalid username and password")
            else:
                speak_va("Welcome to Face Recognition system  Neoscape University")
                messagebox.showinfo("Success", "The Face Recognition World")
                self.new_window = Toplevel(self.root)
                self.app = Face_Recognition_System(self.new_window)
            conn.commit()
            conn.close()

    def reset_pass(self):
        if self.combo_security_Q.get() == "Select":
            messagebox.showerror("Error", "select the security question", parent=self.root2)
        elif self.txt_security.get() == "":
            messagebox.showerror("Error", "select your answer", parent=self.root2)
        elif self.txt_newpassword.get() == "":
            messagebox.showerror("Error", "please enter your new password", parent=self.root2)
        else:
            conn = sqlite3.connect('neoscapedb.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM login_user WHERE email=? AND securityQ=? AND securityA=?",
                           (self.txtuser.get(), self.combo_security_Q.get(), self.txt_security.get()))
            row = cursor.fetchone()
            if row is None:
                speak_va("Wrong Security Answer")
                messagebox.showerror("Error", "Invalid security answer")
            else:
                cursor.execute("UPDATE login_user SET password=? WHERE email=?",
                               (self.txt_newpassword.get(), self.txtuser.get()))
                speak_va("Your password has been reset successfully.")
                messagebox.showinfo("Info",
                                    "Your password has been reset successfully. Please login with new password.",
                                    parent=self.root2)
            conn.commit()
            conn.close()
            self.root2.destroy()

    def forgot_password_window(self):
        if self.txtuser.get() == "":
            messagebox.showerror("Error", "please enter the email address to reset password")
        else:
            conn = sqlite3.connect('neoscapedb.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM login_user WHERE email=?", (self.txtuser.get(),))
            row = cursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Please enter the valid username")
            else:
                conn.close()
                self.root2 = Toplevel()
                self.root2.title("Forget password")
                self.root2.geometry("340x450+610+170")
                l = Label(self.root2, text="Forget Password", font=("times new roman", 15, "bold"), bg="white",
                          fg="red")
                l.place(x=0, y=0, relwidth=1)

                security_Q = Label(self.root2, text="Select Security Question", font=("times new roman", 15, "bold"),
                                   bg="white")
                security_Q.place(x=50, y=80)

                self.combo_security_Q = ttk.Combobox(self.root2, font=("times new roman", 15, "bold"), state="readonly")
                self.combo_security_Q["values"] = ("Select", "Your Birth place", "your dad name", "your mother name")
                self.combo_security_Q.place(x=50, y=110, width=250)
                self.combo_security_Q.current(0)

                security_A = Label(self.root2, text="Security Answer", font=("times new roman", 15, "bold"), bg="white")
                security_A.place(x=50, y=150)

                self.txt_security = ttk.Entry(self.root2, font=("times new roman", 15))
                self.txt_security.place(x=50, y=180, width=250)

                new_password = Label(self.root2, text="New password", font=("times new roman", 15, "bold"), bg="white")
                new_password.place(x=50, y=220)

                self.txt_newpassword = ttk.Entry(self.root2, font=("times new roman", 15))
                self.txt_newpassword.place(x=50, y=250, width=250)

                btn = Button(self.root2, text="Reset", command=self.reset_pass, font=("times new roman", 15, "bold"),
                             bg="orange", fg="green")
                btn.place(x=100, y=300)


class Register:
    def __init__(self, root):
        self.root = root
        self.root.title('Registration Form')
        self.root.geometry("1600x800+0+0")

        # Variables
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_securityQ = StringVar()
        self.var_securityA = StringVar()
        self.var_pass = StringVar()
        self.var_confpass = StringVar()

        # Background Image
        self.bg = ImageTk.PhotoImage(file="img/nepal.jpg")
        lbl_lbl = Label(self.root, image=self.bg)
        lbl_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Left image
        self.bg1 = ImageTk.PhotoImage(file="img/6.jpg")
        left_lbl = Label(self.root, image=self.bg1)
        left_lbl.place(x=30, y=100, width=500, height=550)

        # Main frame
        frame = Frame(self.root, bg="white")
        frame.place(x=520, y=100, width=800, height=550)

        register_lbl = Label(frame, text="REGISTER HERE", font=("times new roman", 20, "bold"), fg="green", bg="white")
        register_lbl.place(x=20, y=20)

        # Label and Entry fields within a label frame for cleaner UI
        Register_frame = LabelFrame(frame, bd=2, bg="white", relief=RIDGE, text="REGISTER HERE",
                                    font=("times new roman", 20, "bold"), fg="blue")
        Register_frame.place(x=5, y=5, width=670, height=400)

        fname = Label(Register_frame, text="First and Middle Name", font=("times new roman", 15, "bold"), bg="white")
        fname.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        fname_entry = ttk.Entry(Register_frame, textvariable=self.var_fname, width=25,
                                font=("times new roman", 13, "bold"))
        fname_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        lname = Label(Register_frame, text="Last Name", font=("times new roman", 15, "bold"), bg="white")
        lname.grid(row=1, column=2, padx=10, pady=5, sticky=W)

        lname_entry = ttk.Entry(Register_frame, textvariable=self.var_lname, width=25,
                                font=("times new roman", 13, "bold"))
        lname_entry.grid(row=2, column=2, padx=10, pady=5, sticky=W)

        contact = Label(Register_frame, text="Contact No.", font=("times new roman", 15, "bold"), bg="white")
        contact.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        contact_entry = ttk.Entry(Register_frame, textvariable=self.var_contact, width=25,
                                  font=("times new roman", 13, "bold"))
        contact_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        email = Label(Register_frame, text="Email or Username", font=("times new roman", 15, "bold"), bg="white")
        email.grid(row=3, column=2, padx=10, pady=5, sticky=W)

        email_entry = ttk.Entry(Register_frame, textvariable=self.var_email, width=25,
                                font=("times new roman", 13, "bold"))
        email_entry.grid(row=4, column=2, padx=10, pady=5, sticky=W)

        Security_Q = Label(Register_frame, text="Security Question", font=("times new roman", 15, "bold"), bg="white")
        Security_Q.grid(row=6, column=1, padx=5, pady=5, sticky=W)

        Security_combo = ttk.Combobox(Register_frame, textvariable=self.var_securityQ,
                                      font=("times new roman", 13, "bold"), state="readonly", width=23)
        Security_combo["values"] = ("Select Security Question", "Your Dad's Name", "Your Mom's name")
        Security_combo.current(0)
        Security_combo.grid(row=7, column=1, padx=5, pady=10, sticky=W)

        security_A = Label(Register_frame, text="Security Answer", font=("times new roman", 15, "bold"), bg="white")
        security_A.grid(row=6, column=2, padx=10, pady=5, sticky=W)

        security_entry = ttk.Entry(Register_frame, textvariable=self.var_securityA, width=25,
                                   font=("times new roman", 13, "bold"))
        security_entry.grid(row=7, column=2, padx=10, pady=5, sticky=W)

        pswd = Label(Register_frame, text="Password", font=("times new roman", 15, "bold"), bg="white")
        pswd.grid(row=8, column=1, padx=10, pady=5, sticky=W)

        pswd_entry = ttk.Entry(Register_frame, textvariable=self.var_pass, width=25,
                               font=("times new roman", 13, "bold"))
        pswd_entry.grid(row=9, column=1, padx=10, pady=5, sticky=W)

        confirm_pswd = Label(Register_frame, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white")
        confirm_pswd.grid(row=8, column=2, padx=10, pady=5, sticky=W)

        confirm_pswd_entry = ttk.Entry(Register_frame, textvariable=self.var_confpass, width=25,
                                       font=("times new roman", 13, "bold"))
        confirm_pswd_entry.grid(row=9, column=2, padx=10, pady=5, sticky=W)

        self.var_check = IntVar()
        checkbtn = Checkbutton(frame, variable=self.var_check, text="I Agree with the terms and conditions",
                               font=("times new roman", 12, "bold"), bg="white", onvalue=1, offvalue=0)
        checkbtn.place(x=50, y=370)

        img = Image.open("img/7.jpg")
        img = img.resize((200, 50), Image.LANCZOS)
        self.photoimage = ImageTk.PhotoImage(img)
        b1 = Button(frame, command=self.register_data, image=self.photoimage, borderwidth=0, cursor="hand2")
        b1.place(x=10, y=420, width=200)

        img1 = Image.open("img/8.jpg")
        img1 = img1.resize((200, 50), Image.LANCZOS)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        b1 = Button(frame, image=self.photoimage1, command=self.return_login, borderwidth=0, cursor="hand2")
        b1.place(x=330, y=420, width=200)

        # Register functionality

    def register_data(self):
        if self.var_fname.get() == "" or self.var_email.get() == "" or self.var_securityQ.get() == "Select":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        elif self.var_pass.get() != self.var_confpass.get():
            messagebox.showerror("Error", "Password and Confirm Password must be same", parent=self.root)
        elif self.var_check.get() == 0:
            messagebox.showerror("Error", "Please agree to our terms and conditions", parent=self.root)
        else:
            conn = sqlite3.connect('neoscapedb.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM login_user WHERE email=?", (self.var_email.get(),))
            row = cursor.fetchone()
            if row is not None:
                messagebox.showerror("Error", "User already exists, try another email", parent=self.root)
            else:
                # Insert into login_user table
                cursor.execute(
                    "INSERT INTO login_user (first_name, last_name, contact, email, securityQ, securityA, password) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (self.var_fname.get(), self.var_lname.get(), self.var_contact.get(), self.var_email.get(),
                     self.var_securityQ.get(), self.var_securityA.get(), self.var_pass.get()))
                conn.commit()
                messagebox.showinfo("Success", "Registered Successfully", parent=self.root)
            conn.close()

    def return_login(self):
        self.root.destroy()


class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1450x720+0+0")
        self.root.title("Face Recognition System")

        # Initialize new_window and app attributes
        self.new_window = None
        self.app = None

        # First image
        img1 = Image.open("Images/Neoscape campus.png")
        img1 = img1.resize((400, 100), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(x=0, y=0, width=400, height=100)

        # Second image
        img2 = Image.open("Images/eye.jpg")
        img2 = img2.resize((400, 100), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        f_lbl = Label(self.root, image=self.photoimg2)
        f_lbl.place(x=400, y=0, width=400, height=100)

        # Third image
        img3 = Image.open("Images/ncit-wide2017-11-18.jpg")
        img3 = img3.resize((400, 100), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        f_lbl = Label(self.root, image=self.photoimg3)
        f_lbl.place(x=800, y=0, width=400, height=100)

        # Background image
        img4 = Image.open("Images/ai-shutterstock.jpg")
        img4 = img4.resize((1200, 600), Image.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)
        bg_img = Label(self.root, image=self.photoimg4)
        bg_img.place(x=0, y=100, width=1200, height=600)

        title_lbl = Label(bg_img, text="NEOSCAPE UNIVERSITY EXAM ATTENDANCE SYSTEM",
                          font=("Algerian", 30, "bold"), bg="white", fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1200, height=45)

        # Student button
        img5 = Image.open("Images/student.jpg")
        img5 = img5.resize((195, 195), Image.LANCZOS)
        self.photoimg5 = ImageTk.PhotoImage(img5)

        btn1 = Button(bg_img, image=self.photoimg5, command=self.student_details, cursor="hand2")
        btn1.place(x=100, y=80, width=195, height=195)

        btn1_1 = Button(bg_img, text="Student Details", command=self.student_details, cursor="hand2",
                        font=("times new roman", 15, "bold"),
                        bg="darkblue", fg="white")
        btn1_1.place(x=100, y=245, width=195, height=40)

        # Face Detection button
        img6 = Image.open("Images/faceDetector.jpeg")
        img6 = img6.resize((195, 195), Image.LANCZOS)
        self.photoimg6 = ImageTk.PhotoImage(img6)

        btn2 = Button(bg_img, image=self.photoimg6, cursor="hand2")
        btn2.place(x=400, y=80, width=195, height=195)

        btn2_2 = Button(bg_img, text="Face Detector", command=self.face_data, cursor="hand2",
                        font=("times new roman", 15, "bold"),
                        bg="darkblue", fg="white")
        btn2_2.place(x=400, y=245, width=195, height=40)

        # Attendance button
        img7 = Image.open("Images/face.jpg")
        img7 = img7.resize((195, 195), Image.LANCZOS)
        self.photoimg7 = ImageTk.PhotoImage(img7)

        btn3 = Button(bg_img, image=self.photoimg7, cursor="hand2")
        btn3.place(x=700, y=80, width=195, height=195)

        btn3_3 = Button(bg_img, text="Attendance", command=self.attendance_data, cursor="hand2",
                        font=("times new roman", 15, "bold"),
                        bg="darkblue", fg="white")
        btn3_3.place(x=700, y=245, width=195, height=40)

        # Button 4 help desk
        img8 = Image.open("Images/developer.png")
        img8 = img8.resize((195, 195), Image.LANCZOS)
        self.photoimg8 = ImageTk.PhotoImage(img8)

        btn4 = Button(bg_img, image=self.photoimg8, cursor="hand2")
        btn4.place(x=1000, y=80, width=195, height=195)

        btn4_4 = Button(bg_img, text="Help Desk", command=self.help_system, cursor="hand2",
                        font=("times new roman", 15, "bold"),
                        bg="darkblue", fg="white")
        btn4_4.place(x=1000, y=245, width=195, height=40)

        # Train Data button
        img9 = Image.open("Images/trainFace-khom.png")
        img9 = img9.resize((195, 195), Image.LANCZOS)
        self.photoimg9 = ImageTk.PhotoImage(img9)

        btn5 = Button(bg_img, image=self.photoimg9, cursor="hand2")
        btn5.place(x=100, y=350, width=195, height=195)

        btn5_5 = Button(bg_img, text="Train Data", command=self.train_data, cursor="hand2",
                        font=("times new roman", 15, "bold"),
                        bg="darkblue", fg="white")
        btn5_5.place(x=100, y=525, width=195, height=40)

        # Photos button
        img10 = Image.open("Images/photos.jpg")
        img10 = img10.resize((195, 195), Image.LANCZOS)
        self.photoimg10 = ImageTk.PhotoImage(img10)

        btn6 = Button(bg_img, image=self.photoimg10, cursor="hand2")
        btn6.place(x=400, y=350, width=195, height=195)

        btn6_6 = Button(bg_img, text="Photos", command=self.open_img, cursor="hand2",
                        font=("times new roman", 15, "bold"),
                        bg="darkblue", fg="white")
        btn6_6.place(x=400, y=525, width=195, height=40)

        # Data visualization
        img11 = Image.open("Images/Data1.jpg")
        img11 = img11.resize((195, 195), Image.LANCZOS)
        self.photoimg11 = ImageTk.PhotoImage(img11)

        btn7 = Button(bg_img, image=self.photoimg11, cursor="hand2")
        btn7.place(x=700, y=350, width=195, height=195)

        btn7_7 = Button(bg_img, text="Data Visualization", command=self.data_visualization, cursor="hand2",
                        font=("times new roman", 15, "bold"),
                        bg="darkblue", fg="white")
        btn7_7.place(x=700, y=525, width=195, height=40)

        # Exit button
        img12 = Image.open("Images/exit-sign-neon-style_77399-144.jpg")
        img12 = img12.resize((195, 195), Image.LANCZOS)
        self.photoimg12 = ImageTk.PhotoImage(img12)

        btn8 = Button(bg_img, image=self.photoimg12, cursor="hand2")
        btn8.place(x=1000, y=350, width=195, height=195)

        btn8_8 = Button(bg_img, text="Exit", command=self.iexit, cursor="hand2",
                        font=("times new roman", 15, "bold"),
                        bg="darkblue", fg="white")
        btn8_8.place(x=1000, y=525, width=195, height=40)

        # =================================== Functions =========================================

    def open_img(self):
        os.startfile("data")

    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)

    def face_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)

    def attendance_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    def help_system(self):
        self.new_window = Toplevel(self.root)
        self.app = Help(self.new_window)

    def data_visualization(self):
        self.new_window = Toplevel(self.root)
        self.app = DataVisualization(self.new_window)

        # .................exit button

    def iexit(self):
        speak_va("Are you sure you want to exit this project?")
        user_response = tkinter.messagebox.askyesno("Face Recognition", "Are you sure you want to exit this project?",
                                                    parent=self.root)
        if user_response > 0:
            self.root.destroy()
        else:
            return


# Define object
if __name__ == "__main__":
    main()
    # main_root = Tk()
    # app = Face_Recognition_System(main_root)
    # main_root.mainloop()
