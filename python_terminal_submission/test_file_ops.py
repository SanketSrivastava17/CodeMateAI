#!/usr/bin/env python3
"""
Test script for file operations in the web terminal.
This tests the basic functionality.
"""

import os
import tempfile
import shutil

def test_file_operations():
    """Test basic file operations that should work in the web terminal."""
    
    # Create a test directory
    test_dir = tempfile.mkdtemp(prefix="webterm_test_")
    print(f"Created test directory: {test_dir}")
    
    try:
        # Test file creation
        test_file = os.path.join(test_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("Hello, Web Terminal!")
        print("✅ File creation works")
        
        # Test file reading
        with open(test_file, 'r') as f:
            content = f.read()
        print(f"✅ File reading works: {content}")
        
        # Test directory listing
        files = os.listdir(test_dir)
        print(f"✅ Directory listing works: {files}")
        
        # Test file deletion
        os.remove(test_file)
        print("✅ File deletion works")
        
        # Test directory creation
        sub_dir = os.path.join(test_dir, "subdir")
        os.makedirs(sub_dir)
        print("✅ Directory creation works")
        
        # Test directory deletion
        os.rmdir(sub_dir)
        print("✅ Directory deletion works")
        
    finally:
        # Clean up
        shutil.rmtree(test_dir)
        print("🧹 Cleanup completed")

if __name__ == "__main__":
    test_file_operations()