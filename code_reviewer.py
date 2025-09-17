#!/usr/bin/env python3
"""
AI Code Review Agent
Analyzes code for errors, bugs, security issues, and suggests improvements.
"""

import ast
import re
import sys
import os
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
from colorama import init, Fore, Style

init()  # Initialize colorama for colored output

@dataclass
class CodeIssue:
    """Represents a code issue found during review."""
    severity: str  # "error", "warning", "info", "suggestion"
    line: int
    column: int
    message: str
    rule: str
    suggestion: Optional[str] = None

@dataclass
class CodeReviewResult:
    """Results of a code review."""
    file_path: str
    issues: List[CodeIssue]
    metrics: Dict[str, Any]
    overall_score: float
    suggestions: List[str]

class CodeReviewAgent:
    """
    AI Agent for reviewing code and suggesting improvements.
    
    This agent analyzes code for:
    - Syntax errors
    - Logic bugs
    - Security vulnerabilities
    - Performance issues
    - Code style and best practices
    - Documentation quality
    """
    
    def __init__(self):
        self.security_patterns = [
            (r'eval\s*\(', "Avoid using eval() - potential security risk"),
            (r'exec\s*\(', "Avoid using exec() - potential security risk"),
            (r'input\s*\([^)]*\)', "Validate user input to prevent injection attacks"),
            (r'os\.system\s*\(', "Avoid os.system() - use subprocess module instead"),
            (r'pickle\.loads?\s*\(', "Pickle can execute arbitrary code - consider alternatives"),
            (r'__import__\s*\(', "Dynamic imports can be dangerous - validate input"),
        ]
        
        self.performance_patterns = [
            (r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\([^)]+\)\s*\)', "Use enumerate() instead of range(len())"),
            (r'\.append\s*\([^)]+\)\s*$', "Consider list comprehension for better performance"),
            (r'except\s*:', "Avoid bare except clauses - catch specific exceptions"),
            (r'global\s+\w+', "Minimize global variable usage"),
        ]
        
        self.style_patterns = [
            (r'print\s*\([^)]*\)', "Consider using logging instead of print statements"),
            (r'class\s+(\w+).*:', self._check_class_naming),
            (r'def\s+(\w+)\s*\(', self._check_function_naming),
        ]
    
    def review_file(self, file_path: str) -> CodeReviewResult:
        """
        Review a single code file.
        
        Args:
            file_path: Path to the code file to review
            
        Returns:
            CodeReviewResult with issues and suggestions
        """
        print(f"{Fore.BLUE}🔍 Reviewing file: {file_path}{Style.RESET_ALL}")
        
        if not os.path.exists(file_path):
            return CodeReviewResult(
                file_path=file_path,
                issues=[CodeIssue("error", 0, 0, "File not found", "file_not_found")],
                metrics={},
                overall_score=0.0,
                suggestions=[]
            )
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        metrics = self._calculate_metrics(content)
        
        # Check for syntax errors
        syntax_issues = self._check_syntax(content, file_path)
        issues.extend(syntax_issues)
        
        # Security analysis
        security_issues = self._check_security(content)
        issues.extend(security_issues)
        
        # Performance analysis
        performance_issues = self._check_performance(content)
        issues.extend(performance_issues)
        
        # Style analysis
        style_issues = self._check_style(content)
        issues.extend(style_issues)
        
        # Logic analysis
        logic_issues = self._check_logic(content)
        issues.extend(logic_issues)
        
        # Documentation analysis
        doc_issues = self._check_documentation(content)
        issues.extend(doc_issues)
        
        # Calculate overall score
        overall_score = self._calculate_score(issues, metrics)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(issues, metrics)
        
        return CodeReviewResult(
            file_path=file_path,
            issues=issues,
            metrics=metrics,
            overall_score=overall_score,
            suggestions=suggestions
        )
    
    def review_directory(self, directory_path: str) -> List[CodeReviewResult]:
        """Review all Python files in a directory."""
        results = []
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    result = self.review_file(file_path)
                    results.append(result)
        
        return results
    
    def _check_syntax(self, content: str, file_path: str) -> List[CodeIssue]:
        """Check for syntax errors using AST parsing."""
        issues = []
        
        try:
            ast.parse(content)
        except SyntaxError as e:
            issues.append(CodeIssue(
                severity="error",
                line=e.lineno or 0,
                column=e.offset or 0,
                message=f"Syntax Error: {e.msg}",
                rule="syntax_error",
                suggestion="Fix the syntax error before proceeding"
            ))
        except Exception as e:
            issues.append(CodeIssue(
                severity="error",
                line=0,
                column=0,
                message=f"Parse Error: {str(e)}",
                rule="parse_error"
            ))
        
        return issues
    
    def _check_security(self, content: str) -> List[CodeIssue]:
        """Check for security vulnerabilities."""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern, message in self.security_patterns:
                if re.search(pattern, line):
                    issues.append(CodeIssue(
                        severity="warning",
                        line=i,
                        column=0,
                        message=message,
                        rule="security_risk",
                        suggestion="Review the security implications of this code"
                    ))
        
        # Check for hardcoded credentials
        credential_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern in credential_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(CodeIssue(
                        severity="error",
                        line=i,
                        column=0,
                        message="Hardcoded credentials detected",
                        rule="hardcoded_credentials",
                        suggestion="Use environment variables or secure credential storage"
                    ))
        
        return issues
    
    def _check_performance(self, content: str) -> List[CodeIssue]:
        """Check for performance issues."""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            for pattern, message in self.performance_patterns:
                if re.search(pattern, line):
                    issues.append(CodeIssue(
                        severity="info",
                        line=i,
                        column=0,
                        message=message,
                        rule="performance_optimization",
                        suggestion="Consider the suggested optimization for better performance"
                    ))
        
        # Check for inefficient string concatenation
        if '+=' in content and 'str' in content.lower():
            string_concat_lines = [i+1 for i, line in enumerate(lines) if '+=' in line and any(quote in line for quote in ['"', "'"])]
            for line_num in string_concat_lines:
                issues.append(CodeIssue(
                    severity="info",
                    line=line_num,
                    column=0,
                    message="Consider using join() for multiple string concatenations",
                    rule="string_concatenation",
                    suggestion="Use ''.join(list) for better performance with multiple concatenations"
                ))
        
        return issues
    
    def _check_style(self, content: str) -> List[CodeIssue]:
        """Check for style and naming convention issues."""
        issues = []
        lines = content.split('\n')
        
        # Check line length
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append(CodeIssue(
                    severity="info",
                    line=i,
                    column=len(line),
                    message="Line too long (>120 characters)",
                    rule="line_length",
                    suggestion="Break long lines for better readability"
                ))
        
        # Check for proper naming conventions
        for i, line in enumerate(lines, 1):
            # Function names should be snake_case
            func_match = re.search(r'def\s+([A-Z][a-zA-Z0-9]*)\s*\(', line)
            if func_match:
                issues.append(CodeIssue(
                    severity="info",
                    line=i,
                    column=0,
                    message=f"Function '{func_match.group(1)}' should use snake_case naming",
                    rule="naming_convention",
                    suggestion="Use snake_case for function names (e.g., my_function)"
                ))
            
            # Variable names should be snake_case
            var_match = re.search(r'(\b[A-Z][a-zA-Z0-9]*)\s*=', line)
            if var_match and not re.search(r'class\s+', line):
                issues.append(CodeIssue(
                    severity="info",
                    line=i,
                    column=0,
                    message=f"Variable '{var_match.group(1)}' should use snake_case naming",
                    rule="naming_convention",
                    suggestion="Use snake_case for variable names (e.g., my_variable)"
                ))
        
        return issues
    
    def _check_logic(self, content: str) -> List[CodeIssue]:
        """Check for logical issues and potential bugs."""
        issues = []
        lines = content.split('\n')
        
        # Check for common logical issues
        for i, line in enumerate(lines, 1):
            # Comparison with None
            if re.search(r'==\s*None|!=\s*None', line):
                issues.append(CodeIssue(
                    severity="warning",
                    line=i,
                    column=0,
                    message="Use 'is None' or 'is not None' instead of '== None' or '!= None'",
                    rule="none_comparison",
                    suggestion="Use identity comparison for None"
                ))
            
            # Mutable default arguments
            if re.search(r'def\s+\w+\([^)]*=\s*\[\]', line) or re.search(r'def\s+\w+\([^)]*=\s*\{\}', line):
                issues.append(CodeIssue(
                    severity="warning",
                    line=i,
                    column=0,
                    message="Mutable default argument detected",
                    rule="mutable_default",
                    suggestion="Use None as default and create mutable object inside function"
                ))
            
            # Unreachable code after return
            if i < len(lines) and 'return' in line and not line.strip().startswith('#'):
                next_line_idx = i
                while next_line_idx < len(lines):
                    next_line = lines[next_line_idx].strip()
                    if next_line and not next_line.startswith('#') and not next_line.startswith('def') and not next_line.startswith('class'):
                        # Check indentation to see if it's at the same level
                        current_indent = len(line) - len(line.lstrip())
                        next_indent = len(lines[next_line_idx]) - len(lines[next_line_idx].lstrip())
                        if next_indent > current_indent:
                            issues.append(CodeIssue(
                                severity="warning",
                                line=next_line_idx + 1,
                                column=0,
                                message="Unreachable code after return statement",
                                rule="unreachable_code",
                                suggestion="Remove unreachable code or check logic flow"
                            ))
                        break
                    next_line_idx += 1
        
        return issues
    
    def _check_documentation(self, content: str) -> List[CodeIssue]:
        """Check documentation quality."""
        issues = []
        lines = content.split('\n')
        
        # Check for missing docstrings
        in_function = False
        function_line = 0
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Function definition
            if re.match(r'def\s+\w+', stripped):
                in_function = True
                function_line = i
                continue
            
            # Check if next non-empty line after function def is a docstring
            if in_function and stripped:
                if not stripped.startswith('"""') and not stripped.startswith("'''"):
                    issues.append(CodeIssue(
                        severity="info",
                        line=function_line,
                        column=0,
                        message="Function missing docstring",
                        rule="missing_docstring",
                        suggestion="Add docstring to document function purpose and parameters"
                    ))
                in_function = False
        
        # Check for missing module docstring
        if content.strip() and not content.strip().startswith('"""') and not content.strip().startswith("'''"):
            if not content.strip().startswith('#'):
                issues.append(CodeIssue(
                    severity="info",
                    line=1,
                    column=0,
                    message="Module missing docstring",
                    rule="missing_module_docstring",
                    suggestion="Add module-level docstring to describe the module's purpose"
                ))
        
        return issues
    
    def _calculate_metrics(self, content: str) -> Dict[str, Any]:
        """Calculate code metrics."""
        lines = content.split('\n')
        
        metrics = {
            'total_lines': len(lines),
            'code_lines': len([line for line in lines if line.strip() and not line.strip().startswith('#')]),
            'comment_lines': len([line for line in lines if line.strip().startswith('#')]),
            'blank_lines': len([line for line in lines if not line.strip()]),
            'functions': len(re.findall(r'def\s+\w+', content)),
            'classes': len(re.findall(r'class\s+\w+', content)),
            'complexity_score': self._calculate_complexity(content),
            'avg_line_length': sum(len(line) for line in lines) / len(lines) if lines else 0
        }
        
        return metrics
    
    def _calculate_complexity(self, content: str) -> float:
        """Calculate cyclomatic complexity score."""
        # Simple complexity calculation based on control structures
        complexity_keywords = ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally', 'with']
        total_complexity = 1  # Base complexity
        
        for keyword in complexity_keywords:
            total_complexity += len(re.findall(rf'\b{keyword}\b', content))
        
        # Normalize by number of functions
        function_count = len(re.findall(r'def\s+\w+', content))
        if function_count > 0:
            return total_complexity / function_count
        
        return total_complexity
    
    def _calculate_score(self, issues: List[CodeIssue], metrics: Dict[str, Any]) -> float:
        """Calculate overall code quality score (0-100)."""
        base_score = 100.0
        
        # Deduct points for issues
        for issue in issues:
            if issue.severity == "error":
                base_score -= 15
            elif issue.severity == "warning":
                base_score -= 8
            elif issue.severity == "info":
                base_score -= 3
        
        # Adjust for complexity
        complexity = metrics.get('complexity_score', 1)
        if complexity > 10:
            base_score -= (complexity - 10) * 2
        
        # Adjust for documentation
        code_lines = metrics.get('code_lines', 1)
        comment_lines = metrics.get('comment_lines', 0)
        doc_ratio = comment_lines / code_lines if code_lines > 0 else 0
        
        if doc_ratio < 0.1:  # Less than 10% comments
            base_score -= 10
        elif doc_ratio > 0.3:  # More than 30% comments
            base_score += 5
        
        return max(0.0, min(100.0, base_score))
    
    def _generate_suggestions(self, issues: List[CodeIssue], metrics: Dict[str, Any]) -> List[str]:
        """Generate improvement suggestions based on analysis."""
        suggestions = []
        
        error_count = len([i for i in issues if i.severity == "error"])
        warning_count = len([i for i in issues if i.severity == "warning"])
        
        if error_count > 0:
            suggestions.append("🚨 Fix syntax and critical errors first")
        
        if warning_count > 3:
            suggestions.append("⚠️ Address security and logic warnings to improve code safety")
        
        complexity = metrics.get('complexity_score', 1)
        if complexity > 8:
            suggestions.append("🔄 Consider refactoring complex functions to improve maintainability")
        
        doc_ratio = metrics.get('comment_lines', 0) / max(metrics.get('code_lines', 1), 1)
        if doc_ratio < 0.1:
            suggestions.append("📝 Add more documentation and comments to improve code readability")
        
        avg_line_length = metrics.get('avg_line_length', 0)
        if avg_line_length > 100:
            suggestions.append("📏 Break down long lines for better readability")
        
        function_count = metrics.get('functions', 0)
        class_count = metrics.get('classes', 0)
        if function_count == 0 and class_count == 0:
            suggestions.append("🏗️ Consider organizing code into functions and classes")
        
        if not suggestions:
            suggestions.append("✅ Code quality looks good! Consider minor style improvements")
        
        return suggestions
    
    def _check_class_naming(self, match_obj) -> str:
        """Check class naming convention."""
        class_name = match_obj.group(1) if hasattr(match_obj, 'group') else str(match_obj)
        if not class_name[0].isupper():
            return f"Class '{class_name}' should use PascalCase naming"
        return ""
    
    def _check_function_naming(self, match_obj) -> str:
        """Check function naming convention."""
        func_name = match_obj.group(1) if hasattr(match_obj, 'group') else str(match_obj)
        if any(c.isupper() for c in func_name):
            return f"Function '{func_name}' should use snake_case naming"
        return ""
    
    def print_review_summary(self, result: CodeReviewResult):
        """Print a formatted summary of the review results."""
        print(f"\n{Fore.GREEN}📊 Code Review Summary for {result.file_path}{Style.RESET_ALL}")
        print("=" * 60)
        
        # Overall score
        score_color = Fore.GREEN if result.overall_score >= 80 else Fore.YELLOW if result.overall_score >= 60 else Fore.RED
        print(f"Overall Score: {score_color}{result.overall_score:.1f}/100{Style.RESET_ALL}")
        
        # Metrics
        print(f"\n{Fore.CYAN}📈 Metrics:{Style.RESET_ALL}")
        metrics = result.metrics
        print(f"  Lines of Code: {metrics.get('code_lines', 0)}")
        print(f"  Functions: {metrics.get('functions', 0)}")
        print(f"  Classes: {metrics.get('classes', 0)}")
        print(f"  Complexity Score: {metrics.get('complexity_score', 0):.1f}")
        
        # Issues summary
        errors = [i for i in result.issues if i.severity == "error"]
        warnings = [i for i in result.issues if i.severity == "warning"]
        infos = [i for i in result.issues if i.severity == "info"]
        
        print(f"\n{Fore.CYAN}🔍 Issues Found:{Style.RESET_ALL}")
        print(f"  {Fore.RED}Errors: {len(errors)}{Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}Warnings: {len(warnings)}{Style.RESET_ALL}")
        print(f"  {Fore.BLUE}Info/Style: {len(infos)}{Style.RESET_ALL}")
        
        # Detailed issues
        if result.issues:
            print(f"\n{Fore.CYAN}📋 Detailed Issues:{Style.RESET_ALL}")
            for issue in result.issues[:10]:  # Show first 10 issues
                severity_color = {
                    "error": Fore.RED,
                    "warning": Fore.YELLOW,
                    "info": Fore.BLUE
                }.get(issue.severity, Fore.WHITE)
                
                print(f"  {severity_color}[{issue.severity.upper()}]{Style.RESET_ALL} Line {issue.line}: {issue.message}")
                if issue.suggestion:
                    print(f"    💡 {issue.suggestion}")
        
        # Suggestions
        if result.suggestions:
            print(f"\n{Fore.CYAN}💡 Improvement Suggestions:{Style.RESET_ALL}")
            for suggestion in result.suggestions:
                print(f"  {suggestion}")

