"""AI-powered test generation and validation"""

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.base import AnalysisResult, BaseAnalyzer


@dataclass
class TestResult:
    """Test execution result"""

    passed: bool
    output: str
    coverage: Optional[float]
    duration: float
    test_count: int
    failures: List[str]


@dataclass
class GeneratedTest:
    """AI-generated test case"""

    test_name: str
    test_code: str
    test_type: str  # 'unit', 'integration', 'edge_case'
    confidence: float
    description: str


class TestAnalyzer(BaseAnalyzer):
    """AI-powered testing capabilities"""

    def __init__(self):
        super().__init__()

    def analyze(self, file_path: str) -> AnalysisResult:
        """Analyze code for testability and generate test recommendations"""
        test_analysis = self.analyze_testability(file_path)

        return AnalysisResult(
            file_path=file_path,
            language=self._detect_language(file_path),
            quality_score=test_analysis["testability_score"],
            issues=test_analysis["testing_issues"],
            recommendations=test_analysis["test_recommendations"],
        )

    def analyze_testability(self, file_path: str) -> Dict[str, Any]:
        """Analyze how testable the code is"""
        with open(file_path, "r") as f:
            code = f.read()

        language = self._detect_language(file_path)

        # Analyze testability factors
        testability_factors = {
            "has_functions": self._has_functions(code, language),
            "has_classes": self._has_classes(code, language),
            "complexity": self._estimate_complexity(code),
            "dependencies": self._analyze_dependencies(code, language),
            "side_effects": self._detect_side_effects(code, language),
            "existing_tests": self._find_existing_tests(file_path),
        }

        # Calculate testability score
        testability_score = self._calculate_testability_score(testability_factors)

        # Generate testing issues and recommendations
        issues = self._identify_testing_issues(testability_factors)
        recommendations = self._generate_test_recommendations(
            testability_factors, file_path
        )

        return {
            "testability_score": testability_score,
            "testability_factors": testability_factors,
            "testing_issues": issues,
            "test_recommendations": recommendations,
            "suggested_test_types": self._suggest_test_types(testability_factors),
        }

    def generate_tests(
        self, file_path: str, test_types: List[str] = None
    ) -> List[GeneratedTest]:
        """Generate AI-powered test cases for the given code"""
        if test_types is None:
            test_types = ["unit", "integration", "edge_case"]

        with open(file_path, "r") as f:
            code = f.read()

        language = self._detect_language(file_path)
        generated_tests = []

        # Extract functions and classes for testing
        testable_items = self._extract_testable_items(code, language)

        for item in testable_items:
            for test_type in test_types:
                test = self._generate_test_for_item(item, test_type, language, code)
                if test:
                    generated_tests.append(test)

        return generated_tests

    def run_tests(self, test_path: str, coverage: bool = True) -> TestResult:
        """Execute tests and return results"""
        language = self._detect_language(test_path)

        if language == "python":
            return self._run_python_tests(test_path, coverage)
        elif language in ["javascript", "typescript"]:
            return self._run_js_tests(test_path, coverage)
        else:
            raise ValueError(f"Testing not supported for language: {language}")

    def validate_test_coverage(
        self, source_path: str, test_path: str
    ) -> Dict[str, Any]:
        """Validate test coverage for source code"""
        language = self._detect_language(source_path)

        if language == "python":
            return self._validate_python_coverage(source_path, test_path)
        else:
            return {"coverage": 0, "missing_tests": [], "recommendations": []}

    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix.lower()
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".go": "go",
            ".rs": "rust",
        }
        return language_map.get(ext, "unknown")

    def _has_functions(self, code: str, language: str) -> bool:
        """Check if code has functions"""
        if language == "python":
            return "def " in code
        elif language in ["javascript", "typescript"]:
            return "function " in code or "=>" in code
        return False

    def _has_classes(self, code: str, language: str) -> bool:
        """Check if code has classes"""
        if language == "python":
            return "class " in code
        elif language in ["javascript", "typescript"]:
            return "class " in code
        return False

    def _estimate_complexity(self, code: str) -> int:
        """Estimate code complexity (simplified)"""
        complexity_indicators = [
            "if ",
            "for ",
            "while ",
            "try:",
            "except Exception:",
            "elif ",
        ]
        return sum(code.count(indicator) for indicator in complexity_indicators)

    def _analyze_dependencies(self, code: str, language: str) -> List[str]:
        """Analyze external dependencies"""
        dependencies = []

        if language == "python":
            lines = code.split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith("import ") or line.startswith("from "):
                    dependencies.append(line)

        return dependencies

    def _detect_side_effects(self, code: str, language: str) -> List[str]:
        """Detect potential side effects that make testing harder"""
        side_effects = []

        # Common side effect patterns
        if "print(" in code:
            side_effects.append("console_output")
        if "open(" in code:
            side_effects.append("file_io")
        if "requests." in code or "urllib" in code:
            side_effects.append("network_calls")
        if "os." in code or "sys." in code:
            side_effects.append("system_calls")
        if "random." in code:
            side_effects.append("randomness")

        return side_effects

    def _find_existing_tests(self, file_path: str) -> bool:
        """Check if tests already exist for this file"""
        file_path = Path(file_path)
        test_patterns = [
            file_path.parent / "tests" / f"test_{file_path.name}",
            file_path.parent / f"test_{file_path.name}",
            file_path.parent / "tests" / f"{file_path.stem}_test{file_path.suffix}",
        ]

        return any(test_file.exists() for test_file in test_patterns)

    def _calculate_testability_score(self, factors: Dict[str, Any]) -> float:
        """Calculate testability score from 0-10"""
        score = 5.0  # Base score

        # Positive factors
        if factors["has_functions"]:
            score += 1.5
        if factors["has_classes"]:
            score += 1.0
        if factors["existing_tests"]:
            score += 2.0

        # Negative factors
        complexity_penalty = min(factors["complexity"] * 0.1, 2.0)
        score -= complexity_penalty

        side_effects_penalty = len(factors["side_effects"]) * 0.3
        score -= side_effects_penalty

        return max(0, min(10, score))

    def _identify_testing_issues(self, factors: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify issues that make testing difficult"""
        issues = []

        if not factors["has_functions"] and not factors["has_classes"]:
            issues.append(
                {
                    "type": "structure",
                    "description": (
                        "No functions or classes found - consider refactoring "
                        "into testable units"
                    ),
                }
            )

        if factors["complexity"] > 10:
            issues.append(
                {
                    "type": "complexity",
                    "description": (
                        f'High complexity ({factors["complexity"]}) makes '
                        "testing difficult"
                    ),
                }
            )

        if "file_io" in factors["side_effects"]:
            issues.append(
                {
                    "type": "side_effects",
                    "description": (
                        "File I/O operations detected - consider dependency "
                        "injection for testing"
                    ),
                }
            )

        if "network_calls" in factors["side_effects"]:
            issues.append(
                {
                    "type": "side_effects",
                    "description": (
                        "Network calls detected - consider mocking for "
                        "reliable tests"
                    ),
                }
            )

        if not factors["existing_tests"]:
            issues.append(
                {
                    "type": "coverage",
                    "description": "No existing tests found - consider adding test coverage",
                }
            )

        return issues

    def _generate_test_recommendations(
        self, factors: Dict[str, Any], file_path: str
    ) -> List[str]:
        """Generate testing recommendations"""
        recommendations = []

        if not factors["existing_tests"]:
            recommendations.append(f"Create test file for {Path(file_path).name}")

        if factors["has_functions"]:
            recommendations.append("Add unit tests for individual functions")

        if factors["has_classes"]:
            recommendations.append(
                "Add unit tests for class methods and integration tests for class behavior"
            )

        if "network_calls" in factors["side_effects"]:
            recommendations.append(
                "Use mocking libraries (unittest.mock, pytest-mock) for network dependencies"
            )

        if "file_io" in factors["side_effects"]:
            recommendations.append(
                "Use temporary files or mock file operations in tests"
            )

        if factors["complexity"] > 5:
            recommendations.append(
                "Consider refactoring complex functions for easier testing"
            )

        recommendations.append(
            "Set up continuous testing with pytest or similar framework"
        )

        return recommendations

    def _suggest_test_types(self, factors: Dict[str, Any]) -> List[str]:
        """Suggest appropriate test types"""
        test_types = []

        if factors["has_functions"]:
            test_types.append("unit")

        if factors["has_classes"]:
            test_types.extend(["unit", "integration"])

        if factors["side_effects"]:
            test_types.append("integration")

        if factors["complexity"] > 5:
            test_types.append("edge_case")

        return list(set(test_types)) if test_types else ["unit"]

    def _extract_testable_items(self, code: str, language: str) -> List[Dict[str, str]]:
        """Extract functions and classes that can be tested"""
        items = []

        if language == "python":
            lines = code.split("\n")
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith("def ") and not line.startswith("def _"):
                    func_name = line.split("(")[0].replace("def ", "")
                    items.append(
                        {
                            "type": "function",
                            "name": func_name,
                            "line": i + 1,
                            "signature": line,
                        }
                    )
                elif line.startswith("class "):
                    class_name = (
                        line.split("(")[0].replace("class ", "").replace(":", "")
                    )
                    items.append(
                        {
                            "type": "class",
                            "name": class_name,
                            "line": i + 1,
                            "signature": line,
                        }
                    )

        return items

    def _generate_test_for_item(
        self, item: Dict[str, str], test_type: str, language: str, source_code: str
    ) -> Optional[GeneratedTest]:
        """Generate a test case for a specific function or class"""
        if language != "python":
            return None

        if item["type"] == "function":
            return self._generate_python_function_test(item, test_type, source_code)
        elif item["type"] == "class":
            return self._generate_python_class_test(item, test_type, source_code)

        return None

    def _generate_python_function_test(
        self, func_info: Dict[str, str], test_type: str, source_code: str
    ) -> GeneratedTest:
        """Generate Python function test"""
        func_name = func_info["name"]

        if test_type == "unit":
            test_code = f"""def test_{func_name}_basic():
    \"\"\"Test basic functionality of {func_name}\"\"\"
    # TODO: Add test implementation
    # _ = {func_name}(test_input)
    # assert result == expected_output
    pass
"""
        elif test_type == "edge_case":
            test_code = f"""def test_{func_name}_edge_cases():
    \"\"\"Test edge cases for {func_name}\"\"\"
    # TODO: Test edge cases like None, empty values, boundary conditions
    # Test with None input
    # Test with empty input
    # Test with boundary values
    pass
"""
        else:  # integration
            test_code = f"""def test_{func_name}_integration():
    \"\"\"Test {func_name} integration with other components\"\"\"
    # TODO: Test function in realistic usage scenarios
    pass
"""

        return GeneratedTest(
            test_name=f"test_{func_name}_{test_type}",
            test_code=test_code,
            test_type=test_type,
            confidence=0.7,
            description=f"{test_type.title()} test for {func_name} function",
        )

    def _generate_python_class_test(
        self, class_info: Dict[str, str], test_type: str, source_code: str
    ) -> GeneratedTest:
        """Generate Python class test"""
        class_name = class_info["name"]

        test_code = f"""class Test{class_name}:
    \"\"\"Test cases for {class_name} class\"\"\"

    def setup_method(self):
        \"\"\"Set up test fixtures\"\"\"
        self.instance = {class_name}()
    
    def test_{class_name.lower()}_creation(self):
        \"\"\"Test {class_name} instance creation\"\"\"
        assert self.instance is not None
    
    # TODO: Add more specific test methods for class behavior
"""

        return GeneratedTest(
            test_name=f"Test{class_name}",
            test_code=test_code,
            test_type=test_type,
            confidence=0.6,
            description=f"{test_type.title()} test class for {class_name}",
        )

    def _run_python_tests(self, test_path: str, coverage: bool) -> TestResult:
        """Run Python tests using pytest"""
        cmd = ["python", "-m", "pytest", test_path, "-v"]

        if coverage:
            cmd.extend(["--cov=.", "--cov-report=json"])

        try:
            _ = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

            # Parse pytest output
            output = result.stdout + result.stderr
            passed = result.returncode == 0

            # Extract test count and failures
            test_count = output.count("PASSED") + output.count("FAILED")
            failures = []

            if "FAILED" in output:
                for line in output.split("\n"):
                    if "FAILED" in line:
                        failures.append(line.strip())

            # Extract coverage if available
            coverage_pct = None
            if coverage and os.path.exists("coverage.json"):
                try:
                    with open("coverage.json", "r") as f:
                        cov_data = json.load(f)
                        coverage_pct = cov_data.get("totals", {}).get(
                            "percent_covered", 0
                        )
                except Exception:
                    pass

            return TestResult(
                passed=passed,
                output=output,
                coverage=coverage_pct,
                duration=0.0,  # TODO: Extract from pytest output
                test_count=test_count,
                failures=failures,
            )

        except subprocess.TimeoutExpired:
            return TestResult(
                passed=False,
                output="Test execution timed out",
                coverage=None,
                duration=60.0,
                test_count=0,
                failures=["Timeout"],
            )
        except Exception:
            return TestResult(
                passed=False,
                output=f"Test execution failed: {e}",
                coverage=None,
                duration=0.0,
                test_count=0,
                failures=[str(e)],
            )

    def _run_js_tests(self, test_path: str, coverage: bool) -> TestResult:
        """Run JavaScript/TypeScript tests"""
        # TODO: Implement JS test runner (Jest, Mocha, etc.)
        return TestResult(
            passed=False,
            output="JavaScript testing not yet implemented",
            coverage=None,
            duration=0.0,
            test_count=0,
            failures=["Not implemented"],
        )

    def _validate_python_coverage(
        self, source_path: str, test_path: str
    ) -> Dict[str, Any]:
        """Validate Python test coverage"""
        try:
            cmd = [
                "python",
                "-m",
                "pytest",
                test_path,
                f"--cov={source_path}",
                "--cov-report=json",
            ]
            _ = subprocess.run(cmd, capture_output=True, text=True)

            if os.path.exists("coverage.json"):
                with open("coverage.json", "r") as f:
                    cov_data = json.load(f)

                coverage_pct = cov_data.get("totals", {}).get("percent_covered", 0)
                missing_lines = []

                for file_path, file_data in cov_data.get("files", {}).items():
                    if file_data.get("missing_lines"):
                        missing_lines.extend(file_data["missing_lines"])

                recommendations = []
                if coverage_pct < 80:
                    recommendations.append("Increase test coverage to at least 80%")
                if missing_lines:
                    recommendations.append(
                        f"Add tests for {len(missing_lines)} uncovered lines"
                    )

                return {
                    "coverage": coverage_pct,
                    "missing_lines": missing_lines,
                    "recommendations": recommendations,
                }

        except Exception:
            pass

        return {
            "coverage": 0,
            "missing_lines": [],
            "recommendations": [
                "Unable to calculate coverage - ensure pytest-cov is installed"
            ],
        }
