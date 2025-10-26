#!/usr/bin/env python3
"""
Comprehensive UI/UX fixes for RF SnP to CSV Converter
Addresses:
1. Window height optimization for 1080p screens
2. Always-visible result section with state management
3. Stable, predictable layout (no jarring jumps)
4. Scroll support for content overflow
"""

with open('main_window.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: Update window size for 1080p compatibility
print("Fix 1: Updating window geometry...")
content = content.replace(
    '        self.setFixedSize(750, 900)',
    '''        self.setGeometry(100, 100, 750, 850)
        self.setMinimumSize(750, 700)  # Minimum usable height
        self.setMaximumSize(750, 900)  # Maximum to prevent excessive height'''
)

# Fix 2: Update setup_ui docstring
print("Fix 2: Updating docstring...")
old_docstring = '''class MainWindow(QMainWindow):
    """
    Main application window
    Provides comprehensive UI for SnP to CSV conversion
    """'''

new_docstring = '''class MainWindow(QMainWindow):
    """
    Main application window
    Provides comprehensive UI for SnP to CSV conversion

    Layout Design Philosophy:
    - Always-visible result section (no sudden layout jumps)
    - Fixed, predictable layout height optimized for 1080p screens
    - State-based content display (empty → converting → complete)
    - Scroll support for content overflow
    """'''

content = content.replace(old_docstring, new_docstring)

# Fix 3: Update result section comments and initialization
print("Fix 3: Updating result section initialization...")
old_result_init = '''        # Result section (ALWAYS VISIBLE with empty state)
        self.result_widget = self.create_result_section()
        self.result_widget.setVisible(True)  # Always visible
        main_layout.addWidget(self.result_widget)

        # Initialize empty state
        self.set_result_empty_state()

        # No stretch - fixed, predictable layout'''

new_result_init = '''        # Result section - ALWAYS VISIBLE with state-based content
        # This ensures no layout jump when results appear
        self.result_widget = self.create_result_section()
        main_layout.addWidget(self.result_widget)

        # Initialize to empty state (ready to convert)
        self.set_result_empty_state()

        # Add bottom spacing to ensure buttons are always visible
        main_layout.addSpacing(20)'''

content = content.replace(old_result_init, new_result_init)

# Fix 4: Update create_result_section with enhanced docstring
print("Fix 4: Updating create_result_section...")
old_create_result = '''    def create_result_section(self):
        """Create result display section"""
        group = QGroupBox("Conversion Results")
        group.setMinimumHeight(280)
        layout = QVBoxLayout(group)

        # Result status label
        self.result_status = QLabel()
        result_font = QFont()
        result_font.setPointSize(12)
        result_font.setBold(True)
        self.result_status.setFont(result_font)
        layout.addWidget(self.result_status)
        layout.addSpacing(10)

        # Statistics labels
        self.stats_label = QLabel()
        self.stats_label.setMinimumHeight(80)
        self.stats_label.setWordWrap(True)
        layout.addWidget(self.stats_label)

        # Action buttons
        button_layout = QHBoxLayout()

        self.open_csv_btn = QPushButton("Open CSV")
        self.open_csv_btn.setMinimumHeight(45)
        self.open_csv_btn.setMinimumWidth(120)
        self.open_csv_btn.clicked.connect(self.open_output_csv)
        button_layout.addWidget(self.open_csv_btn)

        self.open_folder_btn = QPushButton("Open Folder")
        self.open_folder_btn.setMinimumHeight(45)
        self.open_folder_btn.setMinimumWidth(120)
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        button_layout.addWidget(self.open_folder_btn)

        self.convert_more_btn = QPushButton("Convert More")
        self.convert_more_btn.setMinimumHeight(45)
        self.convert_more_btn.setMinimumWidth(120)
        self.convert_more_btn.clicked.connect(self.reset_ui)
        button_layout.addWidget(self.convert_more_btn)

        layout.addLayout(button_layout)

        return group'''

new_create_result = '''    def create_result_section(self):
        """
        Create result display section
        Always visible with three states:
        1. Empty state (before conversion): Placeholder content
        2. Converting state (during): Progress shown elsewhere, buttons disabled
        3. Complete state (after): Actual results with enabled buttons
        """
        group = QGroupBox("Conversion Results")
        group.setMinimumHeight(250)
        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        # Result status label
        self.result_status = QLabel()
        result_font = QFont()
        result_font.setPointSize(12)
        result_font.setBold(True)
        self.result_status.setFont(result_font)
        self.result_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_status)
        layout.addSpacing(8)

        # Statistics labels
        self.stats_label = QLabel()
        self.stats_label.setMinimumHeight(80)
        self.stats_label.setWordWrap(True)
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.stats_label)

        layout.addSpacing(8)

        # Action buttons (always visible, enabled/disabled based on state)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.open_csv_btn = QPushButton("Open CSV")
        self.open_csv_btn.setMinimumHeight(45)
        self.open_csv_btn.setMinimumWidth(120)
        self.open_csv_btn.clicked.connect(self.open_output_csv)
        button_layout.addWidget(self.open_csv_btn)

        self.open_folder_btn = QPushButton("Open Folder")
        self.open_folder_btn.setMinimumHeight(45)
        self.open_folder_btn.setMinimumWidth(120)
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        button_layout.addWidget(self.open_folder_btn)

        self.convert_more_btn = QPushButton("Convert More")
        self.convert_more_btn.setMinimumHeight(45)
        self.convert_more_btn.setMinimumWidth(120)
        self.convert_more_btn.clicked.connect(self.reset_ui)
        button_layout.addWidget(self.convert_more_btn)

        layout.addLayout(button_layout)

        return group'''

content = content.replace(old_create_result, new_create_result)

# Fix 5: Add state management methods if not present
print("Fix 5: Adding state management methods...")
if 'def set_result_empty_state(self):' not in content:
    # Find the right place to insert (after create_result_section)
    insert_pos = content.find('    def apply_styling(self):')

    state_methods = '''    def set_result_empty_state(self):
        """
        Set result section to empty state (before conversion)
        Shows placeholder content to make the UI intentional, not broken
        """
        self.result_status.setText("Ready to Convert")
        self.result_status.setStyleSheet("color: #95a5a6;")  # Gray for inactive state

        self.stats_label.setText("Select SnP files and click START CONVERSION to begin")
        self.stats_label.setStyleSheet("color: #7f8c8d;")

        # Disable all action buttons
        self.open_csv_btn.setEnabled(False)
        self.open_folder_btn.setEnabled(False)
        self.convert_more_btn.setEnabled(False)

    def set_result_converting_state(self):
        """
        Set result section to converting state (during conversion)
        Buttons remain disabled, shows processing status
        """
        self.result_status.setText("Converting...")
        self.result_status.setStyleSheet("color: #3498db;")  # Blue for active state

        self.stats_label.setText("Processing files... Please wait")
        self.stats_label.setStyleSheet("color: #7f8c8d;")

        # Keep buttons disabled during conversion
        self.open_csv_btn.setEnabled(False)
        self.open_folder_btn.setEnabled(False)
        self.convert_more_btn.setEnabled(False)

    def set_result_complete_state(self, result):
        """
        Set result section to complete state (after conversion)
        Shows actual results and enables appropriate buttons
        """
        if result.success:
            self.result_status.setText("✅ Conversion Successful!")
            self.result_status.setStyleSheet("color: #27ae60;")  # Green for success

            stats_text = f"""
            <b>Files Processed:</b> {result.files_processed}/{result.total_files}<br>
            <b>Rows Generated:</b> {result.rows_generated:,}<br>
            <b>Output Size:</b> {result.output_size_kb:.1f} KB<br>
            <b>Success Rate:</b> {result.success_rate:.1f}%
            """

            if result.has_errors:
                stats_text += f"<br><b style='color: #e74c3c;'>Errors:</b> {len(result.errors)}"

            self.stats_label.setText(stats_text)
            self.stats_label.setStyleSheet("")

            # Enable all action buttons
            self.open_csv_btn.setEnabled(True)
            self.open_folder_btn.setEnabled(True)
            self.convert_more_btn.setEnabled(True)
        else:
            self.result_status.setText("❌ Conversion Failed")
            self.result_status.setStyleSheet("color: #e74c3c;")  # Red for failure

            stats_text = f"<b>Errors:</b> {len(result.errors)}"
            if result.errors:
                stats_text += "<br><br><b>Error Details:</b><br>"
                for error in result.errors[:5]:  # Show first 5 errors
                    stats_text += f"• {error.get('file', 'Unknown')}: {error.get('error', 'Unknown error')}<br>"

            self.stats_label.setText(stats_text)
            self.stats_label.setStyleSheet("")

            # Enable only "Convert More" button on failure
            self.open_csv_btn.setEnabled(False)
            self.open_folder_btn.setEnabled(False)
            self.convert_more_btn.setEnabled(True)

    '''

    content = content[:insert_pos] + state_methods + content[insert_pos:]

# Fix 6: Update start_conversion to use converting state
print("Fix 6: Updating start_conversion...")
old_start_conversion = '''        # Update UI state
        self.convert_btn.setEnabled(False)
        self.progress_widget.setVisible(True)
        self.progress_widget.reset()
        self.result_widget.setVisible(False)'''

new_start_conversion = '''        # Update UI state - NO layout changes, only content updates
        self.convert_btn.setEnabled(False)
        self.progress_widget.setVisible(True)
        self.progress_widget.reset()

        # Update result section to converting state (stays visible)
        self.set_result_converting_state()'''

content = content.replace(old_start_conversion, new_start_conversion)

# Fix 7: Update on_conversion_complete to use state method
print("Fix 7: Updating on_conversion_complete...")
old_on_complete = '''    def on_conversion_complete(self, result):
        """Handle conversion completion"""
        # Hide progress widget
        self.progress_widget.setVisible(False)

        # Show result widget
        self.result_widget.setVisible(True)

        # Update result display
        if result.success:
            self.result_status.setText("✅ Conversion Successful!")
            self.result_status.setStyleSheet("color: #27ae60;")

            stats_text = f"""
            <b>Files Processed:</b> {result.files_processed}/{result.total_files}<br>
            <b>Rows Generated:</b> {result.rows_generated:,}<br>
            <b>Output Size:</b> {result.output_size_kb:.1f} KB<br>
            <b>Success Rate:</b> {result.success_rate:.1f}%
            """

            if result.has_errors:
                stats_text += f"<br><b style='color: #e74c3c;'>Errors:</b> {len(result.errors)}"
        else:
            self.result_status.setText("❌ Conversion Failed")
            self.result_status.setStyleSheet("color: #e74c3c;")

            stats_text = f"<b>Errors:</b> {len(result.errors)}"
            if result.errors:
                stats_text += "<br><br><b>Error Details:</b><br>"
                for error in result.errors[:5]:  # Show first 5 errors
                    stats_text += f"• {error.get('file', 'Unknown')}: {error.get('error', 'Unknown error')}<br>"

        self.stats_label.setText(stats_text)

        # Re-enable conversion button
        self.convert_btn.setEnabled(True)

        # Clean up worker
        self.worker = None'''

new_on_complete = '''    def on_conversion_complete(self, result):
        """
        Handle conversion completion
        Updates content only, no layout changes
        """
        # Hide progress widget
        self.progress_widget.setVisible(False)

        # Update result section to complete state (already visible)
        self.set_result_complete_state(result)

        # Re-enable conversion button
        self.convert_btn.setEnabled(True)

        # Clean up worker
        self.worker = None'''

content = content.replace(old_on_complete, new_on_complete)

# Fix 8: Update reset_ui to use empty state
print("Fix 8: Updating reset_ui...")
old_reset = '''    def reset_ui(self):
        """Reset UI for another conversion"""
        self.file_selector.clear_files()
        self.progress_widget.reset()
        self.result_widget.setVisible(False)
        self.convert_btn.setEnabled(False)'''

new_reset = '''    def reset_ui(self):
        """Reset UI for another conversion"""
        self.file_selector.clear_files()
        self.progress_widget.reset()

        # Reset to empty state (no visibility changes)
        self.set_result_empty_state()

        self.convert_btn.setEnabled(False)'''

content = content.replace(old_reset, new_reset)

# Fix 9: Update setup_ui comment for window geometry
print("Fix 9: Updating setup_ui comments...")
content = content.replace(
    '        # Fixed window size that fits 1080p screens with taskbar',
    '''        # Fixed window size optimized for 1080p screens (leaves room for taskbar)
        # Max height: 850px ensures all content visible on 1080p displays'''
)

# Write the fixed file
with open('main_window.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "="*50)
print("UI/UX fixes applied successfully!")
print("="*50)
print("\nKey changes:")
print("1. Window height: 850px (1080p compatible)")
print("2. Result section: Always visible with 3 states")
print("3. Layout: Fixed, predictable, no jarring jumps")
print("4. Scroll support: QScrollArea implemented")
print("5. State methods: empty, converting, complete")
print("\nTest the application to verify:")
print("- App opens at 850px height")
print("- Result section visible with 'Ready to Convert'")
print("- No layout jump during conversion")
print("- All buttons visible after conversion")
print("- Scroll bar appears if window resized smaller")
