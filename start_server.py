#!/usr/bin/env python3
import os
import subprocess
import sys
import time

# Constants
SERVER_DIR = os.path.expanduser("~/ad_server")
PORT = 8080
LOG_FILE = os.path.expanduser("~/ad_server/server.log")


def acquire_wakelock():
    """Acquire the Termux wake-lock and confirm."""
    print("[INFO] Acquiring wakelock...")
    try:
        subprocess.run(["termux-wake-lock"], check=True)
        print("[INFO] Wakelock acquired. Check Termux notification bar.")
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to acquire wakelock. Is Termux API installed?")


def start_server():
    """Start the BusyBox HTTP server."""
    print(f"[INFO] Starting BusyBox HTTP server in '{SERVER_DIR}' on port {PORT}...")
    if not os.path.exists(SERVER_DIR):
        print(f"[ERROR] Directory '{SERVER_DIR}' does not exist!")
        sys.exit(1)

    # Change to the server directory
    os.chdir(SERVER_DIR)

    # Start BusyBox HTTP server
    with open(LOG_FILE, "a") as log:
        process = subprocess.Popen(
            ["busybox", "httpd", "-f", "-p", str(PORT), "-h", SERVER_DIR],
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
        print("[INFO] Server stopped. Releasing wakelock...")
        subprocess.run(["termux-wake-unlock"])
        print("[INFO] Wakelock released. Exiting.")


def main():
    acquire_wakelock()
    server_process = start_server()
    monitor_server(server_process)


if __name__ == "__main__":
    main()