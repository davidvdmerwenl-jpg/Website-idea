#!/usr/bin/env python3
"""
AI Code Generation Agent
Generates code based on natural language prompts using AI capabilities.
"""

import json
import re
import sys
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from colorama import init, Fore, Style

init()  # Initialize colorama for colored output

@dataclass
class CodeGenerationRequest:
    """Represents a code generation request with context."""
    prompt: str
    language: str = "python"
    framework: Optional[str] = None
    complexity: str = "medium"  # simple, medium, complex
    include_tests: bool = False
    include_docs: bool = True

class CodeGenerationAgent:
    """
    AI Agent for generating code based on natural language prompts.
    
    This agent simulates AI-powered code generation by using templates
    and intelligent parsing of user requirements.
    """
    
    def __init__(self):
        self.supported_languages = {
            "python": {"extension": ".py", "comment": "#"},
            "javascript": {"extension": ".js", "comment": "//"},
            "java": {"extension": ".java", "comment": "//"},
            "cpp": {"extension": ".cpp", "comment": "//"},
            "html": {"extension": ".html", "comment": "<!--"},
            "css": {"extension": ".css", "comment": "/*"}
        }
        
    def generate_code(self, request: CodeGenerationRequest) -> Dict[str, str]:
        """
        Generate code based on the provided request.
        
        Args:
            request: CodeGenerationRequest object with prompt and settings
            
        Returns:
            Dictionary containing generated code, explanation, and metadata
        """
        print(f"{Fore.BLUE}🤖 Generating code for: {request.prompt}{Style.RESET_ALL}")
        
        # Analyze the prompt to understand requirements
        analysis = self._analyze_prompt(request.prompt)
        
        # Generate code based on analysis
        code = self._generate_code_for_task(analysis, request)
        
        # Generate explanation
        explanation = self._generate_explanation(analysis, code, request)
        
        # Generate tests if requested
        tests = ""
        if request.include_tests:
            tests = self._generate_tests(analysis, code, request)
        
        return {
            "code": code,
            "explanation": explanation,
            "tests": tests,
            "language": request.language,
            "analysis": analysis
        }
    
    def _analyze_prompt(self, prompt: str) -> Dict[str, any]:
        """Analyze the prompt to extract requirements and intent."""
        analysis = {
            "intent": "general",
            "entities": [],
            "complexity": "medium",
            "requirements": []
        }
        
        prompt_lower = prompt.lower()
        
        # Detect intent
        if any(word in prompt_lower for word in ["function", "method", "def"]):
            analysis["intent"] = "function_creation"
        elif any(word in prompt_lower for word in ["class", "object", "oop"]):
            analysis["intent"] = "class_creation"
        elif any(word in prompt_lower for word in ["api", "endpoint", "server"]):
            analysis["intent"] = "api_creation"
        elif any(word in prompt_lower for word in ["algorithm", "sort", "search"]):
            analysis["intent"] = "algorithm_implementation"
        elif any(word in prompt_lower for word in ["web", "html", "css", "frontend"]):
            analysis["intent"] = "web_development"
        
        # Extract entities (functions, algorithms, etc.)
        entities = re.findall(r'\b(?:fibonacci|factorial|prime|sort|search|login|user|database)\b', prompt_lower)
        analysis["entities"] = list(set(entities))
        
        # Detect complexity
        if any(word in prompt_lower for word in ["simple", "basic", "easy"]):
            analysis["complexity"] = "simple"
        elif any(word in prompt_lower for word in ["complex", "advanced", "sophisticated"]):
            analysis["complexity"] = "complex"
        
        return analysis
    
    def _generate_code_for_task(self, analysis: Dict, request: CodeGenerationRequest) -> str:
        """Generate code based on analysis and request."""
        
        if analysis["intent"] == "function_creation":
            return self._generate_function_code(analysis, request)
        elif analysis["intent"] == "class_creation":
            return self._generate_class_code(analysis, request)
        elif analysis["intent"] == "algorithm_implementation":
            return self._generate_algorithm_code(analysis, request)
        elif analysis["intent"] == "web_development":
            return self._generate_web_code(analysis, request)
        elif analysis["intent"] == "api_creation":
            return self._generate_api_code(analysis, request)
        else:
            return self._generate_general_code(analysis, request)
    
    def _generate_function_code(self, analysis: Dict, request: CodeGenerationRequest) -> str:
        """Generate function-based code."""
        if "fibonacci" in analysis["entities"]:
            if request.language == "python":
                return '''def fibonacci(n):
    """
    Calculate the nth Fibonacci number.
    
    Args:
        n (int): The position in the Fibonacci sequence
        
    Returns:
        int: The nth Fibonacci number
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def fibonacci_optimized(n):
    """Optimized version using memoization."""
    memo = {}
    
    def fib_helper(num):
        if num in memo:
            return memo[num]
        if num <= 0:
            return 0
        elif num == 1:
            return 1
        else:
            memo[num] = fib_helper(num-1) + fib_helper(num-2)
            return memo[num]
    
    return fib_helper(n)

# Example usage
if __name__ == "__main__":
    for i in range(10):
        print(f"F({i}) = {fibonacci_optimized(i)}")'''
        
        elif "factorial" in analysis["entities"]:
            if request.language == "python":
                return '''def factorial(n):
    """
    Calculate the factorial of a number.
    
    Args:
        n (int): Non-negative integer
        
    Returns:
        int: n! (factorial of n)
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def factorial_iterative(n):
    """Iterative version of factorial calculation."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Example usage
if __name__ == "__main__":
    test_values = [0, 1, 5, 10]
    for val in test_values:
        print(f"{val}! = {factorial_iterative(val)}")'''
        
        # Default function template
        return '''def process_data(data):
    """
    Process the input data according to requirements.
    
    Args:
        data: Input data to process
        
    Returns:
        Processed data
    """
    # Implementation based on specific requirements
    processed = data
    return processed'''
    
    def _generate_class_code(self, analysis: Dict, request: CodeGenerationRequest) -> str:
        """Generate class-based code."""
        if "user" in analysis["entities"]:
            return '''class User:
    """
    Represents a user in the system.
    """
    
    def __init__(self, username, email, user_id=None):
        """
        Initialize a new User.
        
        Args:
            username (str): User's username
            email (str): User's email address
            user_id (int, optional): Unique user identifier
        """
        self.username = username
        self.email = email
        self.user_id = user_id
        self.is_active = True
        self.created_at = None
    
    def activate(self):
        """Activate the user account."""
        self.is_active = True
    
    def deactivate(self):
        """Deactivate the user account."""
        self.is_active = False
    
    def update_email(self, new_email):
        """Update user's email address."""
        self.email = new_email
    
    def __str__(self):
        return f"User(username='{self.username}', email='{self.email}')"
    
    def __repr__(self):
        return self.__str__()

# Example usage
if __name__ == "__main__":
    user = User("john_doe", "john@example.com")
    print(user)
    user.update_email("john.doe@newdomain.com")
    print(f"Updated user: {user}")'''
        
        # Default class template
        return '''class DataProcessor:
    """
    A class for processing data according to specific requirements.
    """
    
    def __init__(self, config=None):
        """
        Initialize the DataProcessor.
        
        Args:
            config (dict, optional): Configuration parameters
        """
        self.config = config or {}
        
    def process(self, data):
        """Process the input data."""
        # Implementation details go here
        return data'''
    
    def _generate_algorithm_code(self, analysis: Dict, request: CodeGenerationRequest) -> str:
        """Generate algorithm implementations."""
        if "sort" in analysis["entities"]:
            return '''def quick_sort(arr):
    """
    Implementation of QuickSort algorithm.
    
    Args:
        arr (list): List to be sorted
        
    Returns:
        list: Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr):
    """
    Implementation of MergeSort algorithm.
    
    Args:
        arr (list): List to be sorted
        
    Returns:
        list: Sorted list
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    """Helper function for merge_sort."""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Example usage
if __name__ == "__main__":
    test_array = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original array: {test_array}")
    print(f"Quick sorted: {quick_sort(test_array.copy())}")
    print(f"Merge sorted: {merge_sort(test_array.copy())}")'''
        
        elif "search" in analysis["entities"]:
            return '''def binary_search(arr, target):
    """
    Binary search implementation for sorted arrays.
    
    Args:
        arr (list): Sorted list to search in
        target: Value to search for
        
    Returns:
        int: Index of target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

def linear_search(arr, target):
    """
    Linear search implementation.
    
    Args:
        arr (list): List to search in
        target: Value to search for
        
    Returns:
        int: Index of target if found, -1 otherwise
    """
    for i, item in enumerate(arr):
        if item == target:
            return i
    return -1

# Example usage
if __name__ == "__main__":
    sorted_array = [1, 3, 5, 7, 9, 11, 13, 15]
    target = 7
    
    print(f"Array: {sorted_array}")
    print(f"Searching for: {target}")
    print(f"Binary search result: {binary_search(sorted_array, target)}")
    print(f"Linear search result: {linear_search(sorted_array, target)}")'''
        
        # Default algorithm template
        return '''def algorithm_implementation(data):
    """
    Implementation of a custom algorithm.
    
    Args:
        data: Input data for the algorithm
        
    Returns:
        Processed result
    """
    # Algorithm implementation goes here
    result = data
    return result'''
    
    def _generate_web_code(self, analysis: Dict, request: CodeGenerationRequest) -> str:
        """Generate web development code."""
        if request.language == "html":
            return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Generated Web Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .feature {
            margin: 20px 0;
            padding: 15px;
            border-left: 4px solid #007bff;
            background-color: #f8f9fa;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI-Generated Website</h1>
            <p>This page was created by an AI code generation agent</p>
        </div>
        
        <div class="feature">
            <h3>Feature 1: Dynamic Content</h3>
            <p>Content can be dynamically generated based on user requirements.</p>
        </div>
        
        <div class="feature">
            <h3>Feature 2: Responsive Design</h3>
            <p>The layout adapts to different screen sizes automatically.</p>
        </div>
        
        <div class="feature">
            <h3>Feature 3: Interactive Elements</h3>
            <button onclick="showMessage()">Click Me!</button>
        </div>
    </div>
    
    <script>
        function showMessage() {
            alert('Hello from AI-generated JavaScript!');
        }
    </script>
</body>
</html>'''
        else:
            return '''from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    """Home page route."""
    return render_template('index.html')

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    """API endpoint for data handling."""
    if request.method == 'POST':
        data = request.get_json()
        # Process the data
        processed_data = {"status": "success", "data": data}
        return jsonify(processed_data)
    else:
        # Return sample data
        return jsonify({"message": "Hello from AI-generated API!"})

@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    """Get user by ID."""
    # Simulate user data
    user_data = {
        "id": user_id,
        "name": f"User {user_id}",
        "email": f"user{user_id}@example.com"
    }
    return jsonify(user_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)'''
    
    def _generate_api_code(self, analysis: Dict, request: CodeGenerationRequest) -> str:
        """Generate API-related code."""
        return '''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="AI Generated API", version="1.0.0")

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float

