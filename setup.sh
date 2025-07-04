#!/bin/bash

set -e
echo "🔧 Starting Bop Sense setup..."
echo "🔄 Updating package list..."
sudo apt update

echo "📦 Installing system packages..."
sudo apt install -y \
    python3-venv \
    python3-pip \
    v4l2loopback-utils \
    ffmpeg

if ! uname -a | grep -qi 'raspberrypi'; then
  echo "⚠️  Not running on a Raspberry Pi — skipping Pi-specific packages."
else
  echo "📦 Installing Pi camera packages..."
  sudo apt install -y python3-picamera2 libcamera-apps
fi

echo "🐍 Setting up Python venv (if not already present)..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
echo "📡 Activating venv and installing Python packages..."

source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Bop Sense environment is ready!"