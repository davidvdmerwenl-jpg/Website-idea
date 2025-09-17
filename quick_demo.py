#!/usr/bin/env python3
"""
Quick Demo Script - Shows the basic capabilities of both agents
"""

from code_generator import CodeGenerationAgent, CodeGenerationRequest
from code_reviewer import CodeReviewAgent
from colorama import init, Fore, Style
import tempfile
import os

init()

def quick_demo():
    """Run a quick demonstration of both agents."""
    print(f"{Fore.GREEN}🚀 AI Code Agent System - Quick Demo{Style.RESET_ALL}")
    print("=" * 50)
    
    # Step 1: Generate some code
    print(f"\n{Fore.BLUE}Step 1: Code Generation{Style.RESET_ALL}")
    print("Prompt: 'Create a function to check if a number is prime'")
    
    generator = CodeGenerationAgent()
    request = CodeGenerationRequest(
        prompt="Create a function to check if a number is prime",
        language="python",
        include_docs=True
    )
    
    result = generator.generate_code(request)
    
    # Save generated code to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(result["code"])
        temp_file = f.name
    
    print(f"{Fore.GREEN}✅ Code generated successfully!{Style.RESET_ALL}")
    print("\nGenerated code:")
    print("-" * 30)
    print(result["code"][:300] + "..." if len(result["code"]) > 300 else result["code"])
    print("-" * 30)
    
    # Step 2: Review the generated code
    print(f"\n{Fore.BLUE}Step 2: Code Review{Style.RESET_ALL}")
    print("Analyzing the generated code for quality and issues...")
    
    reviewer = CodeReviewAgent()
    review_result = reviewer.review_file(temp_file)
    
    print(f"\n{Fore.GREEN}📊 Review Results:{Style.RESET_ALL}")
    print(f"Overall Score: {review_result.overall_score:.1f}/100")
    print(f"Issues Found: {len(review_result.issues)}")
    
    if review_result.issues:
        print("\nTop Issues:")
        for issue in review_result.issues[:3]:
            print(f"  • {issue.severity}: {issue.message}")
    
    if review_result.suggestions:
        print(f"\n{Fore.CYAN}💡 Suggestions:{Style.RESET_ALL}")
        for suggestion in review_result.suggestions[:2]:
            print(f"  • {suggestion}")
    
    # Cleanup
    os.unlink(temp_file)
    
    print(f"\n{Fore.GREEN}🎉 Demo completed! Run 'python main.py demo' for the full experience.{Style.RESET_ALL}")

if __name__ == "__main__":
    quick_demo()