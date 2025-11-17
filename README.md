# 🎖️ BRIGADE - Coordinated Code Intelligence (WIP)

**Where specialized AI agents unite for comprehensive code analysis and enhancement.**

BRIGADE deploys coordinated teams of AI agents to analyze, improve, and enhance your code with military precision and efficiency.

## ✨ Features

- **🎖️ Multi-Agent Coordination**: Specialized agents working in perfect harmony
- **🎯 Precision Analysis**: Static analysis + LLM intelligence + Agent coordination
- **⚡ Automated Fixes**: AI-powered code improvements with PR creation
- **🌐 Multi-Language Support**: Python, JavaScript, TypeScript, Java, Go, Rust
- **🔄 Continuous Deployment**: Iterative improvement workflows
- **📊 Comprehensive Reporting**: Detailed analysis and progress tracking

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/ricardosalcedo/brigade.git
cd brigade

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure

# Make BRIGADE executable
chmod +x brigade
```

### Basic Usage
```bash
# Deploy analysis brigade
./brigade analyze myfile.py

# Deploy auto-fix brigade with PR creation
./brigade auto-fix myfile.py --create-pr

# Deploy coordinated multi-agent brigade
./brigade deploy myfile.py --mode coordinated

# Directory analysis with recursive deployment
./brigade analyze src/ --recursive --output results.json
```

## 🎖️ Brigade Commands

### **Repository Analysis**
Analyze entire repositories without context overflow:
```bash
./brigade repo . --output full-analysis.json
./brigade repo /path/to/large-repo --report repo-report.md
./brigade repo . --max-chunk-size 30000 --max-files-per-chunk 15
```

### **Analysis Brigade**
Deploy specialized analysis agents for comprehensive code review:
```bash
./brigade analyze myfile.py --output analysis.json
./brigade analyze src/ --recursive --report brigade_report.md
```

### **Auto-Fix Brigade**
Deploy fix agents with automated PR creation (requires human approval):
```bash
./brigade auto-fix myfile.py --create-pr  # Requests approval before creating PR
./brigade auto-fix myfile.py --dry-run    # Preview fixes without approval
```

### **Approval Management**
Manage pending PR approvals for safety:
```bash
./brigade approve --list                  # List pending approvals
./brigade approve --approve <ID>          # Approve specific request
./brigade approve --deny <ID>             # Deny specific request
```

### **Coordinated Brigade**
Deploy full multi-agent coordination:
```bash
./brigade deploy myfile.py --mode analysis     # Analysis agents only
./brigade deploy myfile.py --mode coordinated  # Coordinated workflow
./brigade deploy myfile.py --mode full        # Complete brigade deployment
```

## 🛡️ Human Approval Workflow

BRIGADE includes a safety mechanism requiring human approval before creating pull requests:

### **Approval Process**
1. **Analysis**: BRIGADE analyzes code and generates fixes
2. **Preview**: Shows proposed fixes with quality impact
3. **Human Review**: Requests approval with detailed information
4. **Decision**: Human approves, denies, or saves for later
5. **Execution**: Only approved fixes create pull requests

### **Interactive Approval**
```
🎖️ BRIGADE PR Approval Required
==================================================
📁 File: example.py
📊 Quality Score: 4/10
🔧 Fixes Proposed: 3

🛠️ Proposed Fixes:
   1. Replace eval() with ast.literal_eval() for security
   2. Add context managers for file operations  
   3. Fix style issues with None comparisons

📈 Expected Quality Improvement: +3 points

❓ Approve PR creation for these fixes?
   [y]es / [n]o / [d]etails / [s]ave for later:
```

### **Approval Commands**
```bash
# List all pending approvals
./brigade approve --list

# Approve a specific request
./brigade approve --approve approval_20241116_143022

