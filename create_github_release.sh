#!/bin/bash
# Script to create a new GitHub release for Jackfield Labeler

# Check if version is provided
if [ $# -ne 1 ]; then
  echo "Usage: $0 <version>"
  echo "Example: $0 1.0.1"
  exit 1
fi

VERSION=$1
TAG_NAME="v$VERSION"

# Ensure we're in the main branch
git checkout main

# Make sure we have the latest code
git pull

# Update version in files if needed
echo "Updating version to $VERSION in files..."

# Update version in pyproject.toml (works on both macOS and Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS version - only replace first occurrence (in the [project] section)
  sed -i "" "0,/version = \".*\"/s//version = \"$VERSION\"/" pyproject.toml
else
  # Linux version - only replace first occurrence (in the [project] section)
  sed -i "0,/version = \".*\"/s//version = \"$VERSION\"/" pyproject.toml
fi

# Update version in the spec file (works on both macOS and Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS version
  sed -i "" "s/'CFBundleShortVersionString': '.*'/'CFBundleShortVersionString': '$VERSION'/" jackfield_labeler.spec
else
  # Linux version
  sed -i "s/'CFBundleShortVersionString': '.*'/'CFBundleShortVersionString': '$VERSION'/" jackfield_labeler.spec
fi

# Commit the version changes
git add .
git commit -m "Bump version to $VERSION"

# Create a tag
git tag -a "$TAG_NAME" -m "Release version $VERSION"

# Push changes and tag
git push origin main
git push origin "$TAG_NAME"

echo "Tag $TAG_NAME pushed to GitHub."
echo "GitHub Actions will automatically create a release and build the executables."
echo "Check the Actions tab on GitHub to monitor progress."
echo ""
echo "Note: If you want to create a draft release first, go to GitHub and convert"
echo "the automatic release to a draft before it completes."
