#!/bin/bash
# Update package list and install dependencies
apt-get update && apt-get install -y portaudio19-dev
# Install dependencies
pip install -r requirements.txt
# Install PyAudio separately
pip install pyaudio
