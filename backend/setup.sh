#!/bin/bash


# Step 1: Download Miniconda3 installer
echo ""
echo "[1/3] Downloading Miniconda3 latest installer..."
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3_installer.sh

# Check if download succeeded
if [ $? -ne 0 ]; then
    echo "ERROR: Download failed. Please check your internet connection."
    exit 1
fi
echo "  ✓ Download complete."

# Step 2: Install Miniconda3
echo ""
echo "[2/3] Installing Miniconda3..."
bash ~/miniconda3_installer.sh -b -u -p ~/miniconda3

if [ $? -ne 0 ]; then
    echo "ERROR: Installation failed."
    exit 1
fi
echo "  ✓ Installation complete."

# Step 3: Remove the installer package
echo ""
echo "[3/3] Cleaning up..."
rm -f ~/miniconda3_installer.sh
echo "  ✓ Installer removed."

# Initialize conda for bash
echo ""
echo "Initializing conda for bash..."
~/miniconda3/bin/conda init bash

# Reload shell configuration
source ~/.bashrc

# Step 4: Create virtual environment 'agent'
echo ""
echo "=========================================="
echo "  Creating virtual environment: agent"
echo "=========================================="

# Ensure conda is in PATH
export PATH="$HOME/miniconda3/bin:$PATH"
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Create the environment
conda create -n agent python=3.11 -y

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment."
    exit 1
fi

echo ""
echo "=========================================="
echo "  ✓ All done!"
echo "=========================================="
echo ""
echo "To activate the environment, run:"
echo "  conda activate agent"
echo ""
echo "Or restart your terminal and run:"
echo "  conda activate agent"