"""
Screen Monitoring Module for Iraqi Aware.

This module contains the background worker thread responsible for capturing
the screen periodically and sending it to the AI Vision Analyzer.
"""

import time
import os
import tempfile
from PyQt6.QtCore import QThread, pyqtSignal
from mss import mss
from PIL import Image
from analyzer import ThreatAnalyzer
from config import AppConfig

class MonitorThread(QThread):
    """
    Background thread that captures the screen and analyzes it.
    Emits a signal when a threat is detected.
    """

    # Signal emitted when a threat is detected: dict containing severity, title, advice
    threat_detected = pyqtSignal(dict)

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self.config = config
        self.analyzer = ThreatAnalyzer(config)
        self._is_running = False
        self._is_paused = False

        # Create a temporary directory for screenshots
        self.temp_dir = tempfile.gettempdir()
        self.screenshot_path = os.path.join(self.temp_dir, "iraqi_aware_capture.jpg")

    def run(self):
        """Main loop for the monitoring thread."""
        self._is_running = True

        with mss() as sct:
            while self._is_running:
                if not self._is_paused:
                    try:
                        # Capture the primary monitor
                        # monitor 1 is usually the primary, 0 is "all monitors"
                        monitor = sct.monitors[1]
                        sct_img = sct.grab(monitor)

                        # Convert to PIL Image and save as JPEG to save space
                        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

                        # Resize if necessary to save bandwidth/API costs (optional)
                        # img.thumbnail((1920, 1080))

                        img.save(self.screenshot_path, format="JPEG", quality=85)

                        # Analyze the image
                        result = self.analyzer.analyze_image(self.screenshot_path)

                        if result:
                            # A threat was detected, emit the signal
                            self.threat_detected.emit(result)

                    except Exception as e:
                        print(f"Error during screen capture or analysis: {e}")

                # Sleep for the configured interval
                # Use smaller sleep intervals to allow responsive stopping/pausing
                interval = self.config.poll_interval
                for _ in range(interval * 10):
                    if not self._is_running:
                        break
                    time.sleep(0.1)

    def stop(self):
        """Stops the monitoring thread."""
        self._is_running = False
        self.wait()

    def pause(self):
        """Pauses the monitoring."""
        self._is_paused = True

    def resume(self):
        """Resumes the monitoring."""
        self._is_paused = False

    def update_config(self, new_config: AppConfig):
        """Updates the configuration being used."""
        self.config = new_config
        self.analyzer = ThreatAnalyzer(self.config)
