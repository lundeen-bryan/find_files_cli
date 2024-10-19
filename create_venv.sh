#!/bin/bash

# Start logging session
exec > >(tee "install_log.txt") 2>&1

echo "This script will create a Python virtual environment using Micromamba."
echo "Ensure that Git-Bash and Micromamba are properly installed."
read -p "Do you want to proceed? (Y/n): " proceed

if [[ ! $proceed =~ ^[Yy](es)?$ ]]; then
    echo "Exiting script."
    exit 1
fi

read -p "Enter the Python version (e.g., 3.8): " py_version
read -p "Enter environment name (Press ENTER for default '.venv'): " env_name
env_name=${env_name:-.venv}

if micromamba create -p "$(pwd)/$env_name" python="$py_version"; then
    attrib +h "$env_name"
    micromamba install pip -c conda-forge -n "$env_name"

    if [ -f "requirements.txt" ]; then
        echo "Found a requirements.txt file."
        read -p "Would you like to install packages from the requirements file? (Y/n): " install_req
        if [[ $install_req =~ ^[Yy](es)?$ ]]; then
            if micromamba activate "$env_name"; then
                micromamba install -n "$env_name" --file requirements.txt
                echo "Packages installed successfully."
            else
                echo "Environment activation failed. You might need to restart your shell."
            fi
        fi
    fi
    echo "Environment '$env_name' with Python $py_version has been created."
else
    echo "Failed to create environment. Please check errors."
    echo "If an error occurred, you can view the log file using: vim install_log.txt"
    read -p "Do you want to open the log file now? (Y/n): " open_log
    if [[ $open_log =~ ^[Yy](es)?$ ]]; then
        vim install_log.txt
    fi
    exit 1
fi

echo "Activate your environment using: micromamba activate $env_name"
echo "If you cannot activate it, you might need to restart your shell."
