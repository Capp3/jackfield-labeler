# Jackfield Labeler - Distribution Guide

## About

Jackfield Labeler is a desktop application for creating strip labels for jackfields. The application allows you to design, preview, and export labels as PDF files.

## Distributing the Application

### GitHub Releases (Recommended)

The easiest way to distribute the application is through GitHub Releases:

1. Use the provided script to create a new release:

   ```bash
   ./create_github_release.sh 1.0.1
   ```

   This will:
   - Update version numbers in relevant files
   - Commit the changes
   - Create and push a tag (e.g., v1.0.1)
   - Trigger GitHub Actions to build executables

2. GitHub Actions will automatically:
   - Build the application for macOS and Windows
   - Create a release with these builds attached
   - Generate release notes based on commits since the last release

3. Users can download the application directly from the GitHub Releases page.

### Manual Distribution

If you prefer to build and distribute manually:

#### macOS

The macOS application is packaged as `Jackfield Labeler.app` in the `dist` directory. To distribute:

1. Compress the app bundle:

   ```bash
   cd dist
   zip -r "Jackfield Labeler-mac.zip" "Jackfield Labeler.app"
   ```

2. The resulting `Jackfield Labeler-mac.zip` file can be distributed to users.

3. Users can then unzip the file and move the application to their Applications folder.

### Windows

To create a Windows executable (if building on Windows):

1. Install PyInstaller: `uv pip install pyinstaller`
2. Run: `pyinstaller jackfield_labeler.spec`
3. The Windows executable will be in the `dist\Jackfield Labeler` directory.
4. Distribute the entire `Jackfield Labeler` directory or create an installer with a tool like NSIS.

### Linux

To create a Linux executable (if building on Linux):

1. Install PyInstaller: `uv pip install pyinstaller`
2. Run: `pyinstaller jackfield_labeler.spec`
3. The Linux executable will be in the `dist/Jackfield Labeler` directory.
4. Distribute the entire `Jackfield Labeler` directory or package it as a .deb or .rpm file.

## Running the Application

### From Source Code

To run the application from source code:

```bash
python -m jackfield_labeler
```

### From Executable

- **macOS**: Double-click the `Jackfield Labeler.app` file
- **Windows**: Run `Jackfield Labeler.exe` in the distribution directory
- **Linux**: Run the `Jackfield Labeler` executable in the distribution directory

## Notes for Distribution

- The application requires no additional dependencies when distributed as an executable.
- For security reasons, executable files may trigger warnings from antivirus software or operating system security features the first time they're run.
- On macOS, users might need to right-click and select "Open" the first time to bypass Gatekeeper.
- Consider code signing your executables for better end-user experience.

## Version History

- Version 1.0.0: Initial release
