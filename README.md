# Investment Finance Calculator

A comprehensive Python-based finance calculator app inspired by the iPhone calculator, but designed specifically for investment analysis and corporate valuation. This professional-grade tool combines familiar calculator interface with advanced financial modeling capabilities.

## 🚀 Features

### 🧮 Basic Calculator
- Standard arithmetic operations (+, -, ×, ÷)
- Percentage calculations
- Sign toggle (±)
- Clear function
- Chain calculations support
- iPhone-inspired dark theme interface

### 📊 NPV Calculator
- **Net Present Value (NPV)** calculation with multiple cash flows
- **Internal Rate of Return (IRR)** using Newton-Raphson method
- **Payback Period** analysis with fractional year precision
- Comprehensive results display with all three metrics
- Support for irregular cash flow patterns

### 🏢 DCF Valuation
- **Discounted Cash Flow** modeling for enterprise valuation
- **Terminal Value** calculation with perpetual growth
- **Present Value** breakdown of cash flows vs terminal value
- **Enterprise Value** estimation
- WACC integration for discount rate
- Scrollable interface for detailed inputs

### 💰 Cash Flow Projections
- **Multi-year cash flow forecasting** with compound growth
- **Growth rate modeling** with customizable parameters
- **CAGR (Compound Annual Growth Rate)** calculation
- **Summary statistics** including total and average cash flows
- Year-by-year detailed projections display

### 🏦 Bond Valuation
- **Bond Price** calculation with semi-annual or custom payment frequency
- **Yield to Maturity (YTM)** analysis using numerical methods
- **Duration** calculation (Macaulay duration)
- **Current Yield** and coupon payment analysis
- **Premium/Discount/Par** status determination
- Support for various payment frequencies (annual, semi-annual, quarterly)

## 🛠 Installation

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)
- NumPy for financial calculations

### Setup
1. Clone or download the project files
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the calculator:
   ```bash
   python main.py
   ```

## 📱 Usage Guide

### Getting Started
Launch the calculator and use the mode selector buttons at the top to switch between different calculation types:

- **Basic**: Standard calculator functionality
- **NPV**: Net Present Value analysis
- **DCF**: Discounted Cash Flow valuation
- **Cash Flow**: Multi-year projections
- **Bonds**: Bond valuation and yield analysis

### Calculator Modes

#### **Basic Mode**
- Use number buttons (0-9) and operators (+, -, ×, ÷)
- Press "=" to calculate results
- "C" clears the display and resets calculator state
- "±" toggles the sign of the current number
- "%" converts the current number to percentage

#### **NPV Mode**
1. Enter **Discount Rate** as percentage (e.g., 10 for 10%)
2. Input **Cash Flows** separated by commas (e.g., -1000, 300, 400, 500)
   - First value typically represents initial investment (negative)
   - Subsequent values represent future cash inflows
3. Click **"Calculate NPV"** for comprehensive results including:
   - Net Present Value
   - Internal Rate of Return (IRR)
   - Payback Period

#### **DCF Mode**
1. Enter **Free Cash Flows** separated by commas (projected annual FCF)
2. Set **Terminal Growth Rate** as percentage (long-term growth assumption)
3. Input **Discount Rate/WACC** as percentage
4. Click **"Calculate DCF"** for enterprise valuation including:
   - Present Value of projected cash flows
   - Terminal value and its present value
   - Total enterprise value

#### **Cash Flow Mode**
1. Enter **Initial Cash Flow** amount in dollars
2. Set **Annual Growth Rate** as percentage
3. Specify **Number of Years** for projection
4. Click **"Project Cash Flows"** for detailed analysis:
   - Year-by-year cash flow projections
   - Total cumulative cash flows
   - Average annual cash flow
   - Compound Annual Growth Rate (CAGR)

