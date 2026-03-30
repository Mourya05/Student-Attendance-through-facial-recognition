# Quick Start Setup Guide

## Step-by-Step Installation

### Step 1: Install Dependencies

Open PowerShell in the project directory and run:

```powershell
pip install -r requirements.txt
```

**Installation time:** 5-10 minutes (depends on dlib compilation)

### Step 2: Configure MySQL Connection

Edit `config.py`:

```python
DB_CONFIG = {
    'host': 'localhost',           # Change if MySQL is on different machine
    'user': 'root',                # Your MySQL username
    'password': 'your_password',   # Your MySQL password
    'database': 'attendance_db',
    'raise_on_warnings': True
}
```

### Step 3: Initialize Database

Run the database setup script:

```powershell
python setup_database.py
```

Expected output:
```
[DATABASE SETUP] Connecting to MySQL server...
[DATABASE SETUP] Connected successfully
[DATABASE SETUP] Database 'attendance_db' created/verified
[DATABASE SETUP] Connecting to the attendance database...
[DATABASE SETUP] Attendance table created/verified
[DATABASE SETUP] Database setup completed successfully!
```

### Step 4: Prepare Known Faces

Create the directory structure:

```
known_faces/
├── john_doe/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── photo3.jpg
├── jane_smith/
│   ├── face1.png
│   └── face2.png
```

**Important Guidelines:**
- Use folder names without spaces (or with underscores)
- Add 2-3 clear photos per person
- Ensure good lighting in photos
- Different angles work better

### Step 5: Run the Application

```powershell
python main.py
```

Expected console output:
```
============================================================
FACIAL RECOGNITION ATTENDANCE SYSTEM - Initializing
============================================================

[SYSTEM] Initializing database connection...
[DATABASE] Connected to MySQL database successfully
[SYSTEM] Loading face recognition engine...
[FACE ENGINE] Loaded john_doe with 3 image(s)
[FACE ENGINE] Loaded jane_smith with 2 image(s)
[FACE ENGINE] Total: 2 people, 5 encodings loaded
[SYSTEM] Initializing camera...
[SYSTEM] System initialized successfully!

============================================================
Press 'q' to quit, 'r' to reset, 's' to show today's attendance
============================================================
```

### Step 6: Test the System

1. Position your face in front of the camera
2. If you are in the known_faces folder, you'll see a green box with your name
3. Attendance is automatically marked
4. If done again today, you'll see "Already Marked" status
5. Press `s` to view today's records
6. Press `q` to quit

## Common Issues & Solutions

### Issue: "No module named 'face_recognition'"

**Solution:**
```powershell
pip install --upgrade face_recognition
```

### Issue: "mysql.connector not found"

**Solution:**
```powershell
pip install mysql-connector-python
```

### Issue: "Cannot open camera"

**Solution:**
1. Check if another application is using the camera
2. Test camera with Windows Camera app
3. Try changing `camera_index` in config.py:
   ```python
   CAMERA_CONFIG = {
       'camera_index': 1  # Try 0, 1, 2... instead of 0
   }
   ```

### Issue: "Failed to connect to database"

**Solution:**
1. Ensure MySQL server is running
2. Check credentials are correct
3. Test connection:
   ```powershell
   mysql -u root -p your_password
   ```

### Issue: Faces not recognized

**Solution:**
1. Check that photos are in the correct folder structure
2. Ensure photos have clear faces
3. Try adjusting tolerance in `config.py`:
   ```python
   FACE_RECOGNITION_CONFIG = {
       'tolerance': 0.5  # More strict (0.3-0.5)
   }
   ```

## Hardware Requirements

- **CPU**: Intel i5/AMD Ryzen 5 or better
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 2GB free space
- **Camera**: Any USB or built-in webcam

## Performance Tips

For slower computers:
```python
CAMERA_CONFIG = {
    'frame_width': 640,
    'frame_height': 480,
    'resize_scale': 0.5
}
```

For better accuracy:
```python
CAMERA_CONFIG = {
    'resize_scale': 0.25  # Smaller = more detailed
}

FACE_RECOGNITION_CONFIG = {
    'model': 'cnn',      # More accurate (slower)
    'tolerance': 0.5     # Stricter matching
}
```

## Database Backup

To backup attendance records:

```powershell
mysqldump -u root -p attendance_db > backup.sql
```

To restore:
```powershell
mysql -u root -p attendance_db < backup.sql
```

## Production Deployment

Before deploying to production:

1. **Secure credentials:**
   ```python
   import os
   DB_CONFIG['password'] = os.getenv('DB_PASSWORD')
   ```

2. **Enable database encryption**

3. **Implement logging:**
   ```python
   import logging
   logging.basicConfig(filename='attendance.log', level=logging.INFO)
   ```

4. **Add authentication** for accessing records

5. **Regular backups** of the database

6. **Monitor system resources** (CPU, memory, disk space)

## File Locations

After setup, your directory will look like:

```
IoT PBL/
├── main.py                    ← Run this
├── config.py                  ← Edit database credentials
├── database.py
├── face_recognition_engine.py
├── setup_database.py          ← Run once
├── requirements.txt
├── README.md
├── SETUP_GUIDE.md            ← You are here
└── known_faces/
    ├── john_doe/
    │   ├── photo1.jpg
    │   └── photo2.jpg
    └── jane_smith/
        ├── photo1.jpg
        └── photo2.jpg
```

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure database
3. ✅ Initialize database
4. ✅ Add known faces
5. ✅ Run main application
6. Read `README.md` for advanced configuration
7. Customize `config.py` for your needs
8. Deploy to production

## Support Resources

- Python: https://www.python.org/
- OpenCV: https://docs.opencv.org/
- face_recognition: https://github.com/ageitgey/face_recognition
- MySQL: https://dev.mysql.com/doc/

---

Happy coding! 🚀
