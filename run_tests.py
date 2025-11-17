#!/usr/bin/env python3
"""Test runner for BRIGADE"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run command and return success status"""
    print("Running {}...".format(description))
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print("PASS: {}".format(description))
        return True
    except subprocess.CalledProcessError as e:
        print("FAIL: {}".format(description))
        if e.stdout:
            print("STDOUT: {}".format(e.stdout))
        if e.stderr:
            print("STDERR: {}".format(e.stderr))
        return False

def main():
    """Run all tests"""
    print("BRIGADE Test Suite")
    print("=" * 30)
    
    # Change to project directory
    os.chdir(str(Path(__file__).parent))
    
    # Install test dependencies
    print("Installing test dependencies...")
    if not run_command("pip3 install -r requirements-test.txt", "Installing test dependencies"):
        print("WARNING: Could not install test dependencies, continuing anyway...")
    
    # Run tests
    tests_passed = 0
    total_tests = 0
    
    # Unit tests
    total_tests += 1
    if run_command("python3 -m pytest tests/unit/ -v", "Unit tests"):
        tests_passed += 1
    
    # Integration tests
    total_tests += 1
    if run_command("python3 -m pytest tests/integration/ -v", "Integration tests"):
        tests_passed += 1
    
    # Code quality checks
    total_tests += 1
    if run_command("flake8 core/ analyzers/ workflows/ --max-line-length=100", "Code style (flake8)"):
        tests_passed += 1
    
    total_tests += 1
    if run_command("black --check core/ analyzers/ workflows/", "Code formatting (black)"):
        tests_passed += 1
    
    total_tests += 1
    if run_command("isort --check-only core/ analyzers/ workflows/", "Import sorting (isort)"):
        tests_passed += 1
    
    # CLI tests
    total_tests += 1
    if run_command("./brigade --help > /dev/null", "CLI help command"):
        tests_passed += 1
    
    total_tests += 1
    if run_command("./brigade analyze --help > /dev/null", "CLI analyze help"):
        tests_passed += 1
    
    total_tests += 1
    if run_command("./brigade approve --help > /dev/null", "CLI approve help"):
        tests_passed += 1
    
    # Summary
    print("\nTest Results:")
    print("   Passed: {}/{}".format(tests_passed, total_tests))
    print("   Success Rate: {:.1f}%".format(tests_passed/total_tests*100))
    
    if tests_passed == total_tests:
        print("All tests passed!")
        return 0
    else:
        print("Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