# In-memory storage for demo
items_db = []

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the AI-generated API!"}

@app.get("/items", response_model=List[Item])
async def get_items():
    """Get all items."""
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get item by ID."""
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    """Create a new item."""
    item.id = len(items_db) + 1
    items_db.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    """Update an existing item."""
    for i, item in enumerate(items_db):
        if item.id == item_id:
            updated_item.id = item_id
            items_db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item."""
    for i, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[i]
            return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)'''
    
    def _generate_general_code(self, analysis: Dict, request: CodeGenerationRequest) -> str:
        """Generate general-purpose code."""
        return '''#!/usr/bin/env python3
"""
AI-Generated Code Module

This module was generated based on the user's requirements.
"""

def main():
    """
    Main function to demonstrate the generated functionality.
    """
    print("AI-Generated Code Execution Started")
    
    # Implementation based on user requirements
    result = process_requirements()
    
    print(f"Processing completed. Result: {result}")
    return result

def process_requirements():
    """
    Process the specific requirements from the user prompt.
    
    Returns:
        Any: The result of processing
    """
    # This function would be customized based on the actual prompt
    return "Requirements processed successfully"

if __name__ == "__main__":
    main()'''
    
    def _generate_explanation(self, analysis: Dict, code: str, request: CodeGenerationRequest) -> str:
        """Generate explanation for the generated code."""
        explanation = f"""
## Code Explanation

### Intent: {analysis['intent'].replace('_', ' ').title()}
The generated code addresses your requirement: "{request.prompt}"

### Key Features:
"""
        
        if analysis["entities"]:
            explanation += f"- Implements: {', '.join(analysis['entities'])}\n"
        
        explanation += f"""- Language: {request.language.title()}
- Complexity: {analysis['complexity'].title()}
- Includes documentation and examples

### Code Structure:
"""
        
        if "def " in code:
            functions = re.findall(r'def (\w+)\(', code)
            if functions:
                explanation += f"- Functions: {', '.join(functions)}\n"
        
        if "class " in code:
            classes = re.findall(r'class (\w+)', code)
            if classes:
                explanation += f"- Classes: {', '.join(classes)}\n"
        
        explanation += f"""
### Usage:
1. Save the code to a {self.supported_languages[request.language]['extension']} file
2. Install any required dependencies
3. Run the code directly or import as a module

### Next Steps:
- Customize the implementation for your specific use case
- Add error handling and validation as needed
- Consider performance optimizations for production use
"""
        
        return explanation
    
    def _generate_tests(self, analysis: Dict, code: str, request: CodeGenerationRequest) -> str:
        """Generate test cases for the generated code."""
        if request.language == "python":
            return '''import unittest
