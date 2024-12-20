#!/usr/bin/env python3
import os
import subprocess
import sys
import time

# Set environment variables for Flask
os.environ["FLASK_APP"] = "app"  # Replace with your main app file (without .py)
os.environ["FLASK_ENV"] = "production"  # Use 'development' for local testing
os.environ["PORT"] = "8080"  # Render will set this automatically

# Directory of the current script (start_server.py)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Constants
SERVER_DIR = SCRIPT_DIR
PORT = int(os.environ.get("PORT", 8080))  # Use the PORT from environment or default to 8080
LOG_FILE = os.path.join(SCRIPT_DIR, "server.log")

def start_flask_server():
    """Start the Flask server using Gunicorn."""
    print(f"[INFO] Starting Gunicorn server in '{SERVER_DIR}' on port {PORT}...")
    with open(LOG_FILE, "a") as log:
        process = subprocess.Popen(
            [
                "gunicorn", 
                "app:app",  # Flask app entry point (update if necessary)
                f"--bind=0.0.0.0:{PORT}",  # Bind to all IP addresses on the specified port
                "--workers=2",  # Number of workers for handling requests (adjust as needed)
                "--threads=4",  # Number of threads per worker (adjust as needed)
            ],
            cwd=SERVER_DIR,
            stdout=log,
            stderr=log,
            text=True,
        )
        print(f"[INFO] Gunicorn server is running at http://0.0.0.0:{PORT}")
        print(f"[INFO] Logs are being saved to {LOG_FILE}")
        return process

def monitor_server(process):
    """Monitor the server process and ensure it runs indefinitely."""
    print("[INFO] Press Ctrl+C to stop monitoring and shut down the server.")
    try:
        while True:
            time.sleep(10)
            if process.poll() is not None:
                print("[ERROR] The server has stopped unexpectedly!")
                break
    except KeyboardInterrupt:
        print("\n[INFO] Stopping the server...")
        process.terminate()
        print("[INFO] Server stopped.")

def main():
    # Start the Flask server with Gunicorn
    server_process = start_flask_server()
    monitor_server(server_process)

if __name__ == "__main__":
    main()
