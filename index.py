#!/usr/bin/env python3
"""
Python-Based Command Terminal
=============================

A fully functioning command terminal built in Python for CodeMate Hackathon.
Compatible with CodeMate Build and CodeMate Extension.

Author: CodeMate Hackathon Participant
Date: September 2025
"""

import os
import sys
import subprocess
import shlex
import platform
from datetime import datetime
import json

# Try to import optional dependencies with fallbacks
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False
    print("Note: psutil not available. System monitoring features will be limited.")

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)  # Initialize colorama for Windows compatibility
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    # Fallback color constants
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = RESET_ALL = ""

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False


class PythonTerminal:
    """
    A Python-based command terminal with full system integration.
    Designed specifically for CodeMate Build compatibility.
    """
    
    def __init__(self):
        """Initialize the terminal with default settings."""
        self.current_directory = os.getcwd()
        self.command_history = []
        self.running = True
        self.version = "1.0.0"
        
        # CodeMate Build compatibility
        self.setup_environment()
        
    def setup_environment(self):
        """Set up environment for CodeMate Build compatibility."""
        # Ensure UTF-8 encoding
        if sys.stdout.encoding != 'utf-8':
            os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        # Set terminal title
        if os.name == 'nt':  # Windows
            os.system('title Python Command Terminal - CodeMate Build')
        
    def display_banner(self):
        """Display startup banner with CodeMate branding."""
        banner = f"""
{Fore.CYAN}{'='*60}
{Fore.GREEN}  Python-Based Command Terminal v{self.version}
{Fore.YELLOW}  Built for CodeMate Hackathon 2025
{Fore.CYAN}{'='*60}
        
{Fore.WHITE}Type 'help' for available commands or 'exit' to quit
{Fore.BLUE}Current directory: {self.current_directory}
{Style.RESET_ALL}
"""
        print(banner)
    
    def display_prompt(self):
        """Display the terminal prompt with color coding."""
        user = os.getenv('USERNAME', os.getenv('USER', 'user'))
        hostname = platform.node()
        cwd = os.path.basename(self.current_directory) or self.current_directory
        
        if HAS_COLORAMA:
            return f"{Fore.GREEN}{user}@{hostname}{Fore.WHITE}:{Fore.BLUE}{cwd}{Fore.WHITE}$ "
        else:
            return f"{user}@{hostname}:{cwd}$ "
    
    def execute_command(self, command_line):
        """Parse and execute commands with comprehensive error handling."""
        if not command_line.strip():
            return
            
        # Add to history (limit to last 100 commands)
        self.command_history.append(command_line)
        if len(self.command_history) > 100:
            self.command_history.pop(0)
        
        # Parse command
        try:
            args = shlex.split(command_line)
            command = args[0].lower()
            
            # Built-in commands
            command_map = {
                'exit': self.cmd_exit,
                'quit': self.cmd_exit,
                'pwd': self.cmd_pwd,
                'ls': lambda args=args[1:]: self.cmd_ls(args),
                'dir': lambda args=args[1:]: self.cmd_ls(args),
                'cd': lambda args=args[1:]: self.cmd_cd(args[0] if args else os.path.expanduser('~')),
                'mkdir': lambda args=args[1:]: self.cmd_mkdir(args),
                'rmdir': lambda args=args[1:]: self.cmd_rmdir(args),
                'rm': lambda args=args[1:]: self.cmd_rm(args),
                'touch': lambda args=args[1:]: self.cmd_touch(args),
                'cat': lambda args=args[1:]: self.cmd_cat(args),
                'echo': lambda args=args[1:]: self.cmd_echo(args),
                'cp': lambda args=args[1:]: self.cmd_cp(args),
                'mv': lambda args=args[1:]: self.cmd_mv(args),
                'ps': self.cmd_ps,
                'top': self.cmd_top,
                'history': self.cmd_history,
                'clear': self.cmd_clear,
                'cls': self.cmd_clear,  # Windows compatibility
                'help': self.cmd_help,
                'sysinfo': self.cmd_sysinfo,
                'version': self.cmd_version,
                'demo': self.cmd_demo
            }
            
            if command in command_map:
                command_map[command]()
            else:
                # Try to execute as system command
                self.execute_system_command(command_line)
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Command interrupted{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
    
    def cmd_exit(self):
        """Exit the terminal."""
        self.running = False
        print(f"{Fore.GREEN}Goodbye! Thank you for using Python Terminal{Style.RESET_ALL}")
    
    def cmd_pwd(self):
        """Print working directory."""
        print(f"{Fore.CYAN}{self.current_directory}{Style.RESET_ALL}")
    
    def cmd_ls(self, args):
        """List directory contents with enhanced formatting."""
        try:
            path = args[0] if args and not args[0].startswith('-') else self.current_directory
            long_format = '-l' in args
            show_all = '-a' in args
            
            if not os.path.exists(path):
                print(f"{Fore.RED}ls: {path}: No such file or directory{Style.RESET_ALL}")
                return
                
            items = os.listdir(path)
            if not show_all:
                items = [item for item in items if not item.startswith('.')]
            items.sort()
            
            if long_format:
                if HAS_TABULATE:
                    table_data = []
                    for item in items:
                        item_path = os.path.join(path, item)
                        try:
                            stat = os.stat(item_path)
                            is_dir = 'd' if os.path.isdir(item_path) else '-'
                            size = stat.st_size
                            mtime = datetime.fromtimestamp(stat.st_mtime).strftime('%b %d %H:%M')
                            color = Fore.BLUE if os.path.isdir(item_path) else Fore.WHITE
                            table_data.append([f"{is_dir}rwxr-xr-x", size, mtime, f"{color}{item}{Style.RESET_ALL}"])
                        except (OSError, PermissionError):
                            table_data.append(["?????????", "?", "? ? ?", f"{Fore.RED}{item}{Style.RESET_ALL}"])
                    
                    print(tabulate(table_data, headers=["Permissions", "Size", "Modified", "Name"]))
                else:
                    for item in items:
                        item_path = os.path.join(path, item)
                        try:
                            stat = os.stat(item_path)
                            is_dir = 'd' if os.path.isdir(item_path) else '-'
                            size = stat.st_size
                            mtime = datetime.fromtimestamp(stat.st_mtime).strftime('%b %d %H:%M')
                            color = Fore.BLUE if os.path.isdir(item_path) else Fore.WHITE
                            print(f"{is_dir}rwxr-xr-x 1 user user {size:>8} {mtime} {color}{item}{Style.RESET_ALL}")
                        except (OSError, PermissionError):
                            print(f"????????? ? user user        ? ? ? {Fore.RED}{item}{Style.RESET_ALL}")
            else:
                for item in items:
                    item_path = os.path.join(path, item)
                    if os.path.isdir(item_path):
                        print(f"{Fore.BLUE}{item}{Style.RESET_ALL}", end='  ')
                    else:
                        print(f"{Fore.WHITE}{item}{Style.RESET_ALL}", end='  ')
                print()  # New line after listing
                
        except PermissionError:
            print(f"{Fore.RED}ls: {path}: Permission denied{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}ls: {str(e)}{Style.RESET_ALL}")
    
    def cmd_cd(self, path):
        """Change directory with enhanced path resolution."""
        try:
            if path == '~':
                path = os.path.expanduser('~')
            elif path == '-':
                # Go to previous directory (if we had one stored)
                path = getattr(self, 'prev_directory', self.current_directory)
            elif not os.path.isabs(path):
                path = os.path.join(self.current_directory, path)
            
            path = os.path.abspath(path)
            
            if os.path.exists(path) and os.path.isdir(path):
                self.prev_directory = self.current_directory
                self.current_directory = path
                os.chdir(self.current_directory)
                print(f"{Fore.GREEN}Changed to: {self.current_directory}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}cd: {path}: No such file or directory{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}cd: {str(e)}{Style.RESET_ALL}")
    
    def cmd_mkdir(self, args):
        """Create directories."""
        if not args:
            print(f"{Fore.RED}mkdir: missing operand{Style.RESET_ALL}")
            return
            
        for dir_name in args:
            try:
                os.makedirs(dir_name, exist_ok=True)
                print(f"{Fore.GREEN}Directory '{dir_name}' created{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}mkdir: {dir_name}: {str(e)}{Style.RESET_ALL}")
    
    def cmd_rmdir(self, args):
        """Remove empty directories."""
        if not args:
            print(f"{Fore.RED}rmdir: missing operand{Style.RESET_ALL}")
            return
            
        for dir_name in args:
            try:
                os.rmdir(dir_name)
                print(f"{Fore.GREEN}Directory '{dir_name}' removed{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}rmdir: {dir_name}: {str(e)}{Style.RESET_ALL}")
    
    def cmd_rm(self, args):
        """Remove files."""
        if not args:
            print(f"{Fore.RED}rm: missing operand{Style.RESET_ALL}")
            return
            
        for file_name in args:
            try:
                if os.path.isfile(file_name):
                    os.remove(file_name)
                    print(f"{Fore.GREEN}File '{file_name}' removed{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}rm: {file_name}: No such file{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}rm: {file_name}: {str(e)}{Style.RESET_ALL}")
    
    def cmd_touch(self, args):
        """Create empty files."""
        if not args:
            print(f"{Fore.RED}touch: missing operand{Style.RESET_ALL}")
            return
            
        for file_name in args:
            try:
                # Create file or update timestamp
                with open(file_name, 'a'):
                    pass
                print(f"{Fore.GREEN}File '{file_name}' created/updated{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}touch: {file_name}: {str(e)}{Style.RESET_ALL}")
    
    def cmd_cat(self, args):
        """Display file contents."""
        if not args:
            print(f"{Fore.RED}cat: missing operand{Style.RESET_ALL}")
            return
            
        for file_name in args:
            try:
                with open(file_name, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                    print(f"{Fore.CYAN}--- {file_name} ---{Style.RESET_ALL}")
                    print(content)
                    print(f"{Fore.CYAN}--- End of {file_name} ---{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}cat: {file_name}: {str(e)}{Style.RESET_ALL}")
    
    def cmd_echo(self, args):
        """Echo text."""
        text = ' '.join(args)
        print(f"{Fore.WHITE}{text}{Style.RESET_ALL}")
    
    def cmd_cp(self, args):
        """Copy files."""
        if len(args) < 2:
            print(f"{Fore.RED}cp: missing operand{Style.RESET_ALL}")
            return
            
        try:
            import shutil
            source, dest = args[0], args[1]
            shutil.copy2(source, dest)
            print(f"{Fore.GREEN}'{source}' copied to '{dest}'{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}cp: {str(e)}{Style.RESET_ALL}")
    
    def cmd_mv(self, args):
        """Move/rename files."""
        if len(args) < 2:
            print(f"{Fore.RED}mv: missing operand{Style.RESET_ALL}")
            return
            
        try:
            import shutil
            source, dest = args[0], args[1]
            shutil.move(source, dest)
            print(f"{Fore.GREEN}'{source}' moved to '{dest}'{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}mv: {str(e)}{Style.RESET_ALL}")
    
    def cmd_ps(self):
        """List running processes."""
        if not HAS_PSUTIL:
            print(f"{Fore.YELLOW}ps: psutil not available. Install with: pip install psutil{Style.RESET_ALL}")
            return
            
        try:
            print(f"{Fore.CYAN}{'PID':<10} {'NAME':<25} {'CPU%':<8} {'MEMORY%':<10} {'STATUS':<12}{Style.RESET_ALL}")
            print(f"{Fore.BLUE}{'-'*70}{Style.RESET_ALL}")
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            
            for i, info in enumerate(processes[:20]):  # Show top 20
                pid = info.get('pid', 'N/A')
                name = (info.get('name', 'N/A') or 'N/A')[:24]
                cpu = info.get('cpu_percent', 0)
                mem = info.get('memory_percent', 0)
                status = info.get('status', 'N/A')
                
                color = Fore.GREEN if cpu > 10 else Fore.WHITE
                print(f"{color}{pid:<10} {name:<25} {cpu:<8.1f} {mem:<10.1f} {status:<12}{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}ps: {str(e)}{Style.RESET_ALL}")
    
    def cmd_top(self):
        """Display system information."""
        if not HAS_PSUTIL:
            print(f"{Fore.YELLOW}top: psutil not available. Install with: pip install psutil{Style.RESET_ALL}")
            return
            
        try:
            # System info
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            
            print(f"{Fore.CYAN}{'='*60}")
            print(f"{Fore.GREEN}System Performance Monitor")
            print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}System Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"CPU Usage: {Fore.RED if cpu_percent > 80 else Fore.GREEN}{cpu_percent:.1f}%{Style.RESET_ALL} ({cpu_count} cores)")
            print(f"Memory: {Fore.RED if memory.percent > 80 else Fore.GREEN}{memory.percent:.1f}%{Style.RESET_ALL} used ({memory.used // 1024**3:.1f}GB / {memory.total // 1024**3:.1f}GB)")
            print(f"Disk: {Fore.RED if disk.percent > 90 else Fore.GREEN}{disk.percent:.1f}%{Style.RESET_ALL} used ({disk.used // 1024**3:.1f}GB / {disk.total // 1024**3:.1f}GB)")
            
            if hasattr(os, 'getloadavg'):
                load_avg = os.getloadavg()
                print(f"Load Average: {load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}")
            
            print(f"{Fore.CYAN}{'-'*60}{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}top: {str(e)}{Style.RESET_ALL}")
    
    def cmd_history(self):
        """Show command history."""
        print(f"{Fore.CYAN}Command History:{Style.RESET_ALL}")
        for i, cmd in enumerate(self.command_history[-20:], 1):  # Show last 20
            print(f"{Fore.YELLOW}{i:4d}{Style.RESET_ALL}  {cmd}")
    
    def cmd_clear(self):
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        self.display_banner()
    
    def cmd_sysinfo(self):
        """Display detailed system information."""
        try:
            info = {
                "System": platform.system(),
                "Release": platform.release(),
                "Version": platform.version(),
                "Machine": platform.machine(),
                "Processor": platform.processor(),
                "Python Version": platform.python_version(),
                "Current Directory": self.current_directory,
                "User": os.getenv('USERNAME', os.getenv('USER', 'unknown')),
                "Home Directory": os.path.expanduser('~'),
                "Terminal Version": self.version
            }
            
            print(f"{Fore.CYAN}{'='*50}")
            print(f"{Fore.GREEN}System Information")
            print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
            
            for key, value in info.items():
                print(f"{Fore.YELLOW}{key}:{Style.RESET_ALL} {value}")
                
        except Exception as e:
            print(f"{Fore.RED}sysinfo: {str(e)}{Style.RESET_ALL}")
    
    def cmd_version(self):
        """Display version information."""
        print(f"{Fore.GREEN}Python Command Terminal v{self.version}")
        print(f"{Fore.CYAN}Built for CodeMate Hackathon 2025")
        print(f"{Fore.YELLOW}Python {platform.python_version()} on {platform.system()}{Style.RESET_ALL}")
    
    def cmd_demo(self):
        """Run a demonstration of terminal features."""
        print(f"{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.GREEN}Python Terminal Demo - CodeMate Hackathon")
        print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
        
        demos = [
            ("System Information", lambda: self.cmd_sysinfo()),
            ("Current Directory", lambda: self.cmd_pwd()),
            ("Directory Listing", lambda: self.cmd_ls([])),
            ("System Processes", lambda: self.cmd_ps() if HAS_PSUTIL else print("Install psutil for process monitoring")),
            ("Performance Monitor", lambda: self.cmd_top() if HAS_PSUTIL else print("Install psutil for system monitoring"))
        ]
        
        for name, func in demos:
            print(f"\n{Fore.CYAN}--- {name} ---{Style.RESET_ALL}")
            try:
                func()
            except Exception as e:
                print(f"{Fore.RED}Demo error: {str(e)}{Style.RESET_ALL}")
            print()
    
    def cmd_help(self):
        """Display available commands."""
        commands = {
            'File Operations': {
                'ls/dir [path] [-l] [-a]': 'List directory contents',
                'cat <file>': 'Display file contents',
                'touch <file>': 'Create empty file',
                'cp <src> <dest>': 'Copy file',
                'mv <src> <dest>': 'Move/rename file',
                'rm <file>': 'Remove file'
            },
            'Directory Operations': {
                'pwd': 'Print working directory',
                'cd <path>': 'Change directory (use ~ for home, - for previous)',
                'mkdir <dir>': 'Create directory',
                'rmdir <dir>': 'Remove empty directory'
            },
            'System Monitoring': {
                'ps': 'List running processes',
                'top': 'Display system performance',
                'sysinfo': 'Show system information'
            },
            'Utility Commands': {
                'echo <text>': 'Print text',
                'history': 'Show command history',
                'clear/cls': 'Clear screen',
                'demo': 'Run feature demonstration',
                'version': 'Show version information',
                'help': 'Show this help',
                'exit/quit': 'Exit terminal'
            }
        }
        
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.GREEN}Python Terminal Help - Available Commands")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        for category, cmds in commands.items():
            print(f"\n{Fore.YELLOW}{category}:{Style.RESET_ALL}")
            for cmd, desc in cmds.items():
                print(f"  {Fore.GREEN}{cmd:<25}{Style.RESET_ALL} - {desc}")
        
        print(f"\n{Fore.BLUE}Note: This terminal is built for CodeMate Build compatibility{Style.RESET_ALL}")
    
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
                print(f"{Fore.RED}{result.stderr}{Style.RESET_ALL}", file=sys.stderr)
            
            if result.returncode != 0:
                print(f"{Fore.YELLOW}Command exited with code {result.returncode}{Style.RESET_ALL}")
                
        except subprocess.TimeoutExpired:
            print(f"{Fore.RED}Command timed out (30s limit){Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}Command not found: {command_line.split()[0]}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Command error: {str(e)}{Style.RESET_ALL}")
    
    def run(self):
        """Main terminal loop."""
        self.display_banner()
        
        while self.running:
            try:
                prompt = self.display_prompt()
                command = input(prompt)
                if command.strip():  # Only process non-empty commands
                    self.execute_command(command)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Use 'exit' to quit or Ctrl+C again to force quit{Style.RESET_ALL}")
                try:
                    input()  # Wait for another input
                except KeyboardInterrupt:
                    print(f"\n{Fore.RED}Force quit{Style.RESET_ALL}")
                    break
            except EOFError:
                print(f"\n{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}Terminal error: {str(e)}{Style.RESET_ALL}")


def main():
    """Main entry point for CodeMate Build."""
    print(f"{Fore.GREEN}Starting Python Command Terminal...{Style.RESET_ALL}")
    
    # Check for required dependencies
    missing_deps = []
    if not HAS_PSUTIL:
        missing_deps.append("psutil")
    if not HAS_COLORAMA:
        missing_deps.append("colorama")
    if not HAS_TABULATE:
        missing_deps.append("tabulate")
    
    if missing_deps:
        print(f"{Fore.YELLOW}Optional dependencies missing: {', '.join(missing_deps)}")
        print(f"Install with: pip install {' '.join(missing_deps)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Terminal will run with limited features...{Style.RESET_ALL}")
    
    terminal = PythonTerminal()
    
    try:
        terminal.run()
    except Exception as e:
        print(f"{Fore.RED}Fatal error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()