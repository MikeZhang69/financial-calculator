#!/usr/bin/env python3
"""
Simple tests for the finance calculator
"""

from finance_utils import FinancialCalculations

def test_npv():
    """Test NPV calculation"""
    # Example: Initial investment of -1000, then 300, 400, 500 over 3 years at 10%
    cashflows = [-1000, 300, 400, 500]
    rate = 0.10
    
    npv = FinancialCalculations.npv(rate, cashflows)
    print(f"NPV Test: ${npv:.2f}")
    
    # Manual verification: -1000 + 300/1.1 + 400/1.1^2 + 500/1.1^3
    manual_npv = -1000 + 300/1.1 + 400/(1.1**2) + 500/(1.1**3)
    print(f"Manual verification: ${manual_npv:.2f}")
    
def test_dcf():
    """Test DCF valuation"""
    free_cashflows = [100, 110, 121, 133]  # Growing at 10%
    terminal_growth = 0.03
    discount_rate = 0.12
    
    result = FinancialCalculations.dcf_valuation(
        free_cashflows, terminal_growth, discount_rate
    )
    
    print(f"\nDCF Test:")
    print(f"PV of Cash Flows: ${result['pv_cashflows']:.2f}")
    print(f"Terminal Value: ${result['terminal_value']:.2f}")
    print(f"PV of Terminal Value: ${result['pv_terminal_value']:.2f}")
    print(f"Enterprise Value: ${result['enterprise_value']:.2f}")

def test_wacc():
    """Test WACC calculation"""
    wacc = FinancialCalculations.wacc(
        cost_of_equity=0.12,
        cost_of_debt=0.06,
        tax_rate=0.25,
        market_value_equity=800,
        market_value_debt=200
    )
    print(f"\nWACC Test: {wacc:.2%}")

def test_bond_valuation():
    """Test bond valuation"""
    # Example: $1000 face value, 5% coupon, 6% yield, 10 years, semi-annual
    bond_result = FinancialCalculations.bond_price(
        face_value=1000,
        coupon_rate=0.05,
        yield_rate=0.06,
        years_to_maturity=10,
        payments_per_year=2
    )
    
    print(f"\nBond Valuation Test:")
    print(f"Bond Price: ${bond_result['bond_price']:.2f}")
    print(f"Current Yield: {bond_result['current_yield']:.2%}")
    print(f"Duration: {bond_result['duration']:.2f} years")
    
    # Test YTM calculation
    ytm = FinancialCalculations.yield_to_maturity(
        bond_price=926.40,  # Approximate price from above
        face_value=1000,
        coupon_rate=0.05,
        years_to_maturity=10,
        payments_per_year=2
    )
    
    if ytm:
        print(f"YTM Test: {ytm:.2%}")

if __name__ == "__main__":
    test_npv()
    test_dcf()
    test_wacc()
    test_bond_valuation()
    print("\nAll tests completed!")