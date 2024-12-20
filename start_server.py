#!/usr/bin/env python3
import os
import subprocess
import sys
import time

# Directory of the current script (start_server.py)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Constants
SERVER_DIR = SCRIPT_DIR
PORT = 8080
LOG_FILE = os.path.join(SERVER_DIR, "server.log")

def start_server():
    """Start the Python built-in HTTP server."""
    print(f"[INFO] Starting Python HTTP server in '{SERVER_DIR}' on port {PORT}...")
    if not os.path.exists(SERVER_DIR):
        print(f"[ERROR] Directory '{SERVER_DIR}' does not exist!")
        sys.exit(1)

    # Start Python HTTP server
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

def run_gunicorn():
    """Run the server using Gunicorn for production."""
    print(f"[INFO] Starting Gunicorn server in '{SERVER_DIR}' on port {PORT}...")
    with open(LOG_FILE, "a") as log:
        subprocess.run(
            ["gunicorn", "start_server:app", "--workers=2", "--threads=4", f"--bind=0.0.0.0:{PORT}"],
            cwd=SERVER_DIR,
            stdout=log,
            stderr=log,
            text=True,
        )
    print("[INFO] Gunicorn server stopped.")

def main():
    # Check environment to decide server type
    if os.getenv("RENDER") == "true":  # Render environment variable
        run_gunicorn()
    else:
        process = start_server()
        monitor_server(process)

if __name__ == "__main__":
    main()
