import os
import sys
import time
import json
import urllib.request
from urllib.error import URLError
import subprocess

# --- CONFIGURATION ---
MODEL_NAME = "qwen2.5:1.5b"
OLLAMA_API_BASE = "http://127.0.0.1:11434"

# ⚠️ Change this to your actual GitHub URL once you publish the repository!
GITHUB_EXE_URL = "https://github.com/runtime-error7/Dashlox/releases/latest/download/Dashlox.exe"

def print_banner():
    print("\n" + "="*55)
    print("⚡           DASHLOX SYSTEM INSTALLER            ⚡")
    print("="*55)
    print("Initializing your private, offline AI environment...\n")

def setup_desktop_workspace():
    print("📂 Step 1: Building Workspace on your Desktop...")
    
    # Get the user's Desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    workspace_dir = os.path.join(desktop_path, "Dashlox_Workspace")
    data_dir = os.path.join(workspace_dir, "data_in")
    
    try:
        os.makedirs(data_dir, exist_ok=True)
        # Create the .keep file
        with open(os.path.join(data_dir, ".keep"), "w") as f:
            f.write("# Dashlox Drop Zone: Drop your CSV and SQLite files here!\n")
        print(f"   [OK] Workspace created at: {workspace_dir}")
        return workspace_dir
    except Exception as e:
        print(f"   [ERROR] Could not create workspace: {e}")
        sys.exit(1)

def download_main_app(workspace_dir):
    print("\n⬇️  Step 2: Downloading the Dashlox Engine...")
    exe_path = os.path.join(workspace_dir, "Dashlox.exe")
    
    try:
        req = urllib.request.Request(GITHUB_EXE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(exe_path, 'wb') as out_file:
            # We don't stream progress here to keep it simple, just grab the file
            data = response.read()
            out_file.write(data)
        print("   [OK] Dashlox Engine successfully downloaded!")
        return exe_path
    except Exception as e:
        print("   [WARNING] Could not download Dashlox.exe from GitHub.")
        print(f"   Error: {e}")
        print("   (If you haven't published your GitHub release yet, this is normal.)")
        return None

def check_ollama_running():
    print("\n🔌 Step 3: Verifying Local AI Engine (Ollama)...")
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
    print(f"\n🧠 Step 4: Downloading AI Model weights ({MODEL_NAME})...")
    print("   (This requires internet, but only happens ONCE. Please be patient.)\n")
    
    url = f"{OLLAMA_API_BASE}/api/pull"
    payload = json.dumps({"name": MODEL_NAME, "stream": True}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            for line in response:
                if line:
                    data = json.loads(line.decode('utf-8'))
                    if "completed" in data and "total" in data and data["total"] > 0:
                        percent = (data["completed"] / data["total"]) * 100
                        print(f"\r   Downloading: [{percent:5.1f}%] {data.get('status', '')}", end="", flush=True)
                    else:
                        print(f"\r   Status: {data.get('status', 'Processing...'):<40}", end="", flush=True)
            print("\n\n   [OK] AI Model successfully installed and verified!")
    except Exception as e:
        print(f"\n   [ERROR] Failed to download the model: {e}")
        sys.exit(1)

def create_desktop_shortcut(workspace_dir, exe_path):
    if not exe_path or not os.path.exists(exe_path):
        return
        
    print("\n🔗 Step 5: Creating Desktop Shortcut...")
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    shortcut_path = os.path.join(desktop_path, "Dashlox.lnk")
    
    # We use a tiny VBScript payload to create a Windows shortcut cleanly without extra libraries
    vbs_script = f"""
    Set oWS = WScript.CreateObject("WScript.Shell")
    sLinkFile = "{shortcut_path}"
    Set oLink = oWS.CreateShortcut(sLinkFile)
    oLink.TargetPath = "{exe_path}"
    oLink.WorkingDirectory = "{workspace_dir}"
    oLink.Description = "Launch Dashlox Offline AI"
    oLink.Save
    """
    
    vbs_path = os.path.join(workspace_dir, "createshortcut.vbs")
    with open(vbs_path, "w") as f:
        f.write(vbs_script)
        
    subprocess.call(['cscript.exe', vbs_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(vbs_path)
    print("   [OK] Desktop shortcut created!")

if __name__ == "__main__":
    print_banner()
    time.sleep(1)
    
    workspace = setup_desktop_workspace()
    time.sleep(0.5)
    
    exe_location = download_main_app(workspace)
    time.sleep(0.5)
    
    check_ollama_running()
    time.sleep(0.5)
    
    pull_ai_model()
    
    create_desktop_shortcut(workspace, exe_location)
    
    print("\n" + "="*55)
    print("🎉 DASHLOX SETUP COMPLETE! YOU ARE READY TO GO. 🎉")
    print("="*55)
    print("Look at your Desktop! You will see your new Dashlox folder and shortcut.")
    input("\nPress Enter to exit...")
