#!/usr/bin/env python3
"""
Investment Finance Calculator
A calculator app inspired by iPhone calculator but focused on investment analysis
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import numpy as np
import json
import csv
from datetime import datetime
import os
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
        
        # Data management
        self.calculation_history = []
        self.favorites = []
        self.history_file = "calculation_history.json"
        self.favorites_file = "calculation_favorites.json"
        self.last_calculation_data = None
        
        # Load existing data
        self.load_history()
        self.load_favorites()
        
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
        
        # Menu bar for data management
        menu_frame = tk.Frame(self.root, bg='#2c2c2e')
        menu_frame.pack(fill='x', padx=5, pady=2)
        
        menu_buttons = [
            ("📊 History", self.show_history_window),
            ("⭐ Favorites", self.show_favorites_window),
            ("� Save", self.save_current_calculation),
            ("📤 Export", self.export_current_calculation)
        ]
        
        for text, command in menu_buttons:
            btn = tk.Button(
                menu_frame,
                text=text,
                command=command,
                bg='#d4d4d2',
                fg='black',
                font=('SF Pro Display', 10, 'bold'),
                relief='flat',
                padx=8,
                pady=2
            )
            btn.pack(side='left', padx=2)
        
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
        
        # Help text
        help_text = tk.Label(
            self.button_frame, 
            text="💡 Analyze investment profitability with Net Present Value, IRR, and Payback Period",
            font=('SF Pro Display', 10), 
            bg='#1c1c1e', 
            fg='#888888',
            wraplength=350
        )
        help_text.pack(pady=(0, 10))
        
        # Discount rate input with tooltip
        rate_frame = tk.Frame(self.button_frame, bg='#1c1c1e')
        rate_frame.pack(fill='x', pady=5)
        
        rate_label_frame = tk.Frame(rate_frame, bg='#1c1c1e')
        rate_label_frame.pack(side='left')
        tk.Label(rate_label_frame, text="Discount Rate (%):", bg='#1c1c1e', fg='white').pack()
        tk.Label(rate_label_frame, text="Required return rate", 
                font=('SF Pro Display', 8), bg='#1c1c1e', fg='#666666').pack()
        
        self.rate_entry = tk.Entry(rate_frame, bg='#333333', fg='white', font=('SF Pro Display', 12))
        self.rate_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.rate_entry.insert(0, "10")  # Default example
        
        # Cash flows input with example
        cashflow_label_frame = tk.Frame(self.button_frame, bg='#1c1c1e')
        cashflow_label_frame.pack(fill='x', pady=(10, 5))
        tk.Label(cashflow_label_frame, text="Cash Flows (comma separated):", 
                bg='#1c1c1e', fg='white').pack(anchor='w')
        tk.Label(cashflow_label_frame, text="Example: -10000, 3000, 4000, 5000, 2000", 
                font=('SF Pro Display', 9), bg='#1c1c1e', fg='#666666').pack(anchor='w')
        
        self.cashflows_entry = tk.Text(self.button_frame, height=3, bg='#333333', fg='white', 
                                     font=('SF Pro Display', 12))
        self.cashflows_entry.pack(fill='x', pady=5)
        self.cashflows_entry.insert("1.0", "-10000, 3000, 4000, 5000, 2000")  # Default example
        
        # Input format help
        format_help = tk.Label(
            self.button_frame,
            text="📝 First value: Initial investment (negative)\n📈 Following values: Future cash inflows (positive)",
            font=('SF Pro Display', 9),
            bg='#1c1c1e',
            fg='#666666',
            justify='left'
        )
        format_help.pack(pady=(5, 10))
        
        # Calculate button
        calc_btn = tk.Button(
            self.button_frame,
            text="Calculate NPV Analysis",
            command=self.calculate_npv,
            bg='#d4d4d2',
            fg='#1c1c1e',
            font=('SF Pro Display', 16),
            relief='flat'
        )
        calc_btn.pack(pady=10, fill='x')
    
    def calculate_npv(self):
        """Calculate NPV from inputs with enhanced validation"""
        try:
            # Validate discount rate
            rate_text = self.rate_entry.get().strip()
            if not rate_text:
                messagebox.showerror("Input Error", "Please enter a discount rate.\n\nExample: 10 (for 10%)")
                return
            
            try:
                rate = float(rate_text) / 100
                if rate < 0:
                    messagebox.showwarning("Input Warning", "Discount rate is negative. This is unusual but will proceed with calculation.")
                elif rate > 1:
                    messagebox.showwarning("Input Warning", f"Discount rate of {rate*100:.1f}% seems very high. Please verify this is correct.")
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid discount rate: '{rate_text}'\n\nPlease enter a number (e.g., 10 for 10%)")
                return
            
            # Validate cash flows
            cashflows_text = self.cashflows_entry.get("1.0", tk.END).strip()
            if not cashflows_text:
                messagebox.showerror("Input Error", "Please enter cash flows.\n\nExample: -10000, 3000, 4000, 5000, 2000")
                return
            
            try:
                cashflows = [float(x.strip()) for x in cashflows_text.split(',') if x.strip()]
                if len(cashflows) < 2:
                    messagebox.showerror("Input Error", "Please enter at least 2 cash flows.\n\nFirst: Initial investment (usually negative)\nFollowing: Future cash inflows")
                    return
                
                # Check for typical investment pattern
                if cashflows[0] > 0:
                    result = messagebox.askyesno("Confirm Input", 
                        f"First cash flow is positive (${cashflows[0]:,.2f}).\n\nTypically, the first value should be negative (initial investment).\n\nContinue anyway?")
                    if not result:
                        return
                        
            except ValueError as e:
                messagebox.showerror("Input Error", 
                    f"Invalid cash flow format.\n\nPlease use comma-separated numbers:\nExample: -10000, 3000, 4000, 5000, 2000\n\nError: {str(e)}")
                return
            
            # Perform calculations
            npv = FinancialCalculations.npv(rate, cashflows)
            irr = FinancialCalculations.irr(cashflows)
            payback = FinancialCalculations.payback_period(cashflows)
            
            # Enhanced results display with interpretation
            result_text = f"NPV: ${npv:,.2f}"
            
            # Add NPV interpretation
            if npv > 0:
                result_text += " ✅ (Profitable)"
            elif npv < 0:
                result_text += " ❌ (Not Profitable)"
            else:
                result_text += " ⚖️ (Break-even)"
            
            if irr:
                result_text += f"\nIRR: {irr:.2%}"
                # Compare IRR to discount rate
                if irr > rate:
                    result_text += " ✅ (> Required Rate)"
                else:
                    result_text += " ❌ (< Required Rate)"
            else:
                result_text += "\nIRR: Unable to calculate"
                
            if payback:
                result_text += f"\nPayback: {payback:.1f} years"
            else:
                result_text += "\nPayback: Never pays back"
            
            self.display_var.set(result_text)
            
            # Save calculation data for export and history
            inputs_data = {
                'discount_rate': rate * 100,  # Convert back to percentage
                'cash_flows': cashflows
            }
            results_data = {
                'npv': npv,
                'irr': irr,
                'payback': payback
            }
            self.save_calculation_data('npv', inputs_data, results_data)
            
            # Show success message with summary and export options
            success_msg = (f"Analysis completed successfully!\n\n" +
                f"Investment Summary:\n" +
                f"• NPV: ${npv:,.2f} ({'Profitable' if npv > 0 else 'Not Profitable'})\n" +
                f"• IRR: {irr:.2%} vs {rate:.2%} required\n" +
                f"• Payback: {payback:.1f} years" if payback else "• Payback: Never pays back")
            
            result = messagebox.askquestion("NPV Analysis Complete", 
                success_msg + "\n\nWould you like to export or save this calculation?",
                icon='question')
            
            if result == 'yes':
                self.export_current_calculation()
            
        except Exception as e:
            messagebox.showerror("Calculation Error", 
                f"An error occurred during calculation:\n\n{str(e)}\n\nPlease check your inputs and try again.")
    
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
        
        # Help text
        help_text = tk.Label(
            scrollable_frame, 
            text="🏢 Value a company using Discounted Cash Flow analysis with terminal value",
            font=('SF Pro Display', 10), 
            bg='#1c1c1e', 
            fg='#888888',
            wraplength=350
        )
        help_text.pack(pady=(0, 10), padx=10)
        
        # Free Cash Flows with example
        fcf_label_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        fcf_label_frame.pack(fill='x', pady=(10, 5), padx=10)
        tk.Label(fcf_label_frame, text="Free Cash Flows (comma separated):", 
                bg='#1c1c1e', fg='white').pack(anchor='w')
        tk.Label(fcf_label_frame, text="Example: 500, 550, 600, 650", 
                font=('SF Pro Display', 9), bg='#1c1c1e', fg='#666666').pack(anchor='w')
        
        self.dcf_cashflows_entry = tk.Text(scrollable_frame, height=3, bg='#333333', fg='white',
                                         font=('SF Pro Display', 12))
        self.dcf_cashflows_entry.pack(fill='x', pady=5, padx=10)
        self.dcf_cashflows_entry.insert("1.0", "500, 550, 600, 650")  # Default example
        
        # Terminal Growth Rate with tooltip
        growth_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        growth_frame.pack(fill='x', pady=5, padx=10)
        
        growth_label_frame = tk.Frame(growth_frame, bg='#1c1c1e')
        growth_label_frame.pack(side='left')
        tk.Label(growth_label_frame, text="Terminal Growth Rate (%):", bg='#1c1c1e', fg='white').pack()
        tk.Label(growth_label_frame, text="Long-term growth (2-4%)", 
                font=('SF Pro Display', 8), bg='#1c1c1e', fg='#666666').pack()
        
        self.terminal_growth_entry = tk.Entry(growth_frame, bg='#333333', fg='white', 
                                            font=('SF Pro Display', 12))
        self.terminal_growth_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.terminal_growth_entry.insert(0, "2.5")  # Default example
        
        # Discount Rate (WACC) with tooltip
        wacc_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        wacc_frame.pack(fill='x', pady=5, padx=10)
        
        wacc_label_frame = tk.Frame(wacc_frame, bg='#1c1c1e')
        wacc_label_frame.pack(side='left')
        tk.Label(wacc_label_frame, text="Discount Rate/WACC (%):", bg='#1c1c1e', fg='white').pack()
        tk.Label(wacc_label_frame, text="Cost of capital", 
                font=('SF Pro Display', 8), bg='#1c1c1e', fg='#666666').pack()
        
        self.wacc_entry = tk.Entry(wacc_frame, bg='#333333', fg='white', 
                                 font=('SF Pro Display', 12))
        self.wacc_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.wacc_entry.insert(0, "10")  # Default example
        
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
        """Calculate DCF valuation from inputs with enhanced validation"""
        try:
            # Validate free cash flows
            cashflows_text = self.dcf_cashflows_entry.get("1.0", tk.END).strip()
            if not cashflows_text:
                messagebox.showerror("Input Error", "Please enter free cash flows.\n\nExample: 500, 550, 600, 650")
                return
            
            try:
                cashflows = [float(x.strip()) for x in cashflows_text.split(',') if x.strip()]
                if len(cashflows) < 2:
                    messagebox.showerror("Input Error", "Please enter at least 2 years of cash flows for meaningful DCF analysis.")
                    return
                
                # Check for negative cash flows (warning, not error)
                negative_count = sum(1 for cf in cashflows if cf < 0)
                if negative_count > 0:
                    result = messagebox.askyesno("Confirm Input", 
                        f"Found {negative_count} negative cash flow(s).\n\nDCF typically uses positive free cash flows.\n\nContinue anyway?")
                    if not result:
                        return
                        
            except ValueError as e:
                messagebox.showerror("Input Error", 
                    f"Invalid cash flow format.\n\nPlease use comma-separated numbers:\nExample: 500, 550, 600, 650\n\nError: {str(e)}")
                return
            
            # Validate terminal growth rate
            terminal_text = self.terminal_growth_entry.get().strip()
            if not terminal_text:
                messagebox.showerror("Input Error", "Please enter terminal growth rate.\n\nTypical range: 2-4% for mature companies")
                return
            
            try:
                terminal_growth = float(terminal_text) / 100
                if terminal_growth < 0:
                    messagebox.showwarning("Input Warning", "Negative terminal growth rate. This implies declining business.")
                elif terminal_growth > 0.06:  # 6%
                    messagebox.showwarning("Input Warning", f"Terminal growth of {terminal_growth*100:.1f}% is very high.\n\nTypical range is 2-4% for long-term growth.")
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid terminal growth rate: '{terminal_text}'\n\nPlease enter a number (e.g., 2.5 for 2.5%)")
                return
            
            # Validate discount rate (WACC)
            wacc_text = self.wacc_entry.get().strip()
            if not wacc_text:
                messagebox.showerror("Input Error", "Please enter discount rate (WACC).\n\nExample: 10 (for 10%)")
                return
            
            try:
                discount_rate = float(wacc_text) / 100
                if discount_rate <= 0:
                    messagebox.showerror("Input Error", "Discount rate must be positive.")
                    return
                elif discount_rate <= terminal_growth:
                    messagebox.showerror("Input Error", 
                        f"Discount rate ({discount_rate*100:.1f}%) must be higher than terminal growth ({terminal_growth*100:.1f}%).\n\nThis is required for terminal value calculation.")
                    return
                elif discount_rate > 0.5:  # 50%
                    messagebox.showwarning("Input Warning", f"Discount rate of {discount_rate*100:.1f}% seems extremely high.")
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid discount rate: '{wacc_text}'\n\nPlease enter a number (e.g., 10 for 10%)")
                return
            
            # Calculate DCF
            dcf_result = FinancialCalculations.dcf_valuation(
                cashflows, terminal_growth, discount_rate
            )
            
            # Enhanced results display with interpretation
            result_text = f"Enterprise Value: ${dcf_result['enterprise_value']:,.0f}"
            
            # Add valuation insights
            terminal_percentage = (dcf_result['pv_terminal_value'] / dcf_result['enterprise_value']) * 100
            if terminal_percentage > 80:
                result_text += f"\n⚠️ Terminal value: {terminal_percentage:.0f}% of total"
            elif terminal_percentage > 60:
                result_text += f"\n📊 Terminal value: {terminal_percentage:.0f}% of total"
            else:
                result_text += f"\n✅ Terminal value: {terminal_percentage:.0f}% of total"
            
            result_text += f"\nPV Cash Flows: ${dcf_result['pv_cashflows']:,.0f}"
            result_text += f"\nPV Terminal: ${dcf_result['pv_terminal_value']:,.0f}"
            
            self.display_var.set(result_text)
            
            # Save calculation data for export and history
            inputs_data = {
                'cash_flows': cashflows,
                'terminal_growth': terminal_growth * 100,  # Convert back to percentage
                'discount_rate': discount_rate * 100  # Convert back to percentage
            }
            results_data = {
                'enterprise_value': dcf_result['enterprise_value'],
                'pv_cashflows': dcf_result['pv_cashflows'],
                'pv_terminal_value': dcf_result['pv_terminal_value'],
                'terminal_value': dcf_result['terminal_value']
            }
            self.save_calculation_data('dcf', inputs_data, results_data)
            
            # Show success message with detailed breakdown and export options
            success_msg = (f"Enterprise valuation completed!\n\n" +
                f"Valuation Summary:\n" +
                f"• Enterprise Value: ${dcf_result['enterprise_value']:,.0f}\n" +
                f"• PV of Cash Flows: ${dcf_result['pv_cashflows']:,.0f} ({100-terminal_percentage:.0f}%)\n" +
                f"• PV of Terminal Value: ${dcf_result['pv_terminal_value']:,.0f} ({terminal_percentage:.0f}%)\n" +
                f"• Terminal Value: ${dcf_result['terminal_value']:,.0f}")
            
            result = messagebox.askquestion("DCF Valuation Complete", 
                success_msg + "\n\nWould you like to export or save this calculation?",
                icon='question')
            
            if result == 'yes':
                self.export_current_calculation()
            
        except Exception as e:
            messagebox.showerror("Calculation Error", 
                f"An error occurred during DCF calculation:\n\n{str(e)}\n\nPlease check your inputs and try again.")
    
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
        
        # Help text
        help_text = tk.Label(
            scrollable_frame, 
            text="📈 Project future cash flows with compound growth modeling",
            font=('SF Pro Display', 10), 
            bg='#1c1c1e', 
            fg='#888888',
            wraplength=350
        )
        help_text.pack(pady=(0, 10), padx=10)
        
        # Initial Cash Flow with tooltip
        initial_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        initial_frame.pack(fill='x', pady=5, padx=10)
        
        initial_label_frame = tk.Frame(initial_frame, bg='#1c1c1e')
        initial_label_frame.pack(side='left')
        tk.Label(initial_label_frame, text="Initial Cash Flow ($):", bg='#1c1c1e', fg='white').pack()
        tk.Label(initial_label_frame, text="Starting year cash flow", 
                font=('SF Pro Display', 8), bg='#1c1c1e', fg='#666666').pack()
        
        self.initial_cf_entry = tk.Entry(initial_frame, bg='#333333', fg='white', 
                                       font=('SF Pro Display', 12))
        self.initial_cf_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.initial_cf_entry.insert(0, "100000")  # Default example
        
        # Growth Rate with tooltip
        growth_cf_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        growth_cf_frame.pack(fill='x', pady=5, padx=10)
        
        growth_cf_label_frame = tk.Frame(growth_cf_frame, bg='#1c1c1e')
        growth_cf_label_frame.pack(side='left')
        tk.Label(growth_cf_label_frame, text="Annual Growth Rate (%):", bg='#1c1c1e', fg='white').pack()
        tk.Label(growth_cf_label_frame, text="Yearly increase rate", 
                font=('SF Pro Display', 8), bg='#1c1c1e', fg='#666666').pack()
        
        self.growth_cf_entry = tk.Entry(growth_cf_frame, bg='#333333', fg='white', 
                                      font=('SF Pro Display', 12))
        self.growth_cf_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.growth_cf_entry.insert(0, "8")  # Default example
        
        # Number of Years with tooltip
        years_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        years_frame.pack(fill='x', pady=5, padx=10)
        
        years_label_frame = tk.Frame(years_frame, bg='#1c1c1e')
        years_label_frame.pack(side='left')
        tk.Label(years_label_frame, text="Number of Years:", bg='#1c1c1e', fg='white').pack()
        tk.Label(years_label_frame, text="Projection period", 
                font=('SF Pro Display', 8), bg='#1c1c1e', fg='#666666').pack()
        
        self.years_entry = tk.Entry(years_frame, bg='#333333', fg='white', 
                                  font=('SF Pro Display', 12))
        self.years_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.years_entry.insert(0, "5")  # Default example
        
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
        """Calculate and display cash flow projections with enhanced validation"""
        try:
            # Validate initial cash flow
            initial_text = self.initial_cf_entry.get().strip()
            if not initial_text:
                messagebox.showerror("Input Error", "Please enter initial cash flow.\n\nExample: 100000")
                return
            
            try:
                initial_cf = float(initial_text)
                if initial_cf == 0:
                    messagebox.showerror("Input Error", "Initial cash flow cannot be zero.")
                    return
                elif initial_cf < 0:
                    result = messagebox.askyesno("Confirm Input", 
                        f"Initial cash flow is negative (${initial_cf:,.2f}).\n\nThis will project declining cash flows.\n\nContinue anyway?")
                    if not result:
                        return
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid initial cash flow: '{initial_text}'\n\nPlease enter a number (e.g., 100000)")
                return
            
            # Validate growth rate
            growth_text = self.growth_cf_entry.get().strip()
            if not growth_text:
                messagebox.showerror("Input Error", "Please enter growth rate.\n\nExample: 8 (for 8%)")
                return
            
            try:
                growth_rate = float(growth_text) / 100
                if growth_rate < -0.5:  # -50%
                    messagebox.showwarning("Input Warning", f"Growth rate of {growth_rate*100:.1f}% is very negative.\n\nThis implies rapid decline.")
                elif growth_rate > 0.5:  # 50%
                    messagebox.showwarning("Input Warning", f"Growth rate of {growth_rate*100:.1f}% is extremely high.\n\nPlease verify this is realistic.")
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid growth rate: '{growth_text}'\n\nPlease enter a number (e.g., 8 for 8%)")
                return
            
            # Validate number of years
            years_text = self.years_entry.get().strip()
            if not years_text:
                messagebox.showerror("Input Error", "Please enter number of years.\n\nExample: 5")
                return
            
            try:
                years = int(float(years_text))  # Allow decimal input but convert to int
                if years <= 0:
                    messagebox.showerror("Input Error", "Number of years must be positive.")
                    return
                elif years > 50:
                    result = messagebox.askyesno("Confirm Input", 
                        f"Projecting {years} years is very long-term.\n\nLong-term projections become less reliable.\n\nContinue anyway?")
                    if not result:
                        return
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid number of years: '{years_text}'\n\nPlease enter a whole number (e.g., 5)")
                return
            
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
            
            # Display results with enhanced formatting
            self.cashflow_results.delete(1.0, tk.END)
            self.cashflow_results.insert(tk.END, "CASH FLOW PROJECTIONS\n")
            self.cashflow_results.insert(tk.END, "=" * 35 + "\n\n")
            
            # Show input parameters
            self.cashflow_results.insert(tk.END, f"📊 Parameters:\n")
            self.cashflow_results.insert(tk.END, f"Initial CF: ${initial_cf:,.0f}\n")
            self.cashflow_results.insert(tk.END, f"Growth Rate: {growth_rate:.1%}\n")
            self.cashflow_results.insert(tk.END, f"Years: {years}\n\n")
            
            # Year-by-year projections
            self.cashflow_results.insert(tk.END, f"📈 Yearly Projections:\n")
            for year, cf in projections:
                growth_from_initial = ((cf / initial_cf) - 1) * 100
                self.cashflow_results.insert(tk.END, f"Year {year}: ${cf:,.0f} (+{growth_from_initial:.0f}%)\n")
            
            # Summary metrics
            self.cashflow_results.insert(tk.END, f"\n📋 Summary:\n")
            self.cashflow_results.insert(tk.END, f"Total Cash Flow: ${total_cf:,.0f}\n")
            self.cashflow_results.insert(tk.END, f"Average Annual CF: ${avg_cf:,.0f}\n")
            self.cashflow_results.insert(tk.END, f"CAGR: {cagr:.2%}\n")
            self.cashflow_results.insert(tk.END, f"Final Year CF: ${projections[-1][1]:,.0f}\n")
            
            # Growth analysis
            total_growth = ((projections[-1][1] / initial_cf) - 1) * 100
            self.cashflow_results.insert(tk.END, f"Total Growth: {total_growth:.0f}%\n")
            
            # Update main display with summary
            self.display_var.set(f"Total: ${total_cf:,.0f}\nCAGR: {cagr:.2%}\nFinal: ${projections[-1][1]:,.0f}")
            
            # Save calculation data for export and history
            inputs_data = {
                'initial_cf': initial_cf,
                'growth_rate': growth_rate * 100,  # Convert back to percentage
                'years': years
            }
            results_data = {
                'projections': [cf for _, cf in projections],
                'total_cf': total_cf,
                'avg_cf': avg_cf,
                'cagr': cagr
            }
            self.save_calculation_data('cashflow', inputs_data, results_data)
            
            # Show success message with export option
            success_msg = (f"Projection completed successfully!\n\n" +
                f"Summary:\n" +
                f"• Total {years}-year cash flow: ${total_cf:,.0f}\n" +
                f"• Average annual: ${avg_cf:,.0f}\n" +
                f"• CAGR: {cagr:.2%}\n" +
                f"• Final year: ${projections[-1][1]:,.0f}")
            
            result = messagebox.askquestion("Cash Flow Projection Complete", 
                success_msg + "\n\nWould you like to export or save this calculation?",
                icon='question')
            
            if result == 'yes':
                self.export_current_calculation()
            
        except Exception as e:
            messagebox.showerror("Calculation Error", 
                f"An error occurred during projection:\n\n{str(e)}\n\nPlease check your inputs and try again.")
    
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
        
        # Help text
        help_text = tk.Label(
            scrollable_frame, 
            text="🏦 Analyze bond pricing, yield to maturity, and duration metrics",
            font=('SF Pro Display', 10), 
            bg='#1c1c1e', 
            fg='#888888',
            wraplength=350
        )
        help_text.pack(pady=(0, 10), padx=10)
        
        # Face Value with tooltip
        face_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        face_frame.pack(fill='x', pady=5, padx=10)
        
        face_label_frame = tk.Frame(face_frame, bg='#1c1c1e')
        face_label_frame.pack(side='left')
        tk.Label(face_label_frame, text="Face Value ($):", bg='#1c1c1e', fg='white').pack()
        tk.Label(face_label_frame, text="Par value at maturity", 
                font=('SF Pro Display', 8), bg='#1c1c1e', fg='#666666').pack()
        
        self.face_value_entry = tk.Entry(face_frame, bg='#333333', fg='white', 
                                       font=('SF Pro Display', 12))
        self.face_value_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.face_value_entry.insert(0, "1000")  # Default value
        
        # Coupon Rate with tooltip
        coupon_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        coupon_frame.pack(fill='x', pady=5, padx=10)
        
        coupon_label_frame = tk.Frame(coupon_frame, bg='#1c1c1e')
        coupon_label_frame.pack(side='left')
        tk.Label(coupon_label_frame, text="Coupon Rate (%):", bg='#1c1c1e', fg='white').pack()
        tk.Label(coupon_label_frame, text="Annual interest rate", 
                font=('SF Pro Display', 8), bg='#1c1c1e', fg='#666666').pack()
        
        self.coupon_rate_entry = tk.Entry(coupon_frame, bg='#333333', fg='white', 
                                        font=('SF Pro Display', 12))
        self.coupon_rate_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.coupon_rate_entry.insert(0, "5.0")  # Default value
        
        # Yield Rate with tooltip
        yield_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        yield_frame.pack(fill='x', pady=5, padx=10)
        
        yield_label_frame = tk.Frame(yield_frame, bg='#1c1c1e')
        yield_label_frame.pack(side='left')
        tk.Label(yield_label_frame, text="Required Yield (%):", bg='#1c1c1e', fg='white').pack()
        tk.Label(yield_label_frame, text="Market discount rate", 
                font=('SF Pro Display', 8), bg='#1c1c1e', fg='#666666').pack()
        
        self.yield_rate_entry = tk.Entry(yield_frame, bg='#333333', fg='white', 
                                       font=('SF Pro Display', 12))
        self.yield_rate_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.yield_rate_entry.insert(0, "6.0")  # Default value
        
        # Years to Maturity with tooltip
        maturity_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        maturity_frame.pack(fill='x', pady=5, padx=10)
        
        maturity_label_frame = tk.Frame(maturity_frame, bg='#1c1c1e')
        maturity_label_frame.pack(side='left')
        tk.Label(maturity_label_frame, text="Years to Maturity:", bg='#1c1c1e', fg='white').pack()
        tk.Label(maturity_label_frame, text="Time until bond expires", 
                font=('SF Pro Display', 8), bg='#1c1c1e', fg='#666666').pack()
        
        self.maturity_entry = tk.Entry(maturity_frame, bg='#333333', fg='white', 
                                     font=('SF Pro Display', 12))
        self.maturity_entry.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.maturity_entry.insert(0, "10")  # Default value
        
        # Payment Frequency with tooltip
        freq_frame = tk.Frame(scrollable_frame, bg='#1c1c1e')
        freq_frame.pack(fill='x', pady=5, padx=10)
        
        freq_label_frame = tk.Frame(freq_frame, bg='#1c1c1e')
        freq_label_frame.pack(side='left')
        tk.Label(freq_label_frame, text="Payments per Year:", bg='#1c1c1e', fg='white').pack()
        tk.Label(freq_label_frame, text="2=semi-annual, 1=annual", 
                font=('SF Pro Display', 8), bg='#1c1c1e', fg='#666666').pack()
        
        self.payment_freq_entry = tk.Entry(freq_frame, bg='#333333', fg='white', 
                                         font=('SF Pro Display', 12))
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
            
            # Save calculation data for export and history
            inputs_data = {
                'face_value': face_value,
                'coupon_rate': coupon_rate * 100,  # Convert back to percentage
                'yield_rate': yield_rate * 100,  # Convert back to percentage
                'years_to_maturity': years_to_maturity,
                'payments_per_year': payments_per_year
            }
            results_data = {
                'bond_price': bond_result['bond_price'],
                'current_yield': bond_result['current_yield'],
                'duration': bond_result['duration'],
                'coupon_payment': bond_result['coupon_payment']
            }
            self.save_calculation_data('bonds', inputs_data, results_data)
            
            # Update main display
            self.display_var.set(f"Price: ${bond_result['bond_price']:,.2f}\nYield: {bond_result['current_yield']:.2%}")
            
            # Show success message with export option
            success_msg = (f"Bond valuation completed!\n\n" +
                f"Bond Analysis:\n" +
                f"• Bond Price: ${bond_result['bond_price']:,.2f}\n" +
                f"• Current Yield: {bond_result['current_yield']:.2%}\n" +
                f"• Duration: {bond_result['duration']:.2f} years\n" +
                f"• Status: Trading at {status}")
            
            result = messagebox.askquestion("Bond Valuation Complete", 
                success_msg + "\n\nWould you like to export or save this calculation?",
                icon='question')
            
            if result == 'yes':
                self.export_current_calculation()
            
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
    
    # Data Management Methods
    def load_history(self):
        """Load calculation history from file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.calculation_history = json.load(f)
        except Exception as e:
            print(f"Error loading history: {e}")
            self.calculation_history = []
    
    def save_history(self):
        """Save calculation history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.calculation_history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def load_favorites(self):
        """Load favorite calculations from file"""
        try:
            if os.path.exists(self.favorites_file):
                with open(self.favorites_file, 'r') as f:
                    self.favorites = json.load(f)
        except Exception as e:
            print(f"Error loading favorites: {e}")
            self.favorites = []
    
    def save_favorites(self):
        """Save favorite calculations to file"""
        try:
            with open(self.favorites_file, 'w') as f:
                json.dump(self.favorites, f, indent=2)
        except Exception as e:
            print(f"Error saving favorites: {e}")
    
    def add_to_history(self, calculation_type, inputs, results, description=""):
        """Add a calculation to history"""
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': calculation_type,
            'inputs': inputs,
            'results': results,
            'description': description
        }
        
        self.calculation_history.insert(0, history_entry)  # Add to beginning
        
        # Keep only last 100 calculations
        if len(self.calculation_history) > 100:
            self.calculation_history = self.calculation_history[:100]
        
        self.last_calculation_data = history_entry
        self.save_history()
    
    def add_to_favorites(self, name, calculation_type, inputs, results, description=""):
        """Add a calculation to favorites"""
        favorite_entry = {
            'name': name,
            'timestamp': datetime.now().isoformat(),
            'type': calculation_type,
            'inputs': inputs,
            'results': results,
            'description': description
        }
        
        self.favorites.append(favorite_entry)
        self.save_favorites()
        messagebox.showinfo("Saved", f"Calculation saved as '{name}' to favorites!")
    
    def export_to_csv(self, data, filename):
        """Export calculation data to CSV"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                if not data:
                    csvfile.write("No data to export\n")
                    return
                
                # Write header
                writer = csv.writer(csvfile)
                
                if data[0].get('type') == 'npv':
                    writer.writerow(['Date', 'Type', 'Discount Rate (%)', 'Cash Flows', 'NPV ($)', 'IRR (%)', 'Payback (years)', 'Description'])
                    for entry in data:
                        inputs = entry.get('inputs', {})
                        results = entry.get('results', {})
                        writer.writerow([
                            entry.get('timestamp', ''),
                            entry.get('type', ''),
                            inputs.get('discount_rate', ''),
                            inputs.get('cash_flows', ''),
                            results.get('npv', ''),
                            results.get('irr', ''),
                            results.get('payback', ''),
                            entry.get('description', '')
                        ])
                
                elif data[0].get('type') == 'dcf':
                    writer.writerow(['Date', 'Type', 'Free Cash Flows', 'Terminal Growth (%)', 'WACC (%)', 'Enterprise Value ($)', 'Description'])
                    for entry in data:
                        inputs = entry.get('inputs', {})
                        results = entry.get('results', {})
                        writer.writerow([
                            entry.get('timestamp', ''),
                            entry.get('type', ''),
                            inputs.get('cash_flows', ''),
                            inputs.get('terminal_growth', ''),
                            inputs.get('wacc', ''),
                            results.get('enterprise_value', ''),
                            entry.get('description', '')
                        ])
                
                elif data[0].get('type') == 'cashflow':
                    writer.writerow(['Date', 'Type', 'Initial CF ($)', 'Growth Rate (%)', 'Years', 'Total CF ($)', 'CAGR (%)', 'Description'])
                    for entry in data:
                        inputs = entry.get('inputs', {})
                        results = entry.get('results', {})
                        writer.writerow([
                            entry.get('timestamp', ''),
                            entry.get('type', ''),
                            inputs.get('initial_cf', ''),
                            inputs.get('growth_rate', ''),
                            inputs.get('years', ''),
                            results.get('total_cf', ''),
                            results.get('cagr', ''),
                            entry.get('description', '')
                        ])
                
                elif data[0].get('type') == 'bonds':
                    writer.writerow(['Date', 'Type', 'Face Value ($)', 'Coupon Rate (%)', 'Yield (%)', 'Years', 'Bond Price ($)', 'Duration', 'Description'])
                    for entry in data:
                        inputs = entry.get('inputs', {})
                        results = entry.get('results', {})
                        writer.writerow([
                            entry.get('timestamp', ''),
                            entry.get('type', ''),
                            inputs.get('face_value', ''),
                            inputs.get('coupon_rate', ''),
                            inputs.get('yield_rate', ''),
                            inputs.get('years', ''),
                            results.get('bond_price', ''),
                            results.get('duration', ''),
                            entry.get('description', '')
                        ])
                
                else:
                    # Generic export for mixed types
                    writer.writerow(['Date', 'Type', 'Inputs', 'Results', 'Description'])
                    for entry in data:
                        writer.writerow([
                            entry.get('timestamp', ''),
                            entry.get('type', ''),
                            str(entry.get('inputs', {})),
                            str(entry.get('results', {})),
                            entry.get('description', '')
                        ])
            
            return True
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export to CSV:\n{str(e)}")
            return False
    
    def show_history_window(self):
        """Show calculation history in a new window"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")
        history_window.geometry("800x600")
        history_window.configure(bg='#1c1c1e')
        
        # Create scrollable text area
        text_frame = tk.Frame(history_window, bg='#1c1c1e')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        history_text = tk.Text(text_frame, bg='#333333', fg='white', 
                              font=('SF Pro Display', 11), yscrollcommand=scrollbar.set)
        history_text.pack(fill='both', expand=True)
        scrollbar.config(command=history_text.yview)
        
        # Display history
        if not self.calculation_history:
            history_text.insert(tk.END, "No calculation history available.\n\nStart making calculations to build your history!")
        else:
            history_text.insert(tk.END, f"CALCULATION HISTORY ({len(self.calculation_history)} entries)\n")
            history_text.insert(tk.END, "=" * 60 + "\n\n")
            
            for i, entry in enumerate(self.calculation_history, 1):
                timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
                history_text.insert(tk.END, f"{i}. {entry['type'].upper()} - {timestamp}\n")
                
                # Display inputs
                inputs = entry.get('inputs', {})
                history_text.insert(tk.END, f"   Inputs: {inputs}\n")
                
                # Display results
                results = entry.get('results', {})
                history_text.insert(tk.END, f"   Results: {results}\n")
                
                if entry.get('description'):
                    history_text.insert(tk.END, f"   Note: {entry['description']}\n")
                
                history_text.insert(tk.END, "\n")
        
        # Buttons
        button_frame = tk.Frame(history_window, bg='#1c1c1e')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        export_btn = tk.Button(button_frame, text="Export History to CSV", 
                              command=self.export_history_csv,
                              bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12))
        export_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = tk.Button(button_frame, text="Clear History", 
                             command=self.clear_history,
                             bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12))
        clear_btn.pack(side='left')
        
        close_btn = tk.Button(button_frame, text="Close", 
                             command=history_window.destroy,
                             bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12))
        close_btn.pack(side='right')
    
    def export_history_csv(self):
        """Export calculation history to CSV file"""
        if not self.calculation_history:
            messagebox.showwarning("No Data", "No calculation history to export.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save History As"
        )
        
        if filename:
            if self.export_to_csv(self.calculation_history, filename):
                messagebox.showinfo("Export Complete", f"History exported successfully to:\n{filename}")
    
    def clear_history(self):
        """Clear calculation history"""
        result = messagebox.askyesno("Confirm Clear", 
            "Are you sure you want to clear all calculation history?\n\nThis action cannot be undone.")
        
        if result:
            self.calculation_history = []
            self.save_history()
            messagebox.showinfo("History Cleared", "Calculation history has been cleared.")
    
    def save_current_calculation(self):
        """Save current calculation to favorites"""
        if not self.last_calculation_data:
            messagebox.showwarning("No Calculation", "No recent calculation to save.")
            return
        
        name = simpledialog.askstring("Save Calculation", 
            "Enter a name for this calculation:", 
            initialvalue=f"{self.last_calculation_data['type'].upper()} - {datetime.now().strftime('%Y-%m-%d')}")
        
        if name:
            self.add_to_favorites(
                name,
                self.last_calculation_data['type'],
                self.last_calculation_data['inputs'],
                self.last_calculation_data['results'],
                self.last_calculation_data.get('description', '')
            )
    
    def show_favorites_window(self):
        """Show favorite calculations in a new window"""
        favorites_window = tk.Toplevel(self.root)
        favorites_window.title("Favorite Calculations")
        favorites_window.geometry("800x600")
        favorites_window.configure(bg='#1c1c1e')
        
        # Create scrollable text area
        text_frame = tk.Frame(favorites_window, bg='#1c1c1e')
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        favorites_text = tk.Text(text_frame, bg='#333333', fg='white', 
                               font=('SF Pro Display', 11), yscrollcommand=scrollbar.set)
        favorites_text.pack(fill='both', expand=True)
        scrollbar.config(command=favorites_text.yview)
        
        # Display favorites
        if not self.favorites:
            favorites_text.insert(tk.END, "No favorite calculations saved.\n\nSave calculations you want to reuse or reference later!")
        else:
            favorites_text.insert(tk.END, f"FAVORITE CALCULATIONS ({len(self.favorites)} saved)\n")
            favorites_text.insert(tk.END, "=" * 60 + "\n\n")
            
            for i, entry in enumerate(self.favorites, 1):
                timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
                favorites_text.insert(tk.END, f"{i}. {entry['name']}\n")
                favorites_text.insert(tk.END, f"   Type: {entry['type'].upper()} - Saved: {timestamp}\n")
                
                # Display inputs
                inputs = entry.get('inputs', {})
                favorites_text.insert(tk.END, f"   Inputs: {inputs}\n")
                
                # Display results
                results = entry.get('results', {})
                favorites_text.insert(tk.END, f"   Results: {results}\n")
                
                if entry.get('description'):
                    favorites_text.insert(tk.END, f"   Note: {entry['description']}\n")
                
                favorites_text.insert(tk.END, "\n")
        
        # Buttons
        button_frame = tk.Frame(favorites_window, bg='#1c1c1e')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        export_btn = tk.Button(button_frame, text="Export Favorites to CSV", 
                              command=self.export_favorites_csv,
                              bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12))
        export_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = tk.Button(button_frame, text="Clear Favorites", 
                             command=self.clear_favorites,
                             bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12))
        clear_btn.pack(side='left', padx=(0, 10))
        
        close_btn = tk.Button(button_frame, text="Close", 
                             command=favorites_window.destroy,
                             bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12))
        close_btn.pack(side='right')
    
    def export_favorites_csv(self):
        """Export favorite calculations to CSV file"""
        if not self.favorites:
            messagebox.showwarning("No Data", "No favorite calculations to export.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Favorites As"
        )
        
        if filename:
            if self.export_to_csv(self.favorites, filename):
                messagebox.showinfo("Export Complete", f"Favorites exported successfully to:\n{filename}")
    
    def clear_favorites(self):
        """Clear all favorite calculations"""
        if not self.favorites:
            messagebox.showinfo("No Data", "No favorite calculations to clear.")
            return
        
        result = messagebox.askyesno("Confirm Clear", 
            f"Are you sure you want to clear all {len(self.favorites)} favorite calculations?\n\nThis action cannot be undone.")
        
        if result:
            self.favorites = []
            self.save_favorites()
            messagebox.showinfo("Favorites Cleared", "All favorite calculations have been cleared.")
            
            # Refresh the favorites window if it's open
            # Note: This is a simple approach - in a more complex app, we'd update the window dynamically
    
    def save_calculation_data(self, calc_type, inputs, results, description=""):
        """Save calculation data for export and history"""
        self.last_calculation_data = {
            'type': calc_type,
            'inputs': inputs,
            'results': results,
            'description': description
        }
        
        # Add to history automatically
        self.add_to_history(calc_type, inputs, results, description)
    
    def export_current_calculation(self):
        """Export the current calculation to CSV"""
        if not self.last_calculation_data:
            messagebox.showwarning("No Data", "No recent calculation to export.\n\nPlease perform a calculation first.")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Current Calculation"
        )
        
        if filename:
            if self.export_to_csv([self.last_calculation_data], filename):
                messagebox.showinfo("Export Complete", f"Current calculation exported to:\n{filename}")
    
    def run(self):
        """Start the calculator"""
        self.root.mainloop()

if __name__ == "__main__":
    calculator = FinanceCalculator()
    calculator.run()
    
    def save_history(self):
        """Save calculation history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.calculation_history, f, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def load_favorites(self):
        """Load favorites from file"""
        try:
            if os.path.exists(self.favorites_file):
                with open(self.favorites_file, 'r') as f:
                    self.favorites = json.load(f)
        except Exception as e:
            print(f"Error loading favorites: {e}")
            self.favorites = []
    
    def save_favorites(self):
        """Save favorites to file"""
        try:
            with open(self.favorites_file, 'w') as f:
                json.dump(self.favorites, f, indent=2)
        except Exception as e:
            print(f"Error saving favorites: {e}")
    
    def add_to_history(self, calculation_type, inputs, results):
        """Add calculation to history"""
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': calculation_type,
            'inputs': inputs,
            'results': results
        }
        
        self.calculation_history.insert(0, history_entry)  # Add to beginning
        
        # Keep only last 50 calculations
        if len(self.calculation_history) > 50:
            self.calculation_history = self.calculation_history[:50]
        
        self.save_history()
    
    def add_to_favorites(self, calculation_type, inputs, results, name=None):
        """Add calculation to favorites"""
        if name is None:
            name = f"{calculation_type.upper()} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        favorite_entry = {
            'name': name,
            'timestamp': datetime.now().isoformat(),
            'type': calculation_type,
            'inputs': inputs,
            'results': results
        }
        
        self.favorites.append(favorite_entry)
        self.save_favorites()
        
        messagebox.showinfo("Added to Favorites", f"Calculation saved as: {name}")
    
    def export_to_csv(self, data, filename):
        """Export calculation data to CSV"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                if data['type'] == 'npv':
                    writer = csv.writer(csvfile)
                    writer.writerow(['NPV Analysis Report'])
                    writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                    writer.writerow([])
                    
                    writer.writerow(['Inputs:'])
                    writer.writerow(['Discount Rate (%)', data['inputs']['discount_rate']])
                    writer.writerow(['Cash Flows', ', '.join(map(str, data['inputs']['cash_flows']))])
                    writer.writerow([])
                    
                    writer.writerow(['Results:'])
                    writer.writerow(['NPV ($)', f"{data['results']['npv']:,.2f}"])
                    writer.writerow(['IRR (%)', f"{data['results']['irr']:.2%}" if data['results']['irr'] else 'N/A'])
                    writer.writerow(['Payback (years)', f"{data['results']['payback']:.1f}" if data['results']['payback'] else 'N/A'])
                
                elif data['type'] == 'dcf':
                    writer = csv.writer(csvfile)
                    writer.writerow(['DCF Valuation Report'])
                    writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                    writer.writerow([])
                    
                    writer.writerow(['Inputs:'])
                    writer.writerow(['Free Cash Flows', ', '.join(map(str, data['inputs']['cash_flows']))])
                    writer.writerow(['Terminal Growth Rate (%)', data['inputs']['terminal_growth']])
                    writer.writerow(['Discount Rate/WACC (%)', data['inputs']['discount_rate']])
                    writer.writerow([])
                    
                    writer.writerow(['Results:'])
                    writer.writerow(['Enterprise Value ($)', f"{data['results']['enterprise_value']:,.0f}"])
                    writer.writerow(['PV of Cash Flows ($)', f"{data['results']['pv_cashflows']:,.0f}"])
                    writer.writerow(['PV of Terminal Value ($)', f"{data['results']['pv_terminal_value']:,.0f}"])
                    writer.writerow(['Terminal Value ($)', f"{data['results']['terminal_value']:,.0f}"])
                
                elif data['type'] == 'cashflow':
                    writer = csv.writer(csvfile)
                    writer.writerow(['Cash Flow Projection Report'])
                    writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                    writer.writerow([])
                    
                    writer.writerow(['Inputs:'])
                    writer.writerow(['Initial Cash Flow ($)', f"{data['inputs']['initial_cf']:,.0f}"])
                    writer.writerow(['Growth Rate (%)', data['inputs']['growth_rate']])
                    writer.writerow(['Number of Years', data['inputs']['years']])
                    writer.writerow([])
                    
                    writer.writerow(['Year-by-Year Projections:'])
                    writer.writerow(['Year', 'Cash Flow ($)', 'Growth from Initial (%)'])
                    for i, projection in enumerate(data['results']['projections'], 1):
                        growth_pct = ((projection / data['inputs']['initial_cf']) - 1) * 100
                        writer.writerow([i, f"{projection:,.0f}", f"{growth_pct:.0f}%"])
                    
                    writer.writerow([])
                    writer.writerow(['Summary:'])
                    writer.writerow(['Total Cash Flow ($)', f"{data['results']['total_cf']:,.0f}"])
                    writer.writerow(['Average Annual CF ($)', f"{data['results']['avg_cf']:,.0f}"])
                    writer.writerow(['CAGR (%)', f"{data['results']['cagr']:.2%}"])
                
                elif data['type'] == 'bonds':
                    writer = csv.writer(csvfile)
                    writer.writerow(['Bond Valuation Report'])
                    writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                    writer.writerow([])
                    
                    writer.writerow(['Inputs:'])
                    writer.writerow(['Face Value ($)', f"{data['inputs']['face_value']:,.0f}"])
                    writer.writerow(['Coupon Rate (%)', data['inputs']['coupon_rate']])
                    writer.writerow(['Required Yield (%)', data['inputs']['yield_rate']])
                    writer.writerow(['Years to Maturity', data['inputs']['years_to_maturity']])
                    writer.writerow(['Payments per Year', data['inputs']['payments_per_year']])
                    writer.writerow([])
                    
                    writer.writerow(['Results:'])
                    writer.writerow(['Bond Price ($)', f"{data['results']['bond_price']:,.2f}"])
                    writer.writerow(['Current Yield (%)', f"{data['results']['current_yield']:.2%}"])
                    writer.writerow(['Duration (years)', f"{data['results']['duration']:.2f}"])
                    writer.writerow(['Annual Coupon ($)', f"{data['results']['coupon_payment']:,.2f}"])
            
            return True
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export to CSV:\n{str(e)}")
            return False
    
    def show_history_window(self):
        """Show calculation history window"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")
        history_window.geometry("600x400")
        history_window.configure(bg='#1c1c1e')
        
        # History list
        history_frame = tk.Frame(history_window, bg='#1c1c1e')
        history_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(history_frame, text="Recent Calculations", 
                font=('SF Pro Display', 16), bg='#1c1c1e', fg='white').pack(pady=(0, 10))
        
        # Scrollable list
        list_frame = tk.Frame(history_frame, bg='#1c1c1e')
        list_frame.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        history_listbox = tk.Listbox(
            list_frame, 
            yscrollcommand=scrollbar.set,
            bg='#333333',
            fg='white',
            font=('SF Pro Display', 11),
            selectbackground='#555555'
        )
        history_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=history_listbox.yview)
        
        # Populate history
        for entry in self.calculation_history:
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
            display_text = f"{timestamp} - {entry['type'].upper()}"
            history_listbox.insert(tk.END, display_text)
        
        # Buttons
        button_frame = tk.Frame(history_window, bg='#1c1c1e')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        def export_selected():
            selection = history_listbox.curselection()
            if selection:
                entry = self.calculation_history[selection[0]]
                filename = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                    title="Export Calculation"
                )
                if filename:
                    if self.export_to_csv(entry, filename):
                        messagebox.showinfo("Export Success", f"Calculation exported to {filename}")
        
        def load_selected():
            selection = history_listbox.curselection()
            if selection:
                entry = self.calculation_history[selection[0]]
                self.load_calculation(entry)
                history_window.destroy()
        
        tk.Button(button_frame, text="Load Selected", command=load_selected,
                 bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12)).pack(side='left', padx=5)
        tk.Button(button_frame, text="Export Selected", command=export_selected,
                 bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12)).pack(side='left', padx=5)
        tk.Button(button_frame, text="Close", command=history_window.destroy,
                 bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12)).pack(side='right', padx=5)
    
    def show_favorites_window(self):
        """Show favorites window"""
        favorites_window = tk.Toplevel(self.root)
        favorites_window.title("Favorite Calculations")
        favorites_window.geometry("600x400")
        favorites_window.configure(bg='#1c1c1e')
        
        # Favorites list
        favorites_frame = tk.Frame(favorites_window, bg='#1c1c1e')
        favorites_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(favorites_frame, text="Saved Calculations", 
                font=('SF Pro Display', 16), bg='#1c1c1e', fg='white').pack(pady=(0, 10))
        
        # Scrollable list
        list_frame = tk.Frame(favorites_frame, bg='#1c1c1e')
        list_frame.pack(fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        favorites_listbox = tk.Listbox(
            list_frame, 
            yscrollcommand=scrollbar.set,
            bg='#333333',
            fg='white',
            font=('SF Pro Display', 11),
            selectbackground='#555555'
        )
        favorites_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=favorites_listbox.yview)
        
        # Populate favorites
        for entry in self.favorites:
            favorites_listbox.insert(tk.END, entry['name'])
        
        # Buttons
        button_frame = tk.Frame(favorites_window, bg='#1c1c1e')
        button_frame.pack(fill='x', padx=10, pady=10)
        
        def load_selected():
            selection = favorites_listbox.curselection()
            if selection:
                entry = self.favorites[selection[0]]
                self.load_calculation(entry)
                favorites_window.destroy()
        
        def delete_selected():
            selection = favorites_listbox.curselection()
            if selection:
                if messagebox.askyesno("Confirm Delete", "Delete selected favorite?"):
                    del self.favorites[selection[0]]
                    self.save_favorites()
                    favorites_listbox.delete(selection[0])
        
        tk.Button(button_frame, text="Load Selected", command=load_selected,
                 bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12)).pack(side='left', padx=5)
        tk.Button(button_frame, text="Delete Selected", command=delete_selected,
                 bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12)).pack(side='left', padx=5)
        tk.Button(button_frame, text="Close", command=favorites_window.destroy,
                 bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12)).pack(side='right', padx=5)
    
    def load_calculation(self, entry):
        """Load a calculation from history or favorites"""
        calc_type = entry['type']
        inputs = entry['inputs']
        
        # Switch to appropriate mode
        self.switch_mode(calc_type)
        
        # Load inputs based on calculation type
        if calc_type == 'npv':
            self.rate_entry.delete(0, tk.END)
            self.rate_entry.insert(0, str(inputs['discount_rate']))
            
            self.cashflows_entry.delete("1.0", tk.END)
            self.cashflows_entry.insert("1.0", ', '.join(map(str, inputs['cash_flows'])))
        
        elif calc_type == 'dcf':
            self.dcf_cashflows_entry.delete("1.0", tk.END)
            self.dcf_cashflows_entry.insert("1.0", ', '.join(map(str, inputs['cash_flows'])))
            
            self.terminal_growth_entry.delete(0, tk.END)
            self.terminal_growth_entry.insert(0, str(inputs['terminal_growth']))
            
            self.wacc_entry.delete(0, tk.END)
            self.wacc_entry.insert(0, str(inputs['discount_rate']))
        
        elif calc_type == 'cashflow':
            self.initial_cf_entry.delete(0, tk.END)
            self.initial_cf_entry.insert(0, str(inputs['initial_cf']))
            
            self.growth_cf_entry.delete(0, tk.END)
            self.growth_cf_entry.insert(0, str(inputs['growth_rate']))
            
            self.years_entry.delete(0, tk.END)
            self.years_entry.insert(0, str(inputs['years']))
        
        elif calc_type == 'bonds':
            self.face_value_entry.delete(0, tk.END)
            self.face_value_entry.insert(0, str(inputs['face_value']))
            
            self.coupon_rate_entry.delete(0, tk.END)
            self.coupon_rate_entry.insert(0, str(inputs['coupon_rate']))
            
            self.yield_rate_entry.delete(0, tk.END)
            self.yield_rate_entry.insert(0, str(inputs['yield_rate']))
            
            self.maturity_entry.delete(0, tk.END)
            self.maturity_entry.insert(0, str(inputs['years_to_maturity']))
            
            self.payment_freq_entry.delete(0, tk.END)
            self.payment_freq_entry.insert(0, str(inputs['payments_per_year']))
        
        messagebox.showinfo("Calculation Loaded", f"Loaded {calc_type.upper()} calculation from {entry.get('name', 'history')}")
    
    def export_current_calculation(self):
        """Export the current calculation results"""
        if self.current_mode == "basic":
            messagebox.showinfo("Export Info", "Basic calculator mode doesn't have exportable calculations.\n\nPlease use NPV, DCF, Cash Flow, or Bond modes for export functionality.")
            return
        
        if not hasattr(self, 'last_calculation_data') or not self.last_calculation_data:
            messagebox.showwarning("No Data", "No calculation results to export.\n\nPlease perform a calculation first.")
            return
        
        # Ask user for export options
        export_window = tk.Toplevel(self.root)
        export_window.title("Export Options")
        export_window.geometry("300x200")
        export_window.configure(bg='#1c1c1e')
        export_window.transient(self.root)
        export_window.grab_set()
        
        tk.Label(export_window, text="Export Current Calculation", 
                font=('SF Pro Display', 14), bg='#1c1c1e', fg='white').pack(pady=10)
        
        button_frame = tk.Frame(export_window, bg='#1c1c1e')
        button_frame.pack(expand=True)
        
        def export_csv():
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Export to CSV"
            )
            if filename:
                if self.export_to_csv(self.last_calculation_data, filename):
                    messagebox.showinfo("Export Success", f"Calculation exported to {filename}")
                export_window.destroy()
        
        def save_favorite():
            name = simpledialog.askstring("Save Favorite", "Enter a name for this calculation:")
            if name:
                self.add_to_favorites(
                    self.last_calculation_data['type'],
                    self.last_calculation_data['inputs'],
                    self.last_calculation_data['results'],
                    name
                )
            export_window.destroy()
        
        tk.Button(button_frame, text="📄 Export to CSV", command=export_csv,
                 bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12), 
                 width=15).pack(pady=5)
        
        tk.Button(button_frame, text="⭐ Save as Favorite", command=save_favorite,
                 bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12), 
                 width=15).pack(pady=5)
        
        tk.Button(button_frame, text="Cancel", command=export_window.destroy,
                 bg='#d4d4d2', fg='#1c1c1e', font=('SF Pro Display', 12), 
                 width=15).pack(pady=5)
    
    def save_calculation_data(self, calc_type, inputs, results):
        """Save calculation data for export and history"""
        self.last_calculation_data = {
            'type': calc_type,
            'inputs': inputs,
            'results': results
        }
        
        # Add to history
        self.add_to_history(calc_type, inputs, results)