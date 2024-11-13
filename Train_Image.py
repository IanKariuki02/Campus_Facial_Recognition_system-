import os
import time
import tkinter as tk
from threading import Thread
from tkinter import filedialog, messagebox

import cv2
import face_recognition
import numpy as np


def getImageAndLabels(path):
    faces = []
    Ids = []
    id_counter = 0
    reg_number_to_id = {}

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                try:
                    imagePath = os.path.join(root, file)
                    print(f"Processing image: {imagePath}")
                    image = face_recognition.load_image_file(imagePath)
                    face_locations = face_recognition.face_locations(image)

                    if len(face_locations) == 0:
                        print(f"No faces found in image: {imagePath}")
                        continue

                    # Assuming one face per image
                    top, right, bottom, left = face_locations[0]
                    face_image = image[top:bottom, left:right]
                    face_image_gray = cv2.cvtColor(face_image, cv2.COLOR_RGB2GRAY)

                    folder_name = os.path.basename(root)
                    reg_number = folder_name.split('_')[1]
                    print(f"Extracted registration number: {reg_number}")

                    if reg_number not in reg_number_to_id:
                        reg_number_to_id[reg_number] = id_counter
                        id_counter += 1
                    Id = reg_number_to_id[reg_number]
                    faces.append(face_image_gray)
                    Ids.append(Id)
                    print(f"Image {file} processed: reg_number={reg_number}, id={Id}")
                except Exception as e:
                    print(f"Error processing image {file}: {e}")
    print(f"Registration Numbers to IDs mapping: {reg_number_to_id}")
    return faces, Ids


def select_folder():
    root = tk.Tk()
    root.withdraw()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    folder_selected = filedialog.askdirectory(initialdir=script_dir, title="Select Folder to Train")
    if folder_selected:
        print(f"Folder selected: {folder_selected}")
        if any(file.lower().endswith(('png', 'jpg', 'jpeg')) for file in os.listdir(folder_selected)):
            return folder_selected
        else:
            messagebox.showerror("Error", "The selected folder does not contain any image files.")
            return None
    else:
        messagebox.showerror("Error", "No folder selected")
        return None


def TrainImages():
    folder = select_folder()
    if not folder:
        return
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    faces, Ids = getImageAndLabels(folder)
    if not faces or not Ids:
        print("No faces or IDs found in the training data. Please check the selected directory.")
        return
    print(f"Training with faces: {len(faces)}, IDs: {len(Ids)}")
    recognizer.train(faces, np.array(Ids))
    print("Model Trained successfully. Saving model.....")

    main_directory = os.path.dirname(os.path.realpath(__file__))
    trained_model_path = os.path.join(main_directory, "TrainingImageLabel", "Trainer.yml")

    if not os.path.exists("TrainingImageLabel"):
        os.makedirs("TrainingImageLabel")
    recognizer.save(trained_model_path)
    print("Trained model saved successfully at:", trained_model_path)
    Thread(target=counter_img, args=(folder,)).start()


def counter_img(path):
    imgcounter = 1
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                print(f"{imgcounter} Images Training", end="\r")
                time.sleep(0.008)
                imgcounter += 1


if __name__ == "__main__":
    TrainImages()