def main():
    """Demo function for the Code Review Agent."""
    print(f"{Fore.GREEN}🔍 AI Code Review Agent Demo{Style.RESET_ALL}")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        # Use current directory if no argument provided
        target_path = "."
    
    agent = CodeReviewAgent()
    
    if os.path.isfile(target_path):
        # Review single file
        result = agent.review_file(target_path)
        agent.print_review_summary(result)
    elif os.path.isdir(target_path):
        # Review all Python files in directory
        results = agent.review_directory(target_path)
        
        if not results:
            print(f"{Fore.YELLOW}No Python files found in {target_path}{Style.RESET_ALL}")
            return
        
        total_score = sum(r.overall_score for r in results) / len(results)
        total_issues = sum(len(r.issues) for r in results)
        
        print(f"\n{Fore.GREEN}📊 Directory Review Summary{Style.RESET_ALL}")
        print(f"Files reviewed: {len(results)}")
        print(f"Average score: {total_score:.1f}/100")
        print(f"Total issues: {total_issues}")
        
        print(f"\n{Fore.CYAN}Individual File Results:{Style.RESET_ALL}")
        for result in results:
            score_emoji = "🟢" if result.overall_score >= 80 else "🟡" if result.overall_score >= 60 else "🔴"
            print(f"  {score_emoji} {result.file_path}: {result.overall_score:.1f}/100 ({len(result.issues)} issues)")
    else:
        print(f"{Fore.RED}Error: {target_path} is not a valid file or directory{Style.RESET_ALL}")

if __name__ == "__main__":
    main()