# Deny a specific request  
./brigade approve --deny approval_20241116_143022
```

BRIGADE deploys specialized agents for different aspects of code intelligence:

### **🎯 Analysis Agent**
- Comprehensive code quality assessment
- Security vulnerability detection
- Performance bottleneck identification
- Style and best practice evaluation

### **🛠️ Fix Agent**
- AI-powered code improvement generation
- Targeted issue resolution
- Safe code transformation
- Quality enhancement suggestions

### **🧪 Testing Agent**
- Automated fix validation
- Syntax and import verification
- Quality assurance checks
- Regression prevention

### **🌿 Deployment Agent**
- Git workflow management
- Pull request creation
- Branch coordination
- Merge facilitation

### **🎖️ Coordinator Agent**
- Multi-agent orchestration
- Workflow management
- Error recovery
- Progress monitoring

## 📊 Example Output

```
🎖️ BRIGADE Coordinated Deployment
==================================================
🎯 Target: example.py
🔤 Language: PYTHON
📊 Quality Score: 7/10
🚨 Issues Found: 3

🤖 Agents deployed: [coordinator, analysis_agent, fix_agent, testing_agent]

💡 Brigade Recommendations:
   1. Replace eval() with ast.literal_eval() for security
   2. Add context managers for file operations
   3. Implement proper error handling

✅ Brigade deployment completed successfully
🔗 Pull Request: https://github.com/user/repo/pull/1
```

## 🏗️ Architecture

```
BRIGADE/
├── core/                    # Core framework
│   ├── base.py             # Base classes and data structures
│   ├── interfaces.py       # Agent coordination interfaces
│   ├── exceptions.py       # Custom exception hierarchy
│   ├── config.py          # Configuration management
│   └── utils.py           # Utility functions
├── analyzers/              # Analysis implementations
│   ├── static_analyzer.py  # Static analysis agents
│   ├── llm_analyzer.py     # LLM-based analysis agents
│   └── unified_analyzer.py # Coordinated analysis
├── workflows/              # Agent coordination workflows
│   ├── workflow_manager.py # Brigade coordination
│   ├── auto_fix_workflow.py # Auto-fix agent deployment
│   └── strands_workflow.py # Multi-agent coordination
└── brigade                 # 🎖️ Main BRIGADE command
```

## 👥 Team Usage & Workflows

### **Team Setup**
```bash
# Team lead sets up BRIGADE for the team
git clone https://github.com/ricardosalcedo/brigade.git
cd brigade

# Configure team-wide settings
export BRIGADE_TEAM_CONFIG="team-config.json"
export QUALITY_THRESHOLD=7
export GITHUB_TOKEN="your_team_token"

# Share configuration with team
cp brigade-team-config.json.example brigade-team-config.json
```

### **Daily Team Workflows**

#### **🔍 Pre-Review Analysis**
Before code reviews, teams can run coordinated analysis:
```bash
# Analyze entire feature branch
./brigade analyze feature-branch/ --recursive --report team-review.md

# Generate team dashboard
./brigade analyze src/ --output team-dashboard.json --format dashboard

# Multi-developer analysis
./brigade deploy . --mode team --assignees "dev1,dev2,dev3"
```

#### **📋 Sprint Planning Integration**
```bash
# Analyze technical debt for sprint planning
./brigade analyze . --recursive --focus technical-debt --output sprint-analysis.json

# Estimate fix effort for backlog items
./brigade analyze backlog-files/ --estimate-effort --output effort-estimates.json

# Generate improvement roadmap
./brigade deploy . --mode roadmap --output team-roadmap.md
```

#### **🚀 Continuous Integration**
```bash
# Pre-merge quality gate
./brigade analyze changed-files --quality-gate --threshold 7

# Automated team fixes (requires approval)
./brigade auto-fix . --team-mode --create-pr --reviewers "team-leads"

# Post-merge quality tracking
./brigade analyze . --track-quality --output quality-metrics.json
```

### **Team Roles & Permissions**

#### **👑 Team Lead**
```bash
# Approve team-wide fixes
./brigade approve --team-lead --list-all

# Configure team standards
./brigade config --set team-quality-threshold 8
./brigade config --set auto-fix-policy "lead-approval"

