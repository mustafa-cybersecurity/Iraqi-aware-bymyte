# Iraqi Aware - Complete Setup Guide for Windows & Linux

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Windows Setup](#windows-setup)
3. [Linux Setup](#linux-setup)
4. [Ollama Setup & Configuration](#ollama-setup--configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

| Requirement | Minimum | Recommended |
|-----------|---------|------------|
| **OS** | Windows 10/Linux (Ubuntu 18.04+) | Windows 11/Ubuntu 20.04+ |
| **Python** | 3.8+ | 3.9+ |
| **RAM** | 4 GB | 8 GB+ |
| **Disk Space** | 2 GB | 5 GB+ |
| **GPU** | Optional | NVIDIA CUDA (faster) |

### What You'll Need
- **Git** installed
- **Python 3.8+** installed
- **Ollama** (for local AI analysis - optional if using OpenAI/NVIDIA)
- **Terminal/Command Prompt** access

---

## Windows Setup

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
   - **Important**: Check "Add Python to PATH" during installation
   - Choose Python 3.9 or higher

2. Verify installation:
   ```cmd
   python --version
   ```
   Should show: `Python 3.x.x`

3. Verify pip is installed:
   ```cmd
   pip --version
   ```

### Step 2: Install Git

1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer with default settings
3. Verify installation:
   ```cmd
   git --version
   ```

### Step 3: Clone the Repository

1. Open **Command Prompt** or **PowerShell**
2. Navigate to where you want to store the project:
   ```cmd
   cd C:\Users\YourUsername\Desktop
   ```
   
3. Clone the repository:
   ```cmd
   git clone https://github.com/mustafa-cybersecurity/Iraqi-aware-bymyte.git
   cd Iraqi-aware-bymyte
   ```

### Step 4: Create Virtual Environment

A virtual environment isolates project dependencies:

```cmd
python -m venv venv
```

Activate it:
```cmd
venv\Scripts\activate
```

You should see `(venv)` at the start of your terminal line, indicating it's active.

### Step 5: Install Dependencies

Navigate to the iraqi_aware directory:
```cmd
cd iraqi_aware
```

Install all required packages:
```cmd
pip install -r requirements.txt
```

This installs:
- `PyQt6` - GUI framework
- `mss` - Screenshot capture
- `Pillow` - Image processing
- `openai` - OpenAI API client
- `requests` - HTTP requests (for Ollama)

### Step 6: Install Ollama (Optional but Recommended)

#### Download & Install Ollama

1. Go to [ollama.ai](https://ollama.ai) or [ollama.com](https://ollama.com)
2. Download the Windows installer
3. Run the installer and follow the prompts
4. Ollama will start automatically as a Windows service

#### Verify Ollama is Running

1. Open Command Prompt
2. Check if Ollama service is running:
   ```cmd
   netstat -an | findstr 11434
   ```
   
   If you see a line with `LISTENING`, Ollama is running ✓

3. Or simply try:
   ```cmd
   curl http://localhost:11434
   ```
   
   Should return some response (not an error)

#### Pull a Vision Model

Open Command Prompt and run:

```cmd
ollama pull llava
```

This downloads the LLaVA model (~5-6 GB). Wait for it to complete.

Other models you can use:
- `ollama pull llava:7b` - Faster, lighter
- `ollama pull llava:13b` - Default, balanced
- `ollama pull bakllava` - Faster alternative

### Step 7: Configure Iraqi Aware

You have two options:

#### Option A: Automatic Setup (Recommended)

1. Navigate to the iraqi_aware directory:
   ```cmd
   cd iraqi_aware
   ```

2. Run the application:
   ```cmd
   python main.py
   ```

3. The Setup Wizard will appear:
   - Select **"ollama"** as the AI Provider
   - Leave **API Key** empty
   - Leave **Model Name** empty (defaults to `llava`)
   - Verify **Local URL** is: `http://localhost:11434/api/generate`
   - Click **"Save & Start"**

#### Option B: Manual Configuration

1. Create a file `config.json` in the `iraqi_aware` directory:

```json
{
    "provider": "ollama",
    "api_key": "",
    "model": "llava",
    "local_url": "http://localhost:11434/api/generate",
    "poll_interval": 5
}
```

2. Save the file

### Step 8: Run the Application

From the `iraqi_aware` directory:

```cmd
python main.py
```

Expected behavior:
- Application launches with a system tray icon
- First time: Setup wizard appears
- After setup: Monitoring starts automatically
- Alerts appear when threats are detected

---

## Linux Setup

### Step 1: Install Python

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y
```

#### Fedora/RHEL:
```bash
sudo dnf install python3 python3-pip git -y
```

#### Arch Linux:
```bash
sudo pacman -S python python-pip git
```

Verify installation:
```bash
python3 --version
pip3 --version
```

### Step 2: Install Required System Dependencies

#### Ubuntu/Debian:
```bash
sudo apt install libxcb-cursor0 libxkbcommon-x11-0 -y
```

#### Fedora/RHEL:
```bash
sudo dnf install libxkbcommon-x11 -y
```

#### Arch Linux:
```bash
sudo pacman -S libxkbcommon-x11
```

### Step 3: Clone the Repository

```bash
cd ~
git clone https://github.com/mustafa-cybersecurity/Iraqi-aware-bymyte.git
cd Iraqi-aware-bymyte
```

### Step 4: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

### Step 5: Install Dependencies

Navigate to the iraqi_aware directory:
```bash
cd iraqi_aware
```

Install all required packages:
```bash
pip install -r requirements.txt
```

### Step 6: Install Ollama (Optional but Recommended)

#### Download & Install Ollama

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

Or download from [ollama.com](https://ollama.com)

#### Start Ollama Service

```bash
ollama serve
```

This starts Ollama on port 11434. Leave this terminal running.

**Alternative**: Run Ollama in background:
```bash
ollama serve &
```

#### In Another Terminal: Pull a Vision Model

Open a new terminal and run:

```bash
ollama pull llava
```

Wait for the download to complete (~5-6 GB for default model).

Other models:
- `ollama pull llava:7b` - Faster
- `ollama pull bakllava` - Fast alternative

### Step 7: Verify Ollama is Running

In another terminal:
```bash
curl http://localhost:11434
```

Should see a response (not an error).

### Step 8: Configure Iraqi Aware

#### Option A: Automatic Setup (Recommended)

```bash
python main.py
```

Setup Wizard will appear:
- Select **"ollama"**
- Leave **API Key** empty
- Leave **Model Name** empty (uses `llava`)
- Verify **Local URL**: `http://localhost:11434/api/generate`
- Click **"Save & Start"**

#### Option B: Manual Configuration

Create `config.json`:

```bash
cat > config.json << EOF
{
    "provider": "ollama",
    "api_key": "",
    "model": "llava",
    "local_url": "http://localhost:11434/api/generate",
    "poll_interval": 5
}
EOF
```

### Step 9: Run the Application

```bash
python main.py
```

---

## Ollama Setup & Configuration

### What is Ollama?

Ollama lets you run large language models locally on your computer without needing:
- Internet connection
- API keys
- Cloud subscriptions
- Sending screenshots to servers

### Available Vision Models

| Model | Size | Speed | Quality | Command |
|-------|------|-------|---------|---------|
| **llava** | 5.5GB | Medium | Good | `ollama pull llava` |
| **llava:7b** | 3.9GB | Fast | Good | `ollama pull llava:7b` |
| **bakllava** | 4.4GB | Fast | Good | `ollama pull bakllava` |
| **neural-chat** | 4GB | Fast | Basic | `ollama pull neural-chat` |

### Checking Installed Models

```bash
ollama list
```

### Testing Ollama Directly

```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llava",
    "prompt": "What is in this image?",
    "stream": false
  }'
```

### Configuration Details

The `config.json` file stores:

```json
{
    "provider": "ollama",           // Use Ollama as AI provider
    "api_key": "",                  // Not needed for Ollama (leave empty)
    "model": "llava",               // Vision model to use
    "local_url": "http://localhost:11434/api/generate",  // Ollama API endpoint
    "poll_interval": 5              // Seconds between screenshots
}
```

---

## Running the Application

### Daily Usage

#### Windows:
```cmd
cd C:\path\to\Iraqi-aware-bymyte\iraqi_aware
venv\Scripts\activate
python main.py
```

#### Linux:
```bash
cd ~/Iraqi-aware-bymyte/iraqi_aware
source ../venv/bin/activate
python main.py
```

### Make Sure Ollama is Running

**Windows**: Ollama runs as a service automatically after installation

**Linux**: Start Ollama in another terminal:
```bash
ollama serve
```

### System Tray Controls

Once the app is running:

1. **Look for the Tray Icon** - Usually in bottom-right (Windows) or top-right (Linux)
2. **Right-click the icon** for menu:
   - **Pause Monitoring** - Stop analyzing screenshots
   - **Resume Monitoring** - Start analyzing again
   - **Settings** - Reconfigure AI provider
   - **Exit** - Close the application

### What Happens

1. Takes a screenshot every 5 seconds
2. Sends it to Ollama for analysis
3. AI analyzes for cybersecurity threats:
   - Phishing emails/websites
   - Fake tech support pop-ups
   - Exposed passwords
   - Suspicious downloads
   - Malicious activity

4. Shows alerts with:
   - **Severity**: none, low, medium, high
   - **Threat Title**: What was detected
   - **Advice**: What you should do

---

## Troubleshooting

### Problem: Python not found

**Windows:**
- Reinstall Python
- **IMPORTANT**: Check "Add Python to PATH"
- Restart Command Prompt

**Linux:**
```bash
python3 --version
# Use 'python3' and 'pip3' instead of 'python' and 'pip'
```

### Problem: PyQt6 installation fails

**Windows:**
```cmd
pip install --upgrade pip
pip install PyQt6==6.6.0
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install python3-pyqt6
pip install PyQt6==6.6.0
```

### Problem: Ollama not responding

**Windows:**
1. Check if Ollama service is running
2. Open Settings > Apps > Services
3. Look for "Ollama"
4. If not running, restart your computer

**Linux:**
```bash
# Kill old process
pkill ollama

# Start fresh
ollama serve
```

### Problem: Application won't start

1. Check Python version:
   ```bash
   python --version  # Should be 3.8+
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. Check for errors in console output

### Problem: No threats detected

1. Verify Ollama is running and model is pulled:
   ```bash
   ollama list
   ```

2. Test Ollama with curl:
   ```bash
   curl http://localhost:11434
   ```

3. Verify config.json settings:
   ```bash
   cat config.json  # Linux/Mac
   type config.json  # Windows
   ```

4. Check console for error messages

### Problem: Screenshot analysis fails

1. Check internet connection (for cloud providers)
2. Verify Ollama service status
3. Check system resources (RAM, disk space)
4. Try a smaller model: `ollama pull llava:7b`

### Problem: High CPU/Memory Usage

1. **Increase poll interval** in config.json (e.g., `"poll_interval": 10`)
2. **Use smaller model**: `ollama pull llava:7b`
3. **Close other applications**
4. **Enable GPU acceleration** (if available)

### Problem: GPU Acceleration (Optional)

For faster analysis, enable GPU:

**NVIDIA GPU - Linux:**
```bash
# Install NVIDIA CUDA toolkit
# Then Ollama will auto-detect and use CUDA
```

**NVIDIA GPU - Windows:**
- Ollama automatically detects and uses NVIDIA GPUs if installed

**AMD GPU - Linux:**
```bash
# Install ROCm for AMD support
```

---

## Performance Tips

1. **Increase Screenshot Interval** - Change `poll_interval` to 10+ seconds
2. **Use Smaller Model** - `llava:7b` is faster
3. **Close Background Apps** - Free up CPU/RAM
4. **Monitor System Resources** - Use Task Manager (Windows) or `top` (Linux)
5. **Disable GPU** if causing issues - Ollama will use CPU instead

---

## Security Notes

1. **Keep API Keys Safe** - Don't share `config.json`
2. **Use Strong Passwords** - For your accounts
3. **Update Regularly** - Run `pip install -r requirements.txt --upgrade`
4. **Screenshots are Local** - With Ollama, screenshots never leave your computer
5. **Backup Config** - Save `config.json` in a safe place

---

## Need Help?

1. Check the main [README.md](README.md)
2. Open an issue on [GitHub](https://github.com/mustafa-cybersecurity/Iraqi-aware-bymyte/issues)
3. Check Ollama documentation at [ollama.com](https://ollama.com)

---

**Happy monitoring! Stay secure with Iraqi Aware by Byte! 🔒**
