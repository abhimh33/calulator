# 💎 Advanced Calculator Pro

A comprehensive PyQt5 calculator with scientific functions, memory operations, base conversion, multiple themes, keyboard support, and persistent history.

## ✨ Features

### **Basic Operations**
- Addition, Subtraction, Multiplication, Division
- Power operations (x², x³, x^y)
- Square root (√), Cube root (³√)
- Pi (π) constant

### **Scientific Functions**
- **Trigonometric**: sin, cos, tan
- **Logarithmic**: log₁₀, ln (natural log)
- **Special**: Factorial (!), e constant, 1/x
- **Parentheses** support for complex expressions

### **Memory Functions**
- M+ (Add to memory)
- M- (Subtract from memory)
- MR (Recall memory)
- MC (Clear memory)
- Real-time memory display

### **Base Conversion**
- Convert to/from Hexadecimal (HEX)
- Convert to/from Binary (BIN)
- Convert to/from Octal (OCT)
- Convert to/from Decimal (DEC)

### **History Management**
- 📊 Full calculation history with timestamps
- Click any history item to load it
- Save history to JSON file (persists between sessions)
- Copy calculations to clipboard
- Clear history option

### **Keyboard Support**
- Type numbers directly: 0-9
- Operators: +, -, *, /
- Enter/Return: Calculate
- Backspace: Delete last character
- Escape: Clear display
- Ctrl+Z: Undo
- Ctrl+Y: Redo
- Parentheses: ( )

### **Undo/Redo**
- Full undo/redo stack
- Navigate through calculation history
- Works with all operations

### **Multiple Themes**
- 🌙 Dark Blue (default)
- 🌙 Dark Purple
- 🌙 Dark Green
- ☀ Light theme
- 🌊 Ocean theme
- Toggle button for quick dark/light switch
- Theme selector dropdown

### **Professional UI**
- Tabbed interface (Basic, Scientific, Advanced)
- Responsive design
- Smooth button animations
- Large, readable display (28pt font)
- Real-time validation

## 📋 Requirements

- Python 3.7+
- PyQt5 5.15.10

## ⚡ Installation

1. Clone or download the project
   ```
   cd D:\Calculator
   ```

2. Install dependencies
   ```
   pip install -r requirements.txt
   ```

## 🚀 Running the Calculator

```bash
python calculator.py
```

## 🎮 Usage Guide

### **Basic Calculations**
1. Click number buttons to enter values
2. Click operator buttons (+, -, ×, ÷)
3. Press = or Enter to calculate
4. Use DEL to delete last character, C to clear all

### **Scientific Mode**
- Click "Scientific" tab for advanced functions
- Use sin, cos, tan for trigonometric functions
- Use log, ln for logarithmic functions
- Use x^y for any power operation

### **Memory Operations**
- Click "Advanced" tab
- Enter a number and click M+ to add to memory
- Use M- to subtract, MR to recall, MC to clear
- Memory value displayed in real-time

### **Base Conversion**
- Enter a number and click HEX, BIN, or OCT to convert
- Click DEC to convert back to decimal
- Useful for programming and technical calculations

### **Keyboard Usage**
- Type directly without clicking buttons
- Numbers: 0-9
- Operators: + - * / ( )
- Calculate: Enter or Return
- Undo: Ctrl+Z
- Redo: Ctrl+Y

### **History**
- All calculations automatically saved
- Click any history item to load it into display
- Copy button: Copy selected history to clipboard
- Clear button: Delete all history
- History persists between sessions (stored in JSON)

## 🎨 Theme Selection

### Method 1: Theme Toggle Button
- Click the 🌙/☀ button to toggle dark/light

### Method 2: Theme Selector
- Go to "Advanced" tab
- Use the "Themes" dropdown to select from 5 themes

## 🔧 Keyboard Shortcuts

| Key | Function |
|-----|----------|
| 0-9 | Number input |
| . | Decimal point |
| + - * / | Operators |
| ( ) | Parentheses |
| Enter | Calculate |
| Backspace | Delete last character |
| Escape | Clear display |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |

## 📊 Calculation Examples

| Operation | Input | Result |
|-----------|-------|--------|
| Basic | 15 + 25 = | 40 |
| Power | 2 ^ 10 = | 1024 |
| Square Root | √16 = | 4 |
| Sin | sin(π/2) = | 1 |
| Factorial | 5! = | 120 |
| Hex Conversion | 255 → HEX | 0xff |
| Binary | 10 → BIN | 0b1010 |

## 💾 Data Storage

- History is automatically saved to `calculator_history.json`
- JSON file stores all calculations with timestamps
- History loads automatically on startup

## 🔒 Security

- `.gitignore` configured to exclude:
  - Python cache and compiled files
  - Virtual environments
  - IDE settings
  - Log files
  - Sensitive environment variables

## 📝 File Structure

```
D:\Calculator/
├── calculator.py           # Main application
├── calculator_history.json # Auto-generated history file
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

## 🐛 Troubleshooting

### Issue: "Error: Invalid expression"
- Check for mismatched parentheses
- Ensure all operators are valid
- Try using the Scientific tab for complex functions

### Issue: History not saving
- Check write permissions in the folder
- Ensure `calculator_history.json` is not corrupted
- Delete and recreate the file if needed

### Issue: Keyboard not responding
- Click on the calculator window to ensure it has focus
- Some shortcuts may conflict with OS shortcuts

## 🎯 Future Enhancements

- Unit converter (length, weight, temperature)
- Statistics calculations (mean, median, std dev)
- Graph plotting for functions
- Custom function definitions
- Dark mode animation
- Sound effects for operations

## 📄 License

Free to use and modify!

## 👨‍💻 Author

Created with PyQt5 - A responsive, modern Python calculator

---

**Enjoy your advanced calculator! 🎉**

