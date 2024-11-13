from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 1 is for female voice and 0 is for male voice


def speak_va(transcribed_query):
    engine.say(transcribed_query)
    engine.runAndWait()


class Train:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1530x790+0+0")
        self.master.title("Face Recognition System")

        title_lbl = Label(self.master, text="TRAIN DATA SET", font=("Algerian", 20, "bold"), bg="lightgreen", fg="Blue")
        title_lbl.place(x=0, y=0, width=1366, height=35)

        img_top = Image.open(r"Images/re2.jpg")
        img_top = img_top.resize((1366, 700), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.master, image=self.photoimg_top)
        f_lbl.place(x=0, y=50, width=1366, height=650)

        # Button
        b1_1 = Button(self.master, text="TRAIN DATA", command=self.train_classifier, cursor="hand2",
                      font=("Algerian", 25, "bold"), bg="green", fg="white")
        b1_1.place(x=500, y=450, width=300, height=150)

    def train_classifier(self):
        data_dir = "data"
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", "Data directory does not exist")
            return

        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if
                file.lower().endswith(('png', 'jpg', 'jpeg'))]
        if not path:
            messagebox.showerror("Error", "No images found in the data directory")
            return

        faces = []
        ids = []

        for image_path in path:
            try:
                img = Image.open(image_path).convert('L')
                image_np = np.array(img, 'uint8')
                user_id = int(os.path.split(image_path)[1].split('.')[1])

                faces.append(image_np)
                ids.append(user_id)
                cv2.imshow("Training", image_np)
                cv2.waitKey(1)
            except Exception as e:
                print(f"Error processing image {image_path}: {e}")

        ids = np.array(ids)

        if len(faces) == 0 or len(ids) == 0:
            messagebox.showerror("Error", "No valid faces found to train")
            return

        # Train the classifier and save
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()
        speak_va("Training datasets completed successfully!")
        messagebox.showinfo("Result", "Training datasets completed successfully!", parent=self.master)


if __name__ == "__main__":
    root = Tk()
    app = Train(root)
    root.mainloop()