# Generate team reports
./brigade report --team-summary --period weekly
```

#### **🧑‍💻 Developer**
```bash
# Individual code analysis
./brigade analyze my-feature.py --personal

# Request team review
./brigade analyze my-changes/ --request-review --assignee "team-lead"

# Self-service fixes
./brigade auto-fix my-code.py --self-approve --max-changes 5
```

#### **👀 Code Reviewer**
```bash
# Review-focused analysis
./brigade analyze pr-files/ --review-mode --output review-checklist.md

# Suggest improvements during review
./brigade auto-fix reviewed-code.py --suggestions-only

# Validate fix quality
./brigade analyze fixed-files/ --validate-fixes
```

### **Team Configuration**

#### **team-config.json**
```json
{
  "team": {
    "name": "Backend Team",
    "quality_threshold": 7,
    "auto_fix_policy": "lead_approval",
    "notification_channels": ["#backend-alerts", "#code-quality"]
  },
  "workflows": {
    "pre_merge": {
      "quality_gate": true,
      "security_scan": true,
      "team_review": true
    },
    "daily_analysis": {
      "enabled": true,
      "schedule": "09:00",
      "scope": "changed_files"
    }
  },
  "permissions": {
    "team_leads": ["alice", "bob"],
    "auto_approve_threshold": 5,
    "require_review_above": 10
  }
}
```

### **Team Metrics & Reporting**

#### **📊 Quality Dashboard**
```bash
# Generate team quality dashboard
./brigade report --dashboard --team --output team-dashboard.html

# Track quality trends
./brigade metrics --quality-trend --period 30days --output quality-trend.json

# Compare team performance
./brigade metrics --team-comparison --output team-comparison.md
```

#### **📈 Progress Tracking**
```bash
# Sprint quality progress
./brigade report --sprint-progress --output sprint-quality.json

# Technical debt tracking
./brigade metrics --technical-debt --trend --output debt-trend.json

# Team productivity metrics
./brigade report --productivity --team --period weekly
```

### **Integration with Team Tools**

#### **🔗 Slack Integration**
```bash
# Configure Slack notifications
./brigade config --slack-webhook "https://hooks.slack.com/..."
./brigade config --slack-channel "#code-quality"

# Daily quality reports to Slack
./brigade report --daily --slack --channel "#team-updates"
```

#### **📋 Jira Integration**
```bash
# Link fixes to Jira tickets
./brigade auto-fix . --jira-link --project "TEAM"

# Create technical debt tickets
./brigade analyze . --create-jira-tickets --assignee "team-lead"

# Update story points based on complexity
./brigade analyze backlog/ --update-story-points --jira-project "TEAM"
```

#### **🐙 GitHub Integration**
```bash
# Team PR templates with BRIGADE analysis
./brigade config --pr-template --team-standards

# Automated team reviews
./brigade auto-fix . --create-pr --team-reviewers --draft

# Quality status checks
./brigade analyze . --github-status --required-checks
```

### **Team Best Practices**

#### **🎯 Quality Standards**
- **Minimum Quality Score**: 7/10 for production code
- **Security Issues**: Zero tolerance, immediate fix required
- **Code Coverage**: Maintain above 80% with BRIGADE validation
- **Technical Debt**: Weekly team review and prioritization

#### **🔄 Workflow Integration**
```bash
# Morning team quality check
./brigade analyze . --team-daily --notify-slack

# Pre-standup code health
./brigade report --team-health --brief

# End-of-sprint quality review
./brigade report --sprint-summary --team --detailed
```

#### **📚 Knowledge Sharing**
```bash
# Generate team learning reports
./brigade report --learning-opportunities --team

# Share best practices
./brigade analyze . --extract-patterns --share-team

# Mentor new team members
./brigade analyze junior-code/ --mentoring-mode --suggestions
```

### **Scaling for Large Teams**

#### **🏢 Multi-Team Coordination**
```bash
# Cross-team analysis
./brigade analyze . --multi-team --teams "backend,frontend,mobile"

