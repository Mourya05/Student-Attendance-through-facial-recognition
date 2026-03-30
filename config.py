"""
Configuration module for the Facial Recognition Attendance System
"""

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',      # MySQL server host
    'user': 'root',           # MySQL username
    'password': 'your_password',   # MySQL password (change as needed)
    'database': 'college_attendance',
    'raise_on_warnings': True
}

# Face Recognition Configuration
FACE_RECOGNITION_CONFIG = {
    'known_faces_dir': 'known_faces',  # Directory containing reference images
    'tolerance': 0.6,                   # Face comparison tolerance (lower = stricter)
    'model': 'hog'                      # Model type: 'hog' or 'cnn' (cnn is more accurate but slower)
}

# Camera Configuration
CAMERA_CONFIG = {
    'camera_index': 0,          # Camera device index (0 = default)
    'frame_width': 1280,
    'frame_height': 720,
    'fps': 30,
    'resize_scale': 0.25        # Scale factor for faster processing
}

# UI Configuration
UI_CONFIG = {
    'font': 'Courier New',
    'font_scale': 0.7,
    'thickness': 2,
    'box_color': (0, 255, 0),           # Green for recognized
    'unknown_color': (0, 0, 255),       # Red for unknown
    'text_color': (255, 255, 255),      # White text
    'status_color': (0, 255, 0),        # Green for success
    'duplicate_color': (255, 165, 0)    # Orange for duplicate
}

# System Configuration
SYSTEM_CONFIG = {
    'attendance_check_interval': 10,    # Seconds between duplicate checks
    'recognition_threshold': 0.5,       # Confidence threshold (0-1)
    'max_face_distance': 0.6            # Maximum distance to consider a match
}
