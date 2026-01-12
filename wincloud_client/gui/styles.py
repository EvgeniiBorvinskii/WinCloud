"""
Liquid Glass UI Styles for WinCloud
Modern glassmorphism design with dark/light theme support
"""

def get_dark_theme():
    """Liquid Glass Dark Theme"""
    return """
    /* Main Window - Frameless with blur effect */
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(15, 15, 20, 0.95),
            stop:1 rgba(25, 25, 35, 0.95));
        border-radius: 16px;
    }
    
    /* Custom Title Bar */
    #titleBar {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(40, 40, 50, 0.9),
            stop:1 rgba(30, 30, 40, 0.8));
        border-top-left-radius: 16px;
        border-top-right-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: 1px solid rgba(100, 100, 120, 0.3);
    }
    
    #titleLabel {
        color: rgba(255, 255, 255, 0.9);
        font-size: 14px;
        font-weight: bold;
        padding: 8px 16px;
    }
    
    /* Title Bar Buttons */
    #titleButton {
        background: transparent;
        border: none;
        color: rgba(255, 255, 255, 0.7);
        font-size: 16px;
        padding: 8px 12px;
        border-radius: 8px;
    }
    
    #titleButton:hover {
        background: rgba(255, 255, 255, 0.1);
        color: rgba(255, 255, 255, 0.9);
    }
    
    #closeButton:hover {
        background: rgba(255, 60, 60, 0.8);
        color: white;
    }
    
    /* Glass Panels */
    QWidget#glassPanel {
        background: rgba(30, 30, 40, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        backdrop-filter: blur(20px);
    }
    
    /* Buttons - Glass effect */
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(60, 60, 80, 0.8),
            stop:1 rgba(40, 40, 60, 0.8));
        color: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 13px;
        font-weight: 600;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(80, 80, 110, 0.9),
            stop:1 rgba(60, 60, 90, 0.9));
        border: 1px solid rgba(255, 255, 255, 0.25);
    }
    
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(40, 40, 60, 0.9),
            stop:1 rgba(30, 30, 50, 0.9));
    }
    
    QPushButton:disabled {
        background: rgba(30, 30, 40, 0.4);
        color: rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Primary Action Button */
    QPushButton#primaryButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(100, 70, 255, 0.9),
            stop:1 rgba(70, 130, 255, 0.9));
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    QPushButton#primaryButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(120, 90, 255, 1),
            stop:1 rgba(90, 150, 255, 1));
    }
    
    /* Tree Widget - Glass effect */
    QTreeWidget {
        background: rgba(20, 20, 30, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: rgba(255, 255, 255, 0.9);
        font-size: 12px;
        padding: 8px;
    }
    
    QTreeWidget::item {
        padding: 8px;
        border-radius: 6px;
    }
    
    QTreeWidget::item:selected {
        background: rgba(100, 70, 255, 0.3);
        border: 1px solid rgba(100, 70, 255, 0.5);
    }
    
    QTreeWidget::item:hover {
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* Progress Bar - Liquid style */
    QProgressBar {
        background: rgba(20, 20, 30, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        height: 20px;
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-weight: bold;
    }
    
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(100, 70, 255, 0.9),
            stop:0.5 rgba(70, 130, 255, 0.9),
            stop:1 rgba(100, 200, 255, 0.9));
        border-radius: 9px;
    }
    
    /* Labels */
    QLabel {
        color: rgba(255, 255, 255, 0.85);
        font-size: 12px;
    }
    
    QLabel#headerLabel {
        color: rgba(255, 255, 255, 0.95);
        font-size: 16px;
        font-weight: bold;
    }
    
    QLabel#statsLabel {
        color: rgba(100, 200, 255, 0.9);
        font-size: 13px;
        font-weight: 600;
    }
    
    /* Text Edit - Glass */
    QTextEdit {
        background: rgba(20, 20, 30, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        color: rgba(255, 255, 255, 0.85);
        padding: 8px;
        font-family: 'Consolas', monospace;
        font-size: 11px;
    }
    
    /* Group Box */
    QGroupBox {
        background: rgba(30, 30, 45, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 10px;
        margin-top: 12px;
        padding: 16px;
        font-weight: bold;
        color: rgba(255, 255, 255, 0.9);
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 8px;
    }
    
    /* Status Bar */
    QStatusBar {
        background: rgba(25, 25, 35, 0.8);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom-left-radius: 16px;
        border-bottom-right-radius: 16px;
        color: rgba(255, 255, 255, 0.7);
        padding: 4px;
    }
    
    /* Scrollbar */
    QScrollBar:vertical {
        background: rgba(20, 20, 30, 0.3);
        width: 12px;
        border-radius: 6px;
        margin: 0px;
    }
    
    QScrollBar::handle:vertical {
        background: rgba(100, 100, 120, 0.6);
        border-radius: 6px;
        min-height: 30px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: rgba(120, 120, 150, 0.8);
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    
    /* Menu Bar */
    QMenuBar {
        background: transparent;
        color: rgba(255, 255, 255, 0.9);
        padding: 4px;
    }
    
    QMenuBar::item {
        background: transparent;
        padding: 8px 12px;
        border-radius: 6px;
    }
    
    QMenuBar::item:selected {
        background: rgba(255, 255, 255, 0.1);
    }
    
    QMenu {
        background: rgba(30, 30, 45, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 8px;
        color: rgba(255, 255, 255, 0.9);
    }
    
    QMenu::item {
        padding: 10px 24px;
        border-radius: 6px;
    }
    
    QMenu::item:selected {
        background: rgba(100, 70, 255, 0.3);
    }
    
    /* Tool Bar */
    QToolBar {
        background: rgba(30, 30, 45, 0.6);
        border: none;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        spacing: 8px;
        padding: 8px;
    }
    
    QToolButton {
        background: transparent;
        border: none;
        border-radius: 8px;
        padding: 8px;
        color: rgba(255, 255, 255, 0.8);
    }
    
    QToolButton:hover {
        background: rgba(255, 255, 255, 0.1);
    }
    
    QToolButton:pressed {
        background: rgba(255, 255, 255, 0.05);
    }
    """

