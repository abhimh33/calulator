import sys
import math
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QListWidget, 
                             QListWidgetItem, QSplitter, QLabel, QFrame)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QRect, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QColor, QLinearGradient, QPainter

class AnimatedButton(QPushButton):
    """Custom button with animation effects"""
    def __init__(self, text, callback, color=None):
        super().__init__(text)
        self.base_color = color
        self.clicked.connect(callback)
        self.setCursor(Qt.PointingHandCursor)
        self.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.setMinimumHeight(55)
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


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💎 Modern Calculator Pro")
        self.setGeometry(50, 50, 1100, 700)
        self.setMinimumSize(1000, 600)
        self.dark_mode = True
        self.history_list = []
        
        # Initialize UI
        self.init_ui()
        self.apply_theme()
        
    def init_ui(self):
        """Initialize the user interface"""
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout
        main_layout = QHBoxLayout(main_widget)
        
        # Left side - Calculator
        calc_layout = QVBoxLayout()
        
        
        # Display with enhanced styling
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Segoe UI", 32, QFont.Bold))
        self.display.setMinimumHeight(80)
        self.display.setText("0")
        calc_layout.addWidget(self.display)
        
        # Input expression for calculation
        self.expression = ""
        
        # Button grid
        buttons_layout = QVBoxLayout()
        
        # Row 1: Functions and Clear
        row1 = QHBoxLayout()
        row1.setSpacing(8)
        row1.addWidget(AnimatedButton("C", self.clear_display, "#FF6B6B"))
        row1.addWidget(AnimatedButton("DEL", self.delete_last, "#FF9999"))
        row1.addWidget(AnimatedButton("√", lambda: self.append_function("sqrt"), "#4ECDC4"))
        row1.addWidget(AnimatedButton("π", lambda: self.append_value(str(math.pi)), "#4ECDC4"))
        buttons_layout.addLayout(row1)
        
        # Row 2: Numbers and operations
        row2 = QHBoxLayout()
        row2.setSpacing(8)
        row2.addWidget(AnimatedButton("7", lambda: self.append_value("7")))
        row2.addWidget(AnimatedButton("8", lambda: self.append_value("8")))
        row2.addWidget(AnimatedButton("9", lambda: self.append_value("9")))
        row2.addWidget(AnimatedButton("÷", lambda: self.append_operator("/"), "#95E1D3"))
        buttons_layout.addLayout(row2)
        
        # Row 3
        row3 = QHBoxLayout()
        row3.setSpacing(8)
        row3.addWidget(AnimatedButton("4", lambda: self.append_value("4")))
        row3.addWidget(AnimatedButton("5", lambda: self.append_value("5")))
        row3.addWidget(AnimatedButton("6", lambda: self.append_value("6")))
        row3.addWidget(AnimatedButton("×", lambda: self.append_operator("*"), "#95E1D3"))
        buttons_layout.addLayout(row3)
        
        # Row 4
        row4 = QHBoxLayout()
        row4.setSpacing(8)
        row4.addWidget(AnimatedButton("1", lambda: self.append_value("1")))
        row4.addWidget(AnimatedButton("2", lambda: self.append_value("2")))
        row4.addWidget(AnimatedButton("3", lambda: self.append_value("3")))
        row4.addWidget(AnimatedButton("-", lambda: self.append_operator("-"), "#95E1D3"))
        buttons_layout.addLayout(row4)
        
        # Row 5
        row5 = QHBoxLayout()
        row5.setSpacing(8)
        row5.addWidget(AnimatedButton("0", lambda: self.append_value("0")))
        row5.addWidget(AnimatedButton(".", lambda: self.append_value(".")))
        row5.addWidget(AnimatedButton("x²", lambda: self.append_function("pow2"), "#4ECDC4"))
        row5.addWidget(AnimatedButton("+", lambda: self.append_operator("+"), "#95E1D3"))
        buttons_layout.addLayout(row5)
        
        # Row 6: Equals
        row6 = QHBoxLayout()
        row6.setSpacing(8)
        equals_btn = AnimatedButton("=", self.calculate, "#FFD93D")
        equals_btn.setMinimumHeight(60)
        row6.addWidget(equals_btn, 2)
        row6.addWidget(AnimatedButton("🌙/☀", self.toggle_theme, "#A8E6CF"))
        buttons_layout.addLayout(row6)
        
        calc_layout.addLayout(buttons_layout)
        
        # Add spacing and margins
        calc_layout.setSpacing(10)
        calc_layout.setContentsMargins(15, 15, 15, 15)
        
        
        # Right side - History with enhanced styling
        history_layout = QVBoxLayout()
        history_label = QLabel("📊 Calculation History")
        history_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        history_label.setAlignment(Qt.AlignCenter)
        history_layout.addWidget(history_label)
        
        self.history_widget = QListWidget()
        self.history_widget.setFont(QFont("Segoe UI", 10))
        self.history_widget.setSpacing(5)
        history_layout.addWidget(self.history_widget)
        
        # Clear history button
        clear_history_btn = AnimatedButton("Clear History", self.clear_history, "#FF6B6B")
        history_layout.addWidget(clear_history_btn)
        
        # Add both sides to main layout
        calc_widget = QWidget()
        calc_widget.setLayout(calc_layout)
        
        history_widget = QWidget()
        history_widget.setLayout(history_layout)
        
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(calc_widget)
        splitter.addWidget(history_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        

    
    def append_value(self, value):
        """Append a value to expression"""
        self.expression += str(value)
        self.update_display()
    
    def append_operator(self, operator):
        """Append an operator to expression"""
        if self.expression and not self.expression.endswith((" + ", " - ", " * ", " / ")):
            self.expression += f" {operator} "
        self.update_display()
    
    def append_function(self, func):
        """Append a function"""
        if func == "sqrt":
            self.expression += "sqrt("
        elif func == "pow2":
            if self.expression:
                self.expression = f"pow({self.expression}, 2)"
        self.update_display()
    
    def update_display(self):
        """Update the display with current expression"""
        self.display.setText(self.expression)
    
    def clear_display(self):
        """Clear the display"""
        self.expression = ""
        self.display.setText("0")
    
    def delete_last(self):
        """Delete the last character"""
        self.expression = self.expression[:-1]
        self.update_display()
    
    def calculate(self):
        """Calculate the expression"""
        try:
            if not self.expression:
                return
            
            # Replace custom operators with Python operators
            calc_expr = self.expression.replace("×", "*").replace("÷", "/")
            calc_expr = calc_expr.replace("sqrt(", "math.sqrt(")
            
            # Evaluate
            result = eval(calc_expr, {"__builtins__": {}}, {"math": math, "pow": pow})
            
            # Format result
            if isinstance(result, float):
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 10)
            
            # Add to history
            timestamp = datetime.now().strftime("%H:%M:%S")
            history_entry = f"{self.expression} = {result}"
            self.history_list.append(history_entry)
            
            # Add to history widget
            item = QListWidgetItem(f"[{timestamp}] {history_entry}")
            self.history_widget.insertItem(0, item)
            
            # Update display
            self.expression = str(result)
            self.update_display()
            
        except ZeroDivisionError:
            self.display.setText("Error: Division by zero")
            self.expression = ""
        except Exception as e:
            self.display.setText(f"Error: Invalid expression")
            self.expression = ""
    
    def clear_history(self):
        """Clear the history"""
        self.history_widget.clear()
        self.history_list = []
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
    
    def apply_theme(self):
        """Apply dark or light theme"""
        if self.dark_mode:
            # Modern Dark theme with gradient
            dark_bg = "#0a0e27"
            dark_text = "#ffffff"
            input_bg = "#1a1f3a"
            button_bg = "#2a2f4a"
            border_color = "#3a4a6a"
            
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-color: {dark_bg};
                }}
                QLineEdit {{
                    background-color: {input_bg};
                    color: {dark_text};
                    border: 2px solid {border_color};
                    border-radius: 12px;
                    padding: 15px;
                    font-size: 32px;
                    font-weight: bold;
                }}
                QLineEdit:focus {{
                    border: 2px solid #4ECDC4;
                    background-color: #242a45;
                }}
                QLabel {{
                    color: {dark_text};
                }}
                QListWidget {{
                    background-color: {input_bg};
                    color: {dark_text};
                    border: 2px solid {border_color};
                    border-radius: 12px;
                    padding: 8px;
                }}
                QListWidget::item {{
                    padding: 8px;
                    border-radius: 6px;
                    margin: 2px 0px;
                }}
                QListWidget::item:hover {{
                    background-color: #3a4a6a;
                    border-left: 3px solid #4ECDC4;
                }}
                QListWidget::item:selected {{
                    background-color: #4ECDC4;
                    color: #0a0e27;
                }}
                QSplitter::handle {{
                    background-color: {border_color};
                }}
            """)
        else:
            # Modern Light theme
            light_bg = "#f8f9fa"
            light_text = "#1a1a1a"
            input_bg = "#ffffff"
            button_bg = "#f0f0f0"
            border_color = "#e0e0e0"
            
            self.setStyleSheet(f"""
                QMainWindow {{
                    background-color: {light_bg};
                }}
                QLineEdit {{
                    background-color: {input_bg};
                    color: {light_text};
                    border: 2px solid {border_color};
                    border-radius: 12px;
                    padding: 15px;
                    font-size: 32px;
                    font-weight: bold;
                }}
                QLineEdit:focus {{
                    border: 2px solid #4ECDC4;
                    background-color: #f5f5f5;
                }}
                QLabel {{
                    color: {light_text};
                }}
                QListWidget {{
                    background-color: {input_bg};
                    color: {light_text};
                    border: 2px solid {border_color};
                    border-radius: 12px;
                    padding: 8px;
                }}
                QListWidget::item {{
                    padding: 8px;
                    border-radius: 6px;
                    margin: 2px 0px;
                }}
                QListWidget::item:hover {{
                    background-color: #f0f0f0;
                    border-left: 3px solid #4ECDC4;
                }}
                QListWidget::item:selected {{
                    background-color: #4ECDC4;
                    color: #ffffff;
                }}
                QSplitter::handle {{
                    background-color: {border_color};
                }}
            """)


def main():
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
