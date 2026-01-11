import sys
import math
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QListWidget, 
                             QListWidgetItem, QSplitter, QLabel, QTabWidget,
                             QSpinBox, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QClipboard
from PyQt5.QtWidgets import QMessageBox

class AnimatedButton(QPushButton):
    """Custom button with animation effects"""
    def __init__(self, text, callback, color=None):
        super().__init__(text)
        self.base_color = color
        self.clicked.connect(callback)
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.setMinimumHeight(45)
        self.setStyleSheet(self.get_stylesheet())
    
    def get_stylesheet(self):
        if self.base_color:
            return f"""
                QPushButton {{
                    background-color: {self.base_color};
                    border: none;
                    border-radius: 10px;
                    color: white;
                    font-weight: bold;
                    padding: 5px;
                }}
                QPushButton:hover {{
                    background-color: {self.lighten_color(self.base_color)};
                    box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
                }}
                QPushButton:pressed {{
                    background-color: {self.darken_color(self.base_color)};
                    padding-top: 7px;
                }}
            """
        return """
            QPushButton {
                background-color: #3a3a3a;
                border: none;
                border-radius: 10px;
                color: white;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
                padding-top: 7px;
            }
        """
    
    @staticmethod
    def lighten_color(color):
        color = color.lstrip("#")
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(c + 40, 255) for c in rgb)
        return "#{:02x}{:02x}{:02x}".format(*rgb)
    
    @staticmethod
    def darken_color(color):
        color = color.lstrip("#")
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(max(c - 30, 0) for c in rgb)
        return "#{:02x}{:02x}{:02x}".format(*rgb)


class EnhancedCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💎 Advanced Calculator Pro")
        self.setGeometry(50, 50, 1400, 800)
        self.setMinimumSize(1200, 700)
        
        # Calculator state
        self.expression = ""
        self.memory = 0
        self.history_list = []
        self.undo_stack = []
        self.redo_stack = []
        self.dark_mode = True
        self.scientific_mode = False
        self.current_theme = "dark_blue"
        
        # History file
        self.history_file = "calculator_history.json"
        self.load_history()
        
        # Initialize UI
        self.init_ui()
        self.apply_theme()
        
        # Setup keyboard
        self.setup_keyboard()
    
    def init_ui(self):
        """Initialize the user interface"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QHBoxLayout(main_widget)
        
        # Left side - Calculator with tabs
        calc_widget = QWidget()
        calc_layout = QVBoxLayout(calc_widget)
        
        # Display
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.display.setMinimumHeight(70)
        self.display.setText("0")
        calc_layout.addWidget(self.display)
        
        # Tabs for Basic and Scientific
        self.tabs = QTabWidget()
        
        # Basic calculator tab
        basic_widget = self.create_basic_calculator()
        self.tabs.addTab(basic_widget, "Basic")
        
        # Scientific calculator tab
        scientific_widget = self.create_scientific_calculator()
        self.tabs.addTab(scientific_widget, "Scientific")
        
        # Memory and base conversion tab
        advanced_widget = self.create_advanced_panel()
        self.tabs.addTab(advanced_widget, "Advanced")
        
        calc_layout.addWidget(self.tabs)
        
        # Right side - History and memory panel
        right_widget = self.create_right_panel()
        
        # Splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(calc_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
    
    def create_basic_calculator(self):
        """Create basic calculator buttons"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(6)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Row 1
        row1 = QHBoxLayout()
        row1.setSpacing(6)
        row1.addWidget(AnimatedButton("C", self.clear_display, "#FF6B6B"))
        row1.addWidget(AnimatedButton("DEL", self.delete_last, "#FF9999"))
        row1.addWidget(AnimatedButton("√", lambda: self.append_function("sqrt"), "#4ECDC4"))
        row1.addWidget(AnimatedButton("π", lambda: self.append_value(str(math.pi)), "#4ECDC4"))
        layout.addLayout(row1)
        
        # Row 2
        row2 = QHBoxLayout()
        row2.setSpacing(6)
        row2.addWidget(AnimatedButton("7", lambda: self.append_value("7")))
        row2.addWidget(AnimatedButton("8", lambda: self.append_value("8")))
        row2.addWidget(AnimatedButton("9", lambda: self.append_value("9")))
        row2.addWidget(AnimatedButton("÷", lambda: self.append_operator("/"), "#95E1D3"))
        layout.addLayout(row2)
        
        # Row 3
        row3 = QHBoxLayout()
        row3.setSpacing(6)
        row3.addWidget(AnimatedButton("4", lambda: self.append_value("4")))
        row3.addWidget(AnimatedButton("5", lambda: self.append_value("5")))
        row3.addWidget(AnimatedButton("6", lambda: self.append_value("6")))
        row3.addWidget(AnimatedButton("×", lambda: self.append_operator("*"), "#95E1D3"))
        layout.addLayout(row3)
        
        # Row 4
        row4 = QHBoxLayout()
        row4.setSpacing(6)
        row4.addWidget(AnimatedButton("1", lambda: self.append_value("1")))
        row4.addWidget(AnimatedButton("2", lambda: self.append_value("2")))
        row4.addWidget(AnimatedButton("3", lambda: self.append_value("3")))
        row4.addWidget(AnimatedButton("-", lambda: self.append_operator("-"), "#95E1D3"))
        layout.addLayout(row4)
        
        # Row 5
        row5 = QHBoxLayout()
        row5.setSpacing(6)
        row5.addWidget(AnimatedButton("0", lambda: self.append_value("0")))
        row5.addWidget(AnimatedButton(".", lambda: self.append_value(".")))
        row5.addWidget(AnimatedButton("x²", lambda: self.append_function("pow2"), "#4ECDC4"))
        row5.addWidget(AnimatedButton("+", lambda: self.append_operator("+"), "#95E1D3"))
        layout.addLayout(row5)
        
        # Row 6
        row6 = QHBoxLayout()
        row6.setSpacing(6)
        equals_btn = AnimatedButton("=", self.calculate, "#FFD93D")
        equals_btn.setMinimumHeight(50)
        row6.addWidget(equals_btn, 2)
        row6.addWidget(AnimatedButton("Undo", self.undo, "#A8E6CF"))
        layout.addLayout(row6)
        
        layout.addStretch()
        return widget
    
    def create_scientific_calculator(self):
        """Create scientific calculator buttons"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(6)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Trigonometric functions
        trig_label = QLabel("Trigonometric")
        trig_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        layout.addWidget(trig_label)
        
        row1 = QHBoxLayout()
        row1.setSpacing(6)
        row1.addWidget(AnimatedButton("sin", lambda: self.append_function("sin"), "#FF6B6B"))
        row1.addWidget(AnimatedButton("cos", lambda: self.append_function("cos"), "#FF6B6B"))
        row1.addWidget(AnimatedButton("tan", lambda: self.append_function("tan"), "#FF6B6B"))
        row1.addWidget(AnimatedButton("1/x", lambda: self.append_function("inv"), "#FFB6C1"))
        layout.addLayout(row1)
        
        # Logarithmic functions
        log_label = QLabel("Logarithmic")
        log_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        layout.addWidget(log_label)
        
        row2 = QHBoxLayout()
        row2.setSpacing(6)
        row2.addWidget(AnimatedButton("log₁₀", lambda: self.append_function("log"), "#4ECDC4"))
        row2.addWidget(AnimatedButton("ln", lambda: self.append_function("ln"), "#4ECDC4"))
        row2.addWidget(AnimatedButton("e", lambda: self.append_value(str(math.e)), "#4ECDC4"))
        row2.addWidget(AnimatedButton("!", lambda: self.append_function("fact"), "#95E1D3"))
        layout.addLayout(row2)
        
        # Power functions
        power_label = QLabel("Power & Root")
        power_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        layout.addWidget(power_label)
        
        row3 = QHBoxLayout()
        row3.setSpacing(6)
        row3.addWidget(AnimatedButton("x^y", lambda: self.append_operator("**"), "#A8E6CF"))
        row3.addWidget(AnimatedButton("³√", lambda: self.append_function("cbrt"), "#A8E6CF"))
        row3.addWidget(AnimatedButton("x^3", lambda: self.append_function("pow3"), "#A8E6CF"))
        row3.addWidget(AnimatedButton("(", lambda: self.append_value("("), "#FFB6C1"))
        layout.addLayout(row3)
        
        row4 = QHBoxLayout()
        row4.setSpacing(6)
        row4.addWidget(AnimatedButton(")", lambda: self.append_value(")"), "#FFB6C1"))
        row4.addWidget(AnimatedButton("C", self.clear_display, "#FF6B6B"))
        row4.addWidget(AnimatedButton("DEL", self.delete_last, "#FF9999"))
        row4.addWidget(AnimatedButton("=", self.calculate, "#FFD93D"))
        layout.addLayout(row4)
        
        layout.addStretch()
        return widget
    
    def create_advanced_panel(self):
        """Create advanced features panel"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Memory section
        mem_label = QLabel("Memory Functions")
        mem_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        layout.addWidget(mem_label)
        
        mem_display = QLineEdit()
        mem_display.setReadOnly(True)
        mem_display.setFont(QFont("Segoe UI", 10))
        mem_display.setText(f"Memory: {self.memory}")
        self.mem_display = mem_display
        layout.addWidget(mem_display)
        
        mem_row = QHBoxLayout()
        mem_row.setSpacing(6)
        mem_row.addWidget(AnimatedButton("M+", self.memory_add, "#4ECDC4"))
        mem_row.addWidget(AnimatedButton("M-", self.memory_sub, "#4ECDC4"))
        mem_row.addWidget(AnimatedButton("MR", self.memory_recall, "#95E1D3"))
        mem_row.addWidget(AnimatedButton("MC", self.memory_clear, "#FF9999"))
        layout.addLayout(mem_row)
        
        # Base conversion section
        base_label = QLabel("Base Conversion")
        base_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        layout.addWidget(base_label)
        
        base_row = QHBoxLayout()
        base_row.setSpacing(6)
        base_row.addWidget(AnimatedButton("HEX", self.to_hex, "#FFB6C1"))
        base_row.addWidget(AnimatedButton("BIN", self.to_binary, "#FFB6C1"))
        base_row.addWidget(AnimatedButton("OCT", self.to_octal, "#FFB6C1"))
        base_row.addWidget(AnimatedButton("DEC", self.to_decimal, "#FFB6C1"))
        layout.addLayout(base_row)
        
        # Statistics section
        stats_label = QLabel("Other")
        stats_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        layout.addWidget(stats_label)
        
        stats_row = QHBoxLayout()
        stats_row.setSpacing(6)
        stats_row.addWidget(AnimatedButton("Redo", self.redo, "#A8E6CF"))
        layout.addLayout(stats_row)
        
        # Theme selection
        theme_label = QLabel("Themes")
        theme_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark Blue", "Dark Purple", "Dark Green", "Light", "Ocean"])
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        layout.addWidget(self.theme_combo)
        
        layout.addStretch()
        return widget
    
    def create_right_panel(self):
        """Create right panel with history and info"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # History section
        history_label = QLabel("📊 Calculation History")
        history_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        history_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(history_label)
        
        self.history_widget = QListWidget()
        self.history_widget.setFont(QFont("Segoe UI", 9))
        self.history_widget.setSpacing(4)
        self.history_widget.itemClicked.connect(self.load_from_history)
        layout.addWidget(self.history_widget)
        
        # History buttons
        history_btn_layout = QHBoxLayout()
        history_btn_layout.setSpacing(6)
        history_btn_layout.addWidget(AnimatedButton("Copy", self.copy_to_clipboard, "#4ECDC4"))
        history_btn_layout.addWidget(AnimatedButton("Clear", self.clear_history, "#FF6B6B"))
        layout.addLayout(history_btn_layout)
        
        # Theme toggle
        theme_toggle_btn = AnimatedButton("🌙/☀", self.toggle_theme, "#A8E6CF")
        layout.addWidget(theme_toggle_btn)
        
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
        """Toggle dark/light theme"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
    
    def on_theme_changed(self, theme_name):
        """Change theme by selection"""
        theme_map = {
            "Dark Blue": "dark_blue",
            "Dark Purple": "dark_purple",
            "Dark Green": "dark_green",
            "Light": "light",
            "Ocean": "ocean"
        }
        self.current_theme = theme_map.get(theme_name, "dark_blue")
        self.apply_theme()
    
    def apply_theme(self):
        """Apply color theme"""
        themes = {
            "dark_blue": {
                "bg": "#0a0e27",
                "input_bg": "#1a1f3a",
                "border": "#3a4a6a",
                "text": "#ffffff"
            },
            "dark_purple": {
                "bg": "#1a0a2e",
                "input_bg": "#2d1b4e",
                "border": "#4a2a7e",
                "text": "#ffffff"
            },
            "dark_green": {
                "bg": "#0a2e1a",
                "input_bg": "#1b4e2d",
                "border": "#2a7e4a",
                "text": "#ffffff"
            },
            "light": {
                "bg": "#f8f9fa",
                "input_bg": "#ffffff",
                "border": "#e0e0e0",
                "text": "#1a1a1a"
            },
            "ocean": {
                "bg": "#001a33",
                "input_bg": "#003d66",
                "border": "#0066cc",
                "text": "#ffffff"
            }
        }
        
        theme = themes.get(self.current_theme, themes["dark_blue"])
        
        stylesheet = f"""
            QMainWindow {{
                background-color: {theme['bg']};
            }}
            QLineEdit {{
                background-color: {theme['input_bg']};
                color: {theme['text']};
                border: 2px solid {theme['border']};
                border-radius: 12px;
                padding: 15px;
                font-size: 28px;
                font-weight: bold;
            }}
            QLineEdit:focus {{
                border: 2px solid #4ECDC4;
                background-color: {theme['input_bg']};
            }}
            QLabel {{
                color: {theme['text']};
            }}
            QListWidget {{
                background-color: {theme['input_bg']};
                color: {theme['text']};
                border: 2px solid {theme['border']};
                border-radius: 12px;
                padding: 8px;
            }}
            QListWidget::item {{
                padding: 8px;
                border-radius: 6px;
                margin: 2px 0px;
            }}
            QListWidget::item:hover {{
                background-color: {theme['border']};
                border-left: 3px solid #4ECDC4;
            }}
            QListWidget::item:selected {{
                background-color: #4ECDC4;
                color: {theme['bg']};
            }}
            QTabWidget::pane {{
                border: 2px solid {theme['border']};
                border-radius: 8px;
            }}
            QTabBar::tab {{
                background-color: {theme['input_bg']};
                color: {theme['text']};
                padding: 8px 20px;
                border-radius: 8px 8px 0 0;
            }}
            QTabBar::tab:selected {{
                background-color: #4ECDC4;
                color: {theme['bg']};
            }}
            QComboBox {{
                background-color: {theme['input_bg']};
                color: {theme['text']};
                border: 2px solid {theme['border']};
                border-radius: 8px;
                padding: 5px;
            }}
            QComboBox::drop-down {{
                background-color: {theme['border']};
            }}
        """
        
        self.setStyleSheet(stylesheet)
    
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