#### **Bonds Mode**
1. **Bond Pricing**: Enter bond parameters and click "Calculate Bond Price"
   - **Face Value**: Par value of the bond (default: $1,000)
   - **Coupon Rate**: Annual coupon rate as percentage
   - **Required Yield**: Market yield/discount rate as percentage
   - **Years to Maturity**: Time until bond matures
   - **Payments per Year**: Frequency (2 for semi-annual, 1 for annual)

2. **YTM Calculation**: Click "Calculate YTM" and enter current market price
   - Calculates yield to maturity from market price
   - Determines if bond trades at premium, discount, or par

## 💡 Example Calculations

### NPV Analysis Example
```
Discount Rate: 10%
Cash Flows: -10000, 3000, 4000, 5000, 2000
Results:
- NPV: $1,169.87
- IRR: 13.93%
- Payback: 3.2 years
```

### DCF Valuation Example
```
Free Cash Flows: 500, 550, 600, 650
Terminal Growth: 2.5%
WACC: 10%
Results:
- Enterprise Value: $10,317
- PV of Cash Flows: $1,951
- PV of Terminal Value: $8,366
```

### Bond Valuation Example
```
Face Value: $1,000
Coupon Rate: 5%
Required Yield: 6%
Years to Maturity: 10
Results:
- Bond Price: $925.61
- Current Yield: 5.40%
- Duration: 7.89 years
- Status: Trading at Discount
```

### Cash Flow Projection Example
```
Initial Cash Flow: $100,000
Growth Rate: 8%
Years: 5
Results:
- Year 1: $108,000
- Year 2: $116,640
- Year 3: $125,971
- Year 4: $136,049
- Year 5: $146,933
- Total: $633,593
- CAGR: 8.00%
```

## 🏗 Technical Architecture

### File Structure
```
calculator/
├── main.py              # Main GUI application
├── finance_utils.py     # Financial calculation utilities
├── test_calculator.py   # Test suite for calculations
├── requirements.txt     # Python dependencies
└── README.md           # This documentation
```

### Key Components

#### **FinanceCalculator Class** (`main.py`)
- Main GUI application using tkinter
- Mode switching and interface management
- Button styling and event handling
- Results display and formatting

#### **FinancialCalculations Class** (`finance_utils.py`)
- Core financial calculation methods
- NPV, IRR, and payback period calculations
- DCF valuation with terminal value
- Bond pricing and yield calculations
- WACC, CAPM, and other financial metrics

### Design Features
- **Modular Architecture**: Separate GUI and calculation logic
- **Consistent Styling**: Uniform button colors and dark theme
- **Scrollable Interfaces**: Handle complex multi-input calculations
- **Error Handling**: Comprehensive input validation and error messages
- **Professional Results**: Formatted output with proper financial notation

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_calculator.py
```

Tests include:
- NPV calculations with manual verification
- DCF valuation scenarios
- WACC calculations
- Bond pricing and YTM analysis

## 🔧 Customization

### Adding New Financial Models
The modular design makes it easy to add new calculation modes:

1. Add calculation methods to `FinancialCalculations` class
2. Create new interface method in `FinanceCalculator` class
3. Update mode selector and switch logic
4. Add corresponding tests

### Styling Modifications
Button colors and themes can be easily modified in the `create_button()` method and UI setup functions.

## 🚀 Future Enhancements

### Planned Features
- **Options Pricing**: Black-Scholes model implementation
- **Portfolio Analysis**: Sharpe ratio and risk metrics
- **Mortgage Calculators**: Loan amortization schedules
- **Data Export**: CSV/Excel export functionality
- **Real-time Data**: API integration for current market rates

### Advanced Features
- **Sensitivity Analysis**: What-if scenarios and stress testing
- **Monte Carlo Simulations**: Risk modeling capabilities
- **Currency Conversion**: Multi-currency support
- **Calculation History**: Save and recall previous calculations

## 📄 License

This project is open source and available for educational and commercial use.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional financial models
- Enhanced user interface
- Performance optimizations
- Extended test coverage
- Documentation improvements

---

**Built with Python, tkinter, and NumPy**  
*Professional investment analysis made accessible*