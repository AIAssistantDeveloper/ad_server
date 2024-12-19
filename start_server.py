#!/usr/bin/env python3
import os
import subprocess
import sys
import time
import shutil  # To check for the existence of busybox

# Directory of the current script (start_server.py)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Update constants to use the script's directory
SERVER_DIR = SCRIPT_DIR
PORT = 8080
LOG_FILE = os.path.join(SCRIPT_DIR, "server.log")

def acquire_wakelock():
    """Acquire the Termux wake-lock and confirm."""
    print("[INFO] Acquiring wakelock...")
    try:
        subprocess.run(["termux-wake-lock"], check=True)
        print("[INFO] Wakelock acquired. Check Termux notification bar.")
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to acquire wakelock. Is Termux API installed?")

def start_server():
    """Start the HTTP server, either using BusyBox or Python."""
    print(f"[INFO] Starting HTTP server in '{SERVER_DIR}' on port {PORT}...")
    
    # Check if busybox is available
    if shutil.which("busybox"):
        print("[INFO] Found busybox. Using BusyBox HTTP server...")
        # Start BusyBox HTTP server
        with open(LOG_FILE, "a") as log:
            process = subprocess.Popen(
                ["busybox", "httpd", "-f", "-p", str(PORT), "-h", SERVER_DIR],
                stdout=log,
                stderr=log,
                text=True,
            )
    else:
        print("[WARNING] busybox not found. Falling back to Python HTTP server...")
        # Fall back to Python's built-in HTTP server
        with open(LOG_FILE, "a") as log:
            process = subprocess.Popen(
                ["python3", "-m", "http.server", str(PORT)],
                cwd=SERVER_DIR,
                stdout=log,
                stderr=log,
                text=True,
            )
    print(f"[INFO] HTTP server is running at http://0.0.0.0:{PORT}")
    print(f"[INFO] Logs are being saved to {LOG_FILE}")
    return process

def monitor_server(process):
    """Monitor the server process and ensure it runs indefinitely."""
    print("[INFO] Press Ctrl+C to stop monitoring and shut down the server.")
    try:
        while True:
            time.sleep(10)
            # Check if the process is still running
            if process.poll() is not None:
                print("[ERROR] The server has stopped unexpectedly!")
                break
    except KeyboardInterrupt:
        print("\n[INFO] Stopping the server...")
        process.terminate()
        print("[INFO] Server stopped.")

def main():
    acquire_wakelock()
    server_process = start_server()
    monitor_server(server_process)

if __name__ == "__main__":
    main()
