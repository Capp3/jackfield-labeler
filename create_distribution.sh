#!/bin/bash
# Script to create distributable packages for Jackfield Labeler

echo "Creating distribution packages for Jackfield Labeler..."

# Check if dist directory exists
if [ ! -d "dist" ]; then
  echo "Error: dist directory not found. Run PyInstaller first."
  exit 1
fi

# Create directory for distributable files
mkdir -p dist/release

# macOS distribution
if [ -d "dist/Jackfield Labeler.app" ]; then
  echo "Creating macOS distribution..."
  cd dist
  zip -r "release/Jackfield-Labeler-mac.zip" "Jackfield Labeler.app"
  cd ..
  echo "macOS package created: dist/release/Jackfield-Labeler-mac.zip"
fi

# Windows/Linux distribution (folder)
if [ -d "dist/Jackfield Labeler" ] && [ ! -d "dist/Jackfield Labeler.app" ]; then
  echo "Creating folder-based distribution..."
  cd dist
  zip -r "release/Jackfield-Labeler-dist.zip" "Jackfield Labeler"
  cd ..
  echo "Distribution package created: dist/release/Jackfield-Labeler-dist.zip"
fi

echo "Distribution packages created in dist/release/"
echo "Done!"
