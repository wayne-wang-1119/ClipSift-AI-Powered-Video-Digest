#!/bin/bash

# Define the path to the directory whose contents are to be removed
TARGET_DIR="transcript_based_auto_clip/youtube_downloads"

# Check if the directory exists
if [ -d "$TARGET_DIR" ]; then
    # Remove all contents of the directory without removing the directory itself
    rm -rf "$TARGET_DIR"/*
else
    echo "Directory does not exist: $TARGET_DIR"
fi
