import sys
import math
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QListWidget, 
                             QListWidgetItem, QSplitter, QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

class CalcButton(QPushButton):
    """Custom calculator button with proper styling"""
    def __init__(self, text, callback, button_type="number"):
        super().__init__(text)
        self.button_type = button_type
        self.clicked.connect(callback)
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.setMinimumHeight(60)
        self.setMinimumWidth(60)
        self.apply_style()
    
    def apply_style(self):
        """Apply button styling based on type"""
        if self.button_type == "operator":  # Orange buttons
            self.setStyleSheet("""
                CalcButton {
                    background-color: #FF6B35;
                    border: none;
                    border-radius: 8px;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                }
                CalcButton:hover {
                    background-color: #FF5520;
                }
                CalcButton:pressed {
                    background-color: #E55A2B;
                }
            """)
        elif self.button_type == "function":  # Light gray buttons
            self.setStyleSheet("""
                CalcButton {
                    background-color: #9E9E9E;
                    border: none;
                    border-radius: 8px;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                }
                CalcButton:hover {
                    background-color: #B0B0B0;
                }
                CalcButton:pressed {
                    background-color: #8C8C8C;
                }
            """)
        else:  # Number buttons - Dark gray
            self.setStyleSheet("""
                CalcButton {
                    background-color: #424242;
                    border: none;
                    border-radius: 8px;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                }
                CalcButton:hover {
                    background-color: #545454;
                }
                CalcButton:pressed {
                    background-color: #303030;
                }
            """)


class EnhancedCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💎 Calculator Pro")
        self.setGeometry(100, 100, 900, 750)
        self.setMinimumSize(500, 650)
        
        # Calculator state
        self.expression = ""
        self.memory = 0
        self.history_list = []
        self.undo_stack = []
        self.redo_stack = []
        self.dark_mode = True
        
        # History file
        self.history_file = "calculator_history.json"
        self.load_history()
        
        # Initialize UI
        self.init_ui()
        self.apply_theme()
        self.setup_keyboard()
    
    def init_ui(self):
        """Initialize the user interface"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout(main_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Left side - Calculator
        calc_widget = QWidget()
        calc_layout = QVBoxLayout(calc_widget)
        calc_layout.setSpacing(8)
        calc_layout.setContentsMargins(0, 0, 0, 0)
        
        # Display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Segoe UI", 32, QFont.Bold))
        self.display.setMinimumHeight(80)
        self.display.setText("0")
        calc_layout.addWidget(self.display)
        
        # Button grid - exactly like the image
        grid = QVBoxLayout()
        grid.setSpacing(8)
        
        # Row 1: C, ÷, %, +
        row1 = QHBoxLayout()
        row1.setSpacing(8)
        row1.addWidget(CalcButton("C", self.clear_display, "function"))
        row1.addWidget(CalcButton("÷", lambda: self.append_operator("/"), "function"))
        row1.addWidget(CalcButton("%", lambda: self.append_operator("%"), "function"))
        row1.addWidget(CalcButton("+", lambda: self.append_operator("+"), "operator"))
        grid.addLayout(row1)
        
        # Row 2: 7, 8, 9, ×
        row2 = QHBoxLayout()
        row2.setSpacing(8)
        row2.addWidget(CalcButton("7", lambda: self.append_value("7"), "number"))
        row2.addWidget(CalcButton("8", lambda: self.append_value("8"), "number"))
        row2.addWidget(CalcButton("9", lambda: self.append_value("9"), "number"))
        row2.addWidget(CalcButton("×", lambda: self.append_operator("*"), "operator"))
        grid.addLayout(row2)
        
        # Row 3: 4, 5, 6, -
        row3 = QHBoxLayout()
        row3.setSpacing(8)
        row3.addWidget(CalcButton("4", lambda: self.append_value("4"), "number"))
        row3.addWidget(CalcButton("5", lambda: self.append_value("5"), "number"))
        row3.addWidget(CalcButton("6", lambda: self.append_value("6"), "number"))
        row3.addWidget(CalcButton("-", lambda: self.append_operator("-"), "operator"))
        grid.addLayout(row3)
        
        # Row 4: 1, 2, 3, Backspace
        row4 = QHBoxLayout()
        row4.setSpacing(8)
        row4.addWidget(CalcButton("1", lambda: self.append_value("1"), "number"))
        row4.addWidget(CalcButton("2", lambda: self.append_value("2"), "number"))
        row4.addWidget(CalcButton("3", lambda: self.append_value("3"), "number"))
        row4.addWidget(CalcButton("⌫", self.delete_last, "function"))
        grid.addLayout(row4)
        
        # Row 5: 0 (wide), ., =
        row5 = QHBoxLayout()
        row5.setSpacing(8)
        zero_btn = CalcButton("0", lambda: self.append_value("0"), "number")
        zero_btn.setMinimumWidth(140)  # Make 0 wider
        row5.addWidget(zero_btn)
        row5.addWidget(CalcButton(".", lambda: self.append_value("."), "number"))
        row5.addWidget(CalcButton("=", self.calculate, "operator"))
        grid.addLayout(row5)
        
        # Row 6: ( and )
        row6 = QHBoxLayout()
        row6.setSpacing(8)
        paren_open = CalcButton("(", lambda: self.append_value("("), "number")
        paren_close = CalcButton(")", lambda: self.append_value(")"), "number")
        self.theme_toggle_btn = CalcButton("🌙", self.toggle_theme, "function")
        
        row6.addWidget(paren_open, 1)
        row6.addWidget(paren_close, 1)
        row6.addWidget(self.theme_toggle_btn, 1)
        grid.addLayout(row6)
        
        calc_layout.addLayout(grid)
        calc_layout.addStretch()
        
        # Right side - History and functions
        right_widget = self.create_right_panel()
        
        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(calc_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
    
    def create_right_panel(self):
        """Create right panel with history and advanced functions"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # History section
        history_label = QLabel("📊 History")
        history_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        history_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(history_label)
        
        self.history_widget = QListWidget()
        self.history_widget.setFont(QFont("Segoe UI", 9))
        self.history_widget.setSpacing(2)
        self.history_widget.itemClicked.connect(self.load_from_history)
        layout.addWidget(self.history_widget)
        
        # History buttons
        hist_btn_layout = QHBoxLayout()
        hist_btn_layout.setSpacing(6)
        hist_btn_layout.addWidget(CalcButton("Copy", self.copy_to_clipboard, "function"))
        hist_btn_layout.addWidget(CalcButton("Clear", self.clear_history, "function"))
        layout.addLayout(hist_btn_layout)
        
        # Advanced functions
        adv_label = QLabel("Functions")
        adv_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        adv_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(adv_label)
        
        # Scientific row 1
        sci_row1 = QHBoxLayout()
        sci_row1.setSpacing(6)
        sci_row1.addWidget(CalcButton("√", lambda: self.append_function("sqrt"), "function"))
        sci_row1.addWidget(CalcButton("sin", lambda: self.append_function("sin"), "function"))
        sci_row1.addWidget(CalcButton("cos", lambda: self.append_function("cos"), "function"))
        layout.addLayout(sci_row1)
        
        # Scientific row 2
        sci_row2 = QHBoxLayout()
        sci_row2.setSpacing(6)
        sci_row2.addWidget(CalcButton("ln", lambda: self.append_function("ln"), "function"))
        sci_row2.addWidget(CalcButton("x²", lambda: self.append_function("pow2"), "function"))
        sci_row2.addWidget(CalcButton("!", lambda: self.append_function("fact"), "function"))
        layout.addLayout(sci_row2)
        
        # Memory section
        mem_label = QLabel("Memory")
        mem_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        mem_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(mem_label)
        
        self.mem_display = QLineEdit()
        self.mem_display.setReadOnly(True)
        self.mem_display.setFont(QFont("Segoe UI", 10))
        self.mem_display.setText(f"M: {self.memory}")
        layout.addWidget(self.mem_display)
        
        mem_row = QHBoxLayout()
        mem_row.setSpacing(6)
        mem_row.addWidget(CalcButton("M+", self.memory_add, "function"))
        mem_row.addWidget(CalcButton("M-", self.memory_sub, "function"))
        mem_row.addWidget(CalcButton("MR", self.memory_recall, "function"))
        layout.addLayout(mem_row)
        
        # Base conversion
        base_label = QLabel("Base")
        base_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        base_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(base_label)
        
        base_row = QHBoxLayout()
        base_row.setSpacing(6)
        base_row.addWidget(CalcButton("HEX", self.to_hex, "function"))
        base_row.addWidget(CalcButton("BIN", self.to_binary, "function"))
        base_row.addWidget(CalcButton("OCT", self.to_octal, "function"))
        layout.addLayout(base_row)
        
        layout.addStretch()
        return widget
    
    def append_value(self, value):
        """Append a value to expression"""
        if self.expression == "0":
            self.expression = str(value)
        else:
            self.expression += str(value)
        self.update_display()
    
    def append_operator(self, operator):
        """Append an operator"""
        if self.expression and not self.expression.endswith((" + ", " - ", " * ", " / ", " ** ")):
            if operator == "**":
                self.expression += " ** "
            else:
                self.expression += f" {operator} "
        self.update_display()
    
    def append_function(self, func):
        """Append a mathematical function"""
        if func == "sqrt":
            self.expression += "sqrt("
        elif func == "sin":
            self.expression += "sin("
        elif func == "cos":
            self.expression += "cos("
        elif func == "tan":
            self.expression += "tan("
        elif func == "log":
            self.expression += "log10("
        elif func == "ln":
            self.expression += "log("
        elif func == "fact":
            self.expression += "factorial("
        elif func == "cbrt":
            self.expression += "cbrt("
        elif func == "pow2":
            if self.expression:
                self.expression = f"({self.expression})**2"
        elif func == "pow3":
            if self.expression:
                self.expression = f"({self.expression})**3"
        elif func == "inv":
            if self.expression:
                self.expression = f"1/({self.expression})"
        self.update_display()
    
    def update_display(self):
        """Update the display"""
        self.display.setText(self.expression if self.expression else "0")
    
    def clear_display(self):
        """Clear display"""
        self.undo_stack.append(self.expression)
        self.redo_stack.clear()
        self.expression = ""
        self.update_display()
    
    def delete_last(self):
        """Delete last character"""
        self.expression = self.expression[:-1]
        self.update_display()
    
    def calculate(self):
        """Calculate expression"""
        try:
            if not self.expression:
                return
            
            # Save to undo stack
            self.undo_stack.append(self.expression)
            self.redo_stack.clear()
            
            calc_expr = (self.expression
                        .replace("×", "*")
                        .replace("÷", "/")
                        .replace("sqrt(", "math.sqrt(")
                        .replace("sin(", "math.sin(")
                        .replace("cos(", "math.cos(")
                        .replace("tan(", "math.tan(")
                        .replace("log10(", "math.log10(")
                        .replace("log(", "math.log(")
                        .replace("factorial(", "math.factorial(")
                        .replace("cbrt(", "cbrt("))
            
            # Define custom functions
            def cbrt(x):
                return x ** (1/3)
            
            result = eval(calc_expr, {"__builtins__": {}}, 
                         {"math": math, "cbrt": cbrt})
            
            if isinstance(result, float):
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 10)
            
            # Add to history
            timestamp = datetime.now().strftime("%H:%M:%S")
            history_entry = f"{self.expression} = {result}"
            self.history_list.append(history_entry)
            
            item = QListWidgetItem(f"[{timestamp}] {history_entry}")
            self.history_widget.insertItem(0, item)
            
            # Save history to file
            self.save_history()
            
            self.expression = str(result)
            self.update_display()
            
        except ZeroDivisionError:
            self.display.setText("Error: Division by zero")
            self.expression = ""
        except Exception as e:
            self.display.setText("Error: Invalid expression")
            self.expression = ""
    
    def memory_add(self):
        """Add current value to memory"""
        try:
            if self.expression:
                self.memory += float(eval(self.expression))
                self.mem_display.setText(f"Memory: {self.memory}")
        except:
            pass
    
    def memory_sub(self):
        """Subtract current value from memory"""
        try:
            if self.expression:
                self.memory -= float(eval(self.expression))
                self.mem_display.setText(f"Memory: {self.memory}")
        except:
            pass
    
    def memory_recall(self):
        """Recall memory value"""
        self.expression = str(self.memory)
        self.update_display()
    
    def memory_clear(self):
        """Clear memory"""
        self.memory = 0
        self.mem_display.setText(f"Memory: {self.memory}")
    
    def to_hex(self):
        """Convert to hexadecimal"""
        try:
            if self.expression:
                val = int(float(eval(self.expression)))
                self.expression = hex(val)
                self.update_display()
        except:
            pass
    
    def to_binary(self):
        """Convert to binary"""
        try:
            if self.expression:
                val = int(float(eval(self.expression)))
                self.expression = bin(val)
                self.update_display()
        except:
            pass
    
    def to_octal(self):
        """Convert to octal"""
        try:
            if self.expression:
                val = int(float(eval(self.expression)))
                self.expression = oct(val)
                self.update_display()
        except:
            pass
    
    def to_decimal(self):
        """Convert to decimal"""
        try:
            if self.expression:
                val = int(self.expression, 0)
                self.expression = str(val)
                self.update_display()
        except:
            pass
    
    def undo(self):
        """Undo last operation"""
        if self.undo_stack:
            self.redo_stack.append(self.expression)
            self.expression = self.undo_stack.pop()
            self.update_display()
    
    def redo(self):
        """Redo operation"""
        if self.redo_stack:
            self.undo_stack.append(self.expression)
            self.expression = self.redo_stack.pop()
            self.update_display()
    
    def load_from_history(self, item):
        """Load calculation from history"""
        text = item.text()
        # Extract the expression part
        if " = " in text:
            expr = text.split(" = ")[0]
            # Remove timestamp
            if "] " in expr:
                expr = expr.split("] ", 1)[1]
            self.expression = expr
            self.update_display()
    
    def copy_to_clipboard(self):
        """Copy current value to clipboard"""
        if self.history_widget.currentItem():
            text = self.history_widget.currentItem().text()
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(self, "Copied", "Copied to clipboard!")
    
    def clear_history(self):
        """Clear history"""
        self.history_widget.clear()
        self.history_list = []
        self.save_history()
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        self.dark_mode = not self.dark_mode
        # Update button icon based on theme
        if self.dark_mode:
            self.theme_toggle_btn.setText("🌙")
        else:
            self.theme_toggle_btn.setText("☀️")
        self.apply_theme()
    
    def on_theme_changed(self, theme_name):
        """Change theme by selection"""
        pass
    
    def apply_theme(self):
        """Apply dark or light theme to calculator"""
        if self.dark_mode:
            # Dark theme
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1a1a1a;
                }
                QLineEdit {
                    background-color: #2a2a2a;
                    color: #ffffff;
                    border: 2px solid #3a3a3a;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 32px;
                    font-weight: bold;
                }
                QLabel {
                    color: #ffffff;
                }
                QListWidget {
                    background-color: #2a2a2a;
                    color: #ffffff;
                    border: 2px solid #3a3a3a;
                    border-radius: 8px;
                    padding: 8px;
                }
                QListWidget::item {
                    padding: 5px;
                    border-radius: 4px;
                }
                QListWidget::item:hover {
                    background-color: #3a3a3a;
                }
                QListWidget::item:selected {
                    background-color: #FF6B35;
                    color: #ffffff;
                }
            """)
        else:
            # Light theme
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f5f5f5;
                }
                QLineEdit {
                    background-color: #ffffff;
                    color: #1a1a1a;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 32px;
                    font-weight: bold;
                }
                QLabel {
                    color: #1a1a1a;
                }
                QListWidget {
                    background-color: #ffffff;
                    color: #1a1a1a;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                    padding: 8px;
                }
                QListWidget::item {
                    padding: 5px;
                    border-radius: 4px;
                }
                QListWidget::item:hover {
                    background-color: #f0f0f0;
                }
                QListWidget::item:selected {
                    background-color: #FF6B35;
                    color: #ffffff;
                }
            """)
    
    def setup_keyboard(self):
        """Setup keyboard event handling"""
        pass
    
    def keyPressEvent(self, event):
        """Handle keyboard input"""
        key = event.text()
        
        if key.isdigit():
            self.append_value(key)
        elif key == ".":
            self.append_value(".")
        elif key == "+":
            self.append_operator("+")
        elif key == "-":
            self.append_operator("-")
        elif key == "*":
            self.append_operator("*")
        elif key == "/":
            self.append_operator("/")
        elif key == "(" or key == ")":
            self.append_value(key)
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.calculate()
        elif event.key() == Qt.Key_Backspace:
            self.delete_last()
        elif event.key() == Qt.Key_Escape:
            self.clear_display()
        elif event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self.undo()
        elif event.key() == Qt.Key_Y and event.modifiers() == Qt.ControlModifier:
            self.redo()
    
    def save_history(self):
        """Save history to JSON file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history_list, f)
        except:
            pass
    
    def load_history(self):
        """Load history from JSON file"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.history_list = json.load(f)
        except:
            self.history_list = []


def main():
    app = QApplication(sys.argv)
    calculator = EnhancedCalculator()
    calculator.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
