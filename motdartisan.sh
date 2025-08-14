#!/bin/bash
# MOTD Artisan Shell Wrapper

# Get the directory where this script is located (ZSH/Bash compatible)
if [[ -n "$ZSH_VERSION" ]]; then
    # ZSH way - when sourced, use ${(%):-%x} to get the sourced file path
    if [[ "${(%):-%x}" != "(eval)" ]]; then
        SCRIPT_DIR="${${(%):-%x}:A:h}"
    else
        # Fallback to hardcoded path if eval context
        SCRIPT_DIR="$HOME/.config/motdartisan"
    fi
elif [[ -n "$BASH_VERSION" ]]; then
    # Bash way
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
else
    # Fallback
    SCRIPT_DIR="$HOME/.config/motdartisan"
fi

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

# Note: Functions are automatically available in ZSH after sourcing
# For Bash, we would use export -f, but that's not needed/supported in ZSH