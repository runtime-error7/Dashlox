import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import the database loader from our DuckDB engine
from engine_db import load_file_into_duckdb

class DataDropHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Ignore sub-folder creation; only look for data files
        if not event.is_directory and event.src_path.endswith(('.csv', '.xlsx', '.json')):
            file_name = os.path.basename(event.src_path)
            print(f"⚡ Dashlox Detected New File: {file_name}")
            
            # Pause for 500ms to allow the OS to finish writing the file to the disk
            # This prevents "file locked" or "file in use" errors.
            time.sleep(0.5) 
            
            # Hand the file path over to the database engine
            load_file_into_duckdb(event.src_path)

def start_watching(path_to_watch):
    """
    Initializes the watchdog observer and keeps it alive.
    """
    event_handler = DataDropHandler()
    observer = Observer()
    
    # recursive=False means we only watch the root of data_in/
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()
    
    print(f"📂 Dashlox Magic Folder Active at: {path_to_watch}")
    
    try:
        # Keep the watching thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