# Organization-wide standards
./brigade config --org-standards --apply-all-teams

# Inter-team dependency analysis
./brigade analyze . --team-dependencies --output team-deps.json
```

#### **📊 Management Reporting**
```bash
# Executive quality summary
./brigade report --executive --all-teams --monthly

# Team performance comparison
./brigade metrics --team-rankings --quality-focused

# ROI analysis for code quality
./brigade report --roi-analysis --team-investment
```

## 🎯 Use Cases

### **Individual Developer**
```bash
# Daily code quality check
./brigade analyze myfile.py

# Quick fix deployment
./brigade auto-fix myfile.py --create-pr
```

### **Small Team (2-5 developers)**
```bash
# Team code review preparation
./brigade analyze src/ --recursive --report team_review.md

# Coordinated improvement with team approval
./brigade deploy critical_file.py --mode team --reviewers "team-lead"

# Daily team quality standup
./brigade report --team-daily --brief
```

### **Large Team (5+ developers)**
```bash
# Multi-team coordination
./brigade analyze . --multi-team --teams "backend,frontend"

# Organization-wide quality standards
./brigade deploy . --mode organization --quality-gate

# Executive reporting
./brigade report --executive --all-teams --monthly
```

### **Enterprise Integration**
```bash
# CI/CD pipeline integration
./brigade analyze . --recursive --output quality_gate.json

# Automated improvement pipeline with governance
./brigade auto-fix . --enterprise-mode --compliance-check

# Cross-project analysis and reporting
./brigade analyze multiple-repos/ --enterprise-dashboard
```

## ⚙️ Configuration

### Environment Variables
```bash
export AWS_DEFAULT_REGION=us-west-2
export BRIGADE_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
export QUALITY_THRESHOLD=6
export DEFAULT_BRANCH=main
```

### Configuration File
```json
{
  "aws_region": "us-west-2",
  "model_id": "anthropic.claude-3-sonnet-20240229-v1:0",
  "quality_threshold": 7,
  "max_issues_to_fix": 10,
  "branch_prefix": "brigade-fix"
}
```

## 🎖️ Brigade Principles

- **🎯 Precision**: Every agent has a specific mission
- **🤝 Coordination**: Agents work together seamlessly
- **⚡ Efficiency**: Optimized workflows for maximum impact
- **🛡️ Reliability**: Robust error handling and recovery
- **📈 Excellence**: Continuous improvement and learning

## 🔍 Full Repository Analysis (No Context Limits)

BRIGADE can analyze entire repositories of any size using intelligent chunking strategies that avoid AI context overflow:

### **🧠 Chunking Strategy**
- **File Categorization**: Automatically categorizes files (core, tests, config, docs, build)
- **Size Management**: Splits analysis into manageable chunks (default: 50KB per chunk)
- **Priority Processing**: Analyzes core code first, then tests, then supporting files
- **Parallel Processing**: Uses multiple workers for faster analysis
- **Context Preservation**: Maintains repository-wide insights across chunks

### **📊 Repository Analysis Features**
```bash
# Analyze entire repository
./brigade repo /path/to/large-repo

# Customize chunking parameters
./brigade repo . --max-chunk-size 30000 --max-files-per-chunk 15

# Generate comprehensive report
./brigade repo . --report repo-analysis.md --output detailed-results.json

# Focus on specific categories
./brigade repo . --categories core tests --verbose

# Parallel processing control
./brigade repo . --parallel-workers 5
```

### **🎯 Repository Insights**
BRIGADE provides repository-wide insights including:
- **Overall Quality Score**: Aggregated across all files
- **Language Distribution**: Breakdown by programming languages
- **Issue Patterns**: Common problems across the codebase
- **Architecture Analysis**: Structure and organization insights
- **Technical Debt Assessment**: Prioritized improvement recommendations

### **📈 Example Repository Analysis**
```
🎖️ BRIGADE Repository Analysis
📁 Target: ./my-large-project
⚙️ Max chunk size: 50000 bytes
📊 Max files per chunk: 20

