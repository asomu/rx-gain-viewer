#!/usr/bin/env python3
with open('main_window.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'from PyQt6.QtWidgets import (\n    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,\n    QPushButton, QLabel, QRadioButton, QCheckBox, QLineEdit,\n    QProgressBar, QFileDialog, QMessageBox, QButtonGroup\n)',
    'from PyQt6.QtWidgets import (\n    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,\n    QPushButton, QLabel, QRadioButton, QCheckBox, QLineEdit,\n    QProgressBar, QFileDialog, QMessageBox, QButtonGroup, QScrollArea\n)'
)

old_setup = '''    def setup_ui(self):
        """Initialize UI components and layouts"""
        self.setWindowTitle("RF SnP to CSV Converter")
        self.setMinimumSize(750, 1050)
        self.setMinimumSize(750, 1050)

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)'''

new_setup = '''    def setup_ui(self):
        """Initialize UI components and layouts"""
        self.setWindowTitle("RF SnP to CSV Converter")
        self.setFixedSize(750, 900)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setCentralWidget(scroll_area)

        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        main_layout = QVBoxLayout(content_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)'''

content = content.replace(old_setup, new_setup)

old_result = '''        # Progress display
        self.progress_widget = ProgressWidget()
        self.progress_widget.setVisible(False)
        main_layout.addWidget(self.progress_widget)

        # Result section (initially hidden)
        self.result_widget = self.create_result_section()
        self.result_widget.setVisible(False)
        main_layout.addWidget(self.result_widget)

        # Add stretch at bottom to push everything up
        main_layout.addStretch()'''

new_result = '''        # Progress display
        self.progress_widget = ProgressWidget()
        self.progress_widget.setVisible(False)
        main_layout.addWidget(self.progress_widget)

        # Result section (ALWAYS VISIBLE)
        self.result_widget = self.create_result_section()
        self.result_widget.setVisible(True)
        main_layout.addWidget(self.result_widget)

        self.set_result_empty_state()'''

content = content.replace(old_result, new_result)

with open('main_window.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Part 1 complete")
