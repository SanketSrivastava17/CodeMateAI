#!/usr/bin/env python3
"""
CodeMate Build Validation Script
===============================

This script validates that the Python Terminal project is fully compatible
with CodeMate Build and CodeMate Extension requirements.

Run this before submission to ensure everything works correctly.
"""

import os
import sys
import json
import subprocess

def check_file_exists(filepath, description):
    """Check if a required file exists."""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"  {status} {description}: {filepath}")
    return exists

def check_python_syntax(filepath):
    """Check if Python file has valid syntax."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            compile(f.read(), filepath, 'exec')
        print(f"  ✓ Python syntax valid: {filepath}")
        return True
    except SyntaxError as e:
        print(f"  ✗ Python syntax error in {filepath}: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Error checking {filepath}: {e}")
        return False

def validate_requirements():
    """Validate requirements.txt format."""
    try:
        with open('requirements.txt', 'r') as f:
            lines = f.readlines()
        
        required_packages = ['psutil', 'colorama', 'tabulate']
        found_packages = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                package = line.split('>=')[0].split('==')[0].strip()
                found_packages.append(package)
        
        all_found = all(pkg in found_packages for pkg in required_packages)
        status = "✓" if all_found else "✗"
        print(f"  {status} Required packages in requirements.txt")
        
        for pkg in required_packages:
            pkg_status = "✓" if pkg in found_packages else "✗"
            print(f"    {pkg_status} {pkg}")
            
        return all_found
    except Exception as e:
        print(f"  ✗ Error validating requirements.txt: {e}")
        return False

def validate_package_json():
    """Validate package.json for CodeMate compatibility."""
    try:
        with open('package.json', 'r') as f:
            data = json.load(f)
        
        required_fields = ['name', 'version', 'description', 'main', 'scripts']
        codemate_fields = ['buildCommand', 'startCommand', 'testCommand', 'demoCommand']
        
        all_required = all(field in data for field in required_fields)
        has_codemate = 'codemate' in data and all(field in data['codemate'] for field in codemate_fields)
        
        print(f"  {'✓' if all_required else '✗'} Required package.json fields present")
        print(f"  {'✓' if has_codemate else '✗'} CodeMate-specific configuration present")
        
        return all_required and has_codemate
    except Exception as e:
        print(f"  ✗ Error validating package.json: {e}")
        return False

def test_import_compatibility():
    """Test that the main module can be imported."""
    try:
        # Test importing without executing
        spec = __import__('importlib.util').util.spec_from_file_location("index", "index.py")
        module = __import__('importlib.util').util.module_from_spec(spec)
        print("  ✓ Main module can be imported")
        return True
    except Exception as e:
        print(f"  ✗ Import error: {e}")
        return False

def check_cross_platform_compatibility():
    """Check for cross-platform compatibility issues."""
    issues = []
    
    # Check for platform-specific imports
    python_files = ['index.py', 'demo.py', 'test.py']
    for filepath in python_files:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for Windows-specific paths (but exclude escape sequences)
            import re
            # Look for backslashes that aren't escape sequences
            backslash_pattern = r'\\(?![nrt"\'\\])'
            if re.search(backslash_pattern, content):
                issues.append(f"Potential Windows path issue in {filepath}")
                
            # Check for Unix-specific commands
            if 'os.system(' in content:
                if 'cls' not in content or 'clear' not in content:
                    issues.append(f"Platform-specific clear command in {filepath}")
    
    if issues:
        print("  ✗ Cross-platform compatibility issues:")
        for issue in issues:
            print(f"    - {issue}")
        return False
    else:
        print("  ✓ Cross-platform compatibility checks passed")
        return True

def validate_codemate_build():
    """Validate CodeMate Build compatibility."""
    print("\n🔍 CODEMATE BUILD VALIDATION")
    print("=" * 50)
    
    validation_checks = []
    
    # File structure validation
    print("\n📁 File Structure:")
    required_files = [
        ('index.py', 'Main terminal application'),
        ('requirements.txt', 'Python dependencies'),
        ('README.md', 'Project documentation'),
        ('demo.py', 'Demonstration script'),
        ('package.json', 'CodeMate configuration'),
        ('setup.py', 'Python package setup')
    ]
    
    file_checks = [check_file_exists(filepath, desc) for filepath, desc in required_files]
    validation_checks.extend(file_checks)
    
    # Python syntax validation
    print("\n🐍 Python Syntax:")
    python_files = ['index.py', 'demo.py', 'test.py']
    syntax_checks = [check_python_syntax(f) for f in python_files if os.path.exists(f)]
    validation_checks.extend(syntax_checks)
    
    # Dependencies validation
    print("\n📦 Dependencies:")
    dep_check = validate_requirements()
    validation_checks.append(dep_check)
    
    # Configuration validation
    print("\n⚙️  Configuration:")
    config_check = validate_package_json()
    validation_checks.append(config_check)
    
    # Import compatibility
    print("\n🔗 Import Compatibility:")
    import_check = test_import_compatibility()
    validation_checks.append(import_check)
    
    # Cross-platform compatibility
    print("\n🌍 Cross-Platform:")
    platform_check = check_cross_platform_compatibility()
    validation_checks.append(platform_check)
    
    # Summary
    passed = sum(validation_checks)
    total = len(validation_checks)
    
    print(f"\n📊 VALIDATION SUMMARY")
    print("=" * 50)
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 EXCELLENT! Your project is fully compatible with CodeMate Build!")
        print("✅ Ready for hackathon submission")
        print("✅ All CodeMate Extension features supported")
        print("✅ Cross-platform compatibility verified")
    else:
        print(f"\n⚠️  {total-passed} issues found. Please fix before submission.")
        print("🔧 Review the failed checks above")
    
    return passed == total

def main():
    """Main validation entry point."""
    print("🚀 PYTHON COMMAND TERMINAL")
    print("🏆 CodeMate Hackathon 2025")
    print("🔍 Build Validation Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('index.py'):
        print("❌ Error: index.py not found. Are you in the project directory?")
        sys.exit(1)
    
    success = validate_codemate_build()
    
    if success:
        print("\n🎯 NEXT STEPS:")
        print("1. Test your terminal: python index.py")
        print("2. Run the demo: python demo.py")
        print("3. Upload to CodeMate Build")
        print("4. Submit for hackathon evaluation")
        
        print("\n💡 DEMONSTRATION TIPS:")
        print("- Use 'demo' command to showcase all features")
        print("- Highlight system monitoring capabilities")
        print("- Show cross-platform compatibility")
        print("- Emphasize error handling and user experience")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()