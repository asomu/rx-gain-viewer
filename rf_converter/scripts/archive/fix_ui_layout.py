# Fix UI layout issues

import re

print("Fixing UI layout issues...")

# 1. Fix window size - make it taller
print("1. Increasing window height...")
with open('ui_pyqt6/main_window.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Change window size from 700x900 to 750x1000
content = re.sub(
    r'self\.setGeometry\(100, 100, \d+, \d+\)',
    'self.setGeometry(100, 100, 750, 1050)',
    content
)

content = re.sub(
    r'self\.setMinimumSize\(\d+, \d+\)',
    'self.setMinimumSize(750, 1050)',
    content
)

with open('ui_pyqt6/main_window.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("   [OK] Window size: 750x1050")

# 2. Fix file_selector drop area height
print("2. Fixing drop area height...")
with open('ui_pyqt6/widgets/file_selector.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add minimum height to drop area
old_code = '''        self.drop_area.setStyleSheet("""
            QLabel {
                border: 3px dashed #3498db;
                border-radius: 8px;
                background-color: #ebf5fb;
                color: #2980b9;
                font-size: 11pt;
                padding: 20px;
            }
        """)'''

new_code = '''        self.drop_area.setMinimumHeight(120)
        self.drop_area.setStyleSheet("""
            QLabel {
                border: 3px dashed #3498db;
                border-radius: 8px;
                background-color: #ebf5fb;
                color: #2980b9;
                font-size: 11pt;
                padding: 20px;
            }
        """)'''

content = content.replace(old_code, new_code)

with open('ui_pyqt6/widgets/file_selector.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("   [OK] Drop area minimum height: 120px")

# 3. Increase result section minimum height
print("3. Increasing result section height...")
with open('ui_pyqt6/main_window.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find result section and increase height
content = re.sub(
    r'group\.setMinimumHeight\(200\)',
    'group.setMinimumHeight(280)',
    content
)

with open('ui_pyqt6/main_window.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("   [OK] Result section minimum height: 280px")

# 4. Add spacing between sections
print("4. Adding spacing between UI sections...")
with open('ui_pyqt6/main_window.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add spacing after each section
old_pattern = r'main_layout\.addWidget\(self\.file_selector\)'
new_code = 'main_layout.addWidget(self.file_selector)\n        main_layout.addSpacing(15)'
content = re.sub(old_pattern, new_code, content)

old_pattern = r'main_layout\.addWidget\(measurement_group\)'
new_code = 'main_layout.addWidget(measurement_group)\n        main_layout.addSpacing(15)'
content = re.sub(old_pattern, new_code, content)

old_pattern = r'main_layout\.addWidget\(options_group\)'
new_code = 'main_layout.addWidget(options_group)\n        main_layout.addSpacing(15)'
content = re.sub(old_pattern, new_code, content)

old_pattern = r'main_layout\.addWidget\(output_group\)'
new_code = 'main_layout.addWidget(output_group)\n        main_layout.addSpacing(15)'
content = re.sub(old_pattern, new_code, content)

with open('ui_pyqt6/main_window.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("   [OK] Added 15px spacing between sections")

print("")
print("[SUCCESS] UI layout fixed!")
print("")
print("Changes:")
print("  - Window: 750x1050 (was 700x900)")
print("  - Drop area: 120px min height")
print("  - Result section: 280px min height (was 200px)")
print("  - Section spacing: 15px")
print("")
print("[WARNING] GUI restart required")
