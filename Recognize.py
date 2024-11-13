import datetime
import os
import threading
import time
from tkinter import *

import cv2
import face_recognition
import numpy as np
import pandas as pd


def load_known_faces(known_faces_dir):
    known_faces = []
    known_reg_nums = []
    for name in os.listdir(known_faces_dir):
        if not os.path.isdir(os.path.join(known_faces_dir, name)):
            continue
        for filename in os.listdir(os.path.join(known_faces_dir, name)):
            if filename.lower().endswith(('png', 'jpg', 'jpeg')):
                img_path = os.path.join(known_faces_dir, name, filename)
                img = face_recognition.load_image_file(img_path)
                encoding = face_recognition.face_encodings(img)
                if len(encoding) > 0:
                    known_faces.append(encoding[0])
                    reg_num = name.split('_')[1]
                    known_reg_nums.append(reg_num)
    return known_faces, known_reg_nums


def recognize_attendance():
    directory = "Attendance"
    if not os.path.exists(directory):
        os.makedirs(directory)

    known_faces_dir = "Training Image"
    known_faces, known_reg_nums = load_known_faces(known_faces_dir)

    df = pd.read_csv("StudentDetails" + os.sep + "StudentDetails.csv")
    df.columns = ['Reg_Num', 'Full_Name']
    df['Reg_Num'] = df['Reg_Num'].str.strip()
    df['Full_Name'] = df['Full_Name'].str.strip()
    df.dropna(inplace=True)

    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['RegNum', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)

    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)

    while True:
        ret, im = cam.read()
        if not ret:
            print("Failed to grab frame")
            break

        rgb_frame = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"
            reg_num = "Unknown"

            face_distances = face_recognition.face_distance(known_faces, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                reg_num = known_reg_nums[best_match_index]
                name = df.loc[df['Reg_Num'] == reg_num, 'Full_Name'].values
                if len(name) == 0:
                    name = "Unknown"
                else:
                    name = name[0]

            cv2.rectangle(im, (left, top), (right, bottom), (10, 159, 255), 2)
            display_str = f"{reg_num}-{name}"
            cv2.putText(im, display_str, (left + 5, top - 5), font, 1, (255, 255, 255), 2)

            if name != "Unknown":
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                attendance.loc[len(attendance)] = [reg_num, name, date, timestamp]

        attendance = attendance.drop_duplicates(subset=['RegNum'], keep='first')
        cv2.imshow('Attendance', im)
        if cv2.waitKey(1) == ord('q'):
            break

    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

    try:
        Hour, Minute, Second = timestamp.split(":")
    except ValueError:
        print("Error! Invalid timestamp format. Attendance record skipped.")
        Hour = Minute = Second = "00"

    fileName = os.path.join(directory, f"Attendance_{date}_{Hour}-{Minute}-{Second}.csv")
    attendance.to_csv(fileName, index=False)
    print("Attendance Successful")
    cam.release()
    cv2.destroyAllWindows()


def start_recognition_thread():
    threading.Thread(target=recognize_attendance).start()


def create_gui():
    root = Tk()
    root.title("Face Recognition Attendance System")

    recognize_button = Button(root, text="Recognize", command=start_recognition_thread)
    recognize_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
