#!/usr/bin/env python3
"""
Python Terminal Demo Script
===========================

Demonstrates all features of the Python Command Terminal for CodeMate Build.
This script showcases the terminal's capabilities in an automated way.

Usage:
    python demo.py
    python demo.py --interactive  # For interactive demo
"""

import sys
import time
import os
from index import PythonTerminal

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = RESET_ALL = ""


def print_section(title, delay=1):
    """Print a section header with styling."""
    print(f"\n{Fore.MAGENTA}{'='*80}")
    print(f"{Fore.CYAN}{title.center(80)}")
    print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
    time.sleep(delay)


def execute_demo_command(terminal, command, description="", delay=2):
    """Execute a command in the terminal with description."""
    if description:
        print(f"\n{Fore.YELLOW}> {description}{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}$ {command}{Style.RESET_ALL}")
    time.sleep(1)
    
    # Execute the command
    terminal.execute_command(command)
    time.sleep(delay)


def run_automated_demo():
    """Run an automated demonstration of all terminal features."""
    print_section("PYTHON COMMAND TERMINAL - AUTOMATED DEMO")
    print(f"{Fore.CYAN}Built for CodeMate Hackathon 2025{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}This demo showcases all terminal features automatically{Style.RESET_ALL}")
    
    # Initialize terminal
    terminal = PythonTerminal()
    terminal.display_banner()
    
    # Demo sections
    demos = [
        {
            "title": "BASIC INFORMATION",
            "commands": [
                ("version", "Display terminal version"),
                ("sysinfo", "Show comprehensive system information"),
                ("pwd", "Print current working directory")
            ]
        },
        {
            "title": "FILE SYSTEM OPERATIONS",
            "commands": [
                ("ls", "List current directory contents"),
                ("ls -l", "Detailed directory listing"),
                ("mkdir demo_folder", "Create a demonstration folder"),
                ("touch demo_file.txt", "Create a demonstration file"),
                ("echo 'Hello CodeMate!' > demo_file.txt", "Write content to file"),
                ("cat demo_file.txt", "Display file contents"),
                ("ls -l", "Show updated directory listing"),
                ("cp demo_file.txt demo_copy.txt", "Copy the demonstration file"),
                ("mv demo_copy.txt demo_folder/", "Move file to folder"),
                ("ls demo_folder/", "List folder contents")
            ]
        },
        {
            "title": "DIRECTORY NAVIGATION",
            "commands": [
                ("cd demo_folder", "Change to demonstration folder"),
                ("pwd", "Confirm current directory"),
                ("ls", "List contents of current folder"),
                ("cd ..", "Go back to parent directory"),
                ("pwd", "Confirm we're back")
            ]
        },
        {
            "title": "SYSTEM MONITORING",
            "commands": [
                ("ps", "List running processes (top 20)"),
                ("top", "Display system performance metrics")
            ]
        },
        {
            "title": "UTILITY FEATURES",
            "commands": [
                ("history", "Show command history"),
                ("echo 'Demo completed successfully!'", "Display success message"),
                ("help", "Show all available commands")
            ]
        },
        {
            "title": "CLEANUP",
            "commands": [
                ("rm demo_file.txt", "Remove demonstration file"),
                ("rm demo_folder/demo_copy.txt", "Remove copied file"),
                ("rmdir demo_folder", "Remove demonstration folder"),
                ("ls", "Confirm cleanup completed")
            ]
        }
    ]
    
    # Execute each demo section
    for section in demos:
        print_section(section["title"])
        
        for command, description in section["commands"]:
            try:
                execute_demo_command(terminal, command, description)
            except Exception as e:
                print(f"{Fore.RED}Demo error: {str(e)}{Style.RESET_ALL}")
                continue
    
    # Final message
    print_section("DEMO COMPLETED")
    print(f"{Fore.GREEN}✓ All terminal features demonstrated successfully!")
    print(f"{Fore.CYAN}✓ Compatible with CodeMate Build and Extension")
    print(f"{Fore.YELLOW}✓ Ready for hackathon submission{Style.RESET_ALL}")
    
    return terminal


def run_interactive_demo():
    """Run an interactive demonstration where user can try commands."""
    print_section("PYTHON COMMAND TERMINAL - INTERACTIVE DEMO")
    print(f"{Fore.CYAN}Built for CodeMate Hackathon 2025{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Try any commands! Type 'exit' to end the demo{Style.RESET_ALL}")
    
    terminal = PythonTerminal()
    terminal.run()


def main():
    """Main demo entry point."""
    print(f"{Fore.GREEN}Python Command Terminal Demo{Style.RESET_ALL}")
    print(f"{Fore.CYAN}CodeMate Hackathon 2025{Style.RESET_ALL}")
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_demo()
    else:
        # Show options
        print(f"\n{Fore.YELLOW}Demo Options:")
        print(f"{Fore.WHITE}1. Automated Demo (showcases all features)")
        print(f"2. Interactive Demo (try commands yourself)")
        print(f"3. Exit{Style.RESET_ALL}")
        
        try:
            choice = input(f"\n{Fore.CYAN}Select option (1-3): {Style.RESET_ALL}")
            
            if choice == "1":
                terminal = run_automated_demo()
                
                # Ask if user wants to try interactive mode
                try_interactive = input(f"\n{Fore.YELLOW}Try interactive mode? (y/n): {Style.RESET_ALL}")
                if try_interactive.lower() in ['y', 'yes']:
                    print(f"\n{Fore.GREEN}Starting interactive mode...{Style.RESET_ALL}")
                    time.sleep(2)
                    terminal.run()
                    
            elif choice == "2":
                run_interactive_demo()
            else:
                print(f"{Fore.GREEN}Demo ended{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Demo interrupted{Style.RESET_ALL}")
        except EOFError:
            print(f"\n{Fore.GREEN}Demo ended{Style.RESET_ALL}")


if __name__ == "__main__":
    main()