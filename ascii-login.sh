#!/bin/bash
# ASCII Login Art Shell Wrapper

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Export functions for shell use
ascii-login-fetch() {
    python3 "$SCRIPT_DIR/main.py" fetch "$@"
}

ascii-login-show() {
    python3 "$SCRIPT_DIR/main.py" show "$@"
}

ascii-login-list() {
    python3 "$SCRIPT_DIR/main.py" list
}

ascii-login-clear-cache() {
    python3 "$SCRIPT_DIR/main.py" clear
}

# Auto-display on login (only if interactive shell)
if [[ $- == *i* ]]; then
    # Check if we should display art on login
    if [[ -z "$ASCII_LOGIN_SHOWN" ]]; then
        export ASCII_LOGIN_SHOWN=1
        python3 "$SCRIPT_DIR/main.py" login 2>/dev/null
    fi
fi

# Export the functions
export -f ascii-login-fetch
export -f ascii-login-show
export -f ascii-login-list
export -f ascii-login-clear-cache