"""
Main Window GUI for WinCloud - Liquid Glass Design
"""
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, 
    QTreeWidgetItem, QPushButton, QLabel, QProgressBar, QMenuBar,
    QMenu, QToolBar, QFileDialog, QMessageBox, QStatusBar, QSplitter,
    QTextEdit, QGroupBox, QSlider, QCheckBox, QDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPoint
from PyQt6.QtGui import QIcon, QAction, QPixmap

from wincloud_client.core.compression_engine import CompressionEngine
from wincloud_client.core.network_client import NetworkClient
from wincloud_client.gui.styles import get_dark_theme, get_light_theme
from common.config import Config
from common.logger import get_logger

logger = get_logger('MainWindow')

class CompressionThread(QThread):
    """Background thread for compression operations"""
    progress_update = pyqtSignal(int, str, dict)  # progress, status, stats
    finished = pyqtSignal(bool, str)  # success, message
    
    def __init__(self, engine, files, archive_path, compress=True):
        super().__init__()
        self.engine = engine
        self.files = files
        self.archive_path = archive_path
        self.compress = compress
        self._is_running = True
    
    def run(self):
        """Execute compression or extraction"""
        try:
            if self.compress:
                # Compress files
                result = self.engine.create_archive(
                    self.files,
                    self.archive_path,
                    progress_callback=self.progress_update.emit
                )
            else:
                # Extract files
                result = self.engine.extract_archive(
                    self.archive_path,
                    progress_callback=self.progress_update.emit
                )
            
            if result['success']:
                self.finished.emit(True, result.get('message', 'Operation completed successfully'))
            else:
                self.finished.emit(False, result.get('error', 'Operation failed'))
                
        except Exception as e:
            logger.error(f"Compression thread error: {e}", exc_info=True)
            self.finished.emit(False, str(e))
    
    def stop(self):
        """Stop the compression thread"""
        self._is_running = False
        self.engine.cancel_operation()


