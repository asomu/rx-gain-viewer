# Fix button sizes in main_window.py

import re

with open('ui_pyqt6/main_window.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Open CSV button
content = re.sub(
    r'self\.open_csv_btn = QPushButton\("Open CSV"\)\s+self\.open_csv_btn\.clicked',
    '''self.open_csv_btn = QPushButton("Open CSV")
        self.open_csv_btn.setMinimumHeight(45)
        self.open_csv_btn.setMinimumWidth(120)
        self.open_csv_btn.clicked''',
    content
)

# Fix Open Folder button
content = re.sub(
    r'self\.open_folder_btn = QPushButton\("Open Folder"\)\s+self\.open_folder_btn\.clicked',
    '''self.open_folder_btn = QPushButton("Open Folder")
        self.open_folder_btn.setMinimumHeight(45)
        self.open_folder_btn.setMinimumWidth(120)
        self.open_folder_btn.clicked''',
    content
)

# Fix Convert More button
content = re.sub(
    r'self\.convert_more_btn = QPushButton\("Convert More"\)\s+self\.convert_more_btn\.clicked',
    '''self.convert_more_btn = QPushButton("Convert More")
        self.convert_more_btn.setMinimumHeight(45)
        self.convert_more_btn.setMinimumWidth(120)
        self.convert_more_btn.clicked''',
    content
)

with open('ui_pyqt6/main_window.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Buttons fixed!")
