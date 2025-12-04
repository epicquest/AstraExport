#!/bin/bash

PID_FILE="server.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    
    # Check if the process is actually running
    if ps -p $PID > /dev/null; then
        kill $PID
        echo "Server (PID $PID) stopped."
        rm "$PID_FILE"
    else
        echo "Process $PID not found. Cleaning up stale PID file."
        rm "$PID_FILE"
    fi
else
    echo "No $PID_FILE found. Is the server running?"
fi
