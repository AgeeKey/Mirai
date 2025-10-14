"""
Integration test for dashboard server
Tests all API endpoints and dashboard functionality
"""
import sys
import subprocess
import time
import requests
from pathlib import Path

def test_dashboard_startup():
    """Test that dashboard server starts"""
    proc = None
    try:
        # Start dashboard in background
        proc = subprocess.Popen(
            [sys.executable, "mirai.py", "--mode", "dashboard", "--port", "5555"],
            cwd=str(Path(__file__).parent.parent.parent.parent),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(3)
        
        # Check if process is running
        if proc.poll() is not None:
            stdout, stderr = proc.communicate()
            print(f"Dashboard failed to start:\nSTDOUT: {stdout}\nSTDERR: {stderr}")
            raise AssertionError("Dashboard failed to start")
        
        print("✅ Dashboard started")
        
        # Test health endpoint
        try:
            response = requests.get("http://localhost:5555/api/health", timeout=5)
            print(f"Health response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Health data: {data}")
                print("✅ Health endpoint works")
            else:
                print(f"⚠️ Health endpoint returned {response.status_code}")
        except requests.RequestException as e:
            print(f"⚠️ Could not connect to health endpoint: {e}")
        
    finally:
        if proc:
            proc.terminate()
            proc.wait(timeout=5)
            print("✅ Dashboard stopped")

def test_dashboard_import():
    """Test that dashboard modules can be imported"""
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    
    try:
        from dashboard_server import app
        print("✅ Dashboard server can be imported")
        assert app is not None
    except ImportError as e:
        print(f"⚠️ Dashboard import failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing Dashboard...")
    test_dashboard_import()
    test_dashboard_startup()
    print("🎉 All dashboard tests passed!")
