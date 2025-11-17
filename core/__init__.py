"""
Core module for Intelligent Code Analyzer

Provides base classes, interfaces, and common functionality.
"""

from .approval import ApprovalManager
from .base import BaseAgent, BaseAnalyzer, BaseTool
from .config import Config
from .exceptions import (AnalysisError, FixGenerationError, PRCreationError,
                         TestFailureError)
from .interfaces import ICodeAnalyzer, IFixGenerator, IPRManager, ITestRunner
from .utils import FileUtils, GitUtils, LLMUtils

__all__ = [
    "BaseAnalyzer",
    "BaseAgent",
    "BaseTool",
    "ICodeAnalyzer",
    "IFixGenerator",
    "ITestRunner",
    "IPRManager",
    "AnalysisError",
    "FixGenerationError",
    "TestFailureError",
    "PRCreationError",
    "Config",
    "FileUtils",
    "GitUtils",
    "LLMUtils",
    "ApprovalManager",
]
