"""
Main application for Facial Recognition Attendance System
Captures live camera feed, recognizes faces, and records attendance in MySQL database
"""

import cv2
import sys
from datetime import datetime, timedelta
from config import CAMERA_CONFIG, UI_CONFIG, SYSTEM_CONFIG
from database import AttendanceDatabase
from face_recognition_engine import FaceRecognitionEngine


class AttendanceSystem:
    """Main attendance system orchestrator"""

    def __init__(self):
        """Initialize the attendance system"""
        self.database = AttendanceDatabase()
        self.face_engine = None
        self.camera = None
        self.last_marked = {}  # Track last marked time for each person
        self.running = False

    def initialize(self):
        """Initialize all system components"""
        try:
            print("\n" + "="*60)
            print("FACIAL RECOGNITION ATTENDANCE SYSTEM - Initializing")
            print("="*60 + "\n")

            # Initialize database
            print("[SYSTEM] Initializing database connection...")
            if not self.database.connect():
                print("[SYSTEM ERROR] Failed to connect to database")
                return False

            # Initialize face recognition engine
            print("[SYSTEM] Loading face recognition engine...")
            self.face_engine = FaceRecognitionEngine()
            if self.face_engine.get_known_faces_count() == 0:
                print("[SYSTEM WARNING] No known faces loaded. Please add face images to the 'known_faces' directory")
                print("[SYSTEM WARNING] Create subdirectories for each person (e.g., known_faces/john_doe/image1.jpg)")

            # Initialize camera
            print("[SYSTEM] Initializing camera...")
            self.camera = cv2.VideoCapture(CAMERA_CONFIG['camera_index'])

            if not self.camera.isOpened():
                print("[SYSTEM ERROR] Failed to open camera")
                return False

            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_CONFIG['frame_width'])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_CONFIG['frame_height'])
            self.camera.set(cv2.CAP_PROP_FPS, CAMERA_CONFIG['fps'])

            self.running = True
            print("[SYSTEM] System initialized successfully!")
            print("\n" + "="*60)
            print("Press 'q' to quit, 'r' to reset, 's' to show today's attendance")
            print("="*60 + "\n")
            return True

        except Exception as err:
            print(f"[SYSTEM ERROR] Initialization failed: {err}")
            return False

    def should_mark_attendance(self, name):
        """
        Check if attendance should be marked for a person
        Prevents marking the same person multiple times within a time interval

        Args:
            name (str): Name of the person

        Returns:
            bool: True if attendance should be marked, False otherwise
        """
        current_time = datetime.now()
        check_interval = SYSTEM_CONFIG['attendance_check_interval']

        if name not in self.last_marked:
            return True

        time_diff = (current_time - self.last_marked[name]).total_seconds()
        if time_diff > check_interval:
            return True

        return False

    def draw_face_box_and_label(self, frame, face_info, status):
        """
        Draw bounding box and information on the frame

        Args:
            frame (numpy.ndarray): Video frame to draw on
            face_info (dict): Face information including coordinates
            status (str): Status message ('Present', 'Already Marked', 'Unknown')
        """
        try:
            top = face_info['top']
            right = face_info['right']
            bottom = face_info['bottom']
            left = face_info['left']

            name = face_info['name']
            confidence = face_info['confidence']

            # Determine colors based on status
            if name == "Unknown":
                box_color = UI_CONFIG['unknown_color']
                status_color = UI_CONFIG['unknown_color']
            elif status == "Duplicate":
                box_color = UI_CONFIG['duplicate_color']
                status_color = UI_CONFIG['duplicate_color']
            else:
                box_color = UI_CONFIG['box_color']
                status_color = UI_CONFIG['status_color']

            # Draw bounding box
            cv2.rectangle(frame, (left, top), (right, bottom), box_color, 2)

            # Draw name
            name_text = f"{name}" if name != "Unknown" else "Unknown"
            if confidence > 0:
                name_text += f" ({confidence:.2f})"

            cv2.putText(
                frame,
                name_text,
                (left, top - 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                UI_CONFIG['font_scale'],
                UI_CONFIG['text_color'],
                UI_CONFIG['thickness']
            )

            # Draw status
            cv2.putText(
                frame,
                status,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                UI_CONFIG['font_scale'],
                status_color,
                UI_CONFIG['thickness']
            )

        except Exception as err:
            print(f"[UI ERROR] Failed to draw face box: {err}")

    def process_frame(self, frame):
        """
        Process a video frame for face detection and attendance marking

        Args:
            frame (numpy.ndarray): Video frame to process

        Returns:
            numpy.ndarray: Processed frame with annotations
        """
        try:
            # Detect and recognize faces
            face_infos = self.face_engine.detect_and_recognize_faces(frame)

            # Process each detected face
            for face_info in face_infos:
                name = face_info['name']
                status = "Unknown"

                if name != "Unknown":
                    # Check if attendance already marked today
                    if self.database.is_already_marked(name):
                        status = "Already Marked"
                    elif self.should_mark_attendance(name):
                        # Mark attendance
                        if self.database.mark_attendance(name):
                            status = "Attendance Marked"
                            self.last_marked[name] = datetime.now()
                        else:
                            status = "Duplicate"
                    else:
                        status = "Wait to Mark Again"

                # Draw face box and information
                self.draw_face_box_and_label(frame, face_info, status)

            # Draw system information
            info_text = f"Known Faces: {self.face_engine.get_known_faces_count()} | Detected: {len(face_infos)}"
            cv2.putText(
                frame,
                info_text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                UI_CONFIG['text_color'],
                2
            )

            return frame

        except Exception as err:
            print(f"[PROCESS ERROR] Failed to process frame: {err}")
            return frame

    def display_today_attendance(self):
        """Display today's attendance records in console"""
        try:
            records = self.database.get_today_attendance()
            print("\n" + "="*60)
            print("TODAY'S ATTENDANCE RECORDS")
            print("="*60)
            if records:
                print(f"{'ID':<5} {'Name':<20} {'Timestamp':<25} {'Date':<12}")
                print("-"*60)
                for record in records:
                    print(f"{record[0]:<5} {record[1]:<20} {str(record[2]):<25} {str(record[3]):<12}")
            else:
                print("No attendance records for today")
            print("="*60 + "\n")
        except Exception as err:
            print(f"[SYSTEM ERROR] Failed to display attendance: {err}")

    def run(self):
        """Main loop for the attendance system"""
        if not self.initialize():
            self.cleanup()
            return

        try:
            while self.running:
                ret, frame = self.camera.read()

                if not ret:
                    print("[CAMERA ERROR] Failed to capture frame")
                    break

                # Process the frame
                processed_frame = self.process_frame(frame)

                # Display the frame
                cv2.imshow('Facial Recognition Attendance System', processed_frame)

                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF

                if key == ord('q'):
                    print("[SYSTEM] Quitting application...")
                    break
                elif key == ord('r'):
                    print("[SYSTEM] Resetting system...")
                    self.last_marked.clear()
                elif key == ord('s'):
                    self.display_today_attendance()

        except KeyboardInterrupt:
            print("\n[SYSTEM] Interrupted by user")
        except Exception as err:
            print(f"[SYSTEM ERROR] Error in main loop: {err}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up and release all resources"""
        try:
            print("\n[SYSTEM] Cleaning up resources...")

            if self.camera:
                self.camera.release()
                print("[SYSTEM] Camera released")

            cv2.destroyAllWindows()
            print("[SYSTEM] Display windows closed")

            if self.database:
                self.database.disconnect()
                print("[SYSTEM] Database disconnected")

            print("[SYSTEM] Cleanup completed")
            print("="*60 + "\n")

        except Exception as err:
            print(f"[SYSTEM ERROR] Error during cleanup: {err}")


def main():
    """Entry point for the application"""
    system = AttendanceSystem()
    system.run()


if __name__ == "__main__":
    main()
