# Python Terminal with AI Integration

A powerful command-line terminal built in Python with natural language processing capabilities using Google's Gemini AI.

## 🚀 Features

### Core Terminal Functionality
- ✅ **File Operations**: Create, delete, list, and manage files and directories
- ✅ **Cross-Platform**: Works on Windows, Linux, and macOS
- ✅ **Command History**: Track and recall previous commands
- ✅ **Session Logging**: Automatic logging of all terminal sessions
- ✅ **Graceful Fallbacks**: Works even without optional dependencies

### AI-Powered Natural Language Processing
- ✅ **Gemini AI Integration**: Full natural language understanding using Google's Gemini 1.5 Flash
- ✅ **Smart Command Translation**: Convert natural language to terminal commands
- ✅ **Fallback Pattern Matching**: Basic natural language support without API
- ✅ **Context-Aware Responses**: Understands file creation, counting, and navigation requests

### Supported Commands

#### Traditional Commands
- `ls`/`dir` - List directory contents
- `cd <directory>` - Change directory
- `mkdir <name>` - Create directory
- `touch <filename>` - Create or update file
- `cat <filename>` - Display file contents
- `rm <filename>` - Remove file
- `pwd` - Print working directory
- `clear`/`cls` - Clear screen
- `count` - Count files and directories
- `history` - Show command history
- `version` - Show version information
- `ai` - Show AI status and examples
- `help` - Display help information
- `exit`/`quit` - Exit terminal

#### Natural Language Examples
- *"create a file called test.py"* → `touch test.py`
- *"how many files are here"* → `count`
- *"make a folder named project"* → `mkdir project`
- *"show me the files"* → `ls`
- *"count the files"* → `count`

## 🛠️ Installation & Setup

### Dependencies
The terminal is designed to work with minimal dependencies and provides graceful fallbacks:

**Optional Dependencies** (enhances functionality but not required):
- `colorama` - Enhanced terminal colors
- `psutil` - System monitoring features
- `tabulate` - Improved table formatting
- `requests` - Required for Gemini AI integration

### Installation
```bash
# Install optional dependencies for full functionality
pip install colorama psutil tabulate requests

# Or run with just Python standard library (basic mode)
python main.py
```

## 🚀 Usage

### Basic Usage
```bash
python main.py
```

### Natural Language Commands
The terminal supports natural language input with Gemini AI integration:

```bash
# Traditional way
$ touch myfile.py

# Natural language way
$ create a file called myfile.py
AI: Interpreting as 'touch myfile.py'
File 'myfile.py' created/updated
```

### AI Configuration
The terminal includes fallback natural language processing that works without any API key. For full Gemini AI integration:

1. Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Set environment variable: `GEMINI_API_KEY=your_key_here`
3. Or modify the API key in the source code

**Note**: The terminal works excellently with fallback patterns even without a valid API key, demonstrating robust natural language understanding for common commands.

## 🎯 Key Features Demonstrated

### 1. AI-Driven Terminal
- **Natural Language Processing**: Users can type commands in plain English
- **Smart Command Translation**: AI converts natural language to appropriate terminal commands
- **Context Understanding**: Recognizes file operations, counting requests, and navigation commands

### 2. Command History and Auto-completion
- **Session Logging**: All commands are logged with timestamps
- **Command History**: Access previous commands with `history` command
- **Smart Fallbacks**: Works even when AI is unavailable

### 3. Cross-Platform Compatibility
- **Universal Commands**: Works consistently across Windows, Linux, and macOS
- **Platform-Specific Adaptations**: Automatically uses appropriate system commands
- **Graceful Degradation**: Functions with or without optional dependencies

## 🏗️ Architecture

### Design Principles
1. **Modularity**: Clean separation between AI processing and core terminal functionality
2. **Fallback Strategy**: Multiple layers of fallback for maximum compatibility
3. **User Experience**: Natural language interface with clear feedback
4. **Robustness**: Handles errors gracefully and provides helpful messages

### Code Structure
- **Core Terminal Class**: `PythonTerminal` - Main terminal functionality
- **AI Integration**: Gemini API integration with HTTP requests
- **Command Processing**: Smart routing between traditional and natural language commands
- **Fallback Systems**: Pattern matching for offline natural language processing

## 🎉 Built for CodeMate Hackathon 2025

This project demonstrates advanced terminal functionality with AI integration, showcasing:
- Modern Python development practices
- API integration and error handling
- Natural language processing capabilities
- Cross-platform software design
- User-friendly interface design

---

**Author**: Built for CodeMate Hackathon 2025  
**Version**: 1.3.0  
**License**: Open Source