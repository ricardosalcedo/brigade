"""Unit tests for static analyzer"""

import pytest
from unittest.mock import patch, MagicMock
from analyzers.static_analyzer import StaticAnalyzer
from core.exceptions import AnalysisError, UnsupportedFileTypeError

class TestStaticAnalyzer:
    
    def setup_method(self):
        """Setup test environment"""
        self.analyzer = StaticAnalyzer()
    
    def test_detect_language_python(self):
        """Test Python language detection"""
        language = self.analyzer.detect_language('test.py')
        assert language == 'python'
    
    def test_detect_language_javascript(self):
        """Test JavaScript language detection"""
        language = self.analyzer.detect_language('test.js')
        assert language == 'javascript'
    
    def test_detect_language_unsupported(self):
        """Test unsupported file type"""
        language = self.analyzer.detect_language('test.txt')
        assert language is None
    
    @patch('core.utils.FileUtils.read_file')
    @patch('pathlib.Path.exists')
    def test_analyze_file_unsupported(self, mock_exists, mock_read):
        """Test analyzing unsupported file type"""
        mock_exists.return_value = True
        
        with pytest.raises(UnsupportedFileTypeError):
            self.analyzer.analyze_file('test.txt')
    
    @patch('core.utils.ProcessUtils.run_command')
    @patch('core.utils.FileUtils.read_file')
    @patch('pathlib.Path.exists')
    def test_analyze_python_file(self, mock_exists, mock_read, mock_run):
        """Test analyzing Python file"""
        mock_exists.return_value = True
        mock_read.return_value = "print('hello')"
        mock_run.return_value = {'success': True, 'stdout': '[]'}
        
        result = self.analyzer.analyze_file('test.py')
        
        assert result.language == 'python'
        assert result.file_path == 'test.py'
        assert isinstance(result.quality_score, int)
        assert isinstance(result.issues, list)
    
    def test_calculate_quality_score_no_issues(self):
        """Test quality score calculation with no issues"""
        score = self.analyzer._calculate_quality_score([])
        assert score == 10
    
    def test_calculate_quality_score_with_issues(self):
        """Test quality score calculation with issues"""
        issues = [
            {'severity': 'high'},
            {'severity': 'medium'},
            {'severity': 'low'}
        ]
        score = self.analyzer._calculate_quality_score(issues)
        assert score == 4  # 10 - 3 - 2 - 1 = 4
    
    def test_normalize_flake8_issues(self):
        """Test normalizing flake8 issues"""
        flake8_issues = [
            {
                'line_number': 1,
                'column_number': 5,
                'code': 'E302',
                'text': 'expected 2 blank lines'
            }
        ]
        
        normalized = self.analyzer._normalize_flake8_issues(flake8_issues)
        
        assert len(normalized) == 1
        assert normalized[0]['line'] == 1
        assert normalized[0]['column'] == 5
        assert normalized[0]['code'] == 'E302'
        assert normalized[0]['tool'] == 'flake8'
    
    def test_generate_recommendations(self):
        """Test generating recommendations"""
        issues = [
            {'type': 'syntax'},
            {'type': 'security'},
            {'type': 'style'}
        ]
        
        recommendations = self.analyzer._generate_recommendations(issues)
        
        assert len(recommendations) == 3
        assert any('syntax' in rec.lower() for rec in recommendations)
        assert any('security' in rec.lower() for rec in recommendations)
        assert any('style' in rec.lower() for rec in recommendations)
