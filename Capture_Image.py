import csv
import os
import threading
from tkinter import messagebox
import cv2
import face_recognition

headers = ['Reg_Num', 'Full_Name']


def take_images(reg_number, full_name, callback):
    directory = "StudentDetails"
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.makedirs("Training Image", exist_ok=True)
    person_folder = os.path.join("Training Image", f"{full_name}_{reg_number}")
    os.makedirs(person_folder, exist_ok=True)

    cam = cv2.VideoCapture(0)
    sampleNum = 0
    max_images = 15  # Maximum number of images to capture

    while True:
        ret, img = cam.read()
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_img)

        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(img, (left, top), (right, bottom), (10, 159, 255), 2)
            sampleNum += 1
            # Save the image only if the number of images captured is less than or equal to the maximum
            if sampleNum <= max_images:
                img_path = os.path.join(person_folder, f"{full_name}_{reg_number}_{sampleNum}.jpg")
                face_image = rgb_img[top:bottom, left:right]
                cv2.imwrite(img_path, cv2.cvtColor(face_image, cv2.COLOR_RGB2GRAY))
                print(f"Image saved: {img_path}")
            cv2.imshow('frame', img)

        if cv2.waitKey(100) & 0xFF == ord('q') or sampleNum >= max_images:
            break

    cam.release()
    cv2.destroyAllWindows()

    res = f"Images Saved for Registration: {reg_number}, Name: {full_name}"
    row = [reg_number, full_name]

    with open("StudentDetails" + os.sep + "StudentDetails.csv", 'a+') as csvFile:
        writer = csv.writer(csvFile)
        if csvFile.tell() == 0:
            writer.writerow(headers)
        writer.writerow(row)

    callback(res)


def capture_images(reg_number, full_name):
    thread = threading.Thread(target=take_images, args=(reg_number, full_name, update_gui))
    thread.start()


def update_gui(result):
    messagebox.showinfo("Capture Complete", result)


if __name__ == "__main__":
    reg_number_input = input("Enter Registration Number: ")
    full_name_input = input("Enter Full Name: ")
    capture_images(reg_number_input, full_name_input)
