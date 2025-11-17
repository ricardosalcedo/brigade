"""Repository-wide analysis with context management"""

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from analyzers.unified_analyzer import UnifiedAnalyzer
from core.base import AnalysisResult, BaseAnalyzer


@dataclass
class RepoChunk:
    """Represents a chunk of repository for analysis"""

    files: List[str]
    size_bytes: int
    category: str  # 'core', 'tests', 'config', 'docs'
    priority: int  # 1=high, 2=medium, 3=low


@dataclass
class RepoSummary:
    """High-level repository summary"""

    total_files: int
    languages: Dict[str, int]
    structure: Dict[str, Any]
    key_patterns: List[str]
    quality_overview: Dict[str, float]


class RepositoryAnalyzer(BaseAnalyzer):
    """Analyze entire repositories with context management"""

    def __init__(self, max_chunk_size: int = 50000, max_files_per_chunk: int = 20):
        super().__init__()
        self.max_chunk_size = max_chunk_size
        self.max_files_per_chunk = max_files_per_chunk
        self.unified_analyzer = UnifiedAnalyzer()

    def analyze(self, file_path: str) -> AnalysisResult:
        """Required abstract method - delegates to analyze_repository"""
        results = self.analyze_repository(file_path)

        # Convert to AnalysisResult format
        return AnalysisResult(
            file_path=file_path,
            language="repository",
            quality_score=results["repository_summary"]["overall_quality"],
            issues=[],
            recommendations=results["recommendations"],
        )

    def analyze_repository(self, repo_path: str) -> Dict[str, Any]:
        """Analyze entire repository with chunking strategy"""
        repo_path = Path(repo_path)

        # 1. Repository discovery and categorization
        file_inventory = self._discover_files(repo_path)
        repo_summary = self._create_repo_summary(file_inventory)

        # 2. Create analysis chunks
        chunks = self._create_chunks(file_inventory)

        # 3. Analyze chunks in parallel
        chunk_results = self._analyze_chunks_parallel(chunks)

        # 4. Synthesize results with AI
        final_analysis = self._synthesize_results(repo_summary, chunk_results)

        return final_analysis

    def _discover_files(self, repo_path: Path) -> Dict[str, List[str]]:
        """Discover and categorize all files in repository"""
        categories = {
            "core": [],  # Main source code
            "tests": [],  # Test files
            "config": [],  # Configuration files
            "docs": [],  # Documentation
            "build": [],  # Build/deployment files
            "other": [],  # Everything else
        }

        ignore_patterns = {
            ".git",
            "__pycache__",
            "node_modules",
            ".pytest_cache",
            "venv",
            "env",
            ".venv",
            "dist",
            "build",
            ".cache",
        }

        for root, dirs, files in os.walk(repo_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_patterns]

            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(repo_path)

                # Skip binary and large files
                if self._should_skip_file(file_path):
                    continue

                category = self._categorize_file(relative_path)
                categories[category].append(str(relative_path))

        return categories

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped"""
        # Skip binary files
        binary_extensions = {
            ".pyc",
            ".so",
            ".dll",
            ".exe",
            ".bin",
            ".jpg",
            ".png",
            ".gif",
            ".pdf",
        }
        if file_path.suffix.lower() in binary_extensions:
            return True

        # Skip very large files (>1MB)
        try:
            if file_path.stat().st_size > 1024 * 1024:
                return True
        except OSError:
            return True

        return False

    def _categorize_file(self, file_path: Path) -> str:
        """Categorize file by type and location"""
        path_str = str(file_path).lower()

        # Test files
        if "test" in path_str or file_path.name.startswith("test_"):
            return "tests"

        # Configuration files
        config_patterns = [
            "config",
            "settings",
            ".env",
            "requirements",
            "package.json",
            "Dockerfile",
        ]
        if any(pattern in path_str for pattern in config_patterns):
            return "config"

        # Documentation
        doc_patterns = ["readme", "doc", ".md", ".rst", ".txt"]
        if any(pattern in path_str for pattern in doc_patterns):
            return "docs"

        # Build files
        build_patterns = ["makefile", "setup.py", ".yml", ".yaml", "build", "deploy"]
        if any(pattern in path_str for pattern in build_patterns):
            return "build"

        # Core source code
        code_extensions = {
            ".py",
            ".js",
            ".ts",
            ".java",
            ".go",
            ".rs",
            ".cpp",
            ".c",
            ".h",
        }
        if file_path.suffix.lower() in code_extensions:
            return "core"

        return "other"

    def _create_repo_summary(self, file_inventory: Dict[str, List[str]]) -> RepoSummary:
        """Create high-level repository summary"""
        total_files = sum(len(files) for files in file_inventory.values())

        # Count languages by extension
        languages = {}
        for files in file_inventory.values():
            for file_path in files:
                ext = Path(file_path).suffix.lower()
                if ext:
                    languages[ext] = languages.get(ext, 0) + 1

        # Repository structure
        structure = {
            "categories": {cat: len(files) for cat, files in file_inventory.items()},
            "total_files": total_files,
            "languages": languages,
        }

        return RepoSummary(
            total_files=total_files,
            languages=languages,
            structure=structure,
            key_patterns=[],
            quality_overview={},
        )

    def _create_chunks(self, file_inventory: Dict[str, List[str]]) -> List[RepoChunk]:
        """Create analysis chunks with size and priority management"""
        chunks = []

        # Priority order: core -> tests -> config -> docs -> build -> other
        priority_order = ["core", "tests", "config", "docs", "build", "other"]

        for priority, category in enumerate(priority_order, 1):
            files = file_inventory.get(category, [])
            if not files:
                continue

            # Split category into chunks
            category_chunks = self._split_files_into_chunks(files, category, priority)
            chunks.extend(category_chunks)

        return chunks

    def _split_files_into_chunks(
        self, files: List[str], category: str, priority: int
    ) -> List[RepoChunk]:
        """Split files into manageable chunks"""
        chunks = []
        current_chunk = []
        current_size = 0

        for file_path in files:
            try:
                file_size = Path(file_path).stat().st_size
            except OSError:
                continue

            # Check if adding this file would exceed limits
            if (
                current_size + file_size > self.max_chunk_size
                or len(current_chunk) >= self.max_files_per_chunk
            ):

                if current_chunk:
                    chunks.append(
                        RepoChunk(
                            files=current_chunk.copy(),
                            size_bytes=current_size,
                            category=category,
                            priority=priority,
                        )
                    )

                current_chunk = [file_path]
                current_size = file_size
            else:
                current_chunk.append(file_path)
                current_size += file_size

        # Add final chunk
        if current_chunk:
            chunks.append(
                RepoChunk(
                    files=current_chunk,
                    size_bytes=current_size,
                    category=category,
                    priority=priority,
                )
            )

        return chunks

    def _analyze_chunks_parallel(self, chunks: List[RepoChunk]) -> List[Dict[str, Any]]:
        """Analyze chunks in parallel with priority ordering"""
        results = []

        # Sort chunks by priority
        chunks.sort(key=lambda x: x.priority)

        with ThreadPoolExecutor(max_workers=3) as executor:
            # Submit high-priority chunks first
            future_to_chunk = {}

            for chunk in chunks:
                future = executor.submit(self._analyze_chunk, chunk)
                future_to_chunk[future] = chunk

            # Collect results as they complete
            for future in as_completed(future_to_chunk):
                chunk = future_to_chunk[future]
                try:
                    result = future.result()
                    results.append({"chunk_info": chunk, "analysis": result})
                except Exception as e:
                    print(f"Error analyzing chunk {chunk.category}: {e}")

        return results

    def _analyze_chunk(self, chunk: RepoChunk) -> Dict[str, Any]:
        """Analyze a single chunk of files"""
        chunk_analysis = {
            "category": chunk.category,
            "file_count": len(chunk.files),
            "size_bytes": chunk.size_bytes,
            "files": [],
            "summary": {},
            "patterns": [],
            "issues": [],
        }

        # Analyze each file in chunk
        for file_path in chunk.files:
            try:
                file_result = self.unified_analyzer.analyze_file(file_path)
                chunk_analysis["files"].append(
                    {
                        "path": file_path,
                        "quality_score": file_result.quality_score,
                        "issues": file_result.issues,
                        "language": file_result.language,
                    }
                )
            except Exception as e:
                print(f"Error analyzing file {file_path}: {e}")

        # Create chunk summary
        chunk_analysis["summary"] = self._summarize_chunk(chunk_analysis["files"])

        return chunk_analysis

    def _summarize_chunk(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize analysis results for a chunk"""
        if not file_analyses:
            return {}

        total_files = len(file_analyses)
        avg_quality = (
            sum(f.get("quality_score", 0) for f in file_analyses) / total_files
        )

        # Aggregate issues by type
        issue_counts = {}
        for file_analysis in file_analyses:
            for issue in file_analysis.get("issues", []):
                issue_type = issue.get("type", "unknown")
                issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1

        return {
            "file_count": total_files,
            "average_quality": avg_quality,
            "issue_summary": issue_counts,
            "languages": list(set(f.get("language", "") for f in file_analyses)),
        }

    def _synthesize_results(
        self, repo_summary: RepoSummary, chunk_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Synthesize all results into final repository analysis"""

        # Aggregate all chunk summaries
        total_quality_scores = []
        all_issues = {}
        all_languages = set()

        for chunk_result in chunk_results:
            chunk_summary = chunk_result["analysis"]["summary"]
            if "average_quality" in chunk_summary:
                total_quality_scores.append(chunk_summary["average_quality"])

            # Aggregate issues
            for issue_type, count in chunk_summary.get("issue_summary", {}).items():
                all_issues[issue_type] = all_issues.get(issue_type, 0) + count

            # Collect languages
            all_languages.update(chunk_summary.get("languages", []))

        # Calculate repository-wide metrics
        repo_quality = (
            sum(total_quality_scores) / len(total_quality_scores)
            if total_quality_scores
            else 0
        )

        # Generate AI-powered insights
        insights = self._generate_insights(chunk_results, repo_quality, all_issues)

        return {
            "repository_summary": {
                "total_files": repo_summary.total_files,
                "languages": list(all_languages),
                "structure": repo_summary.structure,
                "overall_quality": repo_quality,
            },
            "analysis_by_category": {
                chunk["chunk_info"].category: chunk["analysis"]["summary"]
                for chunk in chunk_results
            },
            "issue_summary": all_issues,
            "insights": insights,
            "recommendations": self._generate_recommendations(all_issues, repo_quality),
            "chunk_details": chunk_results,
        }

    def _generate_insights(
        self,
        chunk_results: List[Dict[str, Any]],
        repo_quality: float,
        all_issues: Dict[str, int],
    ) -> List[str]:
        """Generate AI-powered insights about the repository"""
        insights = []

        # Quality insights
        if repo_quality >= 8:
            insights.append(
                "🎯 Excellent code quality - repository shows strong engineering practices"
            )
        elif repo_quality >= 6:
            insights.append("⚡ Good code quality with room for targeted improvements")
        else:
            insights.append(
                "🔧 Code quality needs attention - consider systematic refactoring"
            )

        # Issue pattern insights
        if "security" in all_issues and all_issues["security"] > 5:
            insights.append("🛡️ Security issues detected - prioritize security review")

        if "performance" in all_issues and all_issues["performance"] > 10:
            insights.append("🚀 Performance optimization opportunities identified")

        # Structure insights
        core_chunks = [c for c in chunk_results if c["chunk_info"].category == "core"]
        test_chunks = [c for c in chunk_results if c["chunk_info"].category == "tests"]

        if len(test_chunks) == 0:
            insights.append("🧪 No test files detected - consider adding test coverage")
        elif len(core_chunks) > 0 and len(test_chunks) > 0:
            test_ratio = len(test_chunks) / len(core_chunks)
            if test_ratio < 0.3:
                insights.append(
                    "📊 Low test-to-code ratio - consider expanding test coverage"
                )

        return insights

    def _generate_recommendations(
        self, all_issues: Dict[str, int], repo_quality: float
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Priority-based recommendations
        if "security" in all_issues:
            recommendations.append("1. Address security vulnerabilities immediately")

        if repo_quality < 6:
            recommendations.append("2. Implement code quality standards and linting")

        if "style" in all_issues and all_issues["style"] > 20:
            recommendations.append(
                "3. Set up automated code formatting (black, prettier)"
            )

        if "complexity" in all_issues:
            recommendations.append(
                "4. Refactor complex functions for better maintainability"
            )

        recommendations.append("5. Set up continuous quality monitoring with BRIGADE")

        return recommendations
