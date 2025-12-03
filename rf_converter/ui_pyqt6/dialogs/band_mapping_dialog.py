"""
Band Mapping Configuration Dialog

Modal dialog for editing band notation mappings.
Provides table-based editor for creating and modifying band mapping JSON files.
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit,
    QTableWidget, QTableWidgetItem, QToolBar, QDialogButtonBox,
    QLabel, QPushButton, QHeaderView, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QColor

from rf_converter.core.band_mapper import BandMapper


class BandMappingDialog(QDialog):
    """
    Modal dialog for creating/editing band notation mapping configurations.

    Features:
    - Table-based editor with add/delete rows
    - Real-time validation with error highlighting
    - Load/save JSON mapping files
    - Apply changes without saving
    - Unsaved changes detection

    Signals:
        mapping_applied: Emitted when mappings applied (dict of {original: mapped})
        mapping_saved: Emitted when mappings saved to file (file_path: str)
    """

    mapping_applied = pyqtSignal(dict)
    mapping_saved = pyqtSignal(str)

    def __init__(self, parent=None, initial_file: Optional[str] = None):
        """
        Initialize dialog.

        Args:
            parent: Parent widget
            initial_file: Optional path to mapping file to load
        """
        super().__init__(parent)

        # State management
        self._current_file: Optional[str] = initial_file
        self._original_data: Dict[str, str] = {}
        self._is_dirty: bool = False

        # Setup UI
        self.setWindowTitle("밴드 매핑 설정")
        self.setModal(True)
        self.resize(900, 650)

        # Will be initialized in _init_ui
        self.name_edit: QLineEdit
        self.desc_edit: QLineEdit
        self.table: QTableWidget
        self.row_count_label: QLabel
        self.error_panel: QLabel
        self.button_box: QDialogButtonBox

        self._init_ui()
        self._connect_signals()

        if initial_file:
            self._load_file(initial_file)

    def _init_ui(self):
        """Initialize UI components."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # Add sections
        main_layout.addWidget(self._init_info_section())
        main_layout.addWidget(self._init_table_section())

        # Error panel
        self.error_panel = self._init_error_panel()
        main_layout.addWidget(self.error_panel)

        # Dialog buttons
        self.button_box = self._init_button_box()
        main_layout.addWidget(self.button_box)

    def _init_info_section(self) -> QGroupBox:
        """Create configuration info section."""
        group = QGroupBox("📋 설정 정보")
        layout = QVBoxLayout()
        layout.setSpacing(8)

        # Name field
        name_layout = QHBoxLayout()
        name_label = QLabel("이름:")
        name_label.setFixedWidth(60)
        name_layout.addWidget(name_label)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("예: Alpha1C EVB1 Site")
        self.name_edit.setStyleSheet("QLineEdit { padding: 6px; }")
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # Description field
        desc_layout = QHBoxLayout()
        desc_label = QLabel("설명:")
        desc_label.setFixedWidth(60)
        desc_layout.addWidget(desc_label)

        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("예: Mapping for Alpha1C EVB1 test site")
        self.desc_edit.setStyleSheet("QLineEdit { padding: 6px; }")
        desc_layout.addWidget(self.desc_edit)
        layout.addLayout(desc_layout)

        group.setLayout(layout)
        return group

    def _init_table_section(self) -> QGroupBox:
        """Create mappings table section."""
        group = QGroupBox("🔀 밴드 매핑")
        layout = QVBoxLayout()

        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(False)

        add_action = QAction("➕ 추가", self)
        add_action.setToolTip("새 매핑 행 추가")
        add_action.triggered.connect(self._on_add_mapping)
        toolbar.addAction(add_action)

        layout.addWidget(toolbar)

        # Table
        self.table = QTableWidget(0, 3)  # 0 rows, 3 columns
        self.table.setHorizontalHeaderLabels(["원본 밴드", "매핑 값", ""])

        # Configure columns
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)

        self.table.setColumnWidth(0, 350)
        self.table.setColumnWidth(1, 350)
        self.table.setColumnWidth(2, 70)

        # Row height and styling - increased for Korean text rendering
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.verticalHeader().hide()
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

        # Row count label
        self.row_count_label = QLabel("0 rows")
        self.row_count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.row_count_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        layout.addWidget(self.row_count_label)

        group.setLayout(layout)
        return group

    def _init_error_panel(self) -> QLabel:
        """Create validation error panel."""
        error_label = QLabel()
        error_label.setWordWrap(True)
        error_label.setVisible(False)  # Hidden by default
        error_label.setStyleSheet("""
            QLabel {
                background-color: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        return error_label

    def _init_button_box(self) -> QDialogButtonBox:
        """Create dialog buttons."""
        button_box = QDialogButtonBox()

        # Apply button (non-standard, add manually)
        apply_btn = button_box.addButton("적용", QDialogButtonBox.ButtonRole.ApplyRole)
        apply_btn.setToolTip("변경사항을 BandMapper에 적용 (파일 저장 안 함)")
        apply_btn.clicked.connect(self._on_apply)

        # Save button
        save_btn = button_box.addButton("저장", QDialogButtonBox.ButtonRole.AcceptRole)
        save_btn.setToolTip("파일에 저장 후 닫기")
        save_btn.clicked.connect(self._on_save)

        # Cancel button
        cancel_btn = button_box.addButton("취소", QDialogButtonBox.ButtonRole.RejectRole)
        cancel_btn.setToolTip("변경사항 무시하고 닫기")
        cancel_btn.clicked.connect(self.reject)

        return button_box

    def _connect_signals(self):
        """Connect signals to slots."""
        self.table.cellChanged.connect(self._on_cell_changed)
        self.name_edit.textChanged.connect(lambda: self._mark_dirty(True))
        self.desc_edit.textChanged.connect(lambda: self._mark_dirty(True))

    # --- Row Management ---

    def _on_add_mapping(self):
        """Add new empty row to table."""
        # Temporarily disconnect cellChanged to prevent marking dirty on initialization
        self.table.cellChanged.disconnect(self._on_cell_changed)

        row = self.table.rowCount()
        self.table.insertRow(row)

        # Column 0: Original band (editable)
        self.table.setItem(row, 0, QTableWidgetItem(""))

        # Column 1: Mapped value (editable)
        self.table.setItem(row, 1, QTableWidgetItem(""))

        # Column 2: Delete button (full-width in cell)
        delete_btn = QPushButton("Del")
        delete_btn.setToolTip("이 매핑 삭제")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                border: none;
                border-radius: 0px;
                padding: 8px;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        delete_btn.clicked.connect(lambda checked, r=row: self._on_delete_mapping(r))
        self.table.setCellWidget(row, 2, delete_btn)

        # Reconnect signal
        self.table.cellChanged.connect(self._on_cell_changed)

        self._update_row_count()
        self._mark_dirty(True)

        # Set focus to first column of new row
        self.table.setCurrentCell(row, 0)
        self.table.editItem(self.table.item(row, 0))

    def _on_delete_mapping(self, row: int):
        """Delete specified row."""
        # Find actual current row (button reference may be stale)
        sender_btn = self.sender()
        if sender_btn:
            # Find which row contains this button
            for r in range(self.table.rowCount()):
                if self.table.cellWidget(r, 2) == sender_btn:
                    row = r
                    break

        self.table.removeRow(row)
        self._update_row_count()
        self._mark_dirty(True)

    def _on_cell_changed(self, row: int, col: int):
        """Mark dirty when cell edited."""
        self._mark_dirty(True)

    def _update_row_count(self):
        """Update row count label."""
        count = self.table.rowCount()
        self.row_count_label.setText(f"{count} rows")

    # --- Validation ---

    def _validate_mappings(self) -> Tuple[bool, List[str]]:
        """
        Validate all mappings.

        Returns:
            (is_valid, error_messages)
        """
        errors = []
        seen_originals = {}

        for row in range(self.table.rowCount()):
            original_item = self.table.item(row, 0)
            mapped_item = self.table.item(row, 1)

            original = original_item.text().strip() if original_item else ""
            mapped = mapped_item.text().strip() if mapped_item else ""

            # Check empty original
            if not original:
                errors.append(f"Row {row + 1}: 원본 밴드를 입력하세요")
                self._highlight_row_error(row, True)
                continue

            # Check empty mapped
            if not mapped:
                errors.append(f"Row {row + 1}: 매핑 값을 입력하세요")
                self._highlight_row_error(row, True)
                continue

            # Check duplicate
            if original in seen_originals:
                errors.append(
                    f'Row {row + 1}: 중복된 원본 밴드 "{original}" '
                    f'(row {seen_originals[original] + 1}에 이미 존재)'
                )
                self._highlight_row_error(row, True)
                continue

            seen_originals[original] = row
            self._highlight_row_error(row, False)

        return (len(errors) == 0, errors)

    def _highlight_row_error(self, row: int, has_error: bool):
        """Highlight row with error."""
        color = QColor(255, 220, 220) if has_error else QColor(255, 255, 255)

        for col in range(2):  # Only original and mapped columns
            item = self.table.item(row, col)
            if item:
                item.setBackground(color)

    def _update_error_panel(self, errors: List[str]):
        """Update error panel with messages."""
        if errors:
            error_text = f"⚠️ {len(errors)}개 오류 발견:\n"
            error_text += "\n".join(f"• {err}" for err in errors[:5])  # Show first 5
            if len(errors) > 5:
                error_text += f"\n... 외 {len(errors) - 5}개"

            self.error_panel.setText(error_text)
            self.error_panel.setStyleSheet("""
                QLabel {
                    background-color: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                    border-radius: 4px;
                    padding: 8px;
                }
            """)
            self.error_panel.setVisible(True)
        else:
            self.error_panel.setVisible(False)

    # --- File Operations ---

    def _load_file(self, file_path: str) -> bool:
        """Load mapping file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract fields
            self.name_edit.setText(data.get('name', ''))
            self.desc_edit.setText(data.get('description', ''))

            # Populate table
            mappings = data.get('mappings', {})
            self._populate_table(mappings)

            # Store original data
            self._current_file = file_path
            self._original_data = mappings.copy()
            self._mark_dirty(False)

            return True

        except Exception as e:
            QMessageBox.critical(
                self,
                "파일 로드 오류",
                f"파일을 불러올 수 없습니다:\n{file_path}\n\n오류: {str(e)}"
            )
            return False

    def _populate_table(self, mappings: Dict[str, str]):
        """Populate table from mappings dict."""
        # Disconnect signal to prevent marking dirty during population
        self.table.cellChanged.disconnect(self._on_cell_changed)

        self.table.setRowCount(0)  # Clear existing

        for original, mapped in mappings.items():
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(original))
            self.table.setItem(row, 1, QTableWidgetItem(mapped))

            # Delete button (full-width in cell)
            delete_btn = QPushButton("Del")
            delete_btn.setToolTip("이 매핑 삭제")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    font-weight: bold;
                    border: none;
                    border-radius: 0px;
                    padding: 8px;
                    margin: 0px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            delete_btn.clicked.connect(lambda checked, r=row: self._on_delete_mapping(r))
            self.table.setCellWidget(row, 2, delete_btn)

        # Reconnect signal
        self.table.cellChanged.connect(self._on_cell_changed)

        self._update_row_count()

    def _get_mappings_dict(self) -> Dict[str, str]:
        """Extract mappings from table."""
        mappings = {}

        for row in range(self.table.rowCount()):
            original_item = self.table.item(row, 0)
            mapped_item = self.table.item(row, 1)

            original = original_item.text().strip() if original_item else ""
            mapped = mapped_item.text().strip() if mapped_item else ""

            if original and mapped:  # Only include non-empty
                mappings[original] = mapped

        return mappings

    def _save_file(self, file_path: Optional[str] = None) -> bool:
        """Save mappings to file."""
        if file_path is None:
            file_path = self._current_file

        if not file_path:
            # No file specified, prompt user
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "매핑 파일 저장",
                str(Path.home()),
                "JSON Files (*.json)"
            )

            if not file_path:
                return False  # User cancelled

        try:
            # Create backup if file exists
            if Path(file_path).exists():
                backup_path = str(file_path) + '.bak'
                Path(file_path).rename(backup_path)

            # Build JSON structure
            data = {
                "schema_version": "1.0",
                "name": self.name_edit.text().strip(),
                "description": self.desc_edit.text().strip(),
                "mappings": self._get_mappings_dict()
            }

            # Write file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self._current_file = file_path
            self._original_data = data['mappings'].copy()
            self._mark_dirty(False)

            return True

        except Exception as e:
            QMessageBox.critical(
                self,
                "파일 저장 오류",
                f"파일을 저장할 수 없습니다:\n{file_path}\n\n오류: {str(e)}"
            )
            return False

    # --- Actions ---

    def _on_apply(self):
        """Apply mappings to BandMapper without closing."""
        # Validate
        valid, errors = self._validate_mappings()
        if not valid:
            self._update_error_panel(errors)
            QMessageBox.warning(
                self,
                "검증 오류",
                f"{len(errors)}개 오류가 발견되었습니다.\n수정 후 다시 시도하세요."
            )
            return

        # Get mappings
        mappings = self._get_mappings_dict()

        # Update BandMapper
        mapper = BandMapper.get_instance()
        mapper.mappings = mappings.copy()

        # Emit signal
        self.mapping_applied.emit(mappings)

        # Show success
        self.error_panel.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        self.error_panel.setText(f"✅ 적용됨 ({len(mappings)}개 매핑)")
        self.error_panel.setVisible(True)

    def _on_save(self):
        """Save mappings to file and close."""
        # Validate
        valid, errors = self._validate_mappings()
        if not valid:
            self._update_error_panel(errors)
            QMessageBox.warning(
                self,
                "검증 오류",
                f"{len(errors)}개 오류가 발견되었습니다.\n수정 후 다시 시도하세요."
            )
            return

        # Save file
        if self._save_file():
            # Emit signal
            self.mapping_saved.emit(self._current_file)

            # Close dialog
            self.accept()

    # --- Dirty State Tracking ---

    def _mark_dirty(self, dirty: bool = True):
        """Mark dialog as having unsaved changes."""
        self._is_dirty = dirty

        # Update window title
        title = "밴드 매핑 설정"
        if dirty:
            title += " *"
        self.setWindowTitle(title)

    def _is_data_modified(self) -> bool:
        """Check if current data differs from original."""
        current_mappings = self._get_mappings_dict()
        return current_mappings != self._original_data

    def closeEvent(self, event):
        """Handle close with unsaved changes check."""
        if self._is_dirty and self._is_data_modified():
            reply = QMessageBox.question(
                self,
                "저장하지 않은 변경사항",
                "저장하지 않은 변경사항이 있습니다.\n무시하시겠습니까?",
                QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )

            if reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return

        event.accept()

    def reject(self):
        """Handle Cancel button."""
        # closeEvent will handle unsaved changes check
        super().reject()
