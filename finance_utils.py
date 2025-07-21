"""
Financial calculation utilities for the Investment Finance Calculator
"""

import numpy as np
from typing import List, Dict, Optional, Tuple

class FinancialCalculations:
    """Core financial calculation methods"""
    
    @staticmethod
    def npv(rate: float, cashflows: List[float]) -> float:
        """
        Calculate Net Present Value
        
        Args:
            rate: Discount rate (as decimal, e.g., 0.1 for 10%)
            cashflows: List of cash flows, with initial investment as negative
        
        Returns:
            NPV value
        """
        return sum(cf / (1 + rate) ** i for i, cf in enumerate(cashflows))
    
    @staticmethod
    def irr(cashflows: List[float], guess: float = 0.1) -> Optional[float]:
        """
        Calculate Internal Rate of Return using Newton-Raphson method
        
        Args:
            cashflows: List of cash flows
            guess: Initial guess for IRR
        
        Returns:
            IRR as decimal or None if not found
        """
        def npv_derivative(rate, cashflows):
            return sum(-i * cf / (1 + rate) ** (i + 1) for i, cf in enumerate(cashflows))
        
        rate = guess
        for _ in range(100):  # Max iterations
            npv_val = FinancialCalculations.npv(rate, cashflows)
            if abs(npv_val) < 1e-6:
                return rate
            
            derivative = npv_derivative(rate, cashflows)
            if abs(derivative) < 1e-10:
                break
            
            rate = rate - npv_val / derivative
        
        return None
    
    @staticmethod
    def payback_period(cashflows: List[float]) -> Optional[float]:
        """
        Calculate payback period
        
        Args:
            cashflows: List of cash flows (first should be negative investment)
        
        Returns:
            Payback period in years or None if never pays back
        """
        if not cashflows or cashflows[0] >= 0:
            return None
        
        cumulative = cashflows[0]
        for i, cf in enumerate(cashflows[1:], 1):
            cumulative += cf
            if cumulative >= 0:
                # Linear interpolation for fractional year
                if i == 1:
                    return i
                prev_cumulative = cumulative - cf
                return i - 1 + abs(prev_cumulative) / cf
        
        return None
    
    @staticmethod
    def dcf_valuation(
        free_cashflows: List[float],
        terminal_growth_rate: float,
        discount_rate: float,
        terminal_year: int = None
    ) -> Dict[str, float]:
        """
        Discounted Cash Flow valuation
        
        Args:
            free_cashflows: Projected free cash flows
            terminal_growth_rate: Long-term growth rate for terminal value
            discount_rate: WACC or discount rate
            terminal_year: Year for terminal value calculation (default: last year)
        
        Returns:
            Dictionary with valuation components
        """
        if terminal_year is None:
            terminal_year = len(free_cashflows)
        
        # Present value of projected cash flows
        pv_cashflows = [
            cf / (1 + discount_rate) ** (i + 1) 
            for i, cf in enumerate(free_cashflows)
        ]
        
        # Terminal value
        terminal_cf = free_cashflows[-1] * (1 + terminal_growth_rate)
        terminal_value = terminal_cf / (discount_rate - terminal_growth_rate)
        pv_terminal_value = terminal_value / (1 + discount_rate) ** terminal_year
        
        enterprise_value = sum(pv_cashflows) + pv_terminal_value
        
        return {
            'pv_cashflows': sum(pv_cashflows),
            'terminal_value': terminal_value,
            'pv_terminal_value': pv_terminal_value,
            'enterprise_value': enterprise_value,
            'cashflow_breakdown': pv_cashflows
        }
    
    @staticmethod
    def wacc(
        cost_of_equity: float,
        cost_of_debt: float,
        tax_rate: float,
        market_value_equity: float,
        market_value_debt: float
    ) -> float:
        """
        Calculate Weighted Average Cost of Capital
        
        Args:
            cost_of_equity: Cost of equity (as decimal)
            cost_of_debt: Cost of debt (as decimal)
            tax_rate: Corporate tax rate (as decimal)
            market_value_equity: Market value of equity
            market_value_debt: Market value of debt
        
        Returns:
            WACC as decimal
        """
        total_value = market_value_equity + market_value_debt
        equity_weight = market_value_equity / total_value
        debt_weight = market_value_debt / total_value
        
        return (equity_weight * cost_of_equity + 
                debt_weight * cost_of_debt * (1 - tax_rate))
    
    @staticmethod
    def capm(risk_free_rate: float, beta: float, market_return: float) -> float:
        """
        Calculate cost of equity using CAPM
        
        Args:
            risk_free_rate: Risk-free rate (as decimal)
            beta: Stock beta
            market_return: Expected market return (as decimal)
        
        Returns:
            Cost of equity as decimal
        """
        return risk_free_rate + beta * (market_return - risk_free_rate)
    
    @staticmethod
    def compound_annual_growth_rate(
        beginning_value: float,
        ending_value: float,
        periods: int
    ) -> float:
        """
        Calculate Compound Annual Growth Rate
        
        Args:
            beginning_value: Starting value
            ending_value: Ending value
            periods: Number of periods
        
        Returns:
            CAGR as decimal
        """
        return (ending_value / beginning_value) ** (1 / periods) - 1
    
    @staticmethod
    def present_value(future_value: float, rate: float, periods: int) -> float:
        """Calculate present value"""
        return future_value / (1 + rate) ** periods
    
    @staticmethod
    def future_value(present_value: float, rate: float, periods: int) -> float:
        """Calculate future value"""
        return present_value * (1 + rate) ** periods
    
    @staticmethod
    def bond_price(
        face_value: float,
        coupon_rate: float,
        yield_rate: float,
        years_to_maturity: int,
        payments_per_year: int = 2
    ) -> Dict[str, float]:
        """
        Calculate bond price and related metrics
        
        Args:
            face_value: Par value of the bond
            coupon_rate: Annual coupon rate (as decimal)
            yield_rate: Required yield/discount rate (as decimal)
            years_to_maturity: Years until bond matures
            payments_per_year: Coupon payments per year (default 2 for semi-annual)
        
        Returns:
            Dictionary with bond pricing information
        """
        periods = years_to_maturity * payments_per_year
        coupon_payment = (face_value * coupon_rate) / payments_per_year
        period_yield = yield_rate / payments_per_year
        
        # Present value of coupon payments (annuity)
        if period_yield == 0:
            pv_coupons = coupon_payment * periods
        else:
            pv_coupons = coupon_payment * (1 - (1 + period_yield) ** -periods) / period_yield
        
        # Present value of face value
        pv_face_value = face_value / (1 + period_yield) ** periods
        
        # Bond price
        bond_price = pv_coupons + pv_face_value
        
        # Current yield
        current_yield = (coupon_payment * payments_per_year) / bond_price
        
        # Duration calculation (inline to avoid recursion)
        weighted_time = 0
        for t in range(1, periods + 1):
            if t == periods:
                # Final payment includes face value
                cash_flow = coupon_payment + face_value
            else:
                cash_flow = coupon_payment
            
            pv_cash_flow = cash_flow / (1 + period_yield) ** t
            weighted_time += (t / payments_per_year) * pv_cash_flow
        
        duration = weighted_time / bond_price
        
        return {
            'bond_price': bond_price,
            'pv_coupons': pv_coupons,
            'pv_face_value': pv_face_value,
            'current_yield': current_yield,
            'duration': duration,
            'coupon_payment': coupon_payment * payments_per_year
        }
    

    
    @staticmethod
    def yield_to_maturity(
        bond_price: float,
        face_value: float,
        coupon_rate: float,
        years_to_maturity: int,
        payments_per_year: int = 2,
        guess: float = 0.05
    ) -> Optional[float]:
        """
        Calculate yield to maturity using Newton-Raphson method
        
        Args:
            bond_price: Current market price of bond
            face_value: Par value of the bond
            coupon_rate: Annual coupon rate (as decimal)
            years_to_maturity: Years until maturity
            payments_per_year: Coupon payments per year
            guess: Initial guess for YTM
        
        Returns:
            YTM as decimal or None if not found
        """
        def bond_price_function(ytm):
            result = FinancialCalculations.bond_price(
                face_value, coupon_rate, ytm, years_to_maturity, payments_per_year
            )
            return result['bond_price'] - bond_price
        
        def bond_price_derivative(ytm):
            # Numerical derivative
            h = 0.0001
            return (bond_price_function(ytm + h) - bond_price_function(ytm - h)) / (2 * h)
        
        ytm = guess
        for _ in range(100):  # Max iterations
            price_diff = bond_price_function(ytm)
            if abs(price_diff) < 0.01:  # Close enough
                return ytm
            
            derivative = bond_price_derivative(ytm)
            if abs(derivative) < 1e-10:
                break
            
            ytm = ytm - price_diff / derivative
            
            # Keep YTM reasonable
            if ytm < -0.5 or ytm > 1.0:
                break
        
        return None