# Iraqi Aware by Byte

A cybersecurity threat detection application that uses AI vision models to analyze screenshots and identify potential security threats in real-time.

## Overview

Iraqi Aware is a PyQt6-based desktop application that continuously monitors your screen and analyzes it using AI-powered vision models to detect cybersecurity threats such as:
- Phishing emails and websites
- Suspicious pop-ups and fake tech support warnings
- Dangerous file downloads
- Exposed passwords
- Malicious or fraudulent activities

## Features

- **Real-time Screen Monitoring**: Continuously captures and analyzes screenshots
- **Multiple AI Providers**: Support for OpenAI, NVIDIA, and Ollama
- **System Tray Integration**: Runs in the background with system tray controls
- **Pause/Resume Functionality**: Control monitoring from the system tray
- **Setup Wizard**: Easy configuration on first launch
- **Threat Alerts**: Instant notifications when threats are detected
- **Configurable Analysis**: Customize AI provider, model, and API settings

## Requirements

- Python 3.8 or higher
- PyQt6 >= 6.6.0
- mss >= 9.0.0
- Pillow >= 10.0.0
- openai >= 1.0.0
- requests >= 2.31.0

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/mustafa-cybersecurity/Iraqi-aware-bymyte.git
cd Iraqi-aware-bymyte
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
cd iraqi_aware
pip install -r requirements.txt
```

## How to Run

### Basic Startup

```bash
cd iraqi_aware
python main.py
```

### First Time Setup

When you run the application for the first time, a setup wizard will guide you through:
1. Selecting your AI provider (OpenAI, NVIDIA, or Ollama)
2. Entering your API key or local URL
3. Choosing the AI model to use
4. Setting monitoring frequency and screenshot interval

### Run with Configuration Already Set

Once you've completed the initial setup, simply run:

```bash
python main.py
```

The application will:
- Launch with a system tray icon
- Start monitoring your screen automatically
- Display alerts when threats are detected

## Configuration

The application configuration is managed by the `ConfigManager` class. Settings are saved and can be updated through:
- The setup wizard on first launch
- The settings menu in the system tray

### Supported AI Providers

1. **OpenAI**
   - Requires: OpenAI API key
   - Default Model: gpt-4o

2. **NVIDIA**
   - Requires: NVIDIA AI Cloud API key
   - Default Model: meta/llama-3.2-90b-vision-instruct
   - Endpoint: https://integrate.api.nvidia.com/v1

3. **Ollama**
   - Requires: Local Ollama instance running
   - Default Model: llava
   - Default URL: http://localhost:11434/api/generate

## Usage

### System Tray Controls

Once the application is running:
- **Pause/Resume**: Toggle monitoring on/off from the system tray menu
- **Settings**: Access configuration settings
- **Exit**: Close the application

### What It Does

1. **Captures Screenshots**: Takes screenshots at regular intervals
2. **Analyzes with AI**: Sends screenshots to your configured AI provider
3. **Detects Threats**: Identifies potential cybersecurity risks
4. **Alerts You**: Displays notifications with threat details and advice

## Project Structure

```
iraqi_aware/
├── main.py           # Main entry point and application orchestration
├── config.py         # Configuration management
├── analyzer.py       # AI vision analysis module
├── monitor.py        # Screen monitoring and analysis thread
├── ui.py             # PyQt6 UI components (wizard, notifications, tray)
├── requirements.txt  # Python dependencies
└── .gitignore        # Git ignore rules
```

## Key Components

### main.py
Wires together the configuration, monitoring thread, and UI components into a single PyQt6 application.

### analyzer.py
Interfaces with different AI vision models (OpenAI, NVIDIA, Ollama) to analyze screenshots for potential cybersecurity threats.

### monitor.py
Runs a background monitoring thread that captures screenshots and triggers threat analysis.

### ui.py
Provides PyQt6 UI components including setup wizard, notification popups, and system tray application.

### config.py
Manages application configuration, including API keys and model settings.

## Threat Response

When a threat is detected, you'll receive:
- **Severity Level**: none, low, medium, or high
- **Threat Title**: Description of the detected threat
- **Professional Advice**: Actionable steps to take immediately

## Tips for Best Results

1. **Ensure Stable Internet**: Required for API calls to AI providers
2. **Keep API Keys Secure**: Treat API keys as sensitive credentials
3. **Monitor System Resources**: Real-time monitoring uses CPU and memory
4. **Review Alerts**: Check all threat notifications carefully
5. **Update Regularly**: Keep the application and dependencies updated

## Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that PyQt6 is properly installed for your OS

### Setup wizard doesn't appear
- Delete your configuration file or restart the application
- Check application logs for errors

### No threats detected
- Verify your AI provider API key is valid
- Ensure your AI model is properly configured
- Check that the monitoring interval is appropriate

### Screenshot analysis fails
- Verify your internet connection
- Check that your API key hasn't expired
- Try switching to a different AI provider

## License

This project is released as open source. See the repository for more details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to help improve Iraqi Aware.

## Support

For issues, questions, or feedback, please open an issue on the GitHub repository.

---

**Stay secure and aware with Iraqi Aware by Byte!**
