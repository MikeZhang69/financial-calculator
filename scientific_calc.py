#!/usr/bin/env python3
"""
Scientific Calculator Module
Advanced mathematical functions for the Investment Finance Calculator
"""

import math
import cmath
from typing import Union, Optional, List
import re

class ScientificCalculator:
    """Scientific calculator with advanced mathematical functions"""
    
    def __init__(self):
        self.memory = 0.0
        self.angle_mode = 'deg'  # 'deg' or 'rad'
        self.last_result = 0.0
        
    # Basic Scientific Functions
    @staticmethod
    def factorial(n: float) -> float:
        """Calculate factorial of n"""
        if n < 0 or n != int(n):
            raise ValueError("Factorial is only defined for non-negative integers")
        return math.factorial(int(n))
    
    @staticmethod
    def power(base: float, exponent: float) -> float:
        """Calculate base^exponent"""
        return math.pow(base, exponent)
    
    @staticmethod
    def square_root(x: float) -> float:
        """Calculate square root"""
        if x < 0:
            raise ValueError("Square root of negative number")
        return math.sqrt(x)
    
    @staticmethod
    def cube_root(x: float) -> float:
        """Calculate cube root"""
        if x >= 0:
            return math.pow(x, 1/3)
        else:
            return -math.pow(-x, 1/3)
    
    @staticmethod
    def nth_root(x: float, n: float) -> float:
        """Calculate nth root of x"""
        if n == 0:
            raise ValueError("Cannot calculate 0th root")
        return math.pow(x, 1/n)
    
    # Trigonometric Functions
    def sin(self, x: float) -> float:
        """Calculate sine"""
        if self.angle_mode == 'deg':
            x = math.radians(x)
        return math.sin(x)
    
    def cos(self, x: float) -> float:
        """Calculate cosine"""
        if self.angle_mode == 'deg':
            x = math.radians(x)
        return math.cos(x)
    
    def tan(self, x: float) -> float:
        """Calculate tangent"""
        if self.angle_mode == 'deg':
            x = math.radians(x)
        return math.tan(x)
    
    def asin(self, x: float) -> float:
        """Calculate arcsine"""
        if x < -1 or x > 1:
            raise ValueError("Domain error: asin input must be between -1 and 1")
        result = math.asin(x)
        if self.angle_mode == 'deg':
            result = math.degrees(result)
        return result
    
    def acos(self, x: float) -> float:
        """Calculate arccosine"""
        if x < -1 or x > 1:
            raise ValueError("Domain error: acos input must be between -1 and 1")
        result = math.acos(x)
        if self.angle_mode == 'deg':
            result = math.degrees(result)
        return result
    
    def atan(self, x: float) -> float:
        """Calculate arctangent"""
        result = math.atan(x)
        if self.angle_mode == 'deg':
            result = math.degrees(result)
        return result
    
    # Hyperbolic Functions
    @staticmethod
    def sinh(x: float) -> float:
        """Calculate hyperbolic sine"""
        return math.sinh(x)
    
    @staticmethod
    def cosh(x: float) -> float:
        """Calculate hyperbolic cosine"""
        return math.cosh(x)
    
    @staticmethod
    def tanh(x: float) -> float:
        """Calculate hyperbolic tangent"""
        return math.tanh(x)
    
    # Logarithmic Functions
    @staticmethod
    def log10(x: float) -> float:
        """Calculate base-10 logarithm"""
        if x <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers")
        return math.log10(x)
    
    @staticmethod
    def ln(x: float) -> float:
        """Calculate natural logarithm"""
        if x <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers")
        return math.log(x)
    
    @staticmethod
    def log(x: float, base: float) -> float:
        """Calculate logarithm with custom base"""
        if x <= 0 or base <= 0 or base == 1:
            raise ValueError("Invalid logarithm parameters")
        return math.log(x, base)
    
    # Exponential Functions
    @staticmethod
    def exp(x: float) -> float:
        """Calculate e^x"""
        return math.exp(x)
    
    @staticmethod
    def exp10(x: float) -> float:
        """Calculate 10^x"""
        return math.pow(10, x)
    
    # Constants
    @staticmethod
    def pi() -> float:
        """Return π (pi)"""
        return math.pi
    
    @staticmethod
    def e() -> float:
        """Return e (Euler's number)"""
        return math.e
    
    # Memory Functions
    def memory_add(self, value: float) -> None:
        """Add value to memory"""
        self.memory += value
    
    def memory_subtract(self, value: float) -> None:
        """Subtract value from memory"""
        self.memory -= value
    
    def memory_recall(self) -> float:
        """Recall memory value"""
        return self.memory
    
    def memory_clear(self) -> None:
        """Clear memory"""
        self.memory = 0.0
    
    def memory_store(self, value: float) -> None:
        """Store value in memory"""
        self.memory = value
    
    # Angle Mode
    def set_angle_mode(self, mode: str) -> None:
        """Set angle mode: 'deg' or 'rad'"""
        if mode.lower() in ['deg', 'degrees']:
            self.angle_mode = 'deg'
        elif mode.lower() in ['rad', 'radians']:
            self.angle_mode = 'rad'
        else:
            raise ValueError("Angle mode must be 'deg' or 'rad'")
    
    def get_angle_mode(self) -> str:
        """Get current angle mode"""
        return self.angle_mode
    
    # Utility Functions
    @staticmethod
    def degrees_to_radians(degrees: float) -> float:
        """Convert degrees to radians"""
        return math.radians(degrees)
    
    @staticmethod
    def radians_to_degrees(radians: float) -> float:
        """Convert radians to degrees"""
        return math.degrees(radians)
    
    @staticmethod
    def absolute(x: float) -> float:
        """Calculate absolute value"""
        return abs(x)
    
    @staticmethod
    def ceiling(x: float) -> float:
        """Round up to nearest integer"""
        return math.ceil(x)
    
    @staticmethod
    def floor(x: float) -> float:
        """Round down to nearest integer"""
        return math.floor(x)
    
    @staticmethod
    def round_to(x: float, decimals: int = 0) -> float:
        """Round to specified decimal places"""
        return round(x, decimals)
    
    # Expression Evaluator
    def evaluate_expression(self, expression: str) -> float:
        """
        Safely evaluate mathematical expressions
        Supports: +, -, *, /, **, (), scientific functions
        """
        # Replace scientific function names with math module calls
        expression = self._prepare_expression(expression)
        
        try:
            # Create a safe namespace for evaluation
            safe_dict = {
                "__builtins__": {},
                "abs": abs,
                "round": round,
                "pow": pow,
                "sqrt": math.sqrt,
                "sin": self.sin,
                "cos": self.cos,
                "tan": self.tan,
                "asin": self.asin,
                "acos": self.acos,
                "atan": self.atan,
                "sinh": math.sinh,
                "cosh": math.cosh,
                "tanh": math.tanh,
                "log": self.log10,
                "ln": self.ln,
                "exp": math.exp,
                "factorial": self.factorial,
                "pi": math.pi,
                "e": math.e,
            }
            
            result = eval(expression, safe_dict)
            self.last_result = float(result)
            return self.last_result
            
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
    
    def _prepare_expression(self, expression: str) -> str:
        """Prepare expression for evaluation"""
        # Replace common mathematical notation
        expression = expression.replace('×', '*')
        expression = expression.replace('÷', '/')
        expression = expression.replace('−', '-')
        expression = expression.replace('^', '**')
        
        # Replace constants
        expression = expression.replace('π', str(math.pi))
        expression = expression.replace('e', str(math.e))
        
        return expression

