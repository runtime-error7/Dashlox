import os
import sys
import time
import json
import urllib.request
from urllib.error import URLError

# The AI model we are using. Qwen2.5 1.5B is incredibly fast and smart for JSON/Code.
MODEL_NAME = "qwen2.5:1.5b"
OLLAMA_API_BASE = "http://127.0.0.1:11434"

def print_banner():
    print("\n" + "="*50)
    print("⚡           DASHLOX SYSTEM INSTALLER           ⚡")
    print("="*50)
    print("Initializing your private, offline AI environment...\n")

def setup_workspace():
    print("📂 Step 1: Mapping Local Workspace...")
    
    # Resolve the correct path whether running as a .py script or compiled .exe
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        
    data_dir = os.path.join(base_dir, "data_in")
    
    try:
        os.makedirs(data_dir, exist_ok=True)
        # Create the .keep file so the folder isn't empty
        with open(os.path.join(data_dir, ".keep"), "w") as f:
            f.write("# Dashlox Drop Zone: Drop your CSV and SQLite files here!\n")
        print(f"   [OK] Magic folder created at: {data_dir}")
    except Exception as e:
        print(f"   [ERROR] Could not create workspace: {e}")
        sys.exit(1)

def check_ollama_running():
    print("\n🔌 Step 2: Verifying Local AI Engine (Ollama)...")
    try:
        req = urllib.request.Request(OLLAMA_API_BASE)
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                print("   [OK] Ollama is installed and running.")
                return True
    except URLError:
        print("   [ERROR] Ollama is not running or not installed!")
        print("   Dashlox requires Ollama to run the AI completely offline.")
        print("   1. Go to https://ollama.com and install it.")
        print("   2. Start the Ollama application.")
        print("   3. Run this setup file again.")
        sys.exit(1)

def pull_ai_model():
    print(f"\n🧠 Step 3: Downloading AI Model weights ({MODEL_NAME})...")
    print("   (This requires internet, but only happens ONCE. Please be patient.)\n")
    
    url = f"{OLLAMA_API_BASE}/api/pull"
    # We set stream to True so we can give the user real-time download progress
    payload = json.dumps({"name": MODEL_NAME, "stream": True}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            for line in response:
                if line:
                    data = json.loads(line.decode('utf-8'))
                    
                    # If the API provides byte counts, calculate the percentage
                    if "completed" in data and "total" in data and data["total"] > 0:
                        percent = (data["completed"] / data["total"]) * 100
                        # The \r overwrites the current terminal line to create a live updating bar
                        print(f"\r   Downloading: [{percent:5.1f}%] {data.get('status', '')}", end="", flush=True)
                    else:
                        print(f"\r   Status: {data.get('status', 'Processing...'):<40}", end="", flush=True)
                        
            print("\n\n   [OK] AI Model successfully installed and verified!")
            
    except Exception as e:
        print(f"\n   [ERROR] Failed to download the model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print_banner()
    time.sleep(1)
    
    setup_workspace()
    time.sleep(0.5)
    
    check_ollama_running()
    time.sleep(0.5)
    
    pull_ai_model()
    
    print("\n" + "="*50)
    print("🎉 DASHLOX SETUP COMPLETE! YOU ARE READY TO GO. 🎉")
    print("="*50)
    print("You can now safely close this window.")
    print("Run 'Dashlox.exe' anytime to start your offline dashboard.")
    input("\nPress Enter to exit...")
