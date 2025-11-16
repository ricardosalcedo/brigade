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

## 🎯 Use Cases

### **Individual Developer**
```bash
# Daily code quality check
./brigade analyze myfile.py

# Quick fix deployment
./brigade auto-fix myfile.py --create-pr
```

### **Team Code Review**
```bash
# Pre-review analysis
./brigade analyze src/ --recursive --report team_review.md

# Coordinated improvement
./brigade deploy critical_file.py --mode full
```

### **CI/CD Integration**
```bash
# Quality gate deployment
./brigade analyze . --recursive --output quality_gate.json

# Automated improvement pipeline
./brigade auto-fix changed_files.py --create-pr
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

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎖️ BRIGADE - Where Code Intelligence Meets Military Precision** ⚡

Deploy your code analysis brigade: `./brigade analyze your_code.py`
