Facial Recognition Exam Attendance System

Overview
This project is a Facial Recognition System designed for Neoscape University to automate and streamline the student attendance process during exams. The system captures the student's facial features for registration, and uses those features to verify identity during the exam. The system is built to ensure accurate attendance tracking and improve security in exam halls.


Features

Facial Recognition for Attendance: Uses facial recognition technology to mark student attendance during exams.

Student Registration: Allows students to register their facial features along with their registration details.

Real-Time Verification: During the exam, the system verifies student identity in real time.

Database Integration: All student details and facial recognition data are stored in a database.

Automated Attendance Tracking: Attendance is automatically recorded and can be reviewed after the exam.

Technologies Used

Python: Main programming language for implementing the facial recognition system.

OpenCV: Used for image processing and facial recognition tasks.

Dlib: Used for facial feature detection and recognition.

SQLite: Database for storing student registration details and attendance records.

Tkinter: Graphical User Interface (GUI) for interacting with the system.

NumPy: Used for mathematical operations related to image processing.

Installation

Prerequisites

Before you begin, ensure that you have the following installed:


Python 3.x

pip (Python package manager)

Step-by-Step Installation

Clone the repository:


bash

Copy code

git clone https://github.com/username/facial-recognition-exam-attendance.git

cd facial-recognition-exam-attendance

Install the necessary dependencies:


bash

Copy code

pip install -r requirements.txt

The requirements.txt file includes all the necessary libraries such as OpenCV, dlib, numpy, etc.


Set up the database:


The system uses SQLite for student details and attendance tracking. Ensure that the database is created and tables are set up by running the following script:

bash

Copy code

python setup_db.py

Run the application:


To launch the facial recognition system and start registering students, run:

bash

Copy code

python main.py

Usage

1. Student Registration:
 
2. Open the system, navigate to the Student Registration section.

3.Input the student's registration details (name, ID, department, etc.).

4.The system will prompt the user to capture their facial features using the webcam.

5.Once the face is captured, the details are saved to the database along with the student's facial data.

6. Facial Recognition during Exam:
   
7. During the exam, the system uses the webcam to scan students’ faces.

8. It verifies the student's identity and records the attendance in real time.

9. If a match is found, the student’s attendance is marked, and the student is allowed entry.

10. Viewing Attendance:

11.The system allows authorized users (such as administrators) to view the attendance records.

12. Attendance data is stored in the database and can be accessed for review.


Contributing
If you'd like to contribute to the project, please follow these steps:


Fork the repository.

Create a new branch (git checkout -b feature-branch).

Commit your changes (git commit -am 'Add feature').

Push to the branch (git push origin feature-branch).

Open a pull request.

License

This project is licensed under the MIT License - see the LICENSE file for details.

