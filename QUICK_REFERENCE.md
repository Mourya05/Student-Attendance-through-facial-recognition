# 🎯 QUICK REFERENCE CARD

## 📥 Installation & Deployment (Copy-Paste)

```powershell
# Step 1: Install all dependencies
pip install -r requirements.txt

# Step 2: Check system readiness
python check_system.py

# Step 3: Initialize MySQL database (one time only)
python setup_database.py

# Step 4: Start the application
python main.py
```

## ⚙️ Configuration Before Running

**Edit `config.py` Line 5-9:**
```python
DB_CONFIG = {
    'host': 'localhost',           # ← Your MySQL host
    'user': 'root',                # ← Your MySQL username
    'password': 'password',        # ← CHANGE THIS! Your MySQL password
    'database': 'attendance_db',
    'raise_on_warnings': True
}
```

## 📁 Required Folder Structure

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
    └── photo1.jpg
```

**Minimum**: 2 photos per person  
**Ideal**: 3-5 photos per person, different angles

## 🎮 Keyboard Controls During Runtime

| Key | Action |
|-----|--------|
| `q` | Quit safely |
| `r` | Reset system |
| `s` | Show today's attendance |

## 📊 What the System Does

### Real-Time Display
- 🟢 **Green Box** = Recognized & Marked
- 🔴 **Red Box** = Unknown Face
- 🟠 **Orange Box** = Already Marked Today

### Console Output Examples
```
[FACE ENGINE] Loaded john_doe with 3 image(s)
[DATABASE] Attendance marked for john_doe at 2026-03-30 14:23:45
[SYSTEM] john_doe already marked for today
```

## 🔧 Configuration Options (Advanced)

### Adjust Face Recognition Tolerance
**File**: `config.py`, Line 19
```python
'tolerance': 0.6  # Lower = stricter, Higher = lenient
```
- **0.4-0.5**: Very strict (fewer false positives)
- **0.6**: Balanced (default)
- **0.8+**: Lenient (more matches)

### Change Camera
**File**: `config.py`, Line 25
```python
'camera_index': 0  # Try 0, 1, 2... if camera not found
```

### Improve Performance (Slow Computer)
**File**: `config.py`, Line 29
```python
'resize_scale': 0.5  # Increase from 0.25 to 0.5
```

### Better Accuracy (Slower)
**File**: `config.py`, Line 20
```python
'model': 'cnn'  # Change from 'hog' to 'cnn'
```

## 🐛 Quick Troubleshooting

### "ModuleNotFoundError"
```powershell
pip install -r requirements.txt
```

### "Cannot open camera"
1. Check another app isn't using it
2. Try `'camera_index': 1` in config.py
3. Test with Windows Camera app

### "Failed to connect to database"
1. Check MySQL is running
2. Verify username/password in config.py
3. Run `python setup_database.py`

### "Faces not recognized"
1. Add more photos to known_faces/
2. Use different angles/lighting
3. Lower tolerance to 0.5 in config.py

### System runs slow
1. Reduce `frame_width` to 640
2. Increase `resize_scale` to 0.5
3. Use 'hog' model instead of 'cnn'

## 📈 Performance Presets

### Ultra-Fast (Laptop/Raspberry Pi)
```python
# In config.py CAMERA_CONFIG:
'frame_width': 320,
'frame_height': 240,
'resize_scale': 1.0         # Full size = process fast

# In FACE_RECOGNITION_CONFIG:
'model': 'hog',             # Faster
'tolerance': 0.7            # More lenient
```

### Balanced (Default - Most Systems)
```python
# Already configured - just run!
# Frame: 1280x720
# Model: HOG
# Tolerance: 0.6
```

### High-Accuracy (GPU/Powerful PC)
```python
# In config.py FACE_RECOGNITION_CONFIG:
'model': 'cnn',             # More accurate
'tolerance': 0.5            # Strict matching

