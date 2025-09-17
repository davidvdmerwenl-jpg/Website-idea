#!/usr/bin/env python3
"""
AI Code Agent System - Main Demo
Demonstrates both code generation and code review capabilities.
"""

import os
import sys
import tempfile
from pathlib import Path
from colorama import init, Fore, Style

# Import our agents
from code_generator import CodeGenerationAgent, CodeGenerationRequest
from code_reviewer import CodeReviewAgent

init()  # Initialize colorama

def create_demo_directory():
    """Create a temporary directory for demo files."""
    demo_dir = Path("demo_outputs")
    demo_dir.mkdir(exist_ok=True)
    return demo_dir

def demo_code_generation():
    """Demonstrate the code generation capabilities."""
    print(f"\n{Fore.GREEN}🚀 CODE GENERATION AGENT DEMO{Style.RESET_ALL}")
    print("=" * 60)
    
    agent = CodeGenerationAgent()
    demo_dir = create_demo_directory()
    
    # Demo scenarios
    scenarios = [
        {
            "name": "Fibonacci Function",
            "request": CodeGenerationRequest(
                prompt="Create a Python function to calculate fibonacci numbers with optimization",
                language="python",
                include_tests=True,
                include_docs=True
            ),
            "filename": "fibonacci_example.py"
        },
        {
            "name": "User Management Class",
            "request": CodeGenerationRequest(
                prompt="Create a User class with authentication and profile management",
                language="python",
                complexity="medium"
            ),
            "filename": "user_management.py"
        },
        {
            "name": "REST API Server",
            "request": CodeGenerationRequest(
                prompt="Create a REST API with CRUD operations for a task management system",
                language="python",
                framework="fastapi"
            ),
            "filename": "task_api.py"
        },
        {
            "name": "Sorting Algorithms",
            "request": CodeGenerationRequest(
                prompt="Implement quicksort and mergesort algorithms with performance comparison",
                language="python",
                complexity="medium"
            ),
            "filename": "sorting_algorithms.py"
        }
    ]
    
    generated_files = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{Fore.CYAN}📝 Scenario {i}: {scenario['name']}{Style.RESET_ALL}")
        print(f"Prompt: \"{scenario['request'].prompt}\"")
        
        result = agent.generate_code(scenario["request"])
        
        # Save generated code to file
        file_path = demo_dir / scenario["filename"]
        with open(file_path, 'w') as f:
            f.write(result["code"])
        
        generated_files.append(str(file_path))
        
        print(f"{Fore.GREEN}✅ Generated code saved to: {file_path}{Style.RESET_ALL}")
        print(f"📊 Generated {len(result['code'].split())} lines")
        
        # Show a snippet of the generated code
        code_lines = result["code"].split('\n')
        preview_lines = code_lines[:10]
        print(f"\n{Fore.YELLOW}Preview:{Style.RESET_ALL}")
        for line in preview_lines:
            print(f"  {line}")
        if len(code_lines) > 10:
            print(f"  ... ({len(code_lines) - 10} more lines)")
        
        print(f"\n{Fore.BLUE}Explanation:{Style.RESET_ALL}")
        explanation_lines = result["explanation"].split('\n')[:5]
        for line in explanation_lines:
            if line.strip():
                print(f"  {line}")
        
        print("-" * 40)
    
    return generated_files

def demo_code_review(files_to_review):
    """Demonstrate the code review capabilities."""
    print(f"\n{Fore.GREEN}🔍 CODE REVIEW AGENT DEMO{Style.RESET_ALL}")
    print("=" * 60)
    
    agent = CodeReviewAgent()
    
    all_results = []
    
    for file_path in files_to_review:
        print(f"\n{Fore.CYAN}🔍 Reviewing: {file_path}{Style.RESET_ALL}")
        
        result = agent.review_file(file_path)
        all_results.append(result)
        
        # Print summary for each file
        agent.print_review_summary(result)
        print("-" * 40)
    
    # Overall summary
    if all_results:
        print(f"\n{Fore.GREEN}📈 OVERALL REVIEW SUMMARY{Style.RESET_ALL}")
        print("=" * 60)
        
        total_files = len(all_results)
        avg_score = sum(r.overall_score for r in all_results) / total_files
        total_issues = sum(len(r.issues) for r in all_results)
        
        score_color = Fore.GREEN if avg_score >= 80 else Fore.YELLOW if avg_score >= 60 else Fore.RED
        
        print(f"Files Reviewed: {total_files}")
        print(f"Average Quality Score: {score_color}{avg_score:.1f}/100{Style.RESET_ALL}")
        print(f"Total Issues Found: {total_issues}")
        
        # Best and worst files
        best_file = max(all_results, key=lambda x: x.overall_score)
        worst_file = min(all_results, key=lambda x: x.overall_score)
        
        print(f"\n{Fore.GREEN}🏆 Best File: {best_file.file_path} ({best_file.overall_score:.1f}/100){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⚠️ Needs Attention: {worst_file.file_path} ({worst_file.overall_score:.1f}/100){Style.RESET_ALL}")

def create_example_buggy_code():
    """Create an example file with common issues for review demonstration."""
    demo_dir = create_demo_directory()
    buggy_file = demo_dir / "buggy_example.py"
    
    buggy_code = '''# This file contains intentional bugs and issues for demonstration

import os

def BadFunctionName(password="default123"):
    print("Starting function")
    if password == None:
        return False
    eval("print('This is dangerous')")
    result = ""
    for i in range(100):
        result += str(i)
    print("Function completed")
    return True

class badClassName:
    def __init__(self, data=[]):
        self.data = data
        self.API_KEY = "sk-1234567890abcdef"
    
    def process_data(self):
        return self.data

def long_line_function():
    this_is_a_very_long_line_that_exceeds_the_recommended_length_and_should_be_broken_down_for_better_readability_and_maintenance
    
def unreachable_example():
    return "done"
    print("This will never execute")
    x = 1
'''
    
    with open(buggy_file, 'w') as f:
        f.write(buggy_code)
    
    return str(buggy_file)

