"""
User Interface Module for Iraqi Aware.

Contains the Setup Wizard, Notification Popup, and System Tray elements.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QFormLayout, QWidget, QGraphicsOpacityEffect,
    QApplication, QSystemTrayIcon, QMenu
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty, pyqtSignal
from PyQt6.QtGui import QColor, QPalette, QIcon, QAction

from config import ConfigManager, AppConfig

class SetupWizard(QDialog):
    """First-run setup wizard to select AI provider and configure keys."""

    config_saved = pyqtSignal()

    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setWindowTitle("Iraqi Aware - Setup")
        self.setFixedSize(400, 300)
        self.init_ui()
        self.load_current_settings()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Welcome to Iraqi Aware")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)

        form_layout = QFormLayout()

        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["openai", "nvidia", "ollama"])
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        form_layout.addRow("AI Provider:", self.provider_combo)

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("API Key:", self.api_key_input)

        self.model_input = QLineEdit()
        self.model_input.setPlaceholderText("Leave empty for default")
        form_layout.addRow("Model Name:", self.model_input)

        self.local_url_input = QLineEdit()
        self.local_url_input.setText("http://localhost:11434/api/generate")
        form_layout.addRow("Local URL (Ollama):", self.local_url_input)

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save & Start")
        self.save_btn.clicked.connect(self.save_settings)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.on_provider_changed(self.provider_combo.currentText())

    def load_current_settings(self):
        config = self.config_manager.config
        if config.provider:
            index = self.provider_combo.findText(config.provider)
            if index >= 0:
                self.provider_combo.setCurrentIndex(index)
        self.api_key_input.setText(config.api_key)
        self.model_input.setText(config.model)
        self.local_url_input.setText(config.local_url)

    def on_provider_changed(self, provider: str):
        if provider == "ollama":
            self.api_key_input.setEnabled(False)
            self.local_url_input.setEnabled(True)
        else:
            self.api_key_input.setEnabled(True)
            self.local_url_input.setEnabled(False)

    def save_settings(self):
        config = self.config_manager.config
        config.provider = self.provider_combo.currentText()
        config.api_key = self.api_key_input.text()
        config.model = self.model_input.text()
        config.local_url = self.local_url_input.text()

        self.config_manager.save()
        self.config_saved.emit()
        self.accept()


class NotificationPopup(QWidget):
    """Dynamic, frameless popup for showing threat alerts."""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Frameless, always on top, tool window (doesn't show in taskbar)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedSize(350, 120)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)

        # Container widget for styling
        self.container = QWidget(self)
        self.container.setObjectName("container")
        self.container_layout = QVBoxLayout(self.container)

        self.title_label = QLabel("Title")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: white;")
        self.title_label.setWordWrap(True)

        self.advice_label = QLabel("Advice")
        self.advice_label.setStyleSheet("font-size: 12px; color: white;")
        self.advice_label.setWordWrap(True)

        self.container_layout.addWidget(self.title_label)
        self.container_layout.addWidget(self.advice_label)

        self.layout.addWidget(self.container)

        # Opacity effect for fade in/out
        self._opacity = 0.0
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(self._opacity)

        # Animations
        self.fade_in_anim = QPropertyAnimation(self, b"windowOpacityProperty")
        self.fade_in_anim.setDuration(500)
        self.fade_in_anim.setStartValue(0.0)
        self.fade_in_anim.setEndValue(1.0)

        self.fade_out_anim = QPropertyAnimation(self, b"windowOpacityProperty")
        self.fade_out_anim.setDuration(500)
        self.fade_out_anim.setStartValue(1.0)
        self.fade_out_anim.setEndValue(0.0)
        self.fade_out_anim.finished.connect(self.close)

        # Auto-hide timer
        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide_popup)

    # Property for animation
    def get_opacity(self):
        return self._opacity

    def set_opacity(self, opacity):
        self._opacity = opacity
        self.opacity_effect.setOpacity(opacity)

    windowOpacityProperty = pyqtProperty(float, get_opacity, set_opacity)

    def show_alert(self, threat_data: dict):
        severity = threat_data.get("severity", "low")
        title = threat_data.get("title", "Threat Detected")
        advice = threat_data.get("advice", "Please be cautious.")

        self.title_label.setText(title)
        self.advice_label.setText(advice)

        # Color coding
        if severity == "high":
            bg_color = "#D32F2F" # Red
        elif severity == "medium":
            bg_color = "#F57C00" # Orange/Yellow
        else:
            bg_color = "#1976D2" # Blue

        self.container.setStyleSheet(f"""
            QWidget#container {{
                background-color: {bg_color};
                border-radius: 10px;
                border: 2px solid white;
            }}
        """)

        # Position in bottom right
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - self.width() - 20
        y = screen.height() - self.height() - 40
        self.move(x, y)

        self.show()

        # Stop any ongoing fade-out
        if self.fade_out_anim.state() == QPropertyAnimation.State.Running:
            self.fade_out_anim.stop()

        # Fade in
        self.fade_in_anim.start()

        # Hide after 15 seconds
        self.hide_timer.start(15000)

    def hide_popup(self):
        # Stop fade-in just in case
        if self.fade_in_anim.state() == QPropertyAnimation.State.Running:
            self.fade_in_anim.stop()

        # Fade out
        self.fade_out_anim.start()

    def mousePressEvent(self, event):
        """Close on click."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.hide_popup()


class SystemTrayApp:
    """Manages the system tray icon and menu."""

    def __init__(self, parent=None):
        self.tray_icon = QSystemTrayIcon(parent)

        # Try to set an icon
        icon = QIcon.fromTheme("security-high", QIcon("icon.png")) # fallback to generic if icon.png missing
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("Iraqi Aware")

        self.menu = QMenu()

        self.pause_action = QAction("Pause Monitoring", self.menu)
        self.pause_action.setCheckable(True)
        self.menu.addAction(self.pause_action)

        self.settings_action = QAction("Settings...", self.menu)
        self.menu.addAction(self.settings_action)

        self.menu.addSeparator()

        self.exit_action = QAction("Exit", self.menu)
        self.menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(self.menu)

    def show(self):
        self.tray_icon.show()
