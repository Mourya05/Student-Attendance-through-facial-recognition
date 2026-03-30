# Facial Recognition Attendance System

A production-grade Python application for automated attendance marking using facial recognition, OpenCV, and MySQL database.

## Features

- **Real-time Face Detection & Recognition**: Uses `face_recognition` library and OpenCV
- **Database Integration**: MySQL database for persistent attendance records
- **Duplicate Prevention**: Checks if attendance already marked for the current date
- **Live UI/UX**: Bounding boxes with face names and status labels on video feed
- **Error Handling**: Comprehensive try-except blocks for database operations
- **Resource Management**: Proper camera release and database disconnection
- **Keyboard Controls**: Interactive controls for quit, reset, and viewing records

## Project Structure

```
IoT PBL/
├── main.py                      # Main application entry point
├── config.py                    # Configuration settings
├── database.py                  # Database connection and operations
├── face_recognition_engine.py   # Face detection and recognition module
├── setup_database.py            # Database initialization script
├── requirements.txt             # Python dependencies
├── known_faces/                 # Directory for reference face images
│   └── john_doe/               # Person-specific subdirectory
│       ├── photo1.jpg
│       ├── photo2.jpg
│       └── photo3.jpg
└── README.md                    # This file
```

## Prerequisites

- Python 3.7+
- MySQL Server 5.7+ running locally or remotely
- Webcam/Camera device
- CMake (for dlib compilation)

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database Settings

Edit `config.py` and update MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',      # Your MySQL server
    'user': 'root',           # Your MySQL username
    'password': 'password',   # Your MySQL password
    'database': 'attendance_db',
    'raise_on_warnings': True
}
```

### 3. Initialize Database

```bash
python setup_database.py
```

This creates the MySQL database and `attendance` table.

### 4. Add Known Faces

Create subdirectories in `known_faces/` for each person and add their photos:

```
known_faces/
├── john_doe/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg
├── jane_smith/
│   ├── photo1.jpg
│   └── photo2.jpg
└── mike_johnson/
    ├── photo1.jpg
    └── photo2.jpg
```

**Tips for best results:**
- Use at least 2-3 clear photos per person
- Photos should show face clearly with good lighting
- Different angles and expressions improve accuracy
- Use .jpg, .jpeg, .png, or .bmp formats

## Usage

Run the main application:

```bash
python main.py
```

### Keyboard Controls

- **`q`** - Quit the application
- **`r`** - Reset internal state
- **`s`** - Display today's attendance records in console

### Live Display Information

- Green bounding box: Recognized face
- Red bounding box: Unknown face
- Orange bounding box: Already marked for the day
- Status labels show attendance status
- Known faces count displayed at top

## Database Schema

The `attendance` table includes:

| Column    | Type     | Description                          |
|-----------|----------|--------------------------------------|
| id        | INT      | Primary key, auto-increment          |
| name      | VARCHAR  | Person's name                        |
| timestamp | DATETIME | Time of attendance marking           |
| date      | DATE     | Date of attendance marking           |

### Indexes

- Composite index on (name, date) for fast duplicate checks

## Configuration Options

### Face Recognition (`config.py`)

```python
FACE_RECOGNITION_CONFIG = {
    'tolerance': 0.6,        # Lower = stricter matching (0-1)
    'model': 'hog'          # 'hog' (fast) or 'cnn' (accurate)
}
```

**Tolerance Guide:**
- `0.4-0.5`: Very strict, fewer false positives
- `0.6`: Balanced (default)
- `0.8-1.0`: Lenient, more matches

### Camera (`config.py`)

```python
CAMERA_CONFIG = {
    'camera_index': 0,       # 0 = default camera
    'frame_width': 1280,
    'frame_height': 720,
    'fps': 30,
    'resize_scale': 0.25     # Processing speedup factor
}
```

### UI Colors (`config.py`)

```python
UI_CONFIG = {
    'box_color': (0, 255, 0),          # Green for recognized
    'unknown_color': (0, 0, 255),      # Red for unknown
    'duplicate_color': (255, 165, 0)   # Orange for duplicate
}
```
(Colors are in BGR format used by OpenCV)

## Error Handling

The system includes comprehensive error handling for:

### Database Errors
- Connection failures
- Query execution errors
- Transaction rollback on failures

### Camera Errors
- Device not found
- Frame capture failures
- Cleanup on disconnection

### Face Recognition Errors
- Invalid image formats
- Face detection failures
- Encoding errors

All errors are logged with descriptive messages to help troubleshooting.

## Troubleshooting

### Issue: "Failed to connect to database"
- Ensure MySQL server is running
- Check credentials in `config.py`
- Verify database exists and is accessible

### Issue: No faces detected
- Ensure adequate lighting
- Check camera position and angle
- Test camera with another application first
- Adjust `tolerance` in config for stricter/lenient matching

### Issue: Slow performance
- Reduce `frame_width` and `frame_height` in config
- Increase `resize_scale` for faster processing
- Use `'hog'` model instead of `'cnn'` (faster but less accurate)

### Issue: Face encoding errors
- Ensure photos in `known_faces/` are valid image files
- Use clear, well-lit photographs
- Remove corrupted images
- Check file extensions (.jpg, .png, etc.)

## Performance Optimization

### For Faster Processing
```python
CAMERA_CONFIG = {
    'frame_width': 640,
    'frame_height': 480,
    'resize_scale': 0.5
}

FACE_RECOGNITION_CONFIG = {
    'model': 'hog'  # Instead of 'cnn'
}
```

### For Better Accuracy
```python
CAMERA_CONFIG = {
    'resize_scale': 0.5  # Larger processing size
}

FACE_RECOGNITION_CONFIG = {
    'model': 'cnn',      # More accurate CNN model
    'tolerance': 0.5     # Stricter matching
}
```

## Security Considerations

1. **Database Credentials**: Store in environment variables for production
   ```python
   import os
   DB_CONFIG['password'] = os.getenv('DB_PASSWORD')
   ```

2. **Access Control**: Implement user authentication in production

3. **Data Privacy**: Ensure compliance with GDPR/privacy regulations

4. **Log Management**: Implement secure logging for audit trails

## Advanced Features

### Custom Tolerance Per Person
Can be implemented by modifying `face_recognition_engine.py` to use person-specific thresholds.

### Multi-Camera Support
Extend the application to monitor multiple camera feeds simultaneously.

### Email Notifications
Add email alerts when specific individuals mark attendance.

### Analytics Dashboard
Integrate with visualization libraries to create attendance reports.

## License

This project is designed for educational and commercial use.

## Support

For issues or questions, check the troubleshooting section or review error logs in console output.

## Version

- Version 1.0.0
- Last Updated: March 2026

---

**Created by: Senior ML Engineer**
