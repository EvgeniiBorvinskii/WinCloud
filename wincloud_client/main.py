"""
WinCloud - Cloud-Based File Archiver
Main Application Entry Point
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wincloud_client.gui.main_window import WinCloudMainWindow
from common.config import Config
from common.logger import setup_logger

def main():
    """Main entry point for WinCloud application"""
    
    # Setup logging
    logger = setup_logger('WinCloud')
    logger.info("Starting WinCloud Application...")
    
    # Initialize configuration
    config = Config()
    
    # Create Qt Application
    app = QApplication(sys.argv)
    app.setApplicationName("WinCloud")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("WinCloud")
    
    # Set application icon
    icon_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'wincloud.png')
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create and show main window
    window = WinCloudMainWindow()
    window.show()
    
    logger.info("WinCloud Application started successfully")
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
