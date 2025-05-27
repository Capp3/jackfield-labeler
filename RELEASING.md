# Release Process for Jackfield Labeler

This document describes the process for creating and publishing new releases of Jackfield Labeler.

## Automated GitHub Release Process

### Prerequisites

- You have push access to the main repository
- You have set up GitHub Actions in your repository
- You have the necessary files in place:
  - `.github/workflows/release.yml` - The GitHub Actions workflow file
  - `create_github_release.sh` - The release script
  - `jackfield_labeler.spec` - The PyInstaller spec file
  - `pyproject.toml` - The project configuration file

### Creating a New Release

1. **Ensure all changes are committed and pushed** to the main branch.

2. **Run the release script** with the new version number:

   ```bash
   ./create_github_release.sh 1.0.1
   ```

   This script will:
   - Update the version in `pyproject.toml`
   - Update the version in `jackfield_labeler.spec`
   - Commit these changes
   - Create and push a git tag (e.g., v1.0.1)

3. **Monitor the GitHub Actions workflow**:
   - Go to your repository on GitHub
   - Click on the "Actions" tab
   - You should see a "Build and Release" workflow running
   - This workflow will:
     - Build the application for macOS and Windows
     - Create a release with these builds attached
     - Generate release notes based on commits since the last release

4. **Verify the release**:
   - Go to your repository on GitHub
   - Click on the "Releases" tab
   - You should see your new release with attached artifacts
   - Download and test the artifacts to ensure they work as expected

## Manual Release Process

If you prefer to build and release manually:

1. **Update version numbers**:
   - Edit `pyproject.toml` to update the version
   - Edit `jackfield_labeler.spec` to update the `CFBundleShortVersionString`

2. **Build the application**:

   ```bash
   pyinstaller jackfield_labeler.spec
   ```

3. **Create distribution packages**:

   ```bash
   ./create_distribution.sh
   ```

4. **Create a GitHub release manually**:
   - Go to your repository on GitHub
   - Click on "Releases" in the sidebar
   - Click "Draft a new release"
   - Create a new tag (e.g., v1.0.1)
   - Upload the ZIP files from the `dist/release` directory
   - Publish the release

## Troubleshooting

### Common Issues

1. **The GitHub Actions workflow fails**:
   - Check the workflow logs for error messages
   - Make sure all dependencies are correctly specified in `pyproject.toml`
   - Verify that PyInstaller can find all necessary files

2. **The release script fails**:
   - Make sure you have write access to the repository
   - Check that you have the necessary files in the expected locations

3. **The built application doesn't work**:
   - Try building the application locally and testing it
   - Check the PyInstaller spec file for errors
   - Make sure all dependencies are correctly included

For more information, see the [DISTRIBUTION.md](DISTRIBUTION.md) file.
