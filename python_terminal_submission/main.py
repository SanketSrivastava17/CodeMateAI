#!/usr/bin/env python3
"""
Python-Based Command Terminal with AI Integration
Built for CodeMate Hackathon 2025

Features:
- Natural language command processing with Gemini AI
- File operations (create, delete, list, count)
- Cross-platform compatibility
- Command history and session logging
- Graceful fallbacks for missing dependencies
"""

import os
import sys
import subprocess
import platform
import time
from datetime import datetime

# Try to import optional dependencies, provide fallbacks if not available
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

try:
    from colorama import Fore, Style, Back, init
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    # Fallback color definitions
    class MockFore:
        RED = GREEN = BLUE = YELLOW = CYAN = MAGENTA = WHITE = ""
    class MockStyle:
        RESET_ALL = BRIGHT = ""
    class MockBack:
        RED = GREEN = BLUE = ""
    
    Fore = MockFore()
    Style = MockStyle()
    Back = MockBack()
    HAS_COLORAMA = False

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

class PythonTerminal:
    def __init__(self):
        self.version = "1.3.0"
        self.current_directory = os.getcwd()
        self.running = True
        self.command_history = []
        self.aliases = {}
        self.session_log = []
        
        # Initialize AI components
        self.setup_gemini_ai()
        
        print(f"Starting Python Command Terminal...")
        if not HAS_COLORAMA:
            print("Note: colorama not available. Running in basic mode.")
        if not HAS_PSUTIL:
            print("Note: psutil not available. System monitoring features will be limited.")
        if not HAS_TABULATE:
            print("Note: tabulate not available. Table formatting will be basic.")
        if not HAS_REQUESTS:
            print("Note: requests not available. AI features will use fallback patterns.")

    def setup_gemini_ai(self):
        """Initialize Gemini AI integration."""
        # Try multiple ways to get the API key - environment first, then hardcoded
        self.gemini_api_key = (
            os.getenv('GEMINI_API_KEY') or 
            os.getenv('GOOGLE_API_KEY') or
            "AIzaSyCdsKsWvlV79HLSjQ69gk8qBC1oWjTNukI" or  # Fallback API key (may need replacement)
            getattr(self, 'manual_api_key', None)
        )
        
        self.ai_enabled = bool(self.gemini_api_key and HAS_REQUESTS)
        
        if self.ai_enabled:
            print(f"{Fore.GREEN}✅ Gemini AI enabled for natural language processing{Style.RESET_ALL}")
        else:
            if not self.gemini_api_key:
                print(f"{Fore.YELLOW}⚠️  Gemini API key not found. AI features will use fallback patterns.{Style.RESET_ALL}")
                print(f"{Fore.BLUE}💡 To use full AI: Get free API key from https://aistudio.google.com/app/apikey{Style.RESET_ALL}")
                print(f"{Fore.BLUE}💡 Then set GEMINI_API_KEY environment variable{Style.RESET_ALL}")
            elif not HAS_REQUESTS:
                print(f"{Fore.YELLOW}⚠️  requests library not available. AI features will use fallback patterns.{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}💡 Note: Terminal includes advanced pattern-based NLP that works in all environments{Style.RESET_ALL}")
        if not self.ai_enabled:
            print(f"{Fore.GREEN}✅ Pattern-based AI is active and ready for natural language commands{Style.RESET_ALL}")

    def display_banner(self):
        """Display the terminal banner."""
        banner = f"""
{Fore.CYAN}============================================================
  Python-Based Command Terminal v{self.version}
  Built for CodeMate Hackathon 2025
============================================================{Style.RESET_ALL}
        """
        print(banner)
        print("Type 'help' for available commands or 'exit' to quit")
        print(f"Current directory: {self.current_directory}")
        print()

    def display_prompt(self):
        """Generate the command prompt."""
        try:
            username = os.getenv('USER', os.getenv('USERNAME', 'User'))
            hostname = platform.node() or 'localhost'
            dir_name = os.path.basename(self.current_directory) or 'root'
            return f"{Fore.GREEN}{username}@{hostname}:{dir_name}$ {Style.RESET_ALL}"
        except:
            return "$ "

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
  * For copying: "cp source dest" or "copy source dest"
  * For moving: "mv source dest" or "move source dest"
  * For current directory: "pwd"
  * For help: "help"
  * For system info: "sysinfo"

