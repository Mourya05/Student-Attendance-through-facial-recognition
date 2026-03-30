"""
Face recognition engine module using face_recognition library and OpenCV
"""

import os
import face_recognition
import numpy as np
import cv2
from pathlib import Path
from config import FACE_RECOGNITION_CONFIG, CAMERA_CONFIG


class FaceRecognitionEngine:
    """Handles face detection and recognition operations"""

    def __init__(self):
        """Initialize the face recognition engine"""
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        """
        Load and encode all reference faces from the known_faces directory
        Expects subdirectories named after each person containing their photos
        """
        try:
            known_faces_dir = FACE_RECOGNITION_CONFIG['known_faces_dir']

            if not os.path.exists(known_faces_dir):
                print(f"[FACE ENGINE] Creating {known_faces_dir} directory")
                os.makedirs(known_faces_dir)
                print("[FACE ENGINE] Please add person-specific subdirectories with photos")
                return

            person_count = 0
            encoding_count = 0

            # Iterate through subdirectories (each person)
            for person_name in os.listdir(known_faces_dir):
                person_dir = os.path.join(known_faces_dir, person_name)

                # Skip if not a directory
                if not os.path.isdir(person_dir):
                    continue

                person_count += 1
                person_encodings = []

                # Load all images for this person
                for image_file in os.listdir(person_dir):
                    image_path = os.path.join(person_dir, image_file)

                    # Validate file is an image
                    if not image_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                        continue

                    try:
                        # Load and encode the image
                        image = face_recognition.load_image_file(image_path)
                        face_encodings = face_recognition.face_encodings(image)

                        if face_encodings:
                            # Use the first face encoding found
                            person_encodings.append(face_encodings[0])
                            encoding_count += 1

                    except Exception as err:
                        print(f"[FACE ENGINE ERROR] Failed to process {image_path}: {err}")
                        continue

                # Average the encodings for this person (optional but improves accuracy)
                if person_encodings:
                    avg_encoding = np.mean(person_encodings, axis=0)
                    self.known_face_encodings.append(avg_encoding)
                    self.known_face_names.append(person_name)
                    print(f"[FACE ENGINE] Loaded {person_name} with {len(person_encodings)} image(s)")

            print(f"[FACE ENGINE] Total: {person_count} people, {encoding_count} encodings loaded")

        except Exception as err:
            print(f"[FACE ENGINE ERROR] Failed to load known faces: {err}")

    def detect_and_recognize_faces(self, frame):
        """
        Detect and recognize faces in a given frame

        Args:
            frame (numpy.ndarray): Input video frame

        Returns:
            list: List of dictionaries with face information
                  [{
                      'name': str,
                      'top': int,
                      'right': int,
                      'bottom': int,
                      'left': int,
                      'confidence': float
                  }]
        """
        try:
            # Resize frame for faster processing
            scale = CAMERA_CONFIG['resize_scale']
            small_frame = cv2.resize(
                frame,
                (
                    int(frame.shape[1] * scale),
                    int(frame.shape[0] * scale)
                )
            )

            # Convert BGR to RGB for face_recognition library
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Detect face locations and encodings
            face_locations = face_recognition.face_locations(
                rgb_small_frame,
                model=FACE_RECOGNITION_CONFIG['model']
            )
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_infos = []

            # Compare each detected face with known faces
            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(
                    self.known_face_encodings,
                    face_encoding,
                    tolerance=FACE_RECOGNITION_CONFIG['tolerance']
                )
                name = "Unknown"
                confidence = 0.0

                # Calculate face distances
                face_distances = face_recognition.face_distance(
                    self.known_face_encodings,
                    face_encoding
                )

                # Find the best match
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = 1 - face_distances[best_match_index]

                # Scale back the location coordinates
                top, right, bottom, left = face_location
                top = int(top / scale)
                right = int(right / scale)
                bottom = int(bottom / scale)
                left = int(left / scale)

                face_infos.append({
                    'name': name,
                    'top': top,
                    'right': right,
                    'bottom': bottom,
                    'left': left,
                    'confidence': confidence
                })

            return face_infos

        except Exception as err:
            print(f"[FACE ENGINE ERROR] Failed to detect faces: {err}")
            return []

    def get_known_faces_count(self):
        """Get the number of known faces loaded"""
        return len(self.known_face_names)

    def get_known_faces_list(self):
        """Get list of all known face names"""
        return self.known_face_names.copy()
