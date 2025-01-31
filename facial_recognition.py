import face_recognition
import cv2
import numpy as np
from datetime import datetime
import csv
import os

video_capture = cv2.VideoCapture(0)

# Create arrays of known face encodings and their names
known_face_encodings = []
known_face_names = []

known_face_encodings = np.load('encodings.npy')

with open('labels.txt', 'r') as file:
    known_face_names = [line.strip() for line in file]

students = known_face_names.copy()

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

classname = "class"

with open(f"{classname}_{current_date}_Attendance.csv", 'w+', newline="") as f:
    lnwriter = csv.writer(f)
    lnwriter.writerow(["USN", "Time entered"])

    while True:
        ret, frame = video_capture.read()
        
        if not ret:
            print("frame empty")
            continue

        

        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
                if name in known_face_names:
                    if name in students:
                        students.remove(name)
                        print(name)
                        current_time = datetime.now().time()
                        time_string = current_time.strftime("%H:%M:%S")
                        lnwriter.writerow([name, time_string])

        process_this_frame = not process_this_frame
"""
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        frame = cv2.resize(frame,(720,720))
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
"""
video_capture.release()
cv2.destroyAllWindows()