# In CAMERA_CONFIG:
'resize_scale': 0.15        # More detail
```

## 📝 File Quick Reference

| File | When to Use | How to Use |
|------|-------------|-----------|
| **main.py** | Run the app | `python main.py` |
| **config.py** | Change settings | Edit with text editor |
| **setup_database.py** | Setup DB | `python setup_database.py` (1 time) |
| **check_system.py** | Verify setup | `python check_system.py` |
| **README.md** | Full docs | View in text editor/VS Code |
| **SETUP_GUIDE.md** | Installation help | Step-by-step instructions |
| **ARCHITECTURE.md** | System design | How it works internally |

## 🎓 Code Structure Overview

```
main.py
├── AttendanceSystem class
│   ├── initialize()        ← Setup everything
│   ├── run()              ← Main loop
│   ├── process_frame()    ← Create UI
│   └── cleanup()          ← Safe exit
│
├── database.py → AttendanceDatabase
│   ├── connect()
│   ├── mark_attendance()
│   ├── is_already_marked()
│   └── get_today_attendance()
│
└── face_recognition_engine.py → FaceRecognitionEngine
    ├── load_known_faces()
    └── detect_and_recognize_faces()
```

## 🔒 Database Commands (MySQL)

### View attendance table
```sql
SELECT * FROM attendance;
```

### View today's records
```sql
SELECT * FROM attendance WHERE date = CURDATE();
```

### Count by person
```sql
SELECT name, COUNT(*) FROM attendance WHERE date = CURDATE() GROUP BY name;
```

### Backup database
```bash
mysqldump -u root -p attendance_db > backup_2026-03-30.sql
```

## ⏱️ Expected Performance

| Operation | Time |
|-----------|------|
| Startup (with 5 people) | 3-5 seconds |
| Face detection per frame | 100-300ms |
| Database query | <50ms |
| Video frame display | 33ms (30 fps) |
| Full app load | <10 seconds |

## 🏆 Success Checklist

- [ ] Python 3.7+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] MySQL server running
- [ ] config.py updated with DB credentials
- [ ] Database initialized (`python setup_database.py`)
- [ ] known_faces/ folder has subfolders with photos
- [ ] Diagnostics pass (`python check_system.py`)
- [ ] Application starts (`python main.py`)
- [ ] Camera shows live feed
- [ ] Face detection working (green box)
- [ ] Attendance marked in database
- [ ] 's' key shows today's records

## 🚀 Typical Workflow

1. **Morning Setup**
   ```powershell
   python main.py
   ```

2. **People Walk In Front of Camera**
   - System recognizes faces
   - Marks attendance automatically
   - Shows green box with name

3. **Check Records**
   - Press `s` to see today's attendance
   - Or query: `SELECT * FROM attendance WHERE date = CURDATE();`

4. **End of Day**
   - Press `q` to quit
   - Attendance data saved in MySQL

## 🎯 Where to Start

1. **New to system?** → Read SETUP_GUIDE.md
2. **Want quick start?** → Follow Installation section above
3. **Need details?** → Check README.md
4. **Understanding design?** → See ARCHITECTURE.md
5. **Having issues?** → Run check_system.py

## 📞 Error Message Directory

| Error | Fix |
|-------|-----|
| `No module named 'face_recognition'` | `pip install face_recognition` |
| `mysql.connector.Error: 1045` | Wrong password in config.py |
| `mysql.connector.Error: 1049` | Run `python setup_database.py` |
| `mysql.connector.Error: 2003` | MySQL server not running |
| `Failed to open camera` | Change camera_index in config.py |
| `No faces in image` | Improve lighting, closer to camera |

## 💡 Pro Tips

✓ Use 3x3 grid of photos (9 photos per person) for best accuracy  
✓ Ensure good lighting when taking reference photos  
✓ Avoid excessive makeup/accessories variations in reference photos  
✓ Place camera at eye level for better recognition  
✓ Use high-resolution camera for accuracy  
✓ Regularly check database for accuracy  
✓ Take new photos every 6 months for adaptation  
✓ Use underscores in folder names: john_doe (not john doe)  

---

**Version**: 1.0.0  
**Status**: Production Ready  
**Created**: March 2026

Print this page for quick reference during setup!