NEVER use Unix pipe operations like "ls | wc -l" - use "count" instead.

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
            print(f"{Fore.RED}AI parsing error: {e}{Style.RESET_ALL}")
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
            print(f"{Fore.BLUE}[DEBUG] API Response Status: {response.status_code}{Style.RESET_ALL}")
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    content = result['candidates'][0].get('content', {})
                    if 'parts' in content and content['parts']:
                        return content['parts'][0].get('text', '').strip()
                else:
                    print(f"{Fore.YELLOW}[DEBUG] No candidates in response: {result}{Style.RESET_ALL}")
            else:
                try:
                    error_detail = response.json()
                    print(f"{Fore.RED}[DEBUG] API Error {response.status_code}: {error_detail}{Style.RESET_ALL}")
                except:
                    print(f"{Fore.RED}[DEBUG] API Error {response.status_code}: {response.text[:200]}{Style.RESET_ALL}")
                
                # Common API error analysis
                if response.status_code == 400:
                    print(f"{Fore.YELLOW}[DIAGNOSIS] Bad Request - Likely API key format or request structure issue{Style.RESET_ALL}")
                elif response.status_code == 401:
                    print(f"{Fore.YELLOW}[DIAGNOSIS] Unauthorized - API key is invalid or not enabled{Style.RESET_ALL}")
                elif response.status_code == 403:
                    print(f"{Fore.YELLOW}[DIAGNOSIS] Forbidden - API key doesn't have permission or quota exceeded{Style.RESET_ALL}")
                elif response.status_code == 429:
                    print(f"{Fore.YELLOW}[DIAGNOSIS] Rate Limited - Too many requests{Style.RESET_ALL}")
                
                self.ai_enabled = False
            return None
        except requests.exceptions.ConnectionError as e:
            print(f"{Fore.RED}[DEBUG] Connection Error: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[DIAGNOSIS] CodeMate platform may block external API calls{Style.RESET_ALL}")
            return None
        except requests.exceptions.Timeout as e:
            print(f"{Fore.RED}[DEBUG] Timeout Error: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[DIAGNOSIS] CodeMate platform may have network restrictions{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}[DEBUG] Unexpected API error: {type(e).__name__}: {e}{Style.RESET_ALL}")
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
                # Try to extract filename - improved logic
                filename = None
                
                # Look for patterns like "named X", "called X", "file X"
                for i, word in enumerate(words):
                    if word in ['named', 'called'] and i + 1 < len(words):
                        # Get the next word, removing quotes
                        filename = words[i + 1].strip('"\'')
                        break
                    elif word == 'file' and i + 1 < len(words) and words[i + 1] not in ['named', 'called']:
                        # Pattern like "make file test"
                        filename = words[i + 1].strip('"\'')
                        break
                
                if filename:
                    # Add extension if specified
                    if not '.' in filename:
                        if 'java' in cmd_lower:
                            filename += '.java'
                        elif 'py' in cmd_lower or 'python' in cmd_lower:
                            filename += '.py'
                        elif 'txt' in cmd_lower or 'text' in cmd_lower:
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
        """Execute a command."""
        if not command_line.strip():
            return
            
        try:
            self.log_command(command_line)
            args = command_line.split()
            command = args[0] if args else ""
            
            # Create command mapping
            command_map = {
                'exit': self.cmd_exit, 'quit': self.cmd_exit,
                'pwd': self.cmd_pwd, 'ls': self.cmd_ls, 'dir': self.cmd_ls,
                'cd': lambda: self.cmd_cd(args[1:]),
                'mkdir': lambda: self.cmd_mkdir(args[1:]),
                'touch': lambda: self.cmd_touch(args[1:]),
                'cat': lambda: self.cmd_cat(args[1:]),
                'type': lambda: self.cmd_cat(args[1:]),
                'rm': lambda: self.cmd_rm(args[1:]),
                'del': lambda: self.cmd_rm(args[1:]),
                'clear': self.cmd_clear, 'cls': self.cmd_clear,
                'help': self.cmd_help,
                'count': self.cmd_count,
                'ai': self.cmd_ai,
                'history': self.cmd_history,
                'version': self.cmd_version,
                'debug-api': self.cmd_debug_api
            }
            
            if command in command_map:
                command_map[command]()
            else:
                # Try natural language processing first
                if self.looks_like_natural_language(command_line):
                    natural_cmd = self.parse_natural_language(command_line)
                    if natural_cmd:
                        print(f"{Fore.BLUE}AI: Interpreting as '{natural_cmd}'{Style.RESET_ALL}")
                        self.execute_command(natural_cmd)
                        return
                    else:
                        print(f"{Fore.YELLOW}I don't understand that command. Try 'help' for available commands.{Style.RESET_ALL}")
                        return
                
                # Fall back to system command for non-natural language
                self.execute_system_command(command_line)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Command interrupted{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

    def execute_system_command(self, command_line):
        """Execute system commands as fallback."""
        try:
            result = subprocess.run(
                command_line,
                shell=True,
                cwd=self.current_directory,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(f"{Fore.RED}{result.stderr}{Style.RESET_ALL}")
            
            if result.returncode != 0:
                print(f"{Fore.YELLOW}Command exited with code {result.returncode}{Style.RESET_ALL}")
                
        except subprocess.TimeoutExpired:
            print(f"{Fore.RED}Command timed out (30s limit){Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}Command not found: {command_line.split()[0]}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Command error: {str(e)}{Style.RESET_ALL}")

    def log_command(self, command):
        """Log command to history."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.command_history.append(command)
        self.session_log.append(f"[{timestamp}] {command}")

    # Command implementations
    def cmd_exit(self):
        """Exit the terminal."""
        self.running = False
        print(f"{Fore.GREEN}Goodbye! Thank you for using Python Terminal{Style.RESET_ALL}")

    def cmd_pwd(self):
        """Print working directory."""
        print(self.current_directory)

    def cmd_ls(self):
        """List directory contents."""
        try:
            items = os.listdir(self.current_directory)
            if not items:
                print(f"{Fore.YELLOW}Directory is empty{Style.RESET_ALL}")
                return
                
            for item in sorted(items):
                path = os.path.join(self.current_directory, item)
                if os.path.isdir(path):
                    print(f"{Fore.BLUE}{item}/{Style.RESET_ALL}")
                else:
                    print(f"{Fore.WHITE}{item}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error listing directory: {e}{Style.RESET_ALL}")

    def cmd_cd(self, args):
        """Change directory."""
        if not args:
            target = os.path.expanduser("~")
        else:
            target = args[0]
            
        try:
            if not os.path.isabs(target):
                target = os.path.join(self.current_directory, target)
            target = os.path.abspath(target)
            
            if os.path.isdir(target):
                self.current_directory = target
                os.chdir(target)
                print(f"Changed to: {target}")
            else:
                print(f"{Fore.RED}Directory not found: {target}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error changing directory: {e}{Style.RESET_ALL}")

    def cmd_mkdir(self, args):
        """Create directory."""
        if not args:
            print(f"{Fore.RED}Usage: mkdir <directory_name>{Style.RESET_ALL}")
            return
            
        for dirname in args:
            try:
                path = os.path.join(self.current_directory, dirname)
                os.makedirs(path, exist_ok=True)
                print(f"{Fore.GREEN}Directory created: {dirname}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error creating directory {dirname}: {e}{Style.RESET_ALL}")

    def cmd_touch(self, args):
        """Create or update file."""
        if not args:
            print(f"{Fore.RED}Usage: touch <filename>{Style.RESET_ALL}")
            return
            
        for filename in args:
            try:
                path = os.path.join(self.current_directory, filename)
                with open(path, 'a'):
                    pass
                print(f"{Fore.GREEN}File '{filename}' created/updated{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error creating file {filename}: {e}{Style.RESET_ALL}")

    def cmd_cat(self, args):
        """Display file contents."""
        if not args:
            print(f"{Fore.RED}Usage: cat <filename>{Style.RESET_ALL}")
            return
            
        for filename in args:
            try:
                path = os.path.join(self.current_directory, filename)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(content)
            except FileNotFoundError:
                print(f"{Fore.RED}File not found: {filename}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error reading file {filename}: {e}{Style.RESET_ALL}")

    def cmd_rm(self, args):
        """Remove files."""
        if not args:
            print(f"{Fore.RED}Usage: rm <filename>{Style.RESET_ALL}")
            return
            
        for filename in args:
            try:
                path = os.path.join(self.current_directory, filename)
                if os.path.isfile(path):
                    os.remove(path)
                    print(f"{Fore.GREEN}File removed: {filename}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}File not found: {filename}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Error removing file {filename}: {e}{Style.RESET_ALL}")

    def cmd_clear(self):
        """Clear the screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def cmd_count(self):
        """Count files and directories in current directory."""
        try:
            items = os.listdir(self.current_directory)
            files = [item for item in items if os.path.isfile(os.path.join(self.current_directory, item))]
            dirs = [item for item in items if os.path.isdir(os.path.join(self.current_directory, item))]
            
            print(f"{Fore.GREEN}Files: {len(files)}")
            print(f"{Fore.BLUE}Directories: {len(dirs)}")
            print(f"{Fore.CYAN}Total items: {len(items)}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error counting files: {str(e)}{Style.RESET_ALL}")

    def cmd_ai(self):
        """Show AI natural language status."""
        print(f"{Fore.CYAN}AI Natural Language Processing Status:")
        
        if self.ai_enabled:
            print(f"{Fore.GREEN}✅ Gemini AI is ACTIVE - Full natural language understanding enabled!")
            print(f"{Fore.BLUE}Model: Gemini 1.5 Flash via HTTP API")
        else:
            print(f"{Fore.YELLOW}⚠️  Gemini AI is INACTIVE - Using fallback patterns")
            print(f"{Fore.BLUE}💡 To enable full AI:")
            print(f"   1. Get free API key: https://aistudio.google.com/app/apikey")
            print(f"   2. Set environment variable: GEMINI_API_KEY=your_key_here")
        
        print(f"\n{Fore.GREEN}Examples you can try:")
        print(f"  • 'create a file called test.py'")
        print(f"  • 'how many files are here'")
        print(f"  • 'make a folder named project'")
        print(f"  • 'show me the files'{Style.RESET_ALL}")

    def cmd_history(self):
        """Show command history."""
        if not self.command_history:
            print(f"{Fore.YELLOW}No commands in history{Style.RESET_ALL}")
            return
            
        print(f"{Fore.CYAN}Command History:{Style.RESET_ALL}")
        for i, cmd in enumerate(self.command_history[-10:], 1):
            print(f"  {i:2d}. {cmd}")

    def cmd_version(self):
        """Display version information."""
        print(f"{Fore.GREEN}Python Command Terminal v{self.version}")
        print(f"{Fore.CYAN}Built for CodeMate Hackathon 2025")
        print(f"{Fore.YELLOW}Python {platform.python_version()} on {platform.system()}{Style.RESET_ALL}")

    def cmd_debug_api(self):
        """Debug API connectivity and configuration."""
        print(f"{Fore.CYAN}=== API Diagnostics ==={Style.RESET_ALL}")
        
        # Check dependencies
        print(f"requests library: {'✅ Available' if HAS_REQUESTS else '❌ Missing'}")
        
        # Check API key
        if self.gemini_api_key:
            masked_key = self.gemini_api_key[:8] + "..." + self.gemini_api_key[-4:] if len(self.gemini_api_key) > 12 else "***"
            print(f"API Key: ✅ Present ({masked_key})")
        else:
            print(f"API Key: ❌ Missing")
        
        # Test basic connectivity
        if HAS_REQUESTS:
            try:
                import requests
                print(f"{Fore.BLUE}Testing basic internet connectivity...{Style.RESET_ALL}")
                response = requests.get("https://httpbin.org/get", timeout=5)
                print(f"Internet: ✅ Connected (status: {response.status_code})")
            except Exception as e:
                print(f"Internet: ❌ Failed ({e})")
                print(f"{Fore.YELLOW}[DIAGNOSIS] CodeMate platform may block external HTTP requests{Style.RESET_ALL}")
        
        # Test Gemini API specifically
        if self.gemini_api_key and HAS_REQUESTS:
            print(f"{Fore.BLUE}Testing Gemini API connectivity...{Style.RESET_ALL}")
            test_result = self.call_gemini_api("Test connection - respond with 'OK'")
            if test_result:
                print(f"Gemini API: ✅ Working")
            else:
                print(f"Gemini API: ❌ Failed (see error details above)")
        
        print(f"{Fore.CYAN}=== End Diagnostics ==={Style.RESET_ALL}")

    def cmd_help(self):
        """Display help information."""
        help_text = f"""
{Fore.CYAN}Available Commands:{Style.RESET_ALL}
{Fore.GREEN}File Operations:{Style.RESET_ALL}
  ls, dir     - List directory contents
  cd <dir>    - Change directory
  mkdir <dir> - Create directory
  touch <file>- Create or update file
  cat <file>  - View file contents
  rm <file>   - Remove file
  count       - Count files and directories

{Fore.GREEN}System:{Style.RESET_ALL}
  pwd         - Print working directory
  clear, cls  - Clear screen
  history     - Show command history
  version     - Show version information
  ai          - Show AI status and examples
  debug-api   - Run API diagnostics
  help        - Show this help
  exit, quit  - Exit terminal

{Fore.GREEN}Natural Language:{Style.RESET_ALL}
  You can also use natural language! Try:
  • "create a file called test.py"
  • "how many files are here"
  • "make a folder named project"
  • "show me the files"
        """
        print(help_text)

    def run(self):
        """Main terminal loop."""
        self.display_banner()
        
        while self.running:
            try:
                prompt = self.display_prompt()
                command = input(prompt)
                if command.strip():
                    self.execute_command(command)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Use 'exit' to quit or Ctrl+C again to force quit{Style.RESET_ALL}")
                try:
                    input()
                except KeyboardInterrupt:
                    print(f"\n{Fore.RED}Force quit{Style.RESET_ALL}")
                    break
            except EOFError:
                print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Terminal error: {str(e)}{Style.RESET_ALL}")

def main():
    """Main entry point."""
    terminal = PythonTerminal()
    terminal.run()

if __name__ == "__main__":
    main()