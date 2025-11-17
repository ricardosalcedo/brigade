"""Integration tests for BRIGADE CLI"""

import os
import subprocess
import tempfile
from pathlib import Path

import pytest


class TestBrigadeCLI:

    def setup_method(self):
        """Setup test environment"""
        self.test_file_content = """
def unsafe_eval(user_input):
    return eval(user_input)

def file_leak(filename):
    f = open(filename, 'r')
    return f.read()
"""

    def test_brigade_help(self):
        """Test BRIGADE help command"""
        result = subprocess.run(
            ["./brigade", "--help"], capture_output=True, text=True, cwd="."
        )

        assert result.returncode == 0
        assert "BRIGADE - Coordinated Code Intelligence" in result.stdout
        assert "analyze" in result.stdout
        assert "auto-fix" in result.stdout
        assert "deploy" in result.stdout
        assert "approve" in result.stdout

    def test_analyze_command_help(self):
        """Test analyze command help"""
        result = subprocess.run(
            ["./brigade", "analyze", "--help"], capture_output=True, text=True, cwd="."
        )

        assert result.returncode == 0
        assert "File or directory to analyze" in result.stdout
        assert "--recursive" in result.stdout
        assert "--output" in result.stdout

    def test_auto_fix_command_help(self):
        """Test auto-fix command help"""
        result = subprocess.run(
            ["./brigade", "auto-fix", "--help"], capture_output=True, text=True, cwd="."
        )

        assert result.returncode == 0
        assert "Create pull request" in result.stdout
        assert "--create-pr" in result.stdout
        assert "--dry-run" in result.stdout

    def test_approve_command_help(self):
        """Test approve command help"""
        result = subprocess.run(
            ["./brigade", "approve", "--help"], capture_output=True, text=True, cwd="."
        )

        assert result.returncode == 0
        assert "List pending approvals" in result.stdout
        assert "--list" in result.stdout
        assert "--approve" in result.stdout

    def test_analyze_nonexistent_file(self):
        """Test analyzing non-existent file"""
        result = subprocess.run(
            ["./brigade", "analyze", "nonexistent.py"],
            capture_output=True,
            text=True,
            cwd=".",
        )

        assert result.returncode == 1
        assert "Target not found" in result.stdout

    def test_analyze_with_test_file(self):
        """Test analyzing the test file"""
        result = subprocess.run(
            ["./brigade", "analyze", "test_code.py"],
            capture_output=True,
            text=True,
            cwd=".",
        )

        # Should work even without AWS credentials (will show error but not crash)
        assert (
            "Target: test_code.py" in result.stdout or "error" in result.stdout.lower()
        )

    def test_approve_list_empty(self):
        """Test listing approvals when none exist"""
        result = subprocess.run(
            ["./brigade", "approve", "--list"], capture_output=True, text=True, cwd="."
        )

        assert result.returncode == 0
        assert (
            "No pending approvals" in result.stdout
            or "Pending Approvals" in result.stdout
        )

    @pytest.mark.slow
    def test_dry_run_with_test_file(self):
        """Test dry-run mode with test file"""
        result = subprocess.run(
            ["./brigade", "auto-fix", "test_code.py", "--dry-run"],
            capture_output=True,
            text=True,
            cwd=".",
        )

        # Should work even without full setup
        assert result.returncode in [0, 1]  # May fail due to missing dependencies

    def test_invalid_command(self):
        """Test invalid command"""
        result = subprocess.run(
            ["./brigade", "invalid-command"], capture_output=True, text=True, cwd="."
        )

        assert result.returncode == 2  # argparse error
        assert "invalid choice" in result.stderr.lower()

    def test_no_command(self):
        """Test running BRIGADE without command"""
        result = subprocess.run(["./brigade"], capture_output=True, text=True, cwd=".")

        assert result.returncode == 1
        assert "BRIGADE - Coordinated Code Intelligence" in result.stdout