class WinCloudMainWindow(QMainWindow):
    """Main application window with Liquid Glass design"""
    
    def __init__(self):
        super().__init__()
        self.compression_engine = CompressionEngine()
        self.network_client = NetworkClient()
        self.current_thread = None
        self.selected_files = []
        self.config = Config()
        self.is_dark_theme = self.config.get('ui', {}).get('theme', 'dark') == 'dark'
        self.window_opacity = self.config.get('ui', {}).get('opacity', 1.0)
        self.background_transparency = self.config.get('ui', {}).get('background_transparency', False)
        
        # Frameless window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        if self.background_transparency:
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # For window dragging
        self.dragging = False
        self.offset = QPoint()
        
        self.init_ui()
        self.apply_theme()
        self.apply_opacity()
        self.check_server_connection()
    
    def mousePressEvent(self, event):
        """Handle mouse press for window dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            if hasattr(self, 'title_bar') and event.position().toPoint().y() < 50:
                self.dragging = True
                self.offset = event.position().toPoint()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for window dragging"""
        if self.dragging:
            self.move(self.pos() + event.position().toPoint() - self.offset)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False
    
    def init_ui(self):
        """Initialize user interface with Liquid Glass design"""
        self.setWindowTitle("WinCloud - Cloud Archiver")
        self.setGeometry(100, 100, 1200, 800)
        
        # Main container
        container = QWidget()
        container.setObjectName("mainContainer")
        self.setCentralWidget(container)
        
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Custom title bar
        self.create_title_bar()
        main_layout.addWidget(self.title_bar)
        
        # Content area
        content_widget = QWidget()
        content_widget.setObjectName("glassPanel")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(12)
        
        # Toolbar with actions
        self.create_action_buttons(content_layout)
        
        # Top section: File browser
        splitter = QSplitter(Qt.Orientation.Vertical)
        self.create_file_browser(splitter)
        self.create_progress_section(splitter)
        content_layout.addWidget(splitter, 1)
        
        main_layout.addWidget(content_widget, 1)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status("Ready")
    
    def create_title_bar(self):
        """Create custom frameless title bar"""
        self.title_bar = QWidget()
        self.title_bar.setObjectName("titleBar")
        self.title_bar.setFixedHeight(46)
        
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(16, 0, 8, 0)
        title_layout.setSpacing(8)
        
        # App icon and title
        title_label = QLabel(" 🌥️  WinCloud")
        title_label.setObjectName("titleLabel")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        # Settings button
        settings_btn = QPushButton("⚙️")
        settings_btn.setObjectName("titleButton")
        settings_btn.setToolTip("Settings")
        settings_btn.setFixedSize(36, 36)
        settings_btn.clicked.connect(self.show_settings)
        title_layout.addWidget(settings_btn)
        
        # Theme toggle button
        self.theme_btn = QPushButton("☀️" if self.is_dark_theme else "🌙")
        self.theme_btn.setObjectName("titleButton")
        self.theme_btn.setToolTip("Toggle Theme")
        self.theme_btn.setFixedSize(36, 36)
        self.theme_btn.clicked.connect(self.toggle_theme)
        title_layout.addWidget(self.theme_btn)
        
        # Minimize button
        min_btn = QPushButton("−")
        min_btn.setObjectName("titleButton")
        min_btn.setFixedSize(36, 36)
        min_btn.clicked.connect(self.showMinimized)
        title_layout.addWidget(min_btn)
        
        # Maximize button
        self.max_btn = QPushButton("□")
        self.max_btn.setObjectName("titleButton")
        self.max_btn.setFixedSize(36, 36)
        self.max_btn.clicked.connect(self.toggle_maximize)
        title_layout.addWidget(self.max_btn)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setObjectName("closeButton")
        close_btn.setFixedSize(36, 36)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)
    
    def toggle_maximize(self):
        """Toggle window maximize/restore"""
        if self.isMaximized():
            self.showNormal()
            self.max_btn.setText("□")
        else:
            self.showMaximized()
            self.max_btn.setText("❐")
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        try:
            self.is_dark_theme = not self.is_dark_theme
            self.theme_btn.setText("☀️" if self.is_dark_theme else "🌙")
            self.apply_theme()
            
            # Save theme preference
            self.config.set('ui', 'theme', 'dark' if self.is_dark_theme else 'light')
            logger.info(f"Theme changed to {'dark' if self.is_dark_theme else 'light'}")
        except Exception as e:
            logger.error(f"Error toggling theme: {e}", exc_info=True)
            QMessageBox.warning(self, "Error", f"Failed to change theme: {str(e)}")
    
    def apply_theme(self):
        """Apply current theme"""
        try:
            if self.is_dark_theme:
                self.setStyleSheet(get_dark_theme())
            else:
                self.setStyleSheet(get_light_theme())
        except Exception as e:
            logger.error(f"Error applying theme: {e}", exc_info=True)
    
    def apply_opacity(self):
        """Apply window opacity"""
        try:
            self.setWindowOpacity(self.window_opacity)
        except Exception as e:
            logger.error(f"Error applying opacity: {e}", exc_info=True)
    
    def toggle_background_transparency(self):
        """Toggle background transparency"""
        try:
            self.background_transparency = not self.background_transparency
            self.config.set('ui', 'background_transparency', self.background_transparency)
            
            # Notify user that restart is required
            QMessageBox.information(
                self,
                "Restart Required",
                "Background transparency setting will take effect after restarting the application."
            )
            logger.info(f"Background transparency set to {self.background_transparency}")
        except Exception as e:
            logger.error(f"Error toggling background transparency: {e}", exc_info=True)
    
    def set_opacity(self, value):
        """Set window opacity"""
        try:
            self.window_opacity = value / 100.0  # Convert from 0-100 to 0.0-1.0
            self.apply_opacity()
            self.config.set('ui', 'opacity', self.window_opacity)
            logger.info(f"Opacity set to {self.window_opacity}")
        except Exception as e:
            logger.error(f"Error setting opacity: {e}", exc_info=True)
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Settings")
        dialog.setMinimumWidth(400)
        dialog.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        
        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        
        # Opacity settings
        opacity_group = QGroupBox("Window Opacity")
        opacity_layout = QVBoxLayout(opacity_group)
        
        opacity_label = QLabel(f"Opacity: {int(self.window_opacity * 100)}%")
        opacity_layout.addWidget(opacity_label)
        
        opacity_slider = QSlider(Qt.Orientation.Horizontal)
        opacity_slider.setMinimum(20)  # Minimum 20% opacity
        opacity_slider.setMaximum(100)  # Maximum 100% opacity
        opacity_slider.setValue(int(self.window_opacity * 100))
        opacity_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        opacity_slider.setTickInterval(10)
        
        def on_opacity_change(value):
            opacity_label.setText(f"Opacity: {value}%")
            self.set_opacity(value)
        
        opacity_slider.valueChanged.connect(on_opacity_change)
        opacity_layout.addWidget(opacity_slider)
        
        layout.addWidget(opacity_group)
        
        # Background transparency settings
        transparency_group = QGroupBox("Background Transparency")
        transparency_layout = QVBoxLayout(transparency_group)
        
        transparency_checkbox = QCheckBox("Enable transparent background (requires restart)")
        transparency_checkbox.setChecked(self.background_transparency)
        transparency_checkbox.stateChanged.connect(lambda: self.toggle_background_transparency())
        transparency_layout.addWidget(transparency_checkbox)
        
        info_label = QLabel("⚠️ Transparent background may affect performance")
        info_label.setStyleSheet("color: rgba(255, 200, 0, 0.8); font-size: 11px;")
        transparency_layout.addWidget(info_label)
        
        layout.addWidget(transparency_group)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setObjectName("primaryButton")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        # Apply current theme to dialog
        if self.is_dark_theme:
            dialog.setStyleSheet(get_dark_theme())
        else:
            dialog.setStyleSheet(get_light_theme())
        
        dialog.exec()
    
    def create_action_buttons(self, layout):
        """Create main action buttons"""
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setSpacing(12)
        
        # Add Files button
        add_btn = QPushButton("➕ Add Files")
        add_btn.setObjectName("primaryButton")
        add_btn.setMinimumHeight(48)
        add_btn.clicked.connect(self.add_files)
        button_layout.addWidget(add_btn)
        
        # Create Archive button
        create_btn = QPushButton("📦 Create Archive")
        create_btn.setObjectName("primaryButton")
        create_btn.setMinimumHeight(48)
        create_btn.clicked.connect(self.create_archive)
        button_layout.addWidget(create_btn)
        
        # Extract Archive button
        extract_btn = QPushButton("📂 Extract Archive")
        extract_btn.setMinimumHeight(48)
        extract_btn.clicked.connect(self.extract_archive)
        button_layout.addWidget(extract_btn)
        
        layout.addWidget(button_widget)
    
    def create_file_browser(self, parent):
        """Create file browser tree"""
        group = QGroupBox("Files to Archive")
        layout = QVBoxLayout(group)
        
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabels(["Name", "Size", "Type", "Path"])
        self.file_tree.setColumnWidth(0, 300)
        self.file_tree.setColumnWidth(1, 100)
        self.file_tree.setColumnWidth(2, 100)
        
        layout.addWidget(self.file_tree)
        parent.addWidget(group)
    
    def create_progress_section(self, parent):
        """Create progress display section"""
        group = QGroupBox("Operation Progress")
        layout = QVBoxLayout(group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # Status label
        self.progress_label = QLabel("No operation in progress")
        layout.addWidget(self.progress_label)
        
        # Statistics display
        stats_layout = QHBoxLayout()
        
        self.stat_speed = QLabel("Speed: 0 MB/s")
        self.stat_processed = QLabel("Processed: 0 MB")
        self.stat_remaining = QLabel("Remaining: 0 MB")
        self.stat_ratio = QLabel("Compression: 0%")
        
        stats_layout.addWidget(self.stat_speed)
        stats_layout.addWidget(self.stat_processed)
        stats_layout.addWidget(self.stat_remaining)
        stats_layout.addWidget(self.stat_ratio)
        stats_layout.addStretch()
        
        layout.addLayout(stats_layout)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(150)
        layout.addWidget(self.log_display)
        
        parent.addWidget(group)
    
    def add_files(self):
        """Add files to archive list"""
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files to Archive",
            "",
            "All Files (*.*)"
        )
        
        if files:
            for file_path in files:
                self.add_file_to_tree(file_path)
                self.selected_files.append(file_path)
            
            self.log(f"Added {len(files)} file(s)")
    
    def add_folder(self):
        """Add folder to archive list"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder to Archive"
        )
        
        if folder:
            # Add all files in folder
            count = 0
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    self.add_file_to_tree(file_path)
                    self.selected_files.append(file_path)
                    count += 1
            
            self.log(f"Added folder with {count} file(s)")
    
    def add_file_to_tree(self, file_path):
        """Add file to tree widget"""
        if not os.path.exists(file_path):
            return
        
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_type = os.path.splitext(file_name)[1] or "File"
        
        # Format size
        size_str = self.format_size(file_size)
        
        item = QTreeWidgetItem([file_name, size_str, file_type, file_path])
        self.file_tree.addTopLevelItem(item)
    
    def clear_files(self):
        """Clear file list"""
        self.file_tree.clear()
        self.selected_files.clear()
        self.log("File list cleared")
    
    def create_archive(self):
        """Create WinCloud archive"""
        if not self.selected_files:
            QMessageBox.warning(self, "No Files", "Please add files to archive first")
            return
        
        # Ask for archive location
        archive_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Archive As",
            "",
            "WinCloud Archive (*.cloud)"
        )
        
        if not archive_path:
            return
        
        # Ensure .cloud extension
        if not archive_path.endswith('.cloud'):
            archive_path += '.cloud'
        
        # Start compression in background thread
        self.current_thread = CompressionThread(
            self.compression_engine,
            self.selected_files,
            archive_path,
            compress=True
        )
        
        self.current_thread.progress_update.connect(self.update_progress)
        self.current_thread.finished.connect(self.on_operation_finished)
        self.current_thread.start()
        
        self.log(f"Creating archive: {archive_path}")
        self.update_status("Creating archive...")
    
    def extract_archive(self):
        """Extract WinCloud archive"""
        archive_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Archive to Extract",
            "",
            "WinCloud Archive (*.wca)"
        )
        
        if not archive_path:
            return
        
        # Start extraction in background thread
        self.current_thread = CompressionThread(
            self.compression_engine,
            [],
            archive_path,
            compress=False
        )
        
        self.current_thread.progress_update.connect(self.update_progress)
        self.current_thread.finished.connect(self.on_operation_finished)
        self.current_thread.start()
        
        self.log(f"Extracting archive: {archive_path}")
        self.update_status("Extracting archive...")
    
    def update_progress(self, progress, status, stats):
        """Update progress display"""
        self.progress_bar.setValue(progress)
        self.progress_label.setText(status)
        
        # Update statistics
        if 'speed' in stats:
            self.stat_speed.setText(f"Speed: {stats['speed']:.2f} MB/s")
        
        if 'processed' in stats:
            self.stat_processed.setText(f"Processed: {self.format_size(stats['processed'])}")
        
        if 'remaining' in stats:
            self.stat_remaining.setText(f"Remaining: {self.format_size(stats['remaining'])}")
        
        if 'compression_ratio' in stats:
            self.stat_ratio.setText(f"Compression: {stats['compression_ratio']:.1f}%")
    
    def on_operation_finished(self, success, message):
        """Handle operation completion"""
        self.progress_bar.setValue(100 if success else 0)
        
        if success:
            self.log(f"✓ Success: {message}")
            self.update_status("Operation completed successfully")
            QMessageBox.information(self, "Success", message)
        else:
            self.log(f"✗ Error: {message}")
            self.update_status("Operation failed")
            QMessageBox.critical(self, "Error", message)
        
        self.current_thread = None
    
    def check_server_connection(self):
        """Check connection to cloud server"""
        if self.network_client.check_connection():
            self.log("✓ Connected to cloud server")
        else:
            self.log("⚠ Warning: Cloud server is not available. Some features may be limited.")
            QMessageBox.warning(
                self,
                "Server Unavailable",
                "Could not connect to cloud server. You can still use local archiving features."
            )
    
    def log(self, message):
        """Add message to log display"""
        self.log_display.append(message)
        logger.info(message)
    
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.showMessage(message)
    
    def format_size(self, size_bytes):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def open_settings(self):
        """Open settings dialog"""
        QMessageBox.information(self, "Settings", "Settings dialog coming soon!")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>WinCloud v1.0.0</h2>
        <p>Cloud-Based File Archiver</p>
        <p>A revolutionary archiving solution that combines local compression with cloud storage.</p>
        <br>
        <p><b>Features:</b></p>
        <ul>
        <li>Hybrid 10%/90% local-cloud storage</li>
        <li>End-to-end encryption</li>
        <li>Fast compression algorithms</li>
        <li>Real-time progress tracking</li>
        </ul>
        <br>
        <p>© 2026 WinCloud. All rights reserved.</p>
        """
        QMessageBox.about(self, "About WinCloud", about_text)
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.current_thread and self.current_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "Operation in Progress",
                "An operation is currently running. Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.current_thread.stop()
                self.current_thread.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