def interactive_demo():
    """Interactive demo allowing users to input custom prompts."""
    print(f"\n{Fore.GREEN}🎯 INTERACTIVE DEMO{Style.RESET_ALL}")
    print("=" * 60)
    print("Enter a custom prompt for code generation, or 'quit' to exit")
    
    agent = CodeGenerationAgent()
    reviewer = CodeReviewAgent()
    demo_dir = create_demo_directory()
    
    while True:
        print(f"\n{Fore.CYAN}Enter your code generation prompt:{Style.RESET_ALL}")
        prompt = input("> ").strip()
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            break
        
        if not prompt:
            continue
        
        # Get additional parameters
        print(f"{Fore.CYAN}Language (default: python):{Style.RESET_ALL}")
        language = input("> ").strip() or "python"
        
        print(f"{Fore.CYAN}Include tests? (y/n, default: n):{Style.RESET_ALL}")
        include_tests = input("> ").strip().lower() == 'y'
        
        # Generate code
        request = CodeGenerationRequest(
            prompt=prompt,
            language=language,
            include_tests=include_tests
        )
        
        result = agent.generate_code(request)
        
        # Save to file
        filename = f"interactive_{prompt.replace(' ', '_')[:20]}.{agent.supported_languages[language]['extension'][1:]}"
        file_path = demo_dir / filename
        
        with open(file_path, 'w') as f:
            f.write(result["code"])
        
        print(f"\n{Fore.GREEN}✅ Code generated and saved to: {file_path}{Style.RESET_ALL}")
        
        # Show preview
        print(f"\n{Fore.YELLOW}Generated Code Preview:{Style.RESET_ALL}")
        print("-" * 40)
        print(result["code"][:500] + "..." if len(result["code"]) > 500 else result["code"])
        print("-" * 40)
        
        # Ask if user wants to review the generated code
        print(f"\n{Fore.CYAN}Review the generated code? (y/n):{Style.RESET_ALL}")
        if input("> ").strip().lower() == 'y':
            review_result = reviewer.review_file(str(file_path))
            reviewer.print_review_summary(review_result)

def show_help():
    """Display help information about the system."""
    print(f"\n{Fore.GREEN}🤖 AI CODE AGENT SYSTEM HELP{Style.RESET_ALL}")
    print("=" * 60)
    
    print(f"\n{Fore.CYAN}Available Commands:{Style.RESET_ALL}")
    print("  python main.py demo           - Run full demonstration")
    print("  python main.py generate       - Code generation demo only")
    print("  python main.py review         - Code review demo only")
    print("  python main.py interactive    - Interactive mode")
    print("  python main.py help           - Show this help")
    
    print(f"\n{Fore.CYAN}Individual Agent Usage:{Style.RESET_ALL}")
    print("  python code_generator.py      - Run code generator demo")
    print("  python code_reviewer.py <file/dir> - Review specific file or directory")
    
    print(f"\n{Fore.CYAN}Features:{Style.RESET_ALL}")
    print("  ✨ Code Generation from natural language prompts")
    print("  🔍 Comprehensive code review and analysis")
    print("  🛡️ Security vulnerability detection")
    print("  ⚡ Performance optimization suggestions")
    print("  📝 Documentation and style checking")
    print("  🎯 Multi-language support")
    
    print(f"\n{Fore.CYAN}Example Prompts for Code Generation:{Style.RESET_ALL}")
    print("  • 'Create a Python function to sort a list of dictionaries'")
    print("  • 'Build a REST API for user authentication'")
    print("  • 'Implement a binary search tree class'")
    print("  • 'Create a web scraper for news articles'")
    print("  • 'Generate a machine learning model for classification'")

def main():
    """Main function to run the AI Code Agent System demo."""
    
    print(f"{Fore.GREEN}🤖 AI CODE AGENT SYSTEM{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Demonstrating AI-powered code generation and review{Style.RESET_ALL}")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        command = "demo"
    else:
        command = sys.argv[1].lower()
    
    try:
        if command == "demo":
            # Full demonstration
            print(f"{Fore.YELLOW}🎬 Running full system demonstration...{Style.RESET_ALL}")
            
            # 1. Generate code examples
            generated_files = demo_code_generation()
            
            # 2. Create buggy example for review
            buggy_file = create_example_buggy_code()
            all_files = generated_files + [buggy_file]
            
            # 3. Review all generated code
            demo_code_review(all_files)
            
            print(f"\n{Fore.GREEN}🎉 Demo completed! Check the 'demo_outputs' directory for generated files.{Style.RESET_ALL}")
            
        elif command == "generate":
            # Code generation only
            demo_code_generation()
            
        elif command == "review":
            # Code review only
            demo_dir = create_demo_directory()
            buggy_file = create_example_buggy_code()
            
            # Also review our own agents
            files_to_review = [
                "code_generator.py",
                "code_reviewer.py",
                buggy_file
            ]
            
            demo_code_review(files_to_review)
            
        elif command == "interactive":
            # Interactive mode
            interactive_demo()
            
        elif command == "help":
            # Show help
            show_help()
            
        else:
            print(f"{Fore.RED}Unknown command: {command}{Style.RESET_ALL}")
            show_help()
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Demo interrupted by user.{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error during demo: {str(e)}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()