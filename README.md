# Android Reverse Engineer Framework (AREF)

A powerful command-line interface (CLI) tool for Android APK reverse engineering. AREF simplifies the process of decompiling, modifying, recompiling, and signing Android applications.

## Features

- Interactive CLI interface with command history
- APK decompilation using apktool (by Connor Tumbleson - iBotPeaches)
- APK recompilation with AAPT2 support
- Automatic file patching for common compilation issues
- XML cleaning and file renaming utilities
- APK signing using Uber APK Signer (by patrickfav)
- Session persistence for convenient workflow
- Comprehensive error handling and reporting

## Prerequisites

- Python 3.6 or higher
- Java Runtime Environment (JRE)
- APKTool (by Connor Tumbleson - iBotPeaches)
- AAPT2 (Android Asset Packaging Tool 2)
- Uber APK Signer (by patrickfav)
- Linux enviroment (termux may not work)
## Installation

1. Clone the repository:
```bash
git clone https://github.com/minhmc2007/Android-Reverse-Engineer-Framework
cd Android Reverse Engineer Framework
```

2. Install Python dependencies:
```bash
pip install pyfiglet
```

3. Ensure all required tools are in your system PATH:
   - APKTool
   - AAPT2 (at `/usr/bin/aapt2`)
   - Java
   - Uber APK Signer (named as sign.jar in the same directory as the script)

## Usage

Start the framework by running:
```bash
python3 main.py
```

### Available Commands

- `help`: Display available commands and their descriptions
- `about`: Show information about the framework
- `decompile`: Decompile an APK using apktool
- `compile`: Compile a decompiled folder back to APK
- `patch`: Fix common issues in decompiled files
- `sign`: Sign the compiled APK using Uber APK Signer
- `exit`: Exit the framework

### Workflow Example

1. Decompile an APK:
```
android_re> decompile
Enter the full path to the APK file: /path/to/your.apk
```

2. Apply patches if needed:
```
android_re> patch
```

3. Compile the modified APK:
```
android_re> compile
```

4. Sign the compiled APK:
```
android_re> sign
```

## Patching Features

The `patch` command performs two main operations:

1. **File Renaming**
   - Removes '$' characters from filenames in the res directory
   - Prevents compilation errors due to invalid characters

2. **XML Cleaning**
   - Removes '$' characters from XML content
   - Handles both UTF-8 and Latin-1 encoded files
   - Provides detailed success/error reporting

## Session Management

- The framework maintains session information in a temporary file
- Automatically remembers last decompiled/compiled APK paths
- Cleans up temporary files on exit

## Error Handling

- Comprehensive error checking for all operations
- Detailed error messages for debugging
- Fallback encoding support for XML files
- Graceful handling of common failure scenarios

## Credits

This framework utilizes the following third-party tools:
- APKTool by Connor Tumbleson (iBotPeaches)
- Uber APK Signer by Patrick Favre-Bulle (patrickfav)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the GNU General Public License v3.0

## Troubleshooting

1. **Compilation Errors**
   - Run the `patch` command before compilation
   - Ensure AAPT2 is installed at `/usr/bin/aapt2`
   - Check XML files for syntax errors

2. **Signing Errors**
   - Verify Uber APK Signer (sign.jar) is in the correct location
   - Ensure Java is properly installed

3. **Decompilation Issues**
   - Verify APKTool is properly installed
   - Check APK file integrity

## Note

This tool is intended for legitimate reverse engineering purposes such as app analysis, security research, and debugging. Always ensure you have the right to modify any APK you're working with.
