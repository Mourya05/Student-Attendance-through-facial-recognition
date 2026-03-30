"""
System verification and diagnostics utility
Run this before starting the main application to verify all components
"""

import sys
import os
from datetime import datetime


def check_python_version():
    """Check if Python version is compatible"""
    print("[CHECK] Python Version")
    version = sys.version_info
    print(f"  Version: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 7:
        print("  ✓ Compatible")
        return True
    else:
        print("  ✗ Python 3.7+ required")
        return False


def check_required_directories():
    """Check if required directories exist"""
    print("\n[CHECK] Directory Structure")
    required_dirs = ['known_faces']
    all_ok = True

    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  ✓ {directory}/ exists")
        else:
            print(f"  ✗ {directory}/ not found")
            all_ok = False

    return all_ok


def check_required_files():
    """Check if all required Python files exist"""
    print("\n[CHECK] Required Files")
    required_files = [
        'main.py',
        'config.py',
        'database.py',
        'face_recognition_engine.py',
        'setup_database.py',
        'requirements.txt'
    ]
    all_ok = True

    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} not found")
            all_ok = False

    return all_ok


def check_dependencies():
    """Check if all required Python packages are installed"""
    print("\n[CHECK] Python Dependencies")
    required_packages = {
        'cv2': 'opencv-python',
        'face_recognition': 'face_recognition',
        'mysql': 'mysql-connector-python',
        'numpy': 'numpy',
        'PIL': 'Pillow'
    }

    all_ok = True
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"  ✓ {package_name}")
        except ImportError:
            print(f"  ✗ {package_name} not installed")
            print(f"    Run: pip install {package_name}")
            all_ok = False

    return all_ok


def check_camera():
    """Check if camera is accessible"""
    print("\n[CHECK] Camera Access")
    try:
        import cv2
        camera = cv2.VideoCapture(0)
        if camera.isOpened():
            print("  ✓ Camera is accessible")
            camera.release()
            return True
        else:
            print("  ✗ Camera not found or not accessible")
            print("    - Check if another application is using the camera")
            print("    - Try changing camera_index in config.py")
            return False
    except Exception as err:
        print(f"  ✗ Camera check failed: {err}")
        return False


def check_mysql_connection():
    """Check if MySQL connection works"""
    print("\n[CHECK] MySQL Database Connection")
    try:
        import mysql.connector
        from config import DB_CONFIG

        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            print("  ✓ MySQL connection successful")
            print(f"    Host: {DB_CONFIG['host']}")
            print(f"    Database: {DB_CONFIG['database']}")
            cursor.close()
            connection.close()
            return True
        except mysql.connector.Error as err:
            print(f"  ✗ MySQL connection failed")
            if err.errno == 1045:
                print("    - Wrong username/password")
            elif err.errno == 1049:
                print(f"    - Database '{DB_CONFIG['database']}' doesn't exist")
                print("    - Run: python setup_database.py")
            elif err.errno == 2003:
                print("    - Cannot connect to MySQL server")
                print("    - Check if MySQL is running")
            else:
                print(f"    - Error: {err}")
            return False

    except Exception as err:
        print(f"  ✗ Connection check failed: {err}")
        return False


def check_known_faces():
    """Check contents of known_faces directory"""
    print("\n[CHECK] Known Faces Dataset")
    known_faces_dir = 'known_faces'

    if not os.path.exists(known_faces_dir):
        print(f"  ✗ {known_faces_dir}/ directory not found")
        return False

    subdirs = [d for d in os.listdir(known_faces_dir) if os.path.isdir(os.path.join(known_faces_dir, d))]

    if not subdirs:
        print(f"  ⚠ No person folders found in {known_faces_dir}/")
        print("    Create subdirectories like: known_faces/john_doe/")
        print("    Add photos: known_faces/john_doe/photo1.jpg")
        return False

    print(f"  Found {len(subdirs)} person folder(s):")
    image_count = 0

    for person in subdirs:
        person_path = os.path.join(known_faces_dir, person)
        images = [f for f in os.listdir(person_path)
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

        if images:
            print(f"    ✓ {person}: {len(images)} image(s)")
            image_count += len(images)
        else:
            print(f"    ✗ {person}: No valid images")

    if image_count > 0:
        print(f"  Total: {image_count} images across {len(subdirs)} people")
        return True
    else:
        print("  No valid images found")
        return False


def check_config_file():
    """Check if configuration file is properly set"""
    print("\n[CHECK] Configuration")
    try:
        from config import DB_CONFIG, CAMERA_CONFIG, FACE_RECOGNITION_CONFIG

        print("  ✓ Database configuration loaded")
        print("  ✓ Camera configuration loaded")
        print("  ✓ Face recognition configuration loaded")

        # Check for suspicious values
        if DB_CONFIG['password'] == 'password':
            print("  ⚠ Using default database password - change for production!")

        return True
    except Exception as err:
        print(f"  ✗ Configuration error: {err}")
        return False


def run_diagnostics():
    """Run all diagnostic checks"""
    print("="*60)
    print("FACIAL RECOGNITION ATTENDANCE SYSTEM - DIAGNOSTICS")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    results = {
        'Python Version': check_python_version(),
        'Directory Structure': check_required_directories(),
        'Required Files': check_required_files(),
        'Configuration': check_config_file(),
        'Python Dependencies': check_dependencies(),
        'Camera Access': check_camera(),
        'MySQL Connection': check_mysql_connection(),
        'Known Faces Dataset': check_known_faces()
    }

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    print(f"\nPassed: {passed}/{total}")
    print("\nStatus:")

    for check, result in results.items():
        status = "✓" if result else "✗"
        print(f"  {status} {check}")

    print("\n" + "="*60)

    if passed == total:
        print("✓ All checks passed! Ready to run: python main.py")
        print("="*60 + "\n")
        return 0
    else:
        print("✗ Some checks failed. Please review the messages above.")
        print("="*60 + "\n")
        return 1


if __name__ == "__main__":
    exit_code = run_diagnostics()
    sys.exit(exit_code)