from unittest.mock import patch, MagicMock

class TestGeneratedCode(unittest.TestCase):
    """Test cases for the AI-generated code."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def test_basic_functionality(self):
        """Test basic functionality of the generated code."""
        # Add specific test cases based on the generated code
        self.assertTrue(True)  # Placeholder test
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Add edge case tests
        self.assertTrue(True)  # Placeholder test
    
    def test_error_handling(self):
        """Test error handling capabilities."""
        # Add error handling tests
        self.assertTrue(True)  # Placeholder test

if __name__ == "__main__":
    unittest.main()'''
        else:
            return "# Test cases would be generated based on the target language and framework"

def main():
    """Demo function for the Code Generation Agent."""
    print(f"{Fore.GREEN}🚀 AI Code Generation Agent Demo{Style.RESET_ALL}")
    print("=" * 50)
    
    # Example usage
    agent = CodeGenerationAgent()
    
    # Example 1: Fibonacci function
    request1 = CodeGenerationRequest(
        prompt="Create a Python function to calculate fibonacci numbers",
        language="python",
        include_tests=True
    )
    
    result1 = agent.generate_code(request1)
    print(f"{Fore.YELLOW}Generated Code:{Style.RESET_ALL}")
    print(result1["code"])
    print(f"\n{Fore.CYAN}Explanation:{Style.RESET_ALL}")
    print(result1["explanation"])
    
    print("\n" + "=" * 50)
    
    # Example 2: Web API
    request2 = CodeGenerationRequest(
        prompt="Create a REST API with user management endpoints",
        language="python",
        framework="fastapi"
    )
    
    result2 = agent.generate_code(request2)
    print(f"{Fore.YELLOW}Generated API Code:{Style.RESET_ALL}")
    print(result2["code"][:500] + "..." if len(result2["code"]) > 500 else result2["code"])

if __name__ == "__main__":
    main()