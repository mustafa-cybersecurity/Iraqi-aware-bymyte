"""
Main Entry Point for Iraqi Aware.

Wires together the Configuration, Monitoring Thread, and UI components
into a single PyQt6 application.
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from config import ConfigManager
from ui import SetupWizard, NotificationPopup, SystemTrayApp
from monitor import MonitorThread

class IraqiAwareApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False) # Keep running in tray

        self.config_manager = ConfigManager()

        # UI Components
        self.tray = SystemTrayApp()
        self.notification = NotificationPopup()

        # Connect tray signals
        self.tray.pause_action.toggled.connect(self.toggle_pause)
        self.tray.settings_action.triggered.connect(self.show_settings)
        self.tray.exit_action.triggered.connect(self.exit_app)

        # Monitor Thread
        self.monitor_thread = None

    def start(self):
        """Starts the application."""
        if not self.config_manager.is_setup_complete():
            self.show_settings()
        else:
            self.start_monitoring()

        self.tray.show()
        return self.app.exec()

    def show_settings(self):
        """Shows the setup wizard."""
        wizard = SetupWizard(self.config_manager)
        wizard.config_saved.connect(self.on_settings_saved)
        wizard.exec()

    def on_settings_saved(self):
        """Called when settings are saved from the wizard."""
        if self.monitor_thread:
            self.monitor_thread.update_config(self.config_manager.config)
        elif self.config_manager.is_setup_complete():
            self.start_monitoring()

    def start_monitoring(self):
        """Starts the background monitoring thread."""
        if not self.monitor_thread:
            self.monitor_thread = MonitorThread(self.config_manager.config)
            self.monitor_thread.threat_detected.connect(self.on_threat_detected)
            self.monitor_thread.start()

    def toggle_pause(self, paused: bool):
        """Pauses or resumes monitoring based on tray menu toggle."""
        if self.monitor_thread:
            if paused:
                self.monitor_thread.pause()
                self.tray.pause_action.setText("Resume Monitoring")
                self.tray.tray_icon.showMessage("Iraqi Aware", "Monitoring paused.")
            else:
                self.monitor_thread.resume()
                self.tray.pause_action.setText("Pause Monitoring")
                self.tray.tray_icon.showMessage("Iraqi Aware", "Monitoring resumed.")

    def on_threat_detected(self, threat_data: dict):
        """Callback when the monitor thread detects a threat."""
        self.notification.show_alert(threat_data)

    def exit_app(self):
        """Cleans up and exits the application."""
        if self.monitor_thread:
            self.monitor_thread.stop()
        self.app.quit()

if __name__ == "__main__":
    app = IraqiAwareApp()
    sys.exit(app.start())
