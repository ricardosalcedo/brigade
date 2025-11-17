"""Unit tests for auto-fix workflow"""

import pytest
from unittest.mock import patch, MagicMock
from workflows.auto_fix_workflow import AutoFixWorkflow
from core.config import Config
from core.base import AnalysisResult

class TestAutoFixWorkflow:
    
    def setup_method(self):
        """Setup test environment"""
        self.config = Config()
        self.workflow = AutoFixWorkflow(self.config)
    
    @patch('workflows.auto_fix_workflow.UnifiedAnalyzer')
    def test_execute_no_issues(self, mock_analyzer_class):
        """Test workflow execution with no issues found"""
        mock_analyzer = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer
        
        # Create workflow after mocking
        workflow = AutoFixWorkflow(self.config)
        
        # Mock analysis result with no issues
        mock_result = AnalysisResult(
            file_path='test.py',
            language='python',
            quality_score=9,
            issues=[],
            recommendations=[]
        )
        mock_analyzer.analyze_file.return_value = mock_result
        
        result = workflow.execute('test.py')
        
        assert result['success'] is True
        assert 'No issues found' in result['message']
    
    @patch('workflows.auto_fix_workflow.UnifiedAnalyzer')
    @patch('core.approval.ApprovalManager.request_pr_approval')
    def test_execute_with_approval_denied(self, mock_approval, mock_analyzer_class):
        """Test workflow execution with PR approval denied"""
        mock_analyzer = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer
        mock_approval.return_value = False
        
        # Mock analysis result with issues
        mock_result = AnalysisResult(
            file_path='test.py',
            language='python',
            quality_score=5,
            issues=[{'type': 'security', 'description': 'eval usage'}],
            recommendations=['Use ast.literal_eval()']
        )
        mock_analyzer.analyze_file.return_value = mock_result
        
        result = self.workflow.execute('test.py', create_pr=True)
        
        assert result['success'] is True
        assert result['approval_status'] == 'denied'
        assert 'not approved' in result['message']
    
    @patch('workflows.auto_fix_workflow.UnifiedAnalyzer')
    @patch('core.approval.ApprovalManager.request_pr_approval')
    def test_execute_with_approval_granted(self, mock_approval, mock_analyzer_class):
        """Test workflow execution with PR approval granted"""
        mock_analyzer = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer
        mock_approval.return_value = True
        
        # Mock analysis result with issues
        mock_result = AnalysisResult(
            file_path='test.py',
            language='python',
            quality_score=5,
            issues=[{'type': 'security', 'description': 'eval usage'}],
            recommendations=['Use ast.literal_eval()']
        )
        mock_analyzer.analyze_file.return_value = mock_result
        
        with patch.object(self.workflow, '_apply_fixes') as mock_apply:
            with patch.object(self.workflow, '_create_pull_request') as mock_pr:
                mock_apply.return_value = 'test_fixed.py'
                mock_pr.return_value = 'https://github.com/user/repo/pull/1'
                
                result = self.workflow.execute('test.py', create_pr=True)
        
        assert result['success'] is True
        assert result['approval_status'] == 'approved'
        assert 'pr_url' in result
    
    @patch('workflows.auto_fix_workflow.UnifiedAnalyzer')
    def test_execute_dry_run(self, mock_analyzer_class):
        """Test workflow execution in dry-run mode"""
        mock_analyzer = MagicMock()
        mock_analyzer_class.return_value = mock_analyzer
        
        # Mock analysis result with issues
        mock_result = AnalysisResult(
            file_path='test.py',
            language='python',
            quality_score=5,
            issues=[{'type': 'security', 'description': 'eval usage'}],
            recommendations=['Use ast.literal_eval()']
        )
        mock_analyzer.analyze_file.return_value = mock_result
        
        result = self.workflow.execute('test.py', dry_run=True)
        
        assert result['success'] is True
        assert result['dry_run'] is True
        assert result['fixes_available'] > 0
    
    def test_generate_fixes(self):
        """Test fix generation"""
        mock_analysis = AnalysisResult(
            file_path='test.py',
            language='python',
            quality_score=5,
            issues=[
                {'type': 'security', 'description': 'eval usage'},
                {'type': 'style', 'description': 'style issue'}
            ],
            recommendations=[]
        )
        
        fixes = self.workflow._generate_fixes(mock_analysis)
        
        assert len(fixes) == 2
        assert all('issue' in fix for fix in fixes)
        assert all('fix_type' in fix for fix in fixes)
    
    def test_format_analysis(self):
        """Test analysis formatting"""
        mock_analysis = AnalysisResult(
            file_path='test.py',
            language='python',
            quality_score=7,
            issues=[{'type': 'style'}],
            recommendations=['Fix style']
        )
        
        formatted = self.workflow._format_analysis(mock_analysis)
        
        assert formatted['file_path'] == 'test.py'
        assert formatted['language'] == 'python'
        assert formatted['quality_score'] == 7
        assert formatted['issues_found'] == 1
