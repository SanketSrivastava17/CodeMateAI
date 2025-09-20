# Python-Based Command Terminal

## Overview
A fully functioning command terminal built in Python that mimics the behavior of a real system terminal. This project demonstrates advanced Python programming, system integration, and cross-platform compatibility.

## Features

### Core Terminal Commands
- **File Operations**: `ls`, `cat`, `touch`, `cp`, `mv`, `rm`
- **Directory Operations**: `cd`, `pwd`, `mkdir`, `rmdir`
- **System Monitoring**: `ps`, `top`, `sysinfo`
- **Utility Commands**: `echo`, `clear`, `history`, `help`

### Advanced Features
- **System Monitoring**: Real-time CPU, memory, and process monitoring
- **Error Handling**: Comprehensive error handling for invalid commands
- **Command History**: Track and recall previous commands
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **CodeMate Integration**: Full compatibility with CodeMate Build and Extension

### Enhanced Features (v1.2.0)
- **Script Execution**: Execute Python, batch, and shell scripts directly
  - `script.py [args]` - Execute Python script
  - `script.bat [args]` - Execute batch file (Windows)
  - `script.sh [args]` - Execute shell script (Unix)
  - `run <script> [args]` - Generic script execution
- **Command Aliases**: Create custom command shortcuts
  - `alias ll=ls -la` - Create alias
  - `alias` - Show all aliases
- **Environment Variables**: Manage environment variables
  - `env` - Show all environment variables
  - `set VAR=value` - Set environment variable
- **Session Logging**: Automatic session logging with timestamps
  - Saves to `terminal_session.log` on exit

## Installation

### Using CodeMate Build
1. Clone this repository in CodeMate
2. CodeMate Build will automatically detect and install dependencies
3. Run the terminal with: `python index.py`

### Manual Installation
```bash
pip install -r requirements.txt
python index.py
```

## Usage

### Starting the Terminal
```bash
python index.py
```

### Available Commands
```bash
# File and Directory Operations
ls                 # List directory contents
ls -l             # Detailed directory listing
cd <directory>    # Change directory
pwd               # Print working directory
mkdir <dir>       # Create directory
rmdir <dir>       # Remove empty directory
rm <file>         # Remove file
touch <file>      # Create empty file
cat <file>        # Display file contents
cp <src> <dest>   # Copy file
mv <src> <dest>   # Move/rename file

# System Monitoring
ps                # List running processes
top               # System resource usage
sysinfo           # System information

# Utility Commands
echo <text>       # Print text
clear             # Clear screen
history           # Show command history
help              # Show available commands
exit              # Exit terminal
```

## Architecture

The terminal is built with a modular architecture:
- **Core Engine**: `PythonTerminal` class handles command parsing and execution
- **Built-in Commands**: Native Python implementations of common terminal commands
- **System Integration**: Uses `psutil` for system monitoring and process management
- **Error Handling**: Comprehensive error management with user-friendly messages

## CodeMate Integration

This project is specifically designed to work with:
- **CodeMate Build**: Automatic dependency management and execution
- **CodeMate Extension**: Code completion and debugging support
- **Real-time Testing**: Built-in demo mode for showcasing features

## Demo Mode

Run the demo to see all features:
```bash
python demo.py
```

## Technical Details

### Dependencies
- `psutil`: System and process monitoring
- `colorama`: Cross-platform colored terminal output
- `tabulate`: Formatted table output for system information

### Compatibility
- Python 3.7+
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+)

## Development

This project was developed for the CodeMate Hackathon, showcasing:
- Advanced Python programming techniques
- System-level programming concepts
- Cross-platform development best practices
- Professional code structure and documentation

## License

MIT License - Feel free to use and modify for educational purposes.

## Author

Built for CodeMate Hackathon 2025