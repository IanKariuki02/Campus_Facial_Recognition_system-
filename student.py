import datetime
import os
import sqlite3
from logging import root
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from os import SEEK_CUR, close
from time import strptime
import re

import cv2
import pyttsx3
from PIL import Image, ImageTk
from tkcalendar import DateEntry

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 is for female voice and 0 is for male voice


def speak_va(transcribed_query):
    engine.say(transcribed_query)
    engine.runAndWait()


class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # Variables
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        self.var_searchtxt = StringVar()
        self.var_search = StringVar()

        img2 = Image.open("Images/re1.jpg")
        img2 = img2.resize((1366, 120),
                           Image.LANCZOS)  # Antialias lea high level image lai low level mah convert garxa
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl = Label(self.root, image=self.photoimg2)
        f_lbl.place(x=0, y=0, width=1366, height=120)

        img3 = Image.open("Images/face.jpg")
        img3 = img3.resize((1530, 730),
                           Image.LANCZOS)  # Antialias lea high level image lai low level mah convert garxa
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root, image=self.photoimg3)
        bg_img.place(x=0, y=130, width=1530, height=730)

        title_lbl = Label(bg_img, text="STUDENT DETAILS MANAGEMENT SECTION", font=("Algerian", 30, "bold"), bg="white",
                          fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1530, height=30)

        main_frame = Frame(bg_img, bd=2, bg="white", )
        main_frame.place(x=20, y=35, width=1480, height=600)

        # left label frame
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Details",
                                font=("Algerian", 12, "bold"))
        left_frame.place(x=5, y=5, width=670, height=515)

        img_left = Image.open("Images/Neoscape.png")
        img_left = img_left.resize((660, 100),
                                   Image.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)

        f_lbl = Label(left_frame, image=self.photoimg_left)
        f_lbl.place(x=5, y=0, width=660, height=70)

        # current course information
        current_course_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Current Course Information",
                                          font=("Algerian", 12, "bold"))
        current_course_frame.place(x=5, y=75, width=660, height=115)

        # Department
        dep_label = Label(current_course_frame, text="Department", font=("times new roman", 13, "bold"), bg="white")
        dep_label.grid(row=0, column=0, padx=10, sticky=W)

        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dep, font=("times new roman", 13, "bold"),
                                 state="readonly", width=18)
        dep_combo["values"] = ("Select Department", "IT", "Computer", "Engineering", "Business", "Food&Sci", "Medicine")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        # course
        course_label = Label(current_course_frame, text="Course", font=("times new roman", 13, "bold"), bg="white")
        course_label.grid(row=0, column=2, padx=10, sticky=W)

        course_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course,
                                    font=("times new roman", 13, "bold"), state="readonly", width=18)
        course_combo["values"] = ("Select Course", "BBIT", "IT", "CS", "BBA", "EEE", "BCOM", "GEGIS", "PROCUREMENT", "TIE", "MECHATRONICS", "NURSING")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)

        # Year
        year_label = Label(current_course_frame, text="Year", font=("times new roman", 13, "bold"), bg="white")
        year_label.grid(row=1, column=0, padx=10, sticky=W)

        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year,
                                  font=("times new roman", 13, "bold"), state="readonly", width=18)
        year_combo["values"] = ("Select Year", "2020-21", "2021-22", "2022-23", "2023-24")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        # Semester
        semester_label = Label(current_course_frame, text="Semester", font=("times new roman", 13, "bold"), bg="white")
        semester_label.grid(row=1, column=2, padx=10, sticky=W)

        semester_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester,
                                      font=("times new roman", 13, "bold"), state="readonly", width=18)
        semester_combo["values"] = ("Select Semester", "Semester-I", "Semester-III", "Semester-V", "Semester-VII")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)

        # class student information
        class_student_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Class Student Information",
                                         font=("times new roman", 12, "bold"))
        class_student_frame.place(x=5, y=190, width=660, height=320)

        # student ID
        studentId_label = Label(class_student_frame, text="StudentID:", font=("times new roman", 13, "bold"),
                                bg="white")
        studentId_label.grid(row=0, column=0, padx=10, sticky=W)

        studentId_entry = ttk.Entry(class_student_frame, textvariable=self.var_std_id, width=18,
                                    font=("times new roman", 13, "bold"))
        studentId_entry.grid(row=0, column=1, padx=10, sticky=W)

        validate_id = self.root.register(self.checkid)
        studentId_entry.config(validate='key', validatecommand=(validate_id, '%P'))

        # student name
        studentName_label = Label(class_student_frame, text="Student Name:", font=("times new roman", 13, "bold"),
                                  bg="white")
        studentName_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        studentName_entry = ttk.Entry(class_student_frame, textvariable=self.var_std_name, width=18,
                                      font=("times new roman", 13, "bold"))
        studentName_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # call back and validation
        validate_name = self.root.register(self.checkname)
        studentName_entry.config(validate='key', validatecommand=(validate_name, '%P'))

        # class division
        class_div_label = Label(class_student_frame, text="Unit Division:", font=("times new roman", 13, "bold"),
                                bg="white")
        class_div_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        div_combo = ttk.Combobox(class_student_frame, textvariable=self.var_div, font=("times new roman", 13, "bold"),
                                 state="readonly", width=16)
        div_combo["values"] = ("Select Division", "A", "B", "C", "D", "E")
        div_combo.current(0)
        div_combo.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # roll_no
        roll_no_label = Label(class_student_frame, text="Roll No:", font=("times new roman", 13, "bold"), bg="white")
        roll_no_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)

        roll_no_entry = ttk.Entry(class_student_frame, textvariable=self.var_roll, width=18,
                                  font=("times new roman", 13, "bold"))
        roll_no_entry.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        validate_roll = self.root.register(self.checkroll)
        roll_no_entry.config(validate='key', validatecommand=(validate_roll, '%P'))

        # Gender
        gender_label = Label(class_student_frame, text="Gender:", font=("times new roman", 13, "bold"), bg="white")
        gender_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        gender_combo = ttk.Combobox(class_student_frame, textvariable=self.var_gender,
                                    font=("times new roman", 13, "bold"), state="readonly", width=16)
        gender_combo["values"] = ("Male", "Female", "Others")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        # DOB
        dob_label = Label(class_student_frame, text="DOB:", font=("times new roman", 13, "bold"), bg="white")
        dob_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)

        cal = DateEntry(class_student_frame, textvariable=self.var_dob, width=23, year=2019, month=6, day=22,
                        background='darkblue', foreground='white', borderwidth=2)
        cal.grid(row=2, column=3, padx=10, pady=10)

        # Email
        email_label = Label(class_student_frame, text="Email:", font=("times new roman", 13, "bold"), bg="white")
        email_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)

        email_entry = ttk.Entry(class_student_frame, textvariable=self.var_email, width=18,
                                font=("times new roman", 13, "bold"))
        email_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        email = Label(class_student_frame, text="*ex123@gmail.com", font=("times new roman", 6, "bold"), fg="red",
                      bg="white")

        email.place(x=150, y=149)

        # Phone no
        phone_label = Label(class_student_frame, text="Phone No:", font=("times new roman", 13, "bold"), bg="white")
        phone_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)

        phone_entry = ttk.Entry(class_student_frame, textvariable=self.var_phone, width=18,
                                font=("times new roman", 13, "bold"))
        phone_entry.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        validate_phone = self.root.register(self.checkphone)
        phone_entry.config(validate='key', validatecommand=(validate_phone, '%P'))

        # Address
        address_label = Label(class_student_frame, text="Address:", font=("times new roman", 13, "bold"), bg="white")
        address_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)

        address_entry = ttk.Entry(class_student_frame, textvariable=self.var_address, width=18,
                                  font=("times new roman", 13, "bold"))
        address_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        validate_address = self.root.register(self.checkaddress)
        address_entry.config(validate='key', validatecommand=(validate_address, '%P'))

        # Teacher Name
        teacher_label = Label(class_student_frame, text="Teacher Name:", font=("times new roman", 13, "bold"),
                              bg="white")
        teacher_label.grid(row=4, column=2, padx=10, pady=5, sticky=W)

        teacher_entry = ttk.Entry(class_student_frame, textvariable=self.var_teacher, width=18,
                                  font=("times new roman", 13, "bold"))
        teacher_entry.grid(row=4, column=3, padx=10, pady=5, sticky=W)

        validate_Teacher = self.root.register(self.checkTeachername)
        teacher_entry.config(validate='key', validatecommand=(validate_Teacher, '%P'))

        # radio buttons
        self.var_radio1 = StringVar()
        radiobtn1 = ttk.Radiobutton(class_student_frame, variable=self.var_radio1, text="Take Photo Sample",
                                    value="Yes")
        radiobtn1.grid(row=5, column=0)

        radiobtn2 = ttk.Radiobutton(class_student_frame, variable=self.var_radio1, text="No Photo Sample", value="NO")
        radiobtn2.grid(row=5, column=1)

        # button frame
        btn_frame = Frame(class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=215, width=655, height=80)

        save_btn = Button(btn_frame, text="Save", command=self.add_data, width=16, font=("times new roman", 13, "bold"),
                          bg="Green", fg="white")
        save_btn.grid(row=0, column=0)

        update_btn = Button(btn_frame, text="Update", command=self.update_data, width=16,
                            font=("times new roman", 13, "bold"), bg="Green", fg="white")
        update_btn.grid(row=0, column=1)

        delete_btn = Button(btn_frame, text="Delete", command=self.delete_data, width=16,
                            font=("times new roman", 13, "bold"), bg="Green", fg="white")
        delete_btn.grid(row=0, column=2)

        reset_btn = Button(btn_frame, text="Reset", command=self.reset_data, width=16,
                           font=("times new roman", 13, "bold"), bg="Green", fg="white")
        reset_btn.grid(row=0, column=3)

        # frame for take photo and update photo
        btn_frame1 = Frame(class_student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.place(x=0, y=245, width=655, height=80)

        take_photo_btn = Button(btn_frame1, text="Take Photo Sample", command=self.generate_dataset, width=65,
                                font=("times new roman", 13, "bold"), bg="green", fg="white")
        take_photo_btn.grid(row=0, column=0)

        # Right label frame
        right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Details",
                                 font=("Algerian", 12, "bold"))
        right_frame.place(x=680, y=5, width=650, height=515)

        img_right = Image.open("Images/mycollege1.jpeg")
        img_right = img_right.resize((600, 75),
                                     Image.LANCZOS)  # Antialias lea high level image lai low level mah convert garxa
        self.photoimg_right = ImageTk.PhotoImage(img_right)

        f_lbl = Label(right_frame, image=self.photoimg_right)
        f_lbl.place(x=5, y=0, width=640, height=75)

        search_frame = LabelFrame(right_frame, bd=2, bg="white", relief=RIDGE, text="Search System",
                                  font=("Algerian", 12, "bold"))
        search_frame.place(x=5, y=75, width=640, height=70)

        search_label = Label(search_frame, text="Search By:", font=("times new roman", 15, "bold"), bg="Green",
                             fg="white")
        search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        search_combo = ttk.Combobox(search_frame, textvariable=self.var_search, font=("times new roman", 13, "bold"),
                                    state="readonly", width=11)
        search_combo["values"] = ("Select", "student_id", "roll_number", "course")
        search_combo.current(0)
        search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        search_entry = ttk.Entry(search_frame, textvariable=self.var_searchtxt, width=17,
                                 font=("times new roman", 13, "bold"))
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        search_btn = Button(search_frame, text="Search", command=self.search_data, width=10,
                            font=("times new roman", 12, "bold"), bg="blue", fg="white")
        search_btn.grid(row=0, column=3, padx=4)

        showAll_btn = Button(search_frame, text="Show All", width=10, command=self.show_all,
                             font=("times new roman", 12, "bold"), bg="blue", fg="white")
        showAll_btn.grid(row=0, column=4, padx=4)

        # Table frame
        table_frame = Frame(right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=150, width=640, height=350)

        # scroll bar
        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(table_frame, columns=(
            "dep", "course", "year", "sem", "id", "name", "div", "roll", "gender", "dob", "email", "phone", "address",
            "teacher", "photo"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("id", text="StudentId")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("div", text="Division")
        self.student_table.heading("roll", text="Roll")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="DOB")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("teacher", text="Teacher")
        self.student_table.heading("photo", text="PhotoSampleStatus")
        self.student_table["show"] = "headings"

        self.student_table.column("dep", width=100)
        self.student_table.column("course", width=100)
        self.student_table.column("year", width=100)
        self.student_table.column("sem", width=100)
        self.student_table.column("id", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("roll", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("div", width=100)
        self.student_table.column("dob", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=100)
        self.student_table.column("teacher", width=100)
        self.student_table.column("photo", width=150)

        self.student_table.pack(fill=BOTH, expand=1)

        self.student_table.bind("<ButtonRelease>", self.get_cursor)

        self.fetch_data()

    # call back system

    def checkname(self, name):
        if name.replace(" ", "").isalnum():
            return True
        elif name == '':
            return True
        else:
            speak_va('Invalid! Name Not allowed.')
            messagebox.showerror('Invalid', 'Not allowed' + name[-1])

    def checkaddress(self, name):
        if name.replace(' ', '').isalnum():  # Check if alphanumeric (including spaces)
            return True
        else:
            return False

    def checkTeachername(self, name):
        if name.replace(' ', '').isalpha():  # Check if alphabetic (including spaces)
            return True
        else:
            return False

    # # check phone number

    def checkphone(self, phone):
        if len(phone) <= 10:
            if phone.isdigit():
                return True
            if len(str(phone)) == 0:
                return True
            else:
                speak_va('Invalid phone number Format')
                messagebox.showerror('Invalid', 'Invalid entry. Please enter phone (example:0700000000)')
                return False

        else:
            speak_va('Alert!!! Invalid Phone Number')
            messagebox.showwarning('Alert', 'invalid phone. Please enter phone (example:0700000000)')
            return False

    #     # Id no ko validation
    def checkid(self, id):
        if len(id) <= 5:
            if id.isdigit():
                return True
            if len(str(id)) == 0:
                return True
            else:
                speak_va('Invalid ID. Please enter ID as integer value')
                messagebox.showerror('Invalid',
                                     'Invalid entry ID. Please enter ID as integer value (example: ID :- 1 2 3 4 5 6 '
                                     '7...like this)')
                return False
        else:
            speak_va('Invalid ID.')
            messagebox.showwarning('Alert', 'invalid ID. Please Enter valid ID.')
            return False

    #     # Roll validation
    def checkroll(self, roll):
        if len(roll) <= 6:
            if roll.isdigit():
                return True
            if len(str(roll)) == 0:
                return True
            else:
                speak_va('Invalid Roll number. Please Enter your valid roll number.')
                messagebox.showerror('Invalid', 'Invalid entry enter Roll No (example: Roll No: 171346)')
                return False
        else:
            speak_va('Invalid Roll number.')
            messagebox.showwarning('Alert', 'invalid phone enter Roll No (example: Roll No: 171346)')
            return False

    def create_calendar(self):
        cal = Calendar(self.root, selectmode='day',
                       year=2020, month=5,
                       day=22)
        cal.pack(pady=20)

    def grad_date(self):
        selected_date = self.cal.get_date()
        print("Selected Graduation Date:", selected_date)

    # function declaration
    def add_data(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            speak_va("Alert!!! All Fields are Mandatory.")
            messagebox.showerror("Error", "All fields Are Required", parent=self.root)
        elif "@" not in self.var_email.get() or ".com" not in self.var_email.get():
            speak_va('Try valid email address!!')
            messagebox.showerror("Error", 'Invalid email Enter valid email like kariuki123@gmail.com ', parent=self.root)
        else:
            try:
                conn = sqlite3.connect('neoscapedb.sqlite')
                my_cursor = conn.cursor()
                my_cursor.execute('''CREATE TABLE IF NOT EXISTS student (
                                     department TEXT,
                                     course TEXT,
                                     year TEXT,
                                     semester TEXT,
                                     student_id TEXT PRIMARY KEY,
                                     student_name TEXT,
                                     division TEXT,
                                     roll_number TEXT,
                                     gender TEXT,
                                     dob TEXT,
                                     email TEXT,
                                     phone TEXT,
                                     address TEXT,
                                     teacher TEXT,
                                     radio1 TEXT,
                                     photosample TEXT DEFAULT NULL
                                 )''')
                conn.commit()
                print(f"Inserting student with ID: {self.var_std_id.get()}")

                my_cursor.execute("INSERT INTO student VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (

                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_id.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_radio1.get(),
                    None

                ))
                conn.commit()
                self.fetch_data()
                conn.close()

                speak_va('Student Details has been added successfully.')
                messagebox.showinfo("Success", "Student details has been added Successfully", parent=self.root)
            except Exception as es:
                speak_va('An Exception Occurred!')
                messagebox.showerror("Error", f"Due To :{str(es)}", parent=self.root)

    # Fetch data
    def fetch_data(self):
        conn = None

        try:
            conn = sqlite3.connect('neoscapedb.sqlite')
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM student")
            data = my_cursor.fetchall()

            if len(data) != 0:
                self.student_table.delete(*self.student_table.get_children())
                for i in data:
                    self.student_table.insert("", END, values=i)
        except Exception as e:
            print(f"Error fetching data: {e}")
        finally:
            if conn:
                conn.close()

    # =================== get cursor ======================#
    def get_cursor(self, event):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]

        self.var_dep.set(data[0]),
        self.var_course.set(data[1]),
        self.var_year.set(data[2]),
        self.var_semester.set(data[3]),
        self.var_std_id.set(data[4]),
        self.var_std_name.set(data[5]),
        self.var_div.set(data[6]),
        self.var_roll.set(data[7]),
        self.var_gender.set(data[8]),
        self.var_dob.set(data[9]),
        self.var_email.set(data[10]),
        self.var_phone.set(data[11]),
        self.var_address.set(data[12]),
        self.var_teacher.set(data[13]),
        self.var_radio1.set(data[14])

        # ============= Update function =========================

    def update_data(self):
        if (self.var_dep.get() == "Select Department" or
                self.var_course.get() == "select Course" or
                self.var_year.get() == "select Year" or
                self.var_semester.get() == "select Semester" or
                self.var_std_id.get() == "" or
                self.var_dep.get() == "" or
                self.var_dob.get() == "" or
                self.var_email.get() == "" or
                self.var_gender.get() == "" or
                self.var_phone.get() == "" or
                self.var_address.get() == "" or
                self.var_std_name.get() == "" or
                self.var_teacher.get() == ""):
            speak_va('All Fields are mandatory.')
            messagebox.showerror("Error", "All fields Are Required", parent=self.root)
            return
        else:
            try:
                speak_va("Do you want to Update this Student's Details?")
                Update = messagebox.askyesno("Update", "Do You Want To Update This Student Details", parent=self.root)
                print("Updating student data with ID: ", self.var_std_id.get())
                if Update > 0:
                    conn = sqlite3.connect('neoscapedb.sqlite')
                    my_cursor = conn.cursor()
                    my_cursor.execute(
                        "UPDATE student SET department=?, course=?, year=?, semester=?, student_name=?, division=?, roll_number=?, gender=?, dob=?, email=?, phone=?, address=?, teacher=?, photosample=? WHERE student_id=?",
                        (
                            self.var_dep.get(),
                            self.var_course.get(),
                            self.var_year.get(),
                            self.var_semester.get(),
                            self.var_std_name.get(),
                            self.var_div.get(),
                            self.var_roll.get(),
                            self.var_gender.get(),
                            self.var_dob.get(),
                            self.var_email.get(),
                            self.var_phone.get(),
                            self.var_address.get(),
                            self.var_teacher.get(),
                            self.var_radio1.get(),
                            self.var_std_id.get()
                        ))

                    conn.commit()
                    self.fetch_data()
                    conn.close()

                    speak_va('Student Details updated successfully.')
                    messagebox.showinfo("Success", "Student Details updated Successfully.", parent=self.root)
                else:
                    return
            except Exception as es:
                speak_va('An Exception Occurred!')
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def generate_dataset(self):
        if (self.var_dep.get() == "Select Department" or
                self.var_course.get() == "select Course" or
                self.var_year.get() == "select Year" or
                self.var_semester.get() == "select Semester" or
                self.var_std_id.get() == "" or
                self.var_dep.get() == "" or
                self.var_dob.get() == "" or
                self.var_email.get() == "" or
                self.var_gender.get() == "" or
                self.var_phone.get() == "" or
                self.var_address.get() == "" or
                self.var_std_name.get() == "" or
                self.var_teacher.get() == ""):
            speak_va('All Fields are mandatory.')
            messagebox.showerror("Error", "All fields Are Required", parent=self.root)
            return

        try:
            conn = sqlite3.connect('neoscapedb.sqlite')
            my_cursor = conn.cursor()
            student_id = self.var_std_id.get()
            print(f"Selected student ID: {student_id}")

            my_cursor.execute(
                "UPDATE student SET department=?, course=?, year=?, semester=?, student_name=?, division=?, roll_number=?, gender=?, dob=?, email=?, phone=?, address=?, teacher=?, photosample=? WHERE student_id=?",
                (
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_radio1.get(),
                    student_id

                )
            )

            conn.commit()
            self.fetch_data()
            self.reset_data()
            conn.close()

            # Load pre-trained face classifier
            face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

            def face_cropped(img):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cropped_face = img[y:y + h, x:x + w]
                    return cropped_face
                return None

            cap = cv2.VideoCapture(0)
            img_id = 0
            photo_sample_path = ""

            while True:
                ret, my_frame = cap.read()
                if face_cropped(my_frame) is not None:
                    img_id += 1
                    face = cv2.resize(face_cropped(my_frame), (450, 450))
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    # file_name_path = f"data/user.{self.var_std_id.get()}.{img_id}.jpg"
                    # student_id = self.var_std_id.get()
                    file_name_path = "data/user." + str(student_id) + "." + str(img_id) + ".jpg"
                    cv2.imwrite(file_name_path, face)
                    cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow("Cropped Face", face)

                    # Store the path of the last photo taken
                    photo_sample_path = file_name_path
                    print(f"Image saved: {file_name_path}")

                if cv2.waitKey(1) == 13 or int(img_id) == 100:
                    break

            cap.release()
            cv2.destroyAllWindows()

            # Update the PhotoSample column in the database
            print(f"Updating database with photo sample path: {photo_sample_path}")
            conn = sqlite3.connect('neoscapedb.sqlite')
            my_cursor = conn.cursor()
            my_cursor.execute("UPDATE student SET photosample=? WHERE student_id=?",
                              (photo_sample_path, self.var_std_id.get()))
            conn.commit()
            conn.close()

            messagebox.showinfo("Result", "Generating data sets completed!!!")

        except Exception as es:
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    # ===================Delete Function===================
    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student Id Must be Required", parent=self.root)
        else:
            try:
                speak_va("Do you want to Delete this Student's Details?")
                delete = messagebox.askyesno("Student Delete Page", "Do You Want To Delete This Student Details",
                                             parent=self.root)
                if delete:
                    conn = sqlite3.connect('neoscapedb.sqlite')
                    my_cursor = conn.cursor()
                    sql = "DELETE FROM student WHERE student_id=?"
                    val = (self.var_std_id.get(),)
                    my_cursor.execute(sql, val)
                    conn.commit()
                    self.fetch_data()
                    conn.close()
                    speak_va('Student Details deleted successfully.')
                    messagebox.showinfo("Delete", "Student Details Successfully deleted", parent=self.root)
                else:
                    return
            except Exception as es:
                speak_va('An exception occurred!')
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    # ============Reset Function =============================
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("Select Division")
        self.var_roll.set("")
        self.var_gender.set("Male")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio1.set("")

        # ..............Generate data set or take photo sample

    def search_data(self):
        if self.var_searchtxt.get() == "" or self.var_search.get() == "Select Option":
            messagebox.showerror("Error", "Select Combo option and enter entry box", parent=self.root)
        else:
            try:
                conn = sqlite3.connect('neoscapedb.sqlite')
                my_cursor = conn.cursor()

                # Construct and execute the SQL query
                query = f"SELECT * FROM student WHERE {self.var_search.get()} LIKE ?"
                search_term = f"%{self.var_searchtxt.get()}%"
                my_cursor.execute(query, (search_term,))

                rows = my_cursor.fetchall()

                if len(rows) > 0:
                    self.student_table.delete(*self.student_table.get_children())
                    for row in rows:
                        self.student_table.insert("", END, values=row)
                else:
                    speak_va("Data Not Found")
                    messagebox.showerror("Error", "Data Not Found", parent=self.root)

                conn.commit()
                conn.close()

            except Exception as es:
                speak_va("An Exception Occurred!")
                messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)

    def show_all(self):
        try:
            conn = sqlite3.connect('neoscapedb.sqlite')
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM student")
            data = my_cursor.fetchall()

            if len(data) > 0:
                self.student_table.delete(*self.student_table.get_children())
                for row in data:
                    self.student_table.insert("", END, values=row)
            else:
                speak_va("No records found.")
                messagebox.showinfo("Information", "No records found.", parent=self.root)

            conn.commit()
            conn.close()

        except Exception as es:
            speak_va("An Exception Occurred!")
            messagebox.showerror("Error", f"Due To: {str(es)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
