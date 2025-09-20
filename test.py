#!/usr/bin/env python3
"""
Test Script for Python Command Terminal
=======================================

This script tests all terminal features to ensure CodeMate Build compatibility.
Run this before submitting to verify everything works correctly.

Usage:
    python test.py
"""

import os
import sys
import tempfile
import shutil
from index import PythonTerminal

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = RESET_ALL = ""


class TerminalTester:
    """Test suite for the Python Terminal."""
    
    def __init__(self):
        self.terminal = PythonTerminal()
        self.test_dir = None
        self.original_dir = os.getcwd()
        self.passed_tests = 0
        self.failed_tests = 0
        
    def setup_test_environment(self):
        """Set up isolated test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="python_terminal_test_")
        os.chdir(self.test_dir)
        self.terminal.current_directory = self.test_dir
        print(f"{Fore.CYAN}Test environment: {self.test_dir}{Style.RESET_ALL}")
        
    def cleanup_test_environment(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        
    def run_test(self, test_name, test_func):
        """Run a single test with error handling."""
        try:
            print(f"\n{Fore.YELLOW}Testing: {test_name}{Style.RESET_ALL}")
            test_func()
            print(f"{Fore.GREEN}✓ PASSED: {test_name}{Style.RESET_ALL}")
            self.passed_tests += 1
        except Exception as e:
            print(f"{Fore.RED}✗ FAILED: {test_name} - {str(e)}{Style.RESET_ALL}")
            self.failed_tests += 1
            
    def test_basic_commands(self):
        """Test basic terminal commands."""
        # Test pwd
        self.terminal.execute_command("pwd")
        
        # Test echo
        self.terminal.execute_command("echo Hello Test")
        
        # Test version
        self.terminal.execute_command("version")
        
        # Test sysinfo
        self.terminal.execute_command("sysinfo")
        
    def test_file_operations(self):
        """Test file operations."""
        # Create test file
        self.terminal.execute_command("touch test_file.txt")
        assert os.path.exists("test_file.txt"), "File creation failed"
        
        # Write to file
        with open("test_file.txt", "w") as f:
            f.write("Test content")
            
        # Read file
        self.terminal.execute_command("cat test_file.txt")
        
        # Copy file
        self.terminal.execute_command("cp test_file.txt test_copy.txt")
        assert os.path.exists("test_copy.txt"), "File copy failed"
        
        # Move file
        self.terminal.execute_command("mv test_copy.txt moved_file.txt")
        assert os.path.exists("moved_file.txt"), "File move failed"
        assert not os.path.exists("test_copy.txt"), "Original file not removed"
        
        # Remove files
        self.terminal.execute_command("rm test_file.txt")
        self.terminal.execute_command("rm moved_file.txt")
        assert not os.path.exists("test_file.txt"), "File removal failed"
        
    def test_directory_operations(self):
        """Test directory operations."""
        # Create directory
        self.terminal.execute_command("mkdir test_dir")
        assert os.path.exists("test_dir"), "Directory creation failed"
        assert os.path.isdir("test_dir"), "Created item is not a directory"
        
        # Change directory
        original_cwd = os.getcwd()
        self.terminal.execute_command("cd test_dir")
        assert self.terminal.current_directory.endswith("test_dir"), "Directory change failed"
        
        # Go back
        self.terminal.execute_command("cd ..")
        assert self.terminal.current_directory == original_cwd, "Parent directory navigation failed"
        
        # Remove directory
        self.terminal.execute_command("rmdir test_dir")
        assert not os.path.exists("test_dir"), "Directory removal failed"
        
    def test_listing_commands(self):
        """Test directory listing commands."""
        # Create test files
        for i in range(3):
            with open(f"test{i}.txt", "w") as f:
                f.write(f"Content {i}")
                
        # Test basic ls
        self.terminal.execute_command("ls")
        
        # Test detailed ls
        self.terminal.execute_command("ls -l")
        
        # Clean up
        for i in range(3):
            os.remove(f"test{i}.txt")
            
    def test_system_commands(self):
        """Test system monitoring commands."""
        # Test ps (if psutil available)
        self.terminal.execute_command("ps")
        
        # Test top (if psutil available)
        self.terminal.execute_command("top")
        
    def test_utility_commands(self):
        """Test utility commands."""
        # Test history
        self.terminal.execute_command("history")
        
        # Test help
        self.terminal.execute_command("help")
        
        # Test demo (non-interactive)
        self.terminal.execute_command("demo")
        
    def test_error_handling(self):
        """Test error handling for invalid operations."""
        # Non-existent file
        self.terminal.execute_command("cat nonexistent.txt")
        
        # Non-existent directory
        self.terminal.execute_command("cd nonexistent_dir")
        
        # Invalid command
        self.terminal.execute_command("invalidcommand")
        
        # Remove non-existent file
        self.terminal.execute_command("rm nonexistent.txt")
        
    def test_codemate_compatibility(self):
        """Test CodeMate Build specific features."""
        # Test dependency checking
        missing_deps = []
        try:
            import psutil
        except ImportError:
            missing_deps.append("psutil")
            
        try:
            import colorama
        except ImportError:
            missing_deps.append("colorama")
            
        try:
            import tabulate
        except ImportError:
            missing_deps.append("tabulate")
            
        print(f"{Fore.CYAN}Dependencies status:")
        print(f"  psutil: {'✓' if 'psutil' not in missing_deps else '✗'}")
        print(f"  colorama: {'✓' if 'colorama' not in missing_deps else '✗'}")
        print(f"  tabulate: {'✓' if 'tabulate' not in missing_deps else '✗'}{Style.RESET_ALL}")
        
        # Test terminal initialization
        assert self.terminal.version == "1.0.0", "Version mismatch"
        assert hasattr(self.terminal, 'command_history'), "Command history not initialized"
        assert hasattr(self.terminal, 'current_directory'), "Current directory not set"
        
    def run_all_tests(self):
        """Run all tests."""
        print(f"{Fore.MAGENTA}{'='*80}")
        print(f"{Fore.GREEN}Python Command Terminal - Test Suite")
        print(f"{Fore.CYAN}CodeMate Build Compatibility Tests")
        print(f"{Fore.MAGENTA}{'='*80}{Style.RESET_ALL}")
        
        try:
            self.setup_test_environment()
            
            # Run all tests
            tests = [
                ("Basic Commands", self.test_basic_commands),
                ("File Operations", self.test_file_operations),
                ("Directory Operations", self.test_directory_operations),
                ("Listing Commands", self.test_listing_commands),
                ("System Commands", self.test_system_commands),
                ("Utility Commands", self.test_utility_commands),
                ("Error Handling", self.test_error_handling),
                ("CodeMate Compatibility", self.test_codemate_compatibility)
            ]
            
            for test_name, test_func in tests:
                self.run_test(test_name, test_func)
                
        finally:
            self.cleanup_test_environment()
            
        # Print results
        total_tests = self.passed_tests + self.failed_tests
        print(f"\n{Fore.MAGENTA}{'='*80}")
        print(f"{Fore.CYAN}TEST RESULTS")
        print(f"{Fore.MAGENTA}{'='*80}")
        print(f"{Fore.GREEN}Passed: {self.passed_tests}/{total_tests}")
        print(f"{Fore.RED}Failed: {self.failed_tests}/{total_tests}")
        
        if self.failed_tests == 0:
            print(f"{Fore.GREEN}🎉 ALL TESTS PASSED! Ready for CodeMate submission!")
        else:
            print(f"{Fore.YELLOW}⚠️  Some tests failed. Review issues before submission.")
            
        print(f"{Fore.CYAN}Terminal is {'✓ COMPATIBLE' if self.failed_tests == 0 else '⚠ PARTIALLY COMPATIBLE'} with CodeMate Build{Style.RESET_ALL}")
        
        return self.failed_tests == 0


def main():
    """Main test entry point."""
    print(f"{Fore.GREEN}Starting Python Terminal Test Suite{Style.RESET_ALL}")
    
    tester = TerminalTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()