# 💎 Modern Calculator Pro

A sleek PyQt5 calculator with a classic calculator layout, scientific functions, memory operations, base conversion, dark/light theme toggle, keyboard support, and persistent calculation history.

## ✨ Features

### **Classic Calculator Layout**
- Clean, intuitive button layout
- Dark gray number buttons (0-9)
- Light gray function buttons (C, ÷, %)
- Orange operator buttons (+, -, ×, =)
- Parentheses buttons for complex expressions

### **Basic Operations**
- Addition (+), Subtraction (-), Multiplication (×), Division (÷)
- Percentage (%)
- Decimal support
- Power operations (x²) via sidebar

### **Scientific Functions** (Right Sidebar)
- **Trigonometric**: sin, cos, ln
- **Square Root**: √
- **Factorial**: !
- **Power**: x²
- Easy access from right panel

### **Memory Functions**
- M+ (Add to memory)
- M- (Subtract from memory)
- MR (Recall memory)
- Real-time memory display

### **Base Conversion**
- Convert to Hexadecimal (HEX)
- Convert to Binary (BIN)
- Convert to Octal (OCT)
- Quick conversion buttons

### **History Management**
- 📊 Full calculation history with timestamps
- Click any history item to load it into display
- Save history to JSON file (auto-saves, persists between sessions)
- Copy button to copy selected history
- Clear history option

### **Dark/Light Theme Toggle**
- 🌙 **Dark Theme** (Default) - Professional dark background
- ☀️ **Light Theme** - Clean bright background
- Toggle button in last row (changes icon based on active theme)
- All UI elements update instantly

### **Keyboard Support**
- Type numbers directly: 0-9
- Decimal point: .
- Operators: +, -, *, /
- Parentheses: ( )
- Enter/Return: Calculate
- Backspace: Delete last character
- Escape: Clear display
- Ctrl+Z: Undo
- Ctrl+Y: Redo

### **Professional UI**
- Responsive design
- Large, readable display (32pt font)
- Smooth button interactions with hover effects
- Intuitive right sidebar with functions and history
- Clean dark/light themes

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
4. Use C to clear all, ( ) for complex expressions
### **Scientific Mode**
- Click function buttons in right sidebar (√, sin, cos, ln, x², !)
- All functions appear in sidebar panel
- Example: Click √ → enter 16 → press = → Result: 4

### **Memory Operations**
- Enter a number, click M+ to add to memory
- M- to subtract from memory
- MR to recall stored value
- Memory value displayed in real-time

### **Base Conversion**
- Enter a decimal number
- Click HEX, BIN, or OCT to convert
- Result shows in that number base
- Example: 255 → HEX → 0xff

### **History Panel**
- All calculations auto-saved with timestamps
- Click any history item to reload it
- Copy button to copy to clipboard
- Clear button to delete all history

### **Theme Toggle**
- Click 🌙/☀️ button in last row to switch themes
- Icon changes between moon (dark) and sun (light)
- Everything updates instantly
- Your preference is saved

## 🎨 Button Layout

```
C      ÷      %      +
7      8      9      ×
4      5      6      -
1      2      3      ⌫
0           .        =
(      )           🌙/☀️
```

**Legend:**
- **Dark gray buttons**: Numbers (0-9), Decimal (.)
- **Light gray buttons**: Clear (C), Division (÷), Percentage (%), Backspace (⌫)
- **Orange buttons**: Operators (+, -, ×, =)
- **Last row**: Parentheses and theme toggle

## ⌨️ Keyboard Shortcuts

| Key | Function |
|-----|----------|
| 0-9 | Number input |
| . | Decimal point |
| + - * / | Operators |
| ( ) | Parentheses |
| Enter | Calculate |
| Backspace | Delete last |
| Escape | Clear all |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |

## 📊 Example Calculations

| Input | Result |
|-------|--------|
| 15 + 25 = | 40 |
| 10 × 5 = | 50 |
| 100 ÷ 4 = | 25 |
| √16 = | 4 |
| sin(90) = | 1 |
| 5! = | 120 |
| 255 → HEX | 0xff |
| (5 + 3) × 2 = | 16 |

## 💾 Data Storage

- History automatically saved to `calculator_history.json`
- History loads on startup
- Theme preference not persisted (resets to dark on restart)

## 🔒 Security

- `.gitignore` configured to exclude sensitive files
- No data collection or external calls
- All calculations are local

## 📁 File Structure

```
D:\Calculator/
├── calculator.py           # Main application
├── calculator_history.json # Auto-generated history
├── requirements.txt        # Dependencies
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

## 🐛 Troubleshooting

**Issue: "Error: Invalid expression"**
- Check for balanced parentheses
- Ensure all operators are valid
- Verify decimal numbers are formatted correctly

**Issue: Theme doesn't change**
- Close and reopen the calculator
- Check if dark/light mode toggle is working

**Issue: History not loading**
- Ensure `calculator_history.json` exists
- Check write permissions in the folder

## 🎯 Features

✅ Classic calculator design  
✅ Scientific functions in sidebar  
✅ Memory operations  
✅ Base conversion (HEX, BIN, OCT)  
✅ Dark/Light theme toggle  
✅ Calculation history  
✅ Keyboard support  
✅ Undo/Redo functionality  
✅ Persistent history (JSON)  
✅ No external dependencies  

## 📄 License

Free to use and modify!

---

**Enjoy your modern calculator! 🎉**

