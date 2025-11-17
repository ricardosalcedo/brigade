"""Unit tests for approval system"""

import json
import os
import tempfile
from unittest.mock import mock_open, patch

import pytest

from core.approval import ApprovalManager


class TestApprovalManager:

    def setup_method(self):
        """Setup test environment"""
        self.approval_manager = ApprovalManager()
        self.sample_fixes = [
            {
                "issue_description": "Replace eval() with safer alternative",
                "severity": "high",
                "explanation": "Use ast.literal_eval() instead",
            },
            {
                "issue_description": "Add context manager for file operations",
                "severity": "medium",
                "explanation": "Use with statement",
            },
        ]
        self.sample_analysis = {
            "quality_score": 5,
            "issues_found": 2,
            "quality_improvement": "+2 points",
        }

    @patch("builtins.input", return_value="y")
    @patch("builtins.print")
    def test_approve_pr_yes(self, mock_print, mock_input):
        """Test PR approval with 'yes' response"""
        result = self.approval_manager.request_pr_approval(
            "test.py", self.sample_fixes, self.sample_analysis
        )
        assert result is True

    @patch("builtins.input", return_value="n")
    @patch("builtins.print")
    def test_approve_pr_no(self, mock_print, mock_input):
        """Test PR approval with 'no' response"""
        result = self.approval_manager.request_pr_approval(
            "test.py", self.sample_fixes, self.sample_analysis
        )
        assert result is False

    @patch("builtins.input", side_effect=["d", "y"])
    @patch("builtins.print")
    def test_approve_pr_details_then_yes(self, mock_print, mock_input):
        """Test PR approval with details view then yes"""
        result = self.approval_manager.request_pr_approval(
            "test.py", self.sample_fixes, self.sample_analysis
        )
        assert result is True

    @patch("builtins.input", return_value="s")
    @patch("builtins.print")
    def test_save_for_later(self, mock_print, mock_input):
        """Test saving approval for later"""
        with patch("builtins.open", mock_open()) as mock_file:
            with patch("json.load", return_value=[]):
                with patch("json.dump") as mock_json_dump:
                    result = self.approval_manager.request_pr_approval(
                        "test.py", self.sample_fixes, self.sample_analysis
                    )
                    assert result is False
                    mock_json_dump.assert_called_once()

    def test_list_pending_approvals_empty(self):
        """Test listing pending approvals when none exist"""
        with patch("builtins.open", side_effect=FileNotFoundError):
            pending = self.approval_manager.list_pending_approvals()
            assert pending == []

    def test_list_pending_approvals_with_data(self):
        """Test listing pending approvals with data"""
        mock_data = [
            {"id": "test1", "status": "pending"},
            {"id": "test2", "status": "approved"},
            {"id": "test3", "status": "pending"},
        ]

        with patch("builtins.open", mock_open()):
            with patch("json.load", return_value=mock_data):
                pending = self.approval_manager.list_pending_approvals()
                assert len(pending) == 2
                assert all(a["status"] == "pending" for a in pending)

    def test_approve_saved_request(self):
        """Test approving a saved request"""
        mock_data = [
            {"id": "test1", "status": "pending"},
            {"id": "test2", "status": "pending"},
        ]

        with patch("builtins.open", mock_open()):
            with patch("json.load", return_value=mock_data):
                with patch("json.dump") as mock_dump:
                    result = self.approval_manager.approve_saved_request("test1")
                    assert result is True
                    mock_dump.assert_called_once()

    def test_approve_nonexistent_request(self):
        """Test approving a non-existent request"""
        mock_data = [{"id": "test1", "status": "pending"}]

        with patch("builtins.open", mock_open()):
            with patch("json.load", return_value=mock_data):
                result = self.approval_manager.approve_saved_request("nonexistent")
                assert result is False
