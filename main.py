#!/usr/bin/env python3
"""
Investment Finance Calculator
A calculator app inspired by iPhone calculator but focused on investment analysis
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import numpy as np
from typing import List, Dict, Optional
from finance_utils import FinancialCalculations

class FinanceCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Investment Finance Calculator")
        self.root.geometry("400x600")
        self.root.configure(bg='#1c1c1e')
        
        # Calculator state
        self.display_var = tk.StringVar(value="0")
        self.current_mode = "basic"  # basic, npv, dcf, cashflow
        self.current_input = ""
        self.operator = None
        self.first_number = None
        self.should_reset_display = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI"""
        # Display
        display_frame = tk.Frame(self.root, bg='#1c1c1e')
        display_frame.pack(fill='x', padx=10, pady=10)
        
        self.display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=('SF Pro Display', 48, 'normal'),
            bg='#1c1c1e',
            fg='white',
            anchor='e'
        )
        self.display.pack(fill='x')
        
        # Mode selector
        mode_frame = tk.Frame(self.root, bg='#1c1c1e')
        mode_frame.pack(fill='x', padx=10, pady=5)
        
        modes = [("Basic", "basic"), ("NPV", "npv"), ("DCF", "dcf"), ("Cash Flow", "cashflow"), ("Bonds", "bonds")]
        for text, mode in modes:
            btn = tk.Button(
                mode_frame,
                text=text,
                command=lambda m=mode: self.switch_mode(m),
                bg='#d4d4d2',
                fg='#1c1c1e',
                font=('SF Pro Display', 12),
                relief='flat',
                padx=10
            )
            btn.pack(side='left', padx=2, expand=True, fill='x')
        
        # Button grid
        self.button_frame = tk.Frame(self.root, bg='#1c1c1e')
        self.button_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_basic_buttons()
    
    def create_basic_buttons(self):
        """Create basic calculator buttons"""
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                if i == 4 and j == 0:  # Zero button spans 2 columns
                    btn = self.create_button(btn_text, i, j, columnspan=2)
                elif i == 4 and j == 1:  # Skip this position for zero button
                    continue
                else:
                    btn = self.create_button(btn_text, i, j)
    
    def create_button(self, text, row, col, columnspan=1):
        """Create a calculator button"""
        # Button styling - all buttons use the same light gray color as numbers
        bg_color = '#d4d4d2'  # Light gray for all buttons
        fg_color = '#1c1c1e'  # Dark text for all buttons
        
        btn = tk.Button(
            self.button_frame,
            text=text,
            font=('SF Pro Display', 24),
            bg=bg_color,
            fg=fg_color,
            relief='flat',
            command=lambda: self.button_click(text)
        )
        
        btn.grid(row=row, column=col, columnspan=columnspan, 
                sticky='nsew', padx=2, pady=2)
        
        # Configure grid weights
        self.button_frame.grid_rowconfigure(row, weight=1)
        self.button_frame.grid_columnconfigure(col, weight=1)
        
        return btn
    
    def button_click(self, text):
        """Handle button clicks"""
        current = self.display_var.get()
        
        if text == 'C':
            # Clear everything
            self.display_var.set("0")
            self.current_input = ""
            self.operator = None
            self.first_number = None
            self.should_reset_display = False
            
        elif text in ['÷', '×', '−', '+']:
            # Handle operators
            if self.first_number is None:
                self.first_number = float(current)
            elif self.operator and not self.should_reset_display:
                # Chain calculations
                second_number = float(current)
                result = self.calculate(self.first_number, second_number, self.operator)
                self.display_var.set(str(result))
                self.first_number = result
            
            self.operator = text
            self.should_reset_display = True
            
        elif text == '=':
            # Perform calculation
            if self.operator and self.first_number is not None:
                try:
                    second_number = float(current)
                    result = self.calculate(self.first_number, second_number, self.operator)
                    self.display_var.set(str(result))
                    self.first_number = None
                    self.operator = None
                    self.should_reset_display = True
                except:
                    self.display_var.set("Error")
                    
        elif text == '±':
            # Toggle sign
            try:
                value = float(current)
                self.display_var.set(str(-value))
            except:
                pass
                
        elif text == '%':
            # Percentage
            try:
                value = float(current)
                self.display_var.set(str(value / 100))
            except:
                pass
                
        elif text == '.':
            # Decimal point
            if self.should_reset_display:
                self.display_var.set("0.")
                self.should_reset_display = False
            elif '.' not in current:
                self.display_var.set(current + '.')
                
        else:
            # Numbers
            if self.should_reset_display or current == "0":
                self.display_var.set(text)
                self.should_reset_display = False
            else:
                self.display_var.set(current + text)
    
    def calculate(self, first: float, second: float, operator: str) -> float:
        """Perform basic arithmetic calculations"""
        if operator == '+':
            return first + second
        elif operator == '−':
            return first - second
        elif operator == '×':
            return first * second
        elif operator == '÷':
            if second == 0:
                raise ValueError("Division by zero")
            return first / second
        else:
            return second
    
    def switch_mode(self, mode):
        """Switch between calculator modes"""
        self.current_mode = mode
        if mode == "npv":
            self.create_npv_interface()
        elif mode == "dcf":
            self.create_dcf_interface()
        elif mode == "cashflow":
            self.create_cashflow_interface()
        elif mode == "bonds":
            self.create_bonds_interface()
        else:
            self.create_basic_buttons()
    
    def create_npv_interface(self):
        """Create NPV calculation interface"""
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        # NPV input fields
        tk.Label(self.button_frame, text="NPV Calculator", 
                font=('SF Pro Display', 18), bg='#1c1c1e', fg='white').pack(pady=10)
        
        # Discount rate input
        rate_frame = tk.Frame(self.button_frame, bg='#1c1c1e')
        rate_frame.pack(fill='x', pady=5)
        tk.Label(rate_frame, text="Discount Rate (%):", bg='#1c1c1e', fg='white').pack(side='left')
        self.rate_entry = tk.Entry(rate_frame, bg='#333333', fg='white')
        self.rate_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Cash flows input
        tk.Label(self.button_frame, text="Cash Flows (comma separated):", 
                bg='#1c1c1e', fg='white').pack(pady=(10, 5))
        self.cashflows_entry = tk.Text(self.button_frame, height=4, bg='#333333', fg='white')
        self.cashflows_entry.pack(fill='x', pady=5)
        
        # Calculate button
        calc_btn = tk.Button(
            self.button_frame,
            text="Calculate NPV",
            command=self.calculate_npv,
            bg='#d4d4d2',
            fg='#1c1c1e',
            font=('SF Pro Display', 16),
            relief='flat'
        )
        calc_btn.pack(pady=10, fill='x')
    
    def calculate_npv(self):
        """Calculate NPV from inputs"""
        try:
            rate = float(self.rate_entry.get()) / 100
            cashflows_text = self.cashflows_entry.get("1.0", tk.END).strip()
            cashflows = [float(x.strip()) for x in cashflows_text.split(',') if x.strip()]
            
            # Use our FinancialCalculations class
            npv = FinancialCalculations.npv(rate, cashflows)
            irr = FinancialCalculations.irr(cashflows)
            payback = FinancialCalculations.payback_period(cashflows)
            
            # Display comprehensive results
            result_text = f"NPV: ${npv:,.2f}"
            if irr:
                result_text += f"\nIRR: {irr:.2%}"
            if payback:
                result_text += f"\nPayback: {payback:.1f} years"
            
            self.display_var.set(result_text)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def create_dcf_interface(self):
        """Create DCF valuation interface"""
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        canvas = tk.Canvas(self.button_frame, bg='#1c1c1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.button_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1c1c1e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # DCF input fields
        tk.Label(scrollable_frame, text="DCF Valuation", 
                font=('SF Pro Display', 18), bg='#1c1c1e', fg='white').pack(pady=10)
        
        # Free Cash Flows
        tk.Label(scrollable_frame, text="Free Cash Flows (comma separated):", 
                bg='#1c1c1e', fg='white').pack(pady=(10, 5))
        self.dcf_cashflows_entry = tk.Text(scrollable_frame, height=3, bg='#333333', fg='white')
        self.dcf_cashflows_entry.pack(fill='x', pady=5, padx=10)
        
        # Terminal Growth Rate
        growth_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        growth_frame.pack(fill='x', pady=5, padx=10)
        tk.Label(growth_frame, text="Terminal Growth Rate (%):", bg='#1c1c1e', fg='white').pack(side='left')
        self.terminal_growth_entry = tk.Entry(growth_frame, bg='#333333', fg='white')
        self.terminal_growth_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Discount Rate (WACC)
        wacc_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        wacc_frame.pack(fill='x', pady=5, padx=10)
        tk.Label(wacc_frame, text="Discount Rate/WACC (%):", bg='#1c1c1e', fg='white').pack(side='left')
        self.wacc_entry = tk.Entry(wacc_frame, bg='#333333', fg='white')
        self.wacc_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Calculate button
        calc_btn = tk.Button(
            scrollable_frame,
            text="Calculate DCF",
            command=self.calculate_dcf,
            bg='#d4d4d2',
            fg='#1c1c1e',
            font=('SF Pro Display', 16),
            relief='flat'
        )
        calc_btn.pack(pady=10, fill='x', padx=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def calculate_dcf(self):
        """Calculate DCF valuation from inputs"""
        try:
            # Get inputs
            cashflows_text = self.dcf_cashflows_entry.get("1.0", tk.END).strip()
            cashflows = [float(x.strip()) for x in cashflows_text.split(',') if x.strip()]
            
            terminal_growth = float(self.terminal_growth_entry.get()) / 100
            discount_rate = float(self.wacc_entry.get()) / 100
            
            # Calculate DCF
            dcf_result = FinancialCalculations.dcf_valuation(
                cashflows, terminal_growth, discount_rate
            )
            
            # Format results
            result_text = f"Enterprise Value: ${dcf_result['enterprise_value']:,.0f}\n"
            result_text += f"PV of Cash Flows: ${dcf_result['pv_cashflows']:,.0f}\n"
            result_text += f"PV of Terminal Value: ${dcf_result['pv_terminal_value']:,.0f}\n"
            result_text += f"Terminal Value: ${dcf_result['terminal_value']:,.0f}"
            
            self.display_var.set(result_text)
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def create_cashflow_interface(self):
        """Create cash flow projection interface"""
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        canvas = tk.Canvas(self.button_frame, bg='#1c1c1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.button_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1c1c1e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Cash Flow Projection inputs
        tk.Label(scrollable_frame, text="Cash Flow Projections", 
                font=('SF Pro Display', 18), bg='#1c1c1e', fg='white').pack(pady=10)
        
        # Initial Cash Flow
        initial_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        initial_frame.pack(fill='x', pady=5, padx=10)
        tk.Label(initial_frame, text="Initial Cash Flow ($):", bg='#1c1c1e', fg='white').pack(side='left')
        self.initial_cf_entry = tk.Entry(initial_frame, bg='#333333', fg='white')
        self.initial_cf_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Growth Rate
        growth_cf_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        growth_cf_frame.pack(fill='x', pady=5, padx=10)
        tk.Label(growth_cf_frame, text="Annual Growth Rate (%):", bg='#1c1c1e', fg='white').pack(side='left')
        self.growth_cf_entry = tk.Entry(growth_cf_frame, bg='#333333', fg='white')
        self.growth_cf_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Number of Years
        years_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        years_frame.pack(fill='x', pady=5, padx=10)
        tk.Label(years_frame, text="Number of Years:", bg='#1c1c1e', fg='white').pack(side='left')
        self.years_entry = tk.Entry(years_frame, bg='#333333', fg='white')
        self.years_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Calculate button
        calc_btn = tk.Button(
            scrollable_frame,
            text="Project Cash Flows",
            command=self.calculate_cashflow_projection,
            bg='#d4d4d2',
            fg='#1c1c1e',
            font=('SF Pro Display', 16),
            relief='flat'
        )
        calc_btn.pack(pady=10, fill='x', padx=10)
        
        # Results area
        self.cashflow_results = tk.Text(
            scrollable_frame, 
            height=8, 
            bg='#333333', 
            fg='white',
            font=('SF Pro Display', 12)
        )
        self.cashflow_results.pack(fill='both', expand=True, pady=10, padx=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def calculate_cashflow_projection(self):
        """Calculate and display cash flow projections"""
        try:
            initial_cf = float(self.initial_cf_entry.get())
            growth_rate = float(self.growth_cf_entry.get()) / 100
            years = int(self.years_entry.get())
            
            # Generate cash flow projections
            projections = []
            for year in range(1, years + 1):
                cf = initial_cf * (1 + growth_rate) ** year
                projections.append((year, cf))
            
            # Calculate summary metrics
            total_cf = sum(cf for _, cf in projections)
            avg_cf = total_cf / years
            cagr = FinancialCalculations.compound_annual_growth_rate(
                initial_cf, projections[-1][1], years
            )
            
            # Display results
            self.cashflow_results.delete(1.0, tk.END)
            self.cashflow_results.insert(tk.END, "CASH FLOW PROJECTIONS\n")
            self.cashflow_results.insert(tk.END, "=" * 30 + "\n\n")
            
            for year, cf in projections:
                self.cashflow_results.insert(tk.END, f"Year {year}: ${cf:,.0f}\n")
            
            self.cashflow_results.insert(tk.END, f"\nSUMMARY:\n")
            self.cashflow_results.insert(tk.END, f"Total Cash Flow: ${total_cf:,.0f}\n")
            self.cashflow_results.insert(tk.END, f"Average Annual CF: ${avg_cf:,.0f}\n")
            self.cashflow_results.insert(tk.END, f"CAGR: {cagr:.2%}\n")
            
            # Update main display with summary
            self.display_var.set(f"Total: ${total_cf:,.0f}\nCAGR: {cagr:.2%}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def create_bonds_interface(self):
        """Create bond valuation interface"""
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        canvas = tk.Canvas(self.button_frame, bg='#1c1c1e', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.button_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#1c1c1e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bond Valuation inputs
        tk.Label(scrollable_frame, text="Bond Valuation", 
                font=('SF Pro Display', 18), bg='#1c1c1e', fg='white').pack(pady=10)
        
        # Face Value
        face_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        face_frame.pack(fill='x', pady=5, padx=10)
        tk.Label(face_frame, text="Face Value ($):", bg='#1c1c1e', fg='white').pack(side='left')
        self.face_value_entry = tk.Entry(face_frame, bg='#333333', fg='white')
        self.face_value_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.face_value_entry.insert(0, "1000")  # Default value
        
        # Coupon Rate
        coupon_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        coupon_frame.pack(fill='x', pady=5, padx=10)
        tk.Label(coupon_frame, text="Coupon Rate (%):", bg='#1c1c1e', fg='white').pack(side='left')
        self.coupon_rate_entry = tk.Entry(coupon_frame, bg='#333333', fg='white')
        self.coupon_rate_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.coupon_rate_entry.insert(0, "5.0")  # Default value
        
        # Yield Rate
        yield_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        yield_frame.pack(fill='x', pady=5, padx=10)
        tk.Label(yield_frame, text="Required Yield (%):", bg='#1c1c1e', fg='white').pack(side='left')
        self.yield_rate_entry = tk.Entry(yield_frame, bg='#333333', fg='white')
        self.yield_rate_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.yield_rate_entry.insert(0, "6.0")  # Default value
        
        # Years to Maturity
        maturity_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        maturity_frame.pack(fill='x', pady=5, padx=10)
        tk.Label(maturity_frame, text="Years to Maturity:", bg='#1c1c1e', fg='white').pack(side='left')
        self.maturity_entry = tk.Entry(maturity_frame, bg='#333333', fg='white')
        self.maturity_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.maturity_entry.insert(0, "10")  # Default value
        
        # Payment Frequency
        freq_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        freq_frame.pack(fill='x', pady=5, padx=10)
        tk.Label(freq_frame, text="Payments per Year:", bg='#1c1c1e', fg='white').pack(side='left')
        self.payment_freq_entry = tk.Entry(freq_frame, bg='#333333', fg='white')
        self.payment_freq_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.payment_freq_entry.insert(0, "2")  # Default semi-annual
        
        # Calculate buttons
        button_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        button_frame.pack(fill='x', pady=10, padx=10)
        
        price_btn = tk.Button(
            button_frame,
            text="Calculate Bond Price",
            command=self.calculate_bond_price,
            bg='#d4d4d2',
            fg='#1c1c1e',
            font=('SF Pro Display', 14),
            relief='flat'
        )
        price_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        ytm_btn = tk.Button(
            button_frame,
            text="Calculate YTM",
            command=self.calculate_ytm,
            bg='#d4d4d2',
            fg='#1c1c1e',
            font=('SF Pro Display', 14),
            relief='flat'
        )
        ytm_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))
        
        # Results area
        self.bond_results = tk.Text(
            scrollable_frame, 
            height=10, 
            bg='#333333', 
            fg='white',
            font=('SF Pro Display', 12)
        )
        self.bond_results.pack(fill='both', expand=True, pady=10, padx=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def calculate_bond_price(self):
        """Calculate bond price and related metrics"""
        try:
            face_value = float(self.face_value_entry.get())
            coupon_rate = float(self.coupon_rate_entry.get()) / 100
            yield_rate = float(self.yield_rate_entry.get()) / 100
            years_to_maturity = int(self.maturity_entry.get())
            payments_per_year = int(self.payment_freq_entry.get())
            
            # Calculate bond metrics
            bond_result = FinancialCalculations.bond_price(
                face_value, coupon_rate, yield_rate, years_to_maturity, payments_per_year
            )
            
            # Display results
            self.bond_results.delete(1.0, tk.END)
            self.bond_results.insert(tk.END, "BOND VALUATION RESULTS\n")
            self.bond_results.insert(tk.END, "=" * 30 + "\n\n")
            
            self.bond_results.insert(tk.END, f"Bond Price: ${bond_result['bond_price']:,.2f}\n")
            self.bond_results.insert(tk.END, f"PV of Coupons: ${bond_result['pv_coupons']:,.2f}\n")
            self.bond_results.insert(tk.END, f"PV of Face Value: ${bond_result['pv_face_value']:,.2f}\n")
            self.bond_results.insert(tk.END, f"Annual Coupon: ${bond_result['coupon_payment']:,.2f}\n")
            self.bond_results.insert(tk.END, f"Current Yield: {bond_result['current_yield']:.2%}\n")
            self.bond_results.insert(tk.END, f"Duration: {bond_result['duration']:.2f} years\n")
            
            # Determine if bond is at premium, discount, or par
            if bond_result['bond_price'] > face_value:
                status = "Premium"
            elif bond_result['bond_price'] < face_value:
                status = "Discount"
            else:
                status = "Par"
            
            self.bond_results.insert(tk.END, f"\nBond Status: Trading at {status}\n")
            
            # Update main display
            self.display_var.set(f"Price: ${bond_result['bond_price']:,.2f}\nYield: {bond_result['current_yield']:.2%}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def calculate_ytm(self):
        """Calculate yield to maturity"""
        try:
            # For YTM calculation, we need the current market price
            # Let's use a simple input dialog for this
            market_price = tk.simpledialog.askfloat(
                "Market Price", 
                "Enter current market price of the bond:",
                minvalue=0.01
            )
            
            if market_price is None:
                return
            
            face_value = float(self.face_value_entry.get())
            coupon_rate = float(self.coupon_rate_entry.get()) / 100
            years_to_maturity = int(self.maturity_entry.get())
            payments_per_year = int(self.payment_freq_entry.get())
            
            # Calculate YTM
            ytm = FinancialCalculations.yield_to_maturity(
                market_price, face_value, coupon_rate, years_to_maturity, payments_per_year
            )
            
            # Display results
            self.bond_results.delete(1.0, tk.END)
            self.bond_results.insert(tk.END, "YIELD TO MATURITY CALCULATION\n")
            self.bond_results.insert(tk.END, "=" * 30 + "\n\n")
            
            self.bond_results.insert(tk.END, f"Market Price: ${market_price:,.2f}\n")
            self.bond_results.insert(tk.END, f"Face Value: ${face_value:,.2f}\n")
            self.bond_results.insert(tk.END, f"Coupon Rate: {coupon_rate:.2%}\n")
            self.bond_results.insert(tk.END, f"Years to Maturity: {years_to_maturity}\n")
            
            if ytm:
                self.bond_results.insert(tk.END, f"\nYield to Maturity: {ytm:.2%}\n")
                
                # Compare to coupon rate
                if ytm > coupon_rate:
                    self.bond_results.insert(tk.END, "Bond is trading at a discount\n")
                elif ytm < coupon_rate:
                    self.bond_results.insert(tk.END, "Bond is trading at a premium\n")
                else:
                    self.bond_results.insert(tk.END, "Bond is trading at par\n")
                
                # Update main display
                self.display_var.set(f"YTM: {ytm:.2%}")
            else:
                self.bond_results.insert(tk.END, "\nYTM calculation failed\n")
                self.display_var.set("YTM: Error")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def run(self):
        """Start the calculator"""
        self.root.mainloop()

if __name__ == "__main__":
    calculator = FinanceCalculator()
    calculator.run()