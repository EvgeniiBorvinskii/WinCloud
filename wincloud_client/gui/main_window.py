"""
Main Window GUI for WinCloud - WinRAR-like interface
"""
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, 
    QTreeWidgetItem, QPushButton, QLabel, QProgressBar, QMenuBar,
    QMenu, QToolBar, QFileDialog, QMessageBox, QStatusBar, QSplitter,
    QTextEdit, QGroupBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap

from wincloud_client.core.compression_engine import CompressionEngine
from wincloud_client.core.network_client import NetworkClient
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
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.compression_engine = CompressionEngine()
        self.network_client = NetworkClient()
        self.current_thread = None
        self.selected_files = []
        
        self.init_ui()
        self.check_server_connection()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("WinCloud - Cloud Archiver")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'wincloud.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Top section: Logo and title
        self.create_header(main_layout)
        
        # Middle section: File browser
        splitter = QSplitter(Qt.Orientation.Vertical)
        self.create_file_browser(splitter)
        self.create_progress_section(splitter)
        main_layout.addWidget(splitter)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status("Ready")
    
    def create_header(self, layout):
        """Create header with logo"""
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'wincloud2.png')
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
        
        # Title
        title_label = QLabel("<h1>WinCloud</h1><p>Cloud-Based File Archiver</p>")
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addWidget(header_widget)
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        add_files_action = QAction("Add Files", self)
        add_files_action.setShortcut("Ctrl+O")
        add_files_action.triggered.connect(self.add_files)
        file_menu.addAction(add_files_action)
        
        add_folder_action = QAction("Add Folder", self)
        add_folder_action.triggered.connect(self.add_folder)
        file_menu.addAction(add_folder_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Commands menu
        commands_menu = menubar.addMenu("&Commands")
        
        compress_action = QAction("Create Archive", self)
        compress_action.setShortcut("Ctrl+A")
        compress_action.triggered.connect(self.create_archive)
        commands_menu.addAction(compress_action)
        
        extract_action = QAction("Extract Archive", self)
        extract_action.setShortcut("Ctrl+E")
        extract_action.triggered.connect(self.extract_archive)
        commands_menu.addAction(extract_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)
        tools_menu.addAction(settings_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Create application toolbar"""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Add Files button
        add_btn = QPushButton("Add Files")
        add_btn.clicked.connect(self.add_files)
        toolbar.addWidget(add_btn)
        
        # Add Folder button
        folder_btn = QPushButton("Add Folder")
        folder_btn.clicked.connect(self.add_folder)
        toolbar.addWidget(folder_btn)
        
        toolbar.addSeparator()
        
        # Create Archive button
        compress_btn = QPushButton("Create Archive")
        compress_btn.clicked.connect(self.create_archive)
        toolbar.addWidget(compress_btn)
        
        # Extract Archive button
        extract_btn = QPushButton("Extract Archive")
        extract_btn.clicked.connect(self.extract_archive)
        toolbar.addWidget(extract_btn)
        
        toolbar.addSeparator()
        
        # Clear button
        clear_btn = QPushButton("Clear List")
        clear_btn.clicked.connect(self.clear_files)
        toolbar.addWidget(clear_btn)
    
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
            "WinCloud Archive (*.wca)"
        )
        
        if not archive_path:
            return
        
        # Ensure .wca extension
        if not archive_path.endswith('.wca'):
            archive_path += '.wca'
        
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