class ScientificButtonLayout:
    """Define button layouts for scientific calculator"""
    
    @staticmethod
    def get_basic_layout():
        """Get basic calculator button layout"""
        return [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
    
    @staticmethod
    def get_scientific_layout():
        """Get scientific calculator button layout"""
        return [
            ['2nd', 'π', 'e', 'C', '⌫'],
            ['x²', '1/x', '|x|', 'exp', 'mod'],
            ['√', '(', ')', 'n!', '÷'],
            ['sin', 'cos', 'tan', 'ln', '×'],
            ['7', '8', '9', 'log', '−'],
            ['4', '5', '6', 'x^y', '+'],
            ['1', '2', '3', 'M+', '='],
            ['0', '.', 'EE', 'MR', 'MC']
        ]
    
    @staticmethod
    def get_function_mappings():
        """Get mapping of button text to function names"""
        return {
            'sin': 'sin',
            'cos': 'cos',
            'tan': 'tan',
            'ln': 'ln',
            'log': 'log10',
            'exp': 'exp',
            'x²': 'square',
            '√': 'sqrt',
            'x^y': 'power',
            'n!': 'factorial',
            '1/x': 'reciprocal',
            '|x|': 'abs',
            'π': 'pi',
            'e': 'e_constant',
            'M+': 'memory_add',
            'MR': 'memory_recall',
            'MC': 'memory_clear'
        }

# Utility functions for the GUI
def format_scientific_result(result: float, precision: int = 10) -> str:
    """Format scientific calculator result for display"""
    if abs(result) < 1e-10 and result != 0:
        return "0"
    elif abs(result) >= 1e10 or (abs(result) < 1e-4 and result != 0):
        return f"{result:.{precision-4}e}"
    else:
        # Remove trailing zeros
        formatted = f"{result:.{precision}f}".rstrip('0').rstrip('.')
        return formatted if formatted else "0"

def validate_scientific_input(expression: str) -> bool:
    """Validate scientific calculator input"""
    # Check for balanced parentheses
    if expression.count('(') != expression.count(')'):
        return False
    
    # Check for valid characters
    valid_chars = set('0123456789+-*/().^πe sincotan lnogexpqrtfacbsmodMRC')
    if not all(c in valid_chars or c.isspace() for c in expression):
        return False
    
    return True