import streamlit as st
import os
import subprocess
import platform
import time
from datetime import datetime
import tempfile
import shutil

# Try to import optional dependencies
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

class WebTerminal:
    def __init__(self):
        self.version = "1.3.0-web"
        # Use a temporary directory for web sessions
        if 'work_dir' not in st.session_state:
            st.session_state.work_dir = tempfile.mkdtemp(prefix="webterminal_")
        self.current_directory = st.session_state.work_dir
        
        # Initialize session state
        if 'command_history' not in st.session_state:
            st.session_state.command_history = []
        if 'session_log' not in st.session_state:
            st.session_state.session_log = []
        if 'terminal_output' not in st.session_state:
            st.session_state.terminal_output = []
            
        self.setup_gemini_ai()

    def setup_gemini_ai(self):
        """Initialize Gemini AI integration."""
        # Try environment variable first, then fallback
        self.gemini_api_key = (
            os.getenv('GEMINI_API_KEY') or 
            st.secrets.get('GEMINI_API_KEY', None) if hasattr(st, 'secrets') else None or
            "AIzaSyAy8zh81tSHZ59rYvtKb3hbvYoa7b6psDg"  # Fallback key
        )
        
        self.ai_enabled = bool(self.gemini_api_key and HAS_REQUESTS)
        
        if 'ai_status_shown' not in st.session_state:
            if self.ai_enabled:
                st.session_state.terminal_output.append("✅ Gemini AI enabled for natural language processing")
            else:
                st.session_state.terminal_output.append("⚠️  AI using fallback patterns - full Gemini AI available with API key")
            st.session_state.ai_status_shown = True

    def looks_like_natural_language(self, command):
        """Detect if a command looks like natural language vs system command."""
        cmd_lower = command.lower().strip()
        
        natural_indicators = [
            'how', 'what', 'where', 'when', 'why', 'who', 'which',
            'can you', 'could you', 'please', 'i want', 'i need', 'i would', "i'd",
            'show me', 'tell me', 'give me', 'help me', 'find me',
            'create', 'make', 'build', 'generate', 'add', 'remove', 'delete',
            'count', 'list', 'display', 'print', 'open', 'close',
            'files', 'folders', 'directories', 'project', 'items'
        ]
        
        for indicator in natural_indicators:
            if indicator in cmd_lower:
                return True
        
        words = cmd_lower.split()
        if len(words) > 2:
            common_words = ['the', 'a', 'an', 'is', 'are', 'in', 'on', 'at', 'to', 'for', 'of', 'with']
            if any(word in common_words for word in words):
                return True
        
        return False

    def parse_natural_language(self, command):
        """Parse natural language commands using Gemini AI or fallback patterns."""
        if self.ai_enabled:
            return self.parse_with_gemini(command)
        else:
            return self.parse_with_fallback_patterns(command)

    def parse_with_gemini(self, command):
        """Use Gemini AI to parse natural language commands."""
        try:
            prompt = f"""You are a command-line assistant. Convert this natural language request to a single terminal command.

IMPORTANT RULES:
- Return ONLY the command, no explanations
- Use these specific commands when appropriate:
  * For file/folder counting: "count" 
  * For creating files: "touch filename.ext"
  * For creating folders: "mkdir foldername"
  * For listing files: "ls" or "dir"
  * For deleting files: "rm filename" or "del filename"
  * For current directory: "pwd"
  * For help: "help"

Examples:
- "count the files" → "count"
- "how many files" → "count" 
- "create a file called test.py" → "touch test.py"
- "make a folder named project" → "mkdir project"
- "what files are here" → "ls"

User request: "{command}"
Command:"""

            result = self.call_gemini_api(prompt)
            if result and result.strip():
                return result.strip()
            return None
        except Exception as e:
            st.session_state.terminal_output.append(f"❌ AI parsing error: {e}")
            return None

    def call_gemini_api(self, prompt):
        """Make HTTP request to Gemini API."""
        if not self.gemini_api_key or not HAS_REQUESTS:
            return None
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.gemini_api_key}"
        
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    content = result['candidates'][0].get('content', {})
                    if 'parts' in content and content['parts']:
                        return content['parts'][0].get('text', '').strip()
            else:
                st.session_state.terminal_output.append("⚠️  Gemini API key validation failed. Switching to fallback patterns.")
                self.ai_enabled = False
            return None
        except Exception as e:
            st.session_state.terminal_output.append(f"❌ AI API error: {e}")
            return None

    def parse_with_fallback_patterns(self, command):
        """Fallback pattern matching for basic natural language processing."""
        cmd_lower = command.lower().strip()
        
        # File counting patterns
        if any(phrase in cmd_lower for phrase in ['count', 'how many', 'number of files', 'files count']):
            return 'count'
        
        # File creation patterns
        if 'create' in cmd_lower or 'make' in cmd_lower:
            if 'file' in cmd_lower:
                words = cmd_lower.split()
                filename = None
                
                for i, word in enumerate(words):
                    if word in ['named', 'called'] and i + 1 < len(words):
                        filename = words[i + 1].strip('"\'')
                        break
                    elif word == 'file' and i + 1 < len(words) and words[i + 1] not in ['named', 'called']:
                        filename = words[i + 1].strip('"\'')
                        break
                
                if filename:
                    if not '.' in filename:
                        if 'python' in cmd_lower:
                            filename += '.py'
                        elif 'txt' in cmd_lower:
                            filename += '.txt'
                    return f'touch {filename}'
                return 'touch newfile.txt'
            elif 'folder' in cmd_lower or 'directory' in cmd_lower:
                return 'mkdir newfolder'
        
        # Listing patterns
        if any(phrase in cmd_lower for phrase in ['show', 'list', 'what files', 'see files']):
            return 'ls'
        
        return None

    def execute_command(self, command_line):
        """Execute a command and return output."""
        if not command_line.strip():
            return
            
        # Log command
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.command_history.append(command_line)
        st.session_state.session_log.append(f"[{timestamp}] {command_line}")
        
        args = command_line.split()
        command = args[0] if args else ""
        
        # Handle built-in commands
        if command in ['help']:
            return self.cmd_help()
        elif command in ['pwd']:
            return self.cmd_pwd()
        elif command in ['ls', 'dir']:
            return self.cmd_ls()
        elif command == 'count':
            return self.cmd_count()
        elif command == 'mkdir' and len(args) > 1:
            return self.cmd_mkdir(args[1:])
        elif command == 'touch' and len(args) > 1:
            return self.cmd_touch(args[1:])
        elif command == 'cat' and len(args) > 1:
            return self.cmd_cat(args[1:])
        elif command in ['rm', 'del'] and len(args) > 1:
            return self.cmd_rm(args[1:])
        elif command == 'clear':
            st.session_state.terminal_output = []
            return "Screen cleared"
        elif command == 'history':
            return self.cmd_history()
        elif command == 'ai':
            return self.cmd_ai()
        else:
            # Try natural language processing
            if self.looks_like_natural_language(command_line):
                natural_cmd = self.parse_natural_language(command_line)
                if natural_cmd:
                    st.session_state.terminal_output.append(f"🤖 AI: Interpreting as '{natural_cmd}'")
                    return self.execute_command(natural_cmd)
                else:
                    return "❓ I don't understand that command. Try 'help' for available commands."
            
            # Try system command for simple cases
            return self.execute_system_command(command_line)

    def execute_system_command(self, command_line):
        """Execute system commands safely in the web environment."""
        try:
            # Only allow safe commands in web environment
            safe_commands = ['echo', 'date', 'whoami']
            command = command_line.split()[0]
            
            if command in safe_commands:
                result = subprocess.run(
                    command_line,
                    shell=True,
                    cwd=self.current_directory,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                return result.stdout if result.stdout else f"Command completed with exit code {result.returncode}"
            else:
                return f"❌ Command '{command}' not available in web environment. Use built-in commands instead."
                
        except Exception as e:
            return f"❌ Command error: {str(e)}"

    # Command implementations
    def cmd_help(self):
        """Display help information."""
        help_text = """
🌐 **Web Terminal Commands:**

**File Operations:**
• `ls`, `dir` - List directory contents
• `mkdir <name>` - Create directory  
• `touch <file>` - Create or update file
• `cat <file>` - View file contents
• `rm <file>` - Remove file
• `count` - Count files and directories

**System:**
• `pwd` - Print working directory
• `clear` - Clear screen
• `history` - Show command history
• `ai` - Show AI status
• `help` - Show this help

**Natural Language Examples:**
• "create a file called test.py"
• "how many files are here"
• "make a folder named project"
• "show me the files"
        """
        return help_text

    def cmd_pwd(self):
        """Print working directory."""
        return f"Current directory: {self.current_directory}"

    def cmd_ls(self):
        """List directory contents."""
        try:
            items = os.listdir(self.current_directory)
            if not items:
                return "📁 Directory is empty"
                
            output = "📂 **Directory Contents:**\n"
            for item in sorted(items):
                path = os.path.join(self.current_directory, item)
                if os.path.isdir(path):
                    output += f"📁 {item}/\n"
                else:
                    output += f"📄 {item}\n"
            return output
        except Exception as e:
            return f"❌ Error listing directory: {e}"

    def cmd_mkdir(self, args):
        """Create directory."""
        results = []
        for dirname in args:
            try:
                path = os.path.join(self.current_directory, dirname)
                os.makedirs(path, exist_ok=True)
                results.append(f"✅ Directory created: {dirname}")
            except Exception as e:
                results.append(f"❌ Error creating directory {dirname}: {e}")
        return "\n".join(results)

    def cmd_touch(self, args):
        """Create or update file."""
        results = []
        for filename in args:
            try:
                path = os.path.join(self.current_directory, filename)
                with open(path, 'a'):
                    pass
                results.append(f"✅ File '{filename}' created/updated")
            except Exception as e:
                results.append(f"❌ Error creating file {filename}: {e}")
        return "\n".join(results)

    def cmd_cat(self, args):
        """Display file contents."""
        results = []
        for filename in args:
            try:
                path = os.path.join(self.current_directory, filename)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    results.append(f"📄 **{filename}:**\n```\n{content}\n```")
            except FileNotFoundError:
                results.append(f"❌ File not found: {filename}")
            except Exception as e:
                results.append(f"❌ Error reading file {filename}: {e}")
        return "\n".join(results)

    def cmd_rm(self, args):
        """Remove files."""
        results = []
        for filename in args:
            try:
                path = os.path.join(self.current_directory, filename)
                if os.path.isfile(path):
                    os.remove(path)
                    results.append(f"✅ File removed: {filename}")
                else:
                    results.append(f"❌ File not found: {filename}")
            except Exception as e:
                results.append(f"❌ Error removing file {filename}: {e}")
        return "\n".join(results)

    def cmd_count(self):
        """Count files and directories."""
        try:
            items = os.listdir(self.current_directory)
            files = [item for item in items if os.path.isfile(os.path.join(self.current_directory, item))]
            dirs = [item for item in items if os.path.isdir(os.path.join(self.current_directory, item))]
            
            return f"📊 **File Count:**\n📄 Files: {len(files)}\n📁 Directories: {len(dirs)}\n📦 Total items: {len(items)}"
        except Exception as e:
            return f"❌ Error counting files: {str(e)}"

    def cmd_history(self):
        """Show command history."""
        if not st.session_state.command_history:
            return "📜 No commands in history"
            
        output = "📜 **Command History:**\n"
        for i, cmd in enumerate(st.session_state.command_history[-10:], 1):
            output += f"{i:2d}. {cmd}\n"
        return output

    def cmd_ai(self):
        """Show AI status."""
        output = "🤖 **AI Natural Language Processing Status:**\n\n"
        
        if self.ai_enabled:
            output += "✅ **Gemini AI is ACTIVE** - Full natural language understanding enabled!\n"
            output += "🧠 Model: Gemini 1.5 Flash via HTTP API\n"
        else:
            output += "⚠️  **Gemini AI is INACTIVE** - Using fallback patterns\n"
            output += "💡 To enable full AI: Add GEMINI_API_KEY to Streamlit secrets\n"
        
        output += "\n🌟 **Examples you can try:**\n"
        output += "• 'create a file called test.py'\n"
        output += "• 'how many files are here'\n"
        output += "• 'make a folder named project'\n"
        output += "• 'show me the files'\n"
        
        return output

def main():
    st.set_page_config(
        page_title="AI Terminal Web",
        page_icon="🖥️",
        layout="wide"
    )
    
    st.title("🖥️ AI-Powered Web Terminal")
    st.markdown("*Built for CodeMate Hackathon 2025 - Now accessible to everyone!*")
    
    # Initialize terminal
    terminal = WebTerminal()
    
    # Sidebar with info
    with st.sidebar:
        st.header("🔧 Terminal Info")
        st.info(f"**Version:** {terminal.version}")
        st.info(f"**Session Directory:** `{os.path.basename(terminal.current_directory)}`")
        
        if st.button("🗑️ Clear Terminal"):
            st.session_state.terminal_output = []
            st.rerun()
        
        if st.button("📊 Show AI Status"):
            result = terminal.cmd_ai()
            st.session_state.terminal_output.append(result)
            st.rerun()
        
        st.header("🚀 Quick Commands")
        quick_commands = [
            "help",
            "ls",
            "count",
            "create a file called demo.txt",
            "how many files are here"
        ]
        
        for cmd in quick_commands:
            if st.button(f"`{cmd}`", key=f"quick_{cmd}"):
                result = terminal.execute_command(cmd)
                if result:
                    st.session_state.terminal_output.append(f"$ {cmd}")
                    st.session_state.terminal_output.append(result)
                st.rerun()

    # Main terminal interface
    st.header("💬 Terminal Interface")
    
    # Command input
    command_input = st.text_input(
        "Enter command or natural language:", 
        placeholder="Try: 'create a file called test.py' or 'ls' or 'help'",
        key="command_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        execute_btn = st.button("🚀 Execute", type="primary")
    with col2:
        st.markdown("*Natural language supported! Try asking in plain English.*")
    
    # Execute command
    if execute_btn and command_input:
        result = terminal.execute_command(command_input)
        if result:
            st.session_state.terminal_output.append(f"$ {command_input}")
            st.session_state.terminal_output.append(result)
        st.rerun()
    
    # Terminal output display
    st.header("📺 Terminal Output")
    
    if st.session_state.terminal_output:
        # Create a scrollable output area
        output_container = st.container()
        with output_container:
            for i, line in enumerate(st.session_state.terminal_output):
                if line.startswith("$"):
                    st.code(line, language="bash")
                elif line.startswith("✅") or line.startswith("🤖"):
                    st.success(line)
                elif line.startswith("❌") or line.startswith("⚠️"):
                    st.warning(line)
                elif line.startswith("📊") or line.startswith("📄") or line.startswith("📁"):
                    st.info(line)
                else:
                    st.markdown(line)
    else:
        st.info("🌟 Welcome! Enter a command above to get started. Try natural language like 'create a file called hello.py'")
    
    # Footer
    st.markdown("---")
    st.markdown("🏆 **Built for CodeMate Hackathon 2025** | 🌐 **Web Terminal Version** | 🤖 **AI-Powered Natural Language Processing**")

if __name__ == "__main__":
    main()