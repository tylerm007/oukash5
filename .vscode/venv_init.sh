#!/bin/bash
# Virtual Environment Initialization Script
# This script activates the virtual environment for terminal use

# Set DEBUG_VENV_INIT=1 to enable debug output
DEBUG_VENV_INIT=0

if [ "$DEBUG_VENV_INIT" = "1" ]; then
    echo "=== VENV INIT DEBUG ==="
    echo "Shell: $0"
    echo "ZSH_VERSION: $ZSH_VERSION"
    echo "BASH_VERSION: $BASH_VERSION"
    echo "Current PS1: $PS1"
    echo "VIRTUAL_ENV before: $VIRTUAL_ENV"
fi

# Source the virtual environment activation script
if [ -f "C:\genai-logic\venv\Scripts\activate" ]; then
    if [ "$DEBUG_VENV_INIT" = "1" ]; then
        echo "Found activation script: C:\genai-logic\venv\Scripts\activate"
    fi
    source C:\genai-logic\venv\Scripts\activate
    echo "Virtual environment activated: $(basename $(dirname $(dirname C:\genai-logic\venv\Scripts\activate)))"
    
    if [ "$DEBUG_VENV_INIT" = "1" ]; then
        echo "VIRTUAL_ENV after activation: $VIRTUAL_ENV"
    fi
    
    # Don't let virtualenv override the prompt
    export VIRTUAL_ENV_DISABLE_PROMPT=1
    if [ "$DEBUG_VENV_INIT" = "1" ]; then
        echo "Set VIRTUAL_ENV_DISABLE_PROMPT=1"
    fi
    
    # Override the prompt to ensure (venv) shows
    if [ -n "${ZSH_VERSION}" ]; then
        if [ "$DEBUG_VENV_INIT" = "1" ]; then
            echo "Setting zsh prompt"
        fi
        export PS1="(venv) %n@%m %1~ %# "
    elif [ -n "${BASH_VERSION}" ]; then
        if [ "$DEBUG_VENV_INIT" = "1" ]; then
            echo "Setting bash prompt"
        fi
        export PS1="(venv) \u@\h \W \$ "
    else
        if [ "$DEBUG_VENV_INIT" = "1" ]; then
            echo "Unknown shell - trying generic prompt"
        fi
        export PS1="(venv) $ "
    fi
    
    if [ "$DEBUG_VENV_INIT" = "1" ]; then
        echo "Final PS1: $PS1"
        echo "Final VIRTUAL_ENV: $VIRTUAL_ENV"
    fi
    
else
    echo "Warning: Virtual environment activation script not found at C:\genai-logic\venv\Scripts\activate"
fi

if [ "$DEBUG_VENV_INIT" = "1" ]; then
    echo "=== END DEBUG ==="
fi
