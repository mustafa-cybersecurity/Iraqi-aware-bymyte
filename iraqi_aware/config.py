"""
Configuration Management for Iraqi Aware.

This module handles loading, saving, and managing user preferences
and application settings locally in a JSON format.
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import Optional

CONFIG_FILE = "config.json"

@dataclass
class AppConfig:
    provider: str = ""  # openai, nvidia, ollama
    api_key: str = ""
    model: str = ""
    local_url: str = "http://localhost:11434/api/generate" # default for ollama
    poll_interval: int = 5  # seconds

class ConfigManager:
    """Manages the application configuration."""

    def __init__(self, config_path: str = CONFIG_FILE):
        self.config_path = config_path
        self.config = AppConfig()
        self.load()

    def load(self) -> None:
        """Loads configuration from the JSON file if it exists."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Update dataclass fields with loaded data
                    for key, value in data.items():
                        if hasattr(self.config, key):
                            setattr(self.config, key, value)
            except Exception as e:
                print(f"Error loading config: {e}")

    def save(self) -> None:
        """Saves current configuration to the JSON file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(asdict(self.config), f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def is_setup_complete(self) -> bool:
        """Checks if the initial setup is complete."""
        if not self.config.provider:
            return False
        if self.config.provider in ("openai", "nvidia") and not self.config.api_key:
            return False
        if self.config.provider == "ollama" and not self.config.local_url:
            return False
        return True