🔍 Discovering repository structure...

📊 Repository Analysis Complete
📁 Total files: 247
🔤 Languages: Python, JavaScript, TypeScript, CSS
⭐ Overall quality: 7.2/10

💡 Key Insights:
   ⚡ Good code quality with room for targeted improvements
   🧪 Low test-to-code ratio - consider expanding test coverage
   🔧 Performance optimization opportunities identified

🎯 Recommendations:
   1. Implement code quality standards and linting
   2. Set up automated code formatting (black, prettier)
   3. Refactor complex functions for better maintainability
   4. Set up continuous quality monitoring with BRIGADE

💾 Results saved to analysis-results.json
📄 Report generated: repo-analysis.md
```

### **🏗️ How It Works**

1. **Discovery Phase**: Scans repository and categorizes all files
2. **Chunking Phase**: Groups files into analysis chunks by category and size
3. **Analysis Phase**: Processes chunks in parallel with priority ordering
4. **Synthesis Phase**: Combines results using AI to generate repository-wide insights
5. **Reporting Phase**: Creates comprehensive reports and actionable recommendations

This approach allows BRIGADE to analyze repositories with thousands of files while maintaining context and providing meaningful insights.

## 🧪 Development & Testing

### **Running Tests**
```bash
# Run complete test suite
python3 run_tests.py

# Run specific test categories
python3 -m pytest tests/unit/ -v          # Unit tests
python3 -m pytest tests/integration/ -v   # Integration tests

# Run with coverage
python3 -m pytest --cov=core --cov=analyzers --cov=workflows
```

### **Code Quality Checks**
```bash
# Format code
python3 -m black core/ analyzers/ workflows/

# Sort imports
python3 -m isort core/ analyzers/ workflows/

# Style checks
flake8 core/ analyzers/ workflows/ --max-line-length=100

# Type checking
mypy core/ analyzers/ workflows/ --ignore-missing-imports
```

### **Pre-commit Hooks**
BRIGADE automatically runs tests before every commit to ensure code quality:

```bash
# Normal commit (tests must pass)
git add .
git commit -m "Your changes"

# Bypass hook if needed (use sparingly)
git commit --no-verify -m "Emergency fix"
```

**Pre-commit Hook Features:**
- ✅ Runs complete test suite before commit
- ✅ Blocks commits if tests fail
- ✅ Shows detailed test output
- ✅ Ensures code quality standards

### **GitHub Actions Locally**
Run the same CI/CD pipeline locally using `act`:

```bash
# Install act
brew install act

# Run GitHub Actions locally
act -j test                    # Run test job
act -j security               # Run security checks
act -j quality                # Run code quality checks

# Run all workflows
act
```

### **Test Structure**
```
tests/
├── unit/                     # Unit tests
│   ├── test_config.py       # Configuration tests
│   ├── test_approval.py     # Approval workflow tests
│   ├── test_static_analyzer.py # Static analysis tests
│   └── test_auto_fix_workflow.py # Auto-fix tests
├── integration/             # Integration tests
│   └── test_brigade_cli.py  # CLI integration tests
└── fixtures/                # Test data and fixtures
```

### **Continuous Integration**
BRIGADE uses GitHub Actions for automated testing:

- **✅ Multi-Python Testing**: Tests on Python 3.8, 3.9, 3.10, 3.11
- **✅ Code Quality**: Black, isort, flake8, mypy checks
- **✅ Security Scanning**: Bandit and safety checks
- **✅ Test Coverage**: Comprehensive unit and integration tests

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. **Run tests locally**: `python3 run_tests.py`
4. **Ensure code quality**: Format with black, check with flake8
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

**Note**: The pre-commit hook will automatically run tests before each commit to maintain code quality.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎖️ BRIGADE - Where Code Intelligence Meets Military Precision** ⚡

Deploy your code analysis brigade: `./brigade analyze your_code.py`
