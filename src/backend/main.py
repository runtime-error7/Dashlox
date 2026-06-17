import os
import sys
import threading
import time
import webbrowser
import socket
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

# Import our custom API router
from api import router as api_router

# ==========================================
# 1. PATH RESOLUTION (PyInstaller Support)
# ==========================================
def get_resource_path(relative_path):
    """ 
    Dynamically finds the correct path to assets (like HTML/CSS) 
    whether running from source code or inside a compiled PyInstaller .exe
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # If running from normal python, go up two directories from main.py
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        
    return os.path.join(base_path, relative_path)

# ==========================================
# 2. FASTAPI SERVER INITIALIZATION
# ==========================================
app = FastAPI(title="Dashlox Core Engine")

# Mount the API routes
app.include_router(api_router, prefix="/api")

# Mount the Frontend (HTML/JS/CSS)
# We use our get_resource_path to ensure the .exe knows where the frontend is
frontend_path = get_resource_path("src/frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

# ==========================================
# 3. BACKGROUND THREAD WORKERS
# ==========================================
def launch_browser(port):
    """ Waits 2 seconds for the server to boot, then opens Chrome/Edge """
    time.sleep(2)
    webbrowser.open(f"http://127.0.0.1:{port}")

def start_folder_watcher():
    """ Boots up the watchdog script to monitor the data_in/ folder """
    from watcher import start_watching
    
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        
    data_dir = os.path.join(base_dir, "data_in")
    os.makedirs(data_dir, exist_ok=True)
    
    start_watching(data_dir)

def is_port_in_use(port):
    """ Safety check to ensure we don't crash if port 3000 is blocked """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

# ==========================================
# 4. APP ENTRY POINT
# ==========================================
if __name__ == "__main__":
    PORT = 3000
    
    print("\n" + "="*50)
    print("🚀 DASHLOX ENGINE STARTING...")
    print("="*50)
    
    if is_port_in_use(PORT):
        print(f"⚠️  Warning: Port {PORT} is already in use!")
        PORT = 3001 # Fallback port
        print(f"🔄 Switching to fallback port {PORT}...")

    # Start the Folder Watcher in a background Daemon thread
    watcher_thread = threading.Thread(target=start_folder_watcher, daemon=True)
    watcher_thread.start()
    
    # Start the Browser Auto-Launcher in a background Daemon thread
    browser_thread = threading.Thread(target=launch_browser, args=(PORT,), daemon=True)
    browser_thread.start()
    
    print(f"\n🌐 Dashboard will open at: http://127.0.0.1:{PORT}")
    print("🛑 Close this terminal window to stop the application.\n")
    
    # Run the Uvicorn web server
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")
