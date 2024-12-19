#!/bin/bash

# Check if an interval is passed as an argument
if [ -z "$1" ]; then
    echo "Please provide the interval (in seconds)."
    exit 1
fi

# The interval (in seconds) between runs
INTERVAL=$1
cd "$(pwd)"
# The Python file to run
PYTHON_FILE="adminapp/django_automation.py"

# Check if the Python file exists
if [ ! -f "$PYTHON_FILE" ]; then
    echo "Python file '$PYTHON_FILE' does not exist."
    exit 1
fi

# Run the Python file at the specified interval
while true; do
    echo "Running $PYTHON_FILE..."
    python3 "$PYTHON_FILE"
    echo "Next run in $INTERVAL seconds..."
    sleep "$INTERVAL"
done
