#!/usr/bin/env python3
"""
Quickstart validation script to test the foundation
"""
import subprocess
import sys
import time
import requests
from pathlib import Path

def check_backend_running():
    """Check if backend is running by testing the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("[INFO] Validating Phase II Foundation...")

    # Check if backend directory exists
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("[ERROR] Backend directory not found")
        return False

    print("[SUCCESS] Backend directory found")

    # Check if required files exist
    required_files = [
        "backend/main.py",
        "backend/requirements.txt",
        "backend/database/engine.py",
        "backend/models/task.py",
        ".env.example"
    ]

    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"[ERROR] Required file missing: {file_path}")
            return False
        print(f"[SUCCESS] Found: {file_path}")

    print("\n[INFO] All required files are in place!")

    # Check if we can import the dependencies (without running the server)
    try:
        import fastapi
        import sqlmodel
        import uvicorn
        print("[SUCCESS] Dependencies can be imported")
    except ImportError as e:
        print(f"[ERROR] Dependency import failed: {e}")
        return False

    print("\n[SUCCESS] Foundation validation successful!")
    print("All Phase II foundation components are properly set up.")
    print("\nTo run the application:")
    print("  cd backend")
    print("  python main.py")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)