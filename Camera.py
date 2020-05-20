import glob
import cv2
import os
import face_recognition
import numpy as np


class Camera:
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'known_users/')

    def __init__(self, video_device=0):
        self.__cap = cv2.VideoCapture(video_device)
        self.__known_face_encodings = []
        self.__known_face_names = []
        self.__face_locations = []
        self.__face_names = []

        self.start()

    def __initialize_faces(self):
        list_of_files = [f for f in glob.glob(f"{Camera.path}*.jpg")]
        number_of_known_faces = len(list_of_files)
        names = list_of_files.copy()

        for i in range(number_of_known_faces):
            globals()[f"image_{i}"] = face_recognition.load_image(list_of_files[i])
            globals()[f"image_encoding_{i}"] = face_recognition.face_encodings(globals()[f"image_{i}"])[0]
            self.__known_face_names.append(globals()[f"image_encoding_{i}"])

            names[i] = names[i].replace("known_people/", "")
            self.__known_face_names.append(names[i])

    def start(self):
        face_encodings = []

        while self.__cap.isOpened():
            success, frame = self.__cap.read()

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            if success:
                self.__face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, self.__face_locations)

                face_names = []

                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(self.__known_face_encodings, face_encoding)

                    name = 'Unknown'

                    face_distances = face_recognition.face_distance(self.__known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = self.__known_face_names[best_match_index]

                    face_names.append(name)

            self.__display_faces(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.release()
                break

    def __display_faces(self, frame):
        for(top, right, bottom, left), name in zip(self.__face_locations, self.__face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

    def release(self):
        cv2.destroyAllWindows()
        self.__cap.release()
