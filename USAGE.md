# Python Command Terminal - Usage Examples

## Quick Start Guide for CodeMate Build

### 1. Running the Terminal
```bash
# Basic execution
python index.py

# Or run the demo first
python demo.py
```

### 2. Essential Commands

#### File Operations
```bash
# List files
ls                    # Basic listing
ls -l                 # Detailed listing
ls -a                 # Show hidden files
ls /path/to/dir       # List specific directory

# File manipulation
touch myfile.txt      # Create empty file
cat myfile.txt        # Display file contents
echo "Hello" > file   # Write to file
cp source dest        # Copy file
mv source dest        # Move/rename file
rm filename           # Delete file
```

#### Directory Operations
```bash
# Navigation
pwd                   # Show current directory
cd /path/to/dir       # Change directory
cd ~                  # Go to home directory
cd -                  # Go to previous directory

# Directory management
mkdir mydir           # Create directory
rmdir mydir           # Remove empty directory
```

#### System Monitoring
```bash
ps                    # List processes
top                   # System performance
sysinfo               # System information
```

#### Utility Commands
```bash
echo "Hello World"    # Print text
history               # Command history
clear                 # Clear screen
help                  # Show all commands
version               # Terminal version
demo                  # Run built-in demo
```

### 3. Advanced Features

#### Command History
- All commands are automatically saved
- Use `history` to view recent commands
- History persists during the session

#### Error Handling
- Comprehensive error messages
- Graceful handling of missing files/directories
- System command fallback for unsupported commands

#### Cross-Platform Support
- Works on Windows, macOS, and Linux
- Automatic path handling
- Platform-specific optimizations

### 4. CodeMate Build Integration

#### Automatic Dependency Detection
The terminal automatically detects and handles missing dependencies:
- `psutil` - System monitoring (optional)
- `colorama` - Colored output (optional)
- `tabulate` - Formatted tables (optional)

#### Environment Setup
```bash
# CodeMate Build will automatically:
pip install -r requirements.txt
python index.py
```

#### Testing Features
```bash
# Run automated demo
python demo.py

# Interactive testing
python demo.py --interactive

# Or use built-in demo command
python index.py
> demo
```

### 5. Example Session
```bash
$ python index.py

=============================================================
  Python-Based Command Terminal v1.0.0
  Built for CodeMate Hackathon 2025
=============================================================

Type 'help' for available commands or 'exit' to quit
Current directory: /home/user/project

user@computer:project$ ls
README.md  demo.py  index.py  requirements.txt  setup.py

user@computer:project$ mkdir test_folder
Directory 'test_folder' created

user@computer:project$ cd test_folder
Changed to: /home/user/project/test_folder

user@computer:test_folder$ touch hello.txt
File 'hello.txt' created/updated

user@computer:test_folder$ echo "Hello CodeMate!" > hello.txt
Hello CodeMate!

user@computer:test_folder$ cat hello.txt
--- hello.txt ---
Hello CodeMate!
--- End of hello.txt ---

user@computer:test_folder$ ls -l
Permissions    Size  Modified      Name
-rwxr-xr-x       15  Sep 20 14:30  hello.txt

user@computer:test_folder$ cd ..
Changed to: /home/user/project

user@computer:project$ ps
PID        NAME                      CPU%     MEMORY%   STATUS
1234       python                    15.2     2.1       running
5678       code                      8.7      5.3       running
...

user@computer:project$ top
============================================================
System Performance Monitor
============================================================
System Boot Time: 2025-09-20 09:00:00
CPU Usage: 25.4% (8 cores)
Memory: 45.2% used (7.2GB / 16.0GB)
Disk: 35.8% used (180.5GB / 512.0GB)
------------------------------------------------------------

user@computer:project$ help
============================================================
Python Terminal Help - Available Commands
============================================================

File Operations:
  ls/dir [path] [-l] [-a]  - List directory contents
  cat <file>               - Display file contents
  touch <file>             - Create empty file
  cp <src> <dest>          - Copy file
  mv <src> <dest>          - Move/rename file
  rm <file>                - Remove file

Directory Operations:
  pwd                      - Print working directory
  cd <path>                - Change directory (use ~ for home, - for previous)
  mkdir <dir>              - Create directory
  rmdir <dir>              - Remove empty directory

System Monitoring:
  ps                       - List running processes
  top                      - Display system performance
  sysinfo                  - Show system information

Utility Commands:
  echo <text>              - Print text
  history                  - Show command history
  clear/cls                - Clear screen
  demo                     - Run feature demonstration
  version                  - Show version information
  help                     - Show this help
  exit/quit                - Exit terminal

Note: This terminal is built for CodeMate Build compatibility

user@computer:project$ exit
Goodbye! Thank you for using Python Terminal
```

### 6. Troubleshooting

#### Missing Dependencies
If you see warnings about missing packages:
```bash
pip install psutil colorama tabulate
```

#### Permission Errors
On Unix systems, you might need:
```bash
chmod +x index.py
python3 index.py
```

#### CodeMate Build Issues
1. Ensure `requirements.txt` is in the project root
2. Check that Python 3.7+ is being used
3. Verify all files are in the same directory

### 7. Performance Notes

- Process listing shows top 20 processes by CPU usage
- Command history limited to last 100 commands
- System commands have 30-second timeout
- Automatic cleanup of resources

### 8. Extensions for Hackathon

The terminal is designed to be easily extended:
- Add new commands in the `command_map` dictionary
- Implement AI features using the existing architecture
- Add web interface using Flask/FastAPI
- Integrate with external APIs

This structure makes it perfect for the CodeMate Hackathon requirements!