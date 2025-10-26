"""
File Selector Widget
Drag-and-drop support for SnP file selection
"""

from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFileDialog, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QDragEnterEvent, QDropEvent


class FileSelector(QGroupBox):
    """
    Custom widget for file selection with drag-and-drop support
    Emits signals when files are selected or changed
    """

    # Signal emitted when files change: (files: list[Path], total_size_mb: float)
    files_changed = pyqtSignal(list, float)

    def __init__(self):
        super().__init__("File Selection")
        self.selected_files = []
        self.setup_ui()

        # Enable drag and drop
        self.setAcceptDrops(True)

    def setup_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)

        # Drag and drop area
        self.drop_area = QLabel()
        self.drop_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.drop_area.setMinimumHeight(150)
        self.update_drop_area_text()

        # Style the drop area
        self.drop_area.setMinimumHeight(120)
        self.drop_area.setStyleSheet("""
            QLabel {
                border: 3px dashed #3498db;
                border-radius: 8px;
                background-color: #ebf5fb;
                color: #2980b9;
                font-size: 11pt;
                padding: 20px;
            }
        """)

        layout.addWidget(self.drop_area)

        # File info and browse button layout
        info_layout = QHBoxLayout()

        # File count and size label
        self.file_info_label = QLabel("No files selected")
        self.file_info_label.setStyleSheet("font-size: 10pt; color: #34495e;")
        info_layout.addWidget(self.file_info_label)

        info_layout.addStretch()

        # Browse folder button
        browse_btn = QPushButton("Browse Folder...")
        browse_btn.setMaximumWidth(150)
        browse_btn.clicked.connect(self.browse_folder)
        info_layout.addWidget(browse_btn)

        # Clear files button
        self.clear_btn = QPushButton("Clear Files")
        self.clear_btn.setMaximumWidth(120)
        self.clear_btn.clicked.connect(self.clear_files)
        self.clear_btn.setEnabled(False)
        info_layout.addWidget(self.clear_btn)

        layout.addLayout(info_layout)

    def update_drop_area_text(self):
        """Update the drop area display text"""
        if not self.selected_files:
            text = "📁 Drag and drop .s2p files here\n\nor click 'Browse Folder' to select files"
        else:
            count = len(self.selected_files)
            text = f"✅ {count} file{'s' if count != 1 else ''} selected\n\nDrag more files to add"

        self.drop_area.setText(text)

    def browse_folder(self):
        """Open folder browser dialog"""
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder Containing SnP Files",
            str(Path.home())
        )

        if folder_path:
            self.load_files_from_folder(Path(folder_path))

    def load_files_from_folder(self, folder_path):
        """Load all SnP files from selected folder"""
        # Find all SnP files from s1p to s12p (case insensitive)
        snp_files = []
        
        # Support s1p ~ s12p
        for i in range(1, 13):
            snp_files.extend(folder_path.glob(f'*.s{i}p'))
            snp_files.extend(folder_path.glob(f'*.S{i}P'))

        if snp_files:
            self.selected_files = snp_files
            self.on_files_updated()
        else:
            self.file_info_label.setText("No SnP files found in selected folder")

    def clear_files(self):
        """Clear all selected files"""
        self.selected_files = []
        self.on_files_updated()

    def on_files_updated(self):
        """Handle file list updates"""
        # Calculate total size
        total_size = sum(f.stat().st_size for f in self.selected_files)
        total_size_mb = total_size / (1024 * 1024)

        # Update display
        self.update_drop_area_text()
        self.update_display(len(self.selected_files), total_size_mb)

        # Enable/disable clear button
        self.clear_btn.setEnabled(len(self.selected_files) > 0)

        # Emit signal
        self.files_changed.emit(self.selected_files, total_size_mb)

    def update_display(self, file_count, total_size_mb):
        """Update file information display"""
        if file_count > 0:
            self.file_info_label.setText(
                f"{file_count} file{'s' if file_count != 1 else ''} selected "
                f"({total_size_mb:.2f} MB)"
            )
        else:
            self.file_info_label.setText("No files selected")

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

            # Visual feedback
            self.drop_area.setStyleSheet("""
                QLabel {
                    border: 3px dashed #27ae60;
                    border-radius: 8px;
                    background-color: #d5f4e6;
                    color: #27ae60;
                    font-size: 11pt;
                    padding: 20px;
                }
            """)

    def dragLeaveEvent(self, event):
        """Handle drag leave event"""
        # Restore original style
        self.drop_area.setMinimumHeight(120)
        self.drop_area.setStyleSheet("""
            QLabel {
                border: 3px dashed #3498db;
                border-radius: 8px;
                background-color: #ebf5fb;
                color: #2980b9;
                font-size: 11pt;
                padding: 20px;
            }
        """)

    def dropEvent(self, event: QDropEvent):
        """Handle file drop event"""
        # Restore original style
        self.drop_area.setMinimumHeight(120)
        self.drop_area.setStyleSheet("""
            QLabel {
                border: 3px dashed #3498db;
                border-radius: 8px;
                background-color: #ebf5fb;
                color: #2980b9;
                font-size: 11pt;
                padding: 20px;
            }
        """)

        # Process dropped files
        urls = event.mimeData().urls()
        dropped_files = []

        for url in urls:
            file_path = Path(url.toLocalFile())

            if file_path.is_file() and file_path.suffix.lower() in ['.s1p', '.s2p', '.s3p', '.s4p']:
                # Add individual file
                dropped_files.append(file_path)
            elif file_path.is_dir():
                # Add all SnP files from directory
                for ext in ['s1p', 's2p', 's3p', 's4p']:
                    dropped_files.extend(file_path.glob(f'*.{ext}'))
                    dropped_files.extend(file_path.glob(f'*.{ext.upper()}'))

        if dropped_files:
            # Add to existing files (avoid duplicates)
            existing_paths = set(self.selected_files)
            for file_path in dropped_files:
                if file_path not in existing_paths:
                    self.selected_files.append(file_path)
                    existing_paths.add(file_path)

            self.on_files_updated()
            event.acceptProposedAction()
