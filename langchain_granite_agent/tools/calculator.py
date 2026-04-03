#!/usr/bin/env python3
"""
Calculator Tool for LangChain ReAct Agent
Provides mathematical operations and expression evaluation
"""

import math
import re
from typing import Optional
from langchain.tools import BaseTool
from pydantic import Field


class CalculatorTool(BaseTool):
    """Tool for performing mathematical calculations"""
    
    name: str = "calculator"
    description: str = """Useful for performing mathematical calculations and evaluating expressions.
    Input should be a valid mathematical expression as a string.
    Supports:
    - Basic operations: +, -, *, /, //, %, **
    - Functions: sqrt, sin, cos, tan, log, log10, exp, abs
    - Constants: pi, e
    Examples:
    - "2 + 2"
    - "sqrt(16)"
    - "sin(pi/2)"
    - "15 * 0.15"
    - "(100 + 50) / 2"
    """
    
    def _run(self, query: str) -> str:
        """
        Execute the calculator tool
        
        Args:
            query: Mathematical expression to evaluate
            
        Returns:
            Result of the calculation or error message
        """
        try:
            # Clean the input
            query = query.strip()
            
            # Create a safe namespace with math functions
            safe_dict = {
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log,
                'log10': math.log10,
                'exp': math.exp,
                'abs': abs,
                'pi': math.pi,
                'e': math.e,
                'pow': pow,
                'round': round,
            }
            
            # Check for dangerous operations
            dangerous_patterns = [
                r'__',  # Dunder methods
                r'import',  # Import statements
                r'exec',  # Code execution
                r'eval',  # Nested eval
                r'open',  # File operations
                r'compile',  # Code compilation
            ]
            
            for pattern in dangerous_patterns:
                if re.search(pattern, query, re.IGNORECASE):
                    return f"Error: Expression contains forbidden operation: {pattern}"
            
            # Evaluate the expression
            result = eval(query, {"__builtins__": {}}, safe_dict)
            
            # Format the result
            if isinstance(result, float):
                # Round to reasonable precision
                if result.is_integer():
                    return str(int(result))
                else:
                    return f"{result:.6f}".rstrip('0').rstrip('.')
            else:
                return str(result)
                
        except ZeroDivisionError:
            return "Error: Division by zero"
        except ValueError as e:
            return f"Error: Invalid value - {str(e)}"
        except SyntaxError as e:
            return f"Error: Invalid syntax - {str(e)}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def _arun(self, query: str) -> str:
        """Async version of _run"""
        return self._run(query)


# Example usage and testing
if __name__ == "__main__":
    calc = CalculatorTool()
    
    # Test cases
    test_cases = [
        "2 + 2",
        "10 * 5",
        "100 / 4",
        "sqrt(16)",
        "sin(pi/2)",
        "15 * 0.15",
        "(100 + 50) / 2",
        "2 ** 8",
        "log10(100)",
        "abs(-42)",
    ]
    
    print("Calculator Tool Test Cases:")
    print("=" * 50)
    for test in test_cases:
        result = calc._run(test)
        print(f"{test:20} = {result}")

# Made with Bob
