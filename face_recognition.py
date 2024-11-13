from ntpath import join
from pyttsx3 import speak
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from student import Student
import sqlite3
import cv2
import re
import os
import numpy as np
from time import strftime
from datetime import datetime
import cv2 as cv
from os.path import isfile, join
from os import listdir
import time
import pandas as pd
import csv
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 is for female voice and 0 is for male voice


def speak_va(transcribed_query):
    engine.say(transcribed_query)
    engine.runAndWait()


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="FACE RECOGNITION", font=("Algerian", 20, "bold"), bg="lightblue",
                          fg="darkgreen")
        title_lbl.place(x=0, y=0, width=1366, height=35)

        img_bottom = Image.open(r"Images/re1.jpg")
        img_bottom = img_bottom.resize((1366, 700), Image.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)

        f_lbl = Label(self.root, image=self.photoimg_bottom)
        f_lbl.place(x=0, y=50, width=1366, height=650)

        # Unit Name Label and Entry
        # Unit Name Label and Combobox
        unit_lbl = Label(self.root, text="Unit Name:", font=("Algerian", 15, "bold"), bg="lightblue", fg="darkgreen")
        unit_lbl.place(x=20, y=70, width=120, height=30)

        self.unit_combobox = ttk.Combobox(self.root, font=("times new roman", 15, "bold"))
        self.unit_combobox.place(x=150, y=70, width=200, height=30)
        self.unit_combobox.bind("<<ComboboxSelected>>", self.unit_selected)

        # Cohort Label and Entry
        cohort_lbl = Label(self.root, text="Cohort:", font=("Algerian", 15, "bold"), bg="lightblue", fg="darkgreen")
        cohort_lbl.place(x=400, y=70, width=120, height=30)

        self.cohort_entry = Entry(self.root, font=("times new roman", 15, "bold"))
        self.cohort_entry.place(x=530, y=70, width=200, height=30)

        self.load_units()

        # Lecturer Name Label and Entry
        lecturer_lbl = Label(self.root, text="Lecturer:", font=("Algerian", 15, "bold"), bg="lightblue", fg="darkgreen")
        lecturer_lbl.place(x=20, y=110, width=120, height=30)

        self.lecturer_entry = Entry(self.root, font=("times new roman", 15, "bold"))
        self.lecturer_entry.place(x=150, y=110, width=200, height=30)

        # Button
        b1_1 = Button(f_lbl, text="Face Recognition", cursor="hand2", command=self.face_recog,
                      font=("Algerian", 15, "bold"), bg="darkgreen", fg="yellow")
        b1_1.place(x=500, y=450, width=300, height=150)

        # Save Config Button
        save_btn = Button(self.root, text="Save Unit", cursor="hand2", command=self.save_config,
                          font=("Algerian", 15, "bold"), bg="darkgreen", fg="yellow")
        save_btn.place(x=800, y=70, width=150, height=30)

    def load_units(self):
        try:
            conn = sqlite3.connect('neoscapedb.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT unit_name FROM config")
            rows = cursor.fetchall()
            unit_names = [row[0] for row in rows]
            self.unit_combobox['values'] = unit_names
            conn.close()
        except Exception as e:
            print(f"Error loading units: {e}")

    def unit_selected(self, event):
        selected_unit = self.unit_combobox.get()
        if selected_unit:
            self.load_config(selected_unit)

    def load_config(self, selected_unit=None):
        try:
            conn = sqlite3.connect('neoscapedb.sqlite')
            cursor = conn.cursor()
            if selected_unit:
                cursor.execute("SELECT cohort FROM config WHERE unit_name = ? ORDER BY id DESC LIMIT 1",
                               (selected_unit,))
                row = cursor.fetchone()
                if row:
                    cohort = row[0]
                    self.cohort_entry.delete(0, END)
                    self.cohort_entry.insert(0, cohort)
                    # Assuming common units have "Common" in their name, adjust condition as needed
                    if "Common" in selected_unit:
                        self.cohort_entry.config(state=DISABLED)
                    else:
                        self.cohort_entry.config(state=NORMAL)
            else:
                cursor.execute("SELECT unit_name, cohort FROM config ORDER BY id DESC LIMIT 1")
                row = cursor.fetchone()
                if row:
                    unit_name, cohort = row
                    self.unit_combobox.set(unit_name)
                    self.cohort_entry.insert(0, cohort)
            conn.close()
        except Exception as e:
            print(f"Error loading config: {e}")

    def save_config(self):
        unit_name = self.unit_combobox.get()
        cohort = self.cohort_entry.get() if self.cohort_entry.cget('state') == 'normal' else ''
        try:
            conn = sqlite3.connect('neoscapedb.sqlite')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO config (unit_name, cohort) VALUES (?, ?)", (unit_name, cohort))
            conn.commit()
            conn.close()
            print("Config saved successfully")
        except Exception as e:
            print(f"Error saving config: {e}")

    # =================Attendance ====================
    def mark_attendance(self, i, r, n, d, c):
        folder_path = "attendance_records"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        unit_name = self.unit_combobox.get()
        cohort = self.cohort_entry.get() if self.cohort_entry.cget('state') == 'normal' else 'Common'
        lecturer = self.lecturer_entry.get()

        if not unit_name or not lecturer:
            messagebox.showerror("Input Error", "Please select a Unit Name and enter Lecturer's name")
            return None

        # Sanitizing the file name to remove invalid characters
        sanitized_unit_name = re.sub(r'[\\/*?:"<>|]', "", unit_name)
        sanitized_cohort = re.sub(r'[\\/*?:"<>|]', "", cohort)

        date_str = datetime.now().strftime("%Y-%m-%d")
        file_name = f"attendance_{sanitized_unit_name}_{sanitized_cohort}_{date_str}.csv"
        file_path = os.path.join(folder_path, file_name)

        if not os.path.exists(file_path):
            with open(file_path, "w", newline="\n") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(["ID", "Roll Number", "Name", "Department", "Time", "Date", "Status", "Lecturer", "Course"])
                print(f"Created {file_path} with headers.")

        with open(file_path, "r+", newline="\n") as f:
            myDatalist = f.readlines()
            name_list = [line.strip().split(",")[0] for line in myDatalist if line.strip()]
            print(f"Current attendance list: {name_list}")

            if i not in name_list:
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                entry = f"{i},{r},{n},{d}, {dtString},{d1},Present, {lecturer}, {c}"
                f.writelines(f"\n{entry}")
                print(f"Attendance recorded: {entry}")
            else:
                print(f"ID {i} is already in the attendance list.")

    # face recognition
    def face_recog(self):
        unit_name = self.unit_combobox.get()
        cohort = self.cohort_entry.get()

        if not unit_name or (self.cohort_entry.cget('state') == 'normal' and not cohort):
            messagebox.showerror("Input Error", "Please enter Unit Name, Cohort (if applicable), and Lecturer's name")
            return None

        def draw_boundray(img, classifier, scaleFactor, minNeighbors, clf):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray_image = cv2.equalizeHist(gray_image)
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            coord = []
            for (x, y, w, h) in features:
                cv2.rectangle(img, (x, y), (x + w + 20, y + h + 20), (0, 255, 0), 3)
                id, predict = clf.predict(gray_image[y:y + h + 20, x:x + w + 20])

                print(id)
                confidence = int((100 * (1 - predict / 300)))

                conn = sqlite3.connect('neoscapedb.sqlite')
                my_cursor = conn.cursor()

                my_cursor.execute("SELECT student_name FROM student WHERE student_id = ?", (str(id),))
                result = my_cursor.fetchone()
                n = "+".join(result) if result else "Unknown"

                my_cursor.execute("SELECT roll_number FROM student WHERE student_id = ?", (str(id),))
                result = my_cursor.fetchone()
                r = "+".join(result) if result else "Unknown"

                my_cursor.execute("SELECT department FROM student WHERE student_id = ?", (str(id),))
                result = my_cursor.fetchone()
                d = "+".join(result) if result else "Unknown"

                my_cursor.execute("SELECT student_id FROM student WHERE student_id = ?", (str(id),))
                result = my_cursor.fetchone()
                i = "+".join(result) if result else "Unknown"

                my_cursor.execute("SELECT course FROM student WHERE student_id = ?", (str(id),))
                result = my_cursor.fetchone()
                c = "+".join(result) if result else "Unknown"

                conn.close()

                if predict < 500:
                    confidence = int((100 * (1 - predict / 300)))
                    cv2.putText(img, f"Accuracy:{confidence}%", (x, y - 125), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                                (0, 255, 0), 3)

                if confidence > 78:
                    cv2.putText(img, f"id: {i}", (x, y - 100), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Roll:{r}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Name:{n}", (x, y - 50), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Department:{d}", (x, y - 25), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Course:{c}", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    self.mark_attendance(i, r, n, d, c)
                else:
                    cv2.rectangle(img, (x, y), (x + w + 20, y + h + 20), (0, 0, 255), 3)
                    speak_va("Warning!!! Unknown Face")
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                coord.append((x, y, w, h))

            return coord

        def recognize(img, clf, faceCascade):
            coord = draw_boundray(img, faceCascade, 1.1, 10, clf)

            for c in coord:
                print(f"Detected face at: x={c[0]}, y={c[1]}, width={c[2]}, height={c[3]}")
            return img

        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        clf = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
        clf.read("classifier.xml")

        video_cap = cv2.VideoCapture(0)

        while True:
            ret, img = video_cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            img = recognize(img, clf, faceCascade)
            cv2.imshow("Welcome to Face Recognition", img)

            if cv2.waitKey(1) == 13:  # Press 'Enter' to exit
                break
        video_cap.release()
        cv2.destroyAllWindows()

    try:
        df_state = pd.read_csv("attendance.csv")
        DF_RM_DUP = df_state.drop_duplicates(keep=False)
        DF_RM_DUP.to_csv('test1.csv', index=False)
    except Exception as e:
        print(f"Error processing attendance file: {e}")
        messagebox.showerror("Error", f"Due to: {e}")


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