def get_light_theme():
    """Liquid Glass Light Theme"""
    return """
    /* Main Window - Light Glass */
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(245, 245, 250, 0.95),
            stop:1 rgba(235, 235, 245, 0.95));
        border-radius: 16px;
    }
    
    /* Custom Title Bar */
    #titleBar {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(255, 255, 255, 0.95),
            stop:1 rgba(245, 245, 250, 0.9));
        border-top-left-radius: 16px;
        border-top-right-radius: 16px;
        border: 1px solid rgba(200, 200, 210, 0.4);
        border-bottom: 1px solid rgba(200, 200, 210, 0.5);
    }
    
    #titleLabel {
        color: rgba(20, 20, 30, 0.9);
        font-size: 14px;
        font-weight: bold;
        padding: 8px 16px;
    }
    
    #titleButton {
        background: transparent;
        border: none;
        color: rgba(60, 60, 80, 0.8);
        font-size: 16px;
        padding: 8px 12px;
        border-radius: 8px;
    }
    
    #titleButton:hover {
        background: rgba(100, 100, 120, 0.15);
        color: rgba(20, 20, 40, 0.9);
    }
    
    #closeButton:hover {
        background: rgba(255, 60, 60, 0.8);
        color: white;
    }
    
    /* Glass Panels */
    QWidget#glassPanel {
        background: rgba(255, 255, 255, 0.7);
        border: 1px solid rgba(200, 200, 210, 0.3);
        border-radius: 12px;
    }
    
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(250, 250, 255, 0.9),
            stop:1 rgba(240, 240, 250, 0.9));
        color: rgba(20, 20, 40, 0.9);
        border: 1px solid rgba(200, 200, 220, 0.5);
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 13px;
        font-weight: 600;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(255, 255, 255, 1),
            stop:1 rgba(245, 245, 255, 1));
        border: 1px solid rgba(100, 100, 150, 0.4);
    }
    
    QPushButton#primaryButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(100, 70, 255, 0.9),
            stop:1 rgba(70, 130, 255, 0.9));
        color: white;
        border: 1px solid rgba(80, 60, 200, 0.3);
    }
    
    QTreeWidget {
        background: rgba(250, 250, 255, 0.6);
        border: 1px solid rgba(200, 200, 220, 0.4);
        border-radius: 10px;
        color: rgba(20, 20, 40, 0.9);
        font-size: 12px;
        padding: 8px;
    }
    
    QTreeWidget::item:selected {
        background: rgba(100, 70, 255, 0.2);
        border: 1px solid rgba(100, 70, 255, 0.4);
    }
    
    QTreeWidget::item:hover {
        background: rgba(100, 100, 150, 0.1);
    }
    
    QProgressBar {
        background: rgba(240, 240, 250, 0.8);
        border: 1px solid rgba(200, 200, 220, 0.4);
        border-radius: 10px;
        height: 20px;
        text-align: center;
        color: rgba(20, 20, 40, 0.9);
        font-weight: bold;
    }
    
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(100, 70, 255, 0.9),
            stop:0.5 rgba(70, 130, 255, 0.9),
            stop:1 rgba(100, 200, 255, 0.9));
        border-radius: 9px;
    }
    
    QLabel {
        color: rgba(40, 40, 60, 0.9);
        font-size: 12px;
    }
    
    QLabel#headerLabel {
        color: rgba(20, 20, 40, 0.95);
        font-size: 16px;
        font-weight: bold;
    }
    
    QTextEdit {
        background: rgba(250, 250, 255, 0.6);
        border: 1px solid rgba(200, 200, 220, 0.4);
        border-radius: 10px;
        color: rgba(30, 30, 50, 0.9);
        padding: 8px;
        font-family: 'Consolas', monospace;
        font-size: 11px;
    }
    
    QStatusBar {
        background: rgba(245, 245, 250, 0.9);
        border-top: 1px solid rgba(200, 200, 220, 0.4);
        border-bottom-left-radius: 16px;
        border-bottom-right-radius: 16px;
        color: rgba(60, 60, 80, 0.8);
        padding: 4px;
    }
    """
