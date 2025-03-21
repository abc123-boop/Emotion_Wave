#!/bin/bash

# Update package list and install system dependencies
apt-get update && apt-get install -y portaudio19-dev

# Upgrade pip to avoid compatibility issues
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Manually install PyAudio (since it requires system dependencies)
pip install --no-cache-dir --verbose pyaudio
