# Fix window size and result section

with open('ui_pyqt6/main_window.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Increase window size
content = re.sub(
    r'self\.setGeometry\(\d+, \d+, \d+, \d+\)',
    'self.setGeometry(100, 100, 700, 900)',
    content
)

# Also set minimum window size
content = re.sub(
    r'self\.setWindowTitle\("RF SnP to CSV Converter"\)',
    '''self.setWindowTitle("RF SnP to CSV Converter")
        self.setMinimumSize(700, 900)''',
    content
)

with open('ui_pyqt6/main_window.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Window size increased to 700x900!")
