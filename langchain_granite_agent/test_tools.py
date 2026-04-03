#!/usr/bin/env python3
"""
Test script for individual tools
Tests each tool independently before running the full agent
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from tools.calculator import CalculatorTool
from tools.file_operations import FileOperationsTool
from tools.web_search import WebSearchTool


def print_test_header(title: str):
    """Print a formatted test header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_calculator():
    """Test the calculator tool"""
    print_test_header("Testing Calculator Tool")
    
    calc = CalculatorTool()
    
    test_cases = [
        ("2 + 2", "4"),
        ("10 * 5", "50"),
        ("sqrt(16)", "4"),
        ("15 * 0.15", "2.25"),
        ("(100 + 50) / 2", "75"),
    ]
    
    passed = 0
    failed = 0
    
    for expression, expected in test_cases:
        result = calc._run(expression)
        success = expected in result or result == expected
        status = "✓" if success else "✗"
        
        if success:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} {expression:20} = {result:15} (expected: {expected})")
    
    print(f"\nCalculator Tests: {passed} passed, {failed} failed")
    return failed == 0


def test_file_operations():
    """Test the file operations tool"""
    print_test_header("Testing File Operations Tool")
    
    file_ops = FileOperationsTool(workspace_dir="test_workspace")
    
    # Test write
    print("\n1. Testing file write...")
    result = file_ops._run("write: test_file.txt | This is a test file content")
    print(f"   {result}")
    success1 = "Successfully" in result
    
    # Test read
    print("\n2. Testing file read...")
    result = file_ops._run("read: test_file.txt")
    print(f"   {result[:100]}...")
    success2 = "This is a test file content" in result
    
    # Test list
    print("\n3. Testing file list...")
    result = file_ops._run("list")
    print(f"   {result}")
    success3 = "test_file.txt" in result
    
    # Test delete
    print("\n4. Testing file delete...")
    result = file_ops._run("delete: test_file.txt")
    print(f"   {result}")
    success4 = "Successfully deleted" in result
    
    all_passed = all([success1, success2, success3, success4])
    status = "✓ All tests passed" if all_passed else "✗ Some tests failed"
    print(f"\nFile Operations Tests: {status}")
    
    return all_passed


def test_web_search():
    """Test the web search tool"""
    print_test_header("Testing Web Search Tool")
    
    try:
        from duckduckgo_search import DDGS
        print("✓ DuckDuckGo search library is installed")
    except ImportError:
        print("✗ DuckDuckGo search library not installed")
        print("  Install with: pip install duckduckgo-search")
        return False
    
    search = WebSearchTool(max_results=2)
    
    print("\nSearching for 'Python programming language'...")
    result = search._run("Python programming language")
    
    if "Error" in result or "not installed" in result:
        print(f"✗ Search failed: {result[:200]}")
        return False
    else:
        print(f"✓ Search successful")
        print(f"  Results preview: {result[:200]}...")
        return True


def main():
    """Run all tool tests"""
    print("=" * 70)
    print("  LangChain ReAct Agent - Tool Tests")
    print("=" * 70)
    
    results = {
        "Calculator": test_calculator(),
        "File Operations": test_file_operations(),
        "Web Search": test_web_search(),
    }
    
    print_test_header("Test Summary")
    
    for tool, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{tool:20} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ All tools are working correctly!")
        print("\nYou can now run the full agent:")
        print("  python langchain_react_agent.py")
        print("  or")
        print("  ./run_agent.sh")
    else:
        print("✗ Some tools failed. Please check the errors above.")
        print("\nMake sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

# Made with Bob