# AI Code Agent System

A comprehensive system demonstrating how to use AI agents for:
1. **Code Generation** - Writing code based on natural language prompts
2. **Code Review** - Analyzing code for errors and suggesting improvements

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [Code Generation Agent](#code-generation-agent)
- [Code Review Agent](#code-review-agent)
- [Usage Examples](#usage-examples)
- [Features](#features)
- [Installation](#installation)
- [Demo Commands](#demo-commands)
- [API Reference](#api-reference)

## Overview

This project showcases two powerful AI agent capabilities that work together to provide a complete code development assistance workflow:

### 1. Code Generation Agent 🤖
- **Natural Language to Code**: Converts plain English prompts into functional code
- **Multi-Language Support**: Python, JavaScript, Java, C++, HTML, CSS
- **Smart Context Understanding**: Analyzes prompts to understand intent and requirements
- **Best Practices**: Generates code following industry standards and conventions
- **Documentation Included**: Automatically adds docstrings and comments
- **Test Generation**: Optional test case creation for generated code

### 2. Code Review Agent 🔍
- **Comprehensive Analysis**: Examines code for syntax, logic, security, and performance issues
- **Security Scanning**: Detects potential vulnerabilities and unsafe patterns
- **Performance Optimization**: Suggests improvements for better efficiency
- **Style Checking**: Enforces coding standards and naming conventions
- **Quality Scoring**: Provides overall code quality metrics (0-100)
- **Actionable Suggestions**: Gives specific recommendations for improvements

## Getting Started

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Installation
```bash
# Clone the repository
git clone https://github.com/davidvdmerwenl-jpg/Website-idea.git
cd Website-idea

# Install dependencies
pip install -r requirements.txt

# Run the full demonstration
python main.py demo
```

## Code Generation Agent

The Code Generation Agent transforms natural language descriptions into working code:

### Supported Prompts
- **Function Creation**: "Create a function to calculate prime numbers"
- **Class Design**: "Build a User class with authentication methods"
- **Algorithm Implementation**: "Implement quicksort algorithm with optimization"
- **API Development**: "Create a REST API for task management"
- **Web Development**: "Generate an HTML page with responsive design"

### Example Usage
```python
from code_generator import CodeGenerationAgent, CodeGenerationRequest

agent = CodeGenerationAgent()
request = CodeGenerationRequest(
    prompt="Create a Python function to validate email addresses",
    language="python",
    include_tests=True,
    include_docs=True
)

result = agent.generate_code(request)
print(result["code"])
```

## Code Review Agent

The Code Review Agent performs comprehensive code analysis:

### Analysis Categories
- **Syntax Errors**: AST parsing for syntax validation
- **Security Issues**: Detection of common vulnerabilities
- **Performance Problems**: Identification of inefficient patterns
- **Style Violations**: PEP 8 and naming convention checks
- **Logic Issues**: Common programming mistakes
- **Documentation Quality**: Docstring and comment analysis

### Example Usage
```python
from code_reviewer import CodeReviewAgent

agent = CodeReviewAgent()
result = agent.review_file("my_code.py")

print(f"Overall Score: {result.overall_score}/100")
for issue in result.issues:
    print(f"[{issue.severity}] Line {issue.line}: {issue.message}")
```

## Usage Examples

### 1. Interactive Code Generation
```bash
python main.py interactive
```
Enter custom prompts and see real-time code generation with optional review.

### 2. Batch Code Review
```bash
python code_reviewer.py /path/to/project
```
Review all Python files in a directory with detailed analysis.

### 3. Specific File Review
```bash
python code_reviewer.py my_script.py
```
Get detailed analysis of a single file.

### 4. Generate Specific Code Types
```python
# Generate a web API
request = CodeGenerationRequest(
    prompt="Create a FastAPI server with user authentication",
    language="python",
    framework="fastapi"
)

# Generate frontend code
request = CodeGenerationRequest(
    prompt="Create a responsive login form",
    language="html"
)
```

## Features

- 🤖 **Intelligent Code Generation**: Context-aware code creation from natural language
- 🔍 **Comprehensive Code Analysis**: Multi-layered error detection and quality assessment
- 📝 **Documentation Generation**: Automatic docstring and comment creation
- 🛡️ **Security Scanning**: Detection of vulnerabilities and unsafe coding patterns
- ⚡ **Performance Optimization**: Suggestions for more efficient code
- 🎯 **Multi-language Support**: Python, JavaScript, Java, C++, HTML, CSS, and more
- 📊 **Quality Metrics**: Detailed code quality scoring and metrics
- 🔄 **Continuous Improvement**: Iterative code generation and refinement
- 🎨 **Style Enforcement**: Automatic adherence to coding standards
- 🧪 **Test Generation**: Optional unit test creation for generated code

## Installation

### Option 1: Direct Installation
```bash
pip install -r requirements.txt
```

### Option 2: Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Dependencies
- `openai>=1.0.0` - For AI model integration
- `anthropic>=0.7.0` - Alternative AI provider
- `colorama>=0.4.6` - Colored terminal output
- `black>=23.0.0` - Code formatting
- `flake8>=6.0.0` - Linting
- `pylint>=3.0.0` - Advanced code analysis

## Demo Commands

### Full System Demo
```bash
python main.py demo
```
Runs complete demonstration including code generation and review.

### Code Generation Only
```bash
python main.py generate
```
Demonstrates code generation capabilities with multiple examples.

### Code Review Only
```bash
python main.py review
```
Shows code review features on sample files.

### Interactive Mode
```bash
python main.py interactive
```
Enter custom prompts for real-time code generation and review.

### Individual Agents
```bash
# Code generator standalone
python code_generator.py

# Code reviewer standalone
python code_reviewer.py <file_or_directory>
```

## API Reference

### CodeGenerationRequest
```python
@dataclass
class CodeGenerationRequest:
    prompt: str                    # Natural language description
    language: str = "python"       # Target programming language
    framework: Optional[str] = None # Specific framework (e.g., "fastapi")
    complexity: str = "medium"     # "simple", "medium", "complex"
    include_tests: bool = False    # Generate unit tests
    include_docs: bool = True      # Include documentation
```

### CodeReviewResult
```python
@dataclass
class CodeReviewResult:
    file_path: str                 # Path to reviewed file
    issues: List[CodeIssue]        # Found issues and problems
    metrics: Dict[str, Any]        # Code quality metrics
    overall_score: float           # Quality score (0-100)
    suggestions: List[str]         # Improvement recommendations
```

### Issue Severity Levels
- **Error**: Critical issues that prevent code execution
- **Warning**: Important issues that may cause problems
- **Info**: Style and optimization suggestions

## Advanced Usage

### Custom Code Templates
The system can be extended with custom templates for specific use cases:

```python
# Add custom code generation patterns
agent = CodeGenerationAgent()
agent.add_custom_template("microservice", microservice_template)
```

### Integration with IDEs
The agents can be integrated with popular IDEs through plugins:

```python
# VS Code extension example
from code_reviewer import CodeReviewAgent

def review_current_file():
    agent = CodeReviewAgent()
    result = agent.review_file(get_current_file_path())
    display_issues_in_editor(result.issues)
```

### Continuous Integration
Use the code review agent in CI/CD pipelines:

```yaml
# GitHub Actions example
- name: AI Code Review
  run: python code_reviewer.py src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Submit feature requests
- Contribute code improvements

---

**Happy Coding! 🚀** 

Let AI agents help you write better code faster and catch issues before they become problems.