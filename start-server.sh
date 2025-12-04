#!/bin/bash
# Run the Flask app using the venv python interpreter in the background
# Redirect stdout and stderr to server.log
./venv/bin/python app.py > server.log 2>&1 &

# Save the Process ID (PID) to a file so we can kill it later
echo $! > server.pid

echo "Server started in background with PID $(cat server.pid)."
echo "Logs are being written to server.log."
