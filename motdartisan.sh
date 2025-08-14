#!/bin/bash
# MOTD Artisan Shell Wrapper

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Export functions for shell use
motd-fetch() {
    python3 "$SCRIPT_DIR/main.py" fetch "$@"
}

motd-show() {
    python3 "$SCRIPT_DIR/main.py" show "$@"
}

motd-list() {
    python3 "$SCRIPT_DIR/main.py" list
}

motd-clear() {
    python3 "$SCRIPT_DIR/main.py" clear
}

# Auto-display on login (only if interactive shell)
if [[ $- == *i* ]]; then
    # Check if we should display art on login
    if [[ -z "$MOTD_ARTISAN_SHOWN" ]]; then
        export MOTD_ARTISAN_SHOWN=1
        python3 "$SCRIPT_DIR/main.py" login 2>/dev/null
    fi
fi

# Export the functions
export -f motd-fetch
export -f motd-show
export -f motd-list
export -f motd-clear