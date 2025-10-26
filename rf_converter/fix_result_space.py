# Fix result section spacing

with open('ui_pyqt6/main_window.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the create_result_section method and add minimum height
import re

# Add minimum height to result group
content = re.sub(
    r'def create_result_section\(self\):\s+"""Create result display section"""\s+group = QGroupBox\("Conversion Results"\)',
    '''def create_result_section(self):
        """Create result display section"""
        group = QGroupBox("Conversion Results")
        group.setMinimumHeight(200)''',
    content
)

# Add stretch to stats label to take more space
content = re.sub(
    r'self\.stats_label = QLabel\(\)\s+layout\.addWidget\(self\.stats_label\)',
    '''self.stats_label = QLabel()
        self.stats_label.setMinimumHeight(80)
        self.stats_label.setWordWrap(True)
        layout.addWidget(self.stats_label)''',
    content
)

# Add spacing between result status and stats
content = re.sub(
    r'self\.result_status\.setFont\(result_font\)\s+layout\.addWidget\(self\.result_status\)',
    '''self.result_status.setFont(result_font)
        layout.addWidget(self.result_status)
        layout.addSpacing(10)''',
    content
)

with open('ui_pyqt6/main_window.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Result section space fixed!")
