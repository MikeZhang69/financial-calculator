#!/usr/bin/env python3
"""
Test script for scientific calculator functions
"""

from scientific_calc import ScientificCalculator, format_scientific_result
import math

def test_basic_functions():
    """Test basic scientific functions"""
    calc = ScientificCalculator()
    
    print("Testing Basic Functions:")
    print("=" * 30)
    
    # Test power functions
    assert calc.power(2, 3) == 8
    print("✅ Power: 2^3 = 8")
    
    # Test square root
    assert calc.square_root(16) == 4
    print("✅ Square root: √16 = 4")
    
    # Test factorial
    assert calc.factorial(5) == 120
    print("✅ Factorial: 5! = 120")
    
    print()

def test_trigonometric_functions():
    """Test trigonometric functions"""
    calc = ScientificCalculator()
    
    print("Testing Trigonometric Functions:")
    print("=" * 35)
    
    # Test in degrees (default)
    calc.set_angle_mode('deg')
    sin_90 = calc.sin(90)
    assert abs(sin_90 - 1.0) < 1e-10
    print(f"✅ sin(90°) = {sin_90:.10f}")
    
    cos_0 = calc.cos(0)
    assert abs(cos_0 - 1.0) < 1e-10
    print(f"✅ cos(0°) = {cos_0:.10f}")
    
    tan_45 = calc.tan(45)
    assert abs(tan_45 - 1.0) < 1e-10
    print(f"✅ tan(45°) = {tan_45:.10f}")
    
    # Test in radians
    calc.set_angle_mode('rad')
    sin_pi_2 = calc.sin(math.pi/2)
    assert abs(sin_pi_2 - 1.0) < 1e-10
    print(f"✅ sin(π/2) = {sin_pi_2:.10f}")
    
    print()

def test_logarithmic_functions():
    """Test logarithmic functions"""
    calc = ScientificCalculator()
    
    print("Testing Logarithmic Functions:")
    print("=" * 32)
    
    # Test natural log
    ln_e = calc.ln(math.e)
    assert abs(ln_e - 1.0) < 1e-10
    print(f"✅ ln(e) = {ln_e:.10f}")
    
    # Test base-10 log
    log_100 = calc.log10(100)
    assert abs(log_100 - 2.0) < 1e-10
    print(f"✅ log₁₀(100) = {log_100:.10f}")
    
    # Test exponential
    exp_1 = calc.exp(1)
    assert abs(exp_1 - math.e) < 1e-10
    print(f"✅ e^1 = {exp_1:.10f}")
    
    print()

def test_memory_functions():
    """Test memory functions"""
    calc = ScientificCalculator()
    
    print("Testing Memory Functions:")
    print("=" * 27)
    
    # Test memory operations
    calc.memory_store(42)
    assert calc.memory_recall() == 42
    print("✅ Memory store/recall: 42")
    
    calc.memory_add(8)
    assert calc.memory_recall() == 50
    print("✅ Memory add: 42 + 8 = 50")
    
    calc.memory_subtract(10)
    assert calc.memory_recall() == 40
    print("✅ Memory subtract: 50 - 10 = 40")
    
    calc.memory_clear()
    assert calc.memory_recall() == 0
    print("✅ Memory clear: 0")
    
    print()

def test_expression_evaluation():
    """Test expression evaluation"""
    calc = ScientificCalculator()
    calc.set_angle_mode('deg')
    
    print("Testing Expression Evaluation:")
    print("=" * 32)
    
    # Test basic arithmetic
    result1 = calc.evaluate_expression("2 + 3 * 4")
    assert result1 == 14
    print(f"✅ 2 + 3 * 4 = {result1}")
    
    # Test with parentheses
    result2 = calc.evaluate_expression("(2 + 3) * 4")
    assert result2 == 20
    print(f"✅ (2 + 3) * 4 = {result2}")
    
    # Test with scientific functions
    result3 = calc.evaluate_expression("sqrt(16) + sin(90)")
    expected3 = 4 + calc.sin(90)
    assert abs(result3 - expected3) < 1e-10
    print(f"✅ √16 + sin(90°) = {result3:.10f}")
    
    # Test with constants
    result4 = calc.evaluate_expression("pi * 2")
    expected4 = math.pi * 2
    assert abs(result4 - expected4) < 1e-10
    print(f"✅ π * 2 = {result4:.10f}")
    
    print()

def test_formatting():
    """Test result formatting"""
    print("Testing Result Formatting:")
    print("=" * 28)
    
    # Test normal numbers
    assert format_scientific_result(123.456) == "123.456"
    print("✅ Normal: 123.456")
    
    # Test very large numbers
    large_result = format_scientific_result(1.23e15)
    print(f"✅ Large: 1.23e15 → {large_result}")
    
    # Test very small numbers
    small_result = format_scientific_result(1.23e-8)
    print(f"✅ Small: 1.23e-8 → {small_result}")
    
    # Test zero
    assert format_scientific_result(0) == "0"
    print("✅ Zero: 0")
    
    print()

def test_constants():
    """Test mathematical constants"""
    calc = ScientificCalculator()
    
    print("Testing Mathematical Constants:")
    print("=" * 33)
    
    pi_val = calc.pi()
    assert abs(pi_val - math.pi) < 1e-15
    print(f"✅ π = {pi_val}")
    
    e_val = calc.e()
    assert abs(e_val - math.e) < 1e-15
    print(f"✅ e = {e_val}")
    
    print()

if __name__ == "__main__":
    print("🧮 Scientific Calculator Test Suite")
    print("=" * 40)
    print()
    
    try:
        test_basic_functions()
        test_trigonometric_functions()
        test_logarithmic_functions()
        test_memory_functions()
        test_expression_evaluation()
        test_formatting()
        test_constants()
        
        print("🎉 All tests passed successfully!")
        print("Scientific calculator module is ready for integration.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()