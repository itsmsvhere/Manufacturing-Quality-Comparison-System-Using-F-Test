# Installation Guide - Manufacturing Quality Comparison Analyzer

## Overview
This guide provides step-by-step instructions for installing and running the Manufacturing Quality Comparison Analyzer application.

---

## System Requirements

- **Python Version:** 3.8 or higher
- **Operating System:** Windows, macOS, or Linux
- **RAM:** Minimum 512MB (1GB+ recommended)
- **Disk Space:** ~200MB (including Python and dependencies)
- **Internet Connection:** Required for initial installation

### Check Your Python Version

Open terminal/command prompt and run:

```bash
python --version
```

If you don't have Python installed, download from https://www.python.org/downloads/

---

## Installation Steps

### Step 1: Download Application Files

Download all files from the release package:
- `manufacturing_quality_analyzer.py` (Main application)
- `requirements.txt` (Python dependencies)
- `README.md` (Documentation)
- `sample_plant_1.csv` (Sample data)
- `sample_plant_2.csv` (Sample data)

Create a folder for the application:
```bash
mkdir quality_analyzer
cd quality_analyzer
```

Place all files in this folder.

### Step 2: Open Terminal/Command Prompt

**Windows:**
- Press `Win + R`
- Type `cmd` and press Enter
- Navigate to application folder: `cd C:\path\to\quality_analyzer`

**macOS:**
- Open Applications → Utilities → Terminal
- Navigate: `cd /path/to/quality_analyzer`

**Linux:**
- Open Terminal application
- Navigate: `cd /path/to/quality_analyzer`

### Step 3: Install Python Packages

Run this command in the terminal:

```bash
pip install -r requirements.txt
```

This installs all required packages:
- customtkinter (modern GUI)
- pandas (data handling)
- matplotlib (graphs)
- scipy (statistics)
- numpy (numerical computation)
- reportlab (PDF export)

**Installation Time:** 2-5 minutes (depending on internet speed)

### Step 4: Verify Installation

Run this command to verify successful installation:

```bash
python -c "import customtkinter, pandas, matplotlib, scipy, numpy, reportlab; print('All packages installed successfully!')"
```

You should see: `All packages installed successfully!`

### Step 5: Run the Application

Execute the application:

```bash
python manufacturing_quality_analyzer.py
```

The application window should appear in 2-3 seconds.

---

## Troubleshooting Installation

### Issue: "Python not found" or "python: command not found"

**Solution:**
1. Verify Python is installed: https://www.python.org/downloads/
2. During Python installation, check "Add Python to PATH"
3. Restart terminal after installing Python
4. On Windows, try `python3` instead of `python`

### Issue: "pip is not recognized as an internal or external command"

**Solution:**
```bash
python -m pip install -r requirements.txt
```

### Issue: "Permission denied" error on macOS/Linux

**Solution:**
```bash
pip install --user -r requirements.txt
```

### Issue: "Requirement already satisfied" warnings

**Solution:** This is normal - skip and run the application

### Issue: "ModuleNotFoundError: No module named 'customtkinter'"

**Solution:**
```bash
pip install customtkinter --upgrade
```

### Issue: "No module named '_tkinter'"

**Solution:**

**Windows:** Reinstall Python and select "tcl/tk and IDLE"

**macOS:**
```bash
brew install python-tk
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

---

## Running the Application

### Basic Launch

Navigate to application folder and run:

```bash
python manufacturing_quality_analyzer.py
```

### Create a Shortcut (Windows)

1. Right-click on desktop
2. Select "New → Shortcut"
3. Enter: `cmd /c "cd C:\path\to\quality_analyzer && python manufacturing_quality_analyzer.py"`
4. Click Next and name it "Quality Analyzer"
5. Click Finish
6. Double-click shortcut to launch

### Create a Shortcut (macOS)

1. Open Terminal
2. Create script:
```bash
cat > ~/Desktop/run_analyzer.command << 'EOF'
#!/bin/bash
cd /path/to/quality_analyzer
python manufacturing_quality_analyzer.py
EOF
chmod +x ~/Desktop/run_analyzer.command
```
3. Double-click the file on Desktop to run

### Create a Shortcut (Linux)

Create desktop shortcut file:
```bash
cat > ~/Desktop/quality_analyzer.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Quality Analyzer
Exec=bash -c "cd /path/to/quality_analyzer && python manufacturing_quality_analyzer.py"
Icon=application-x-executable
Terminal=false
EOF
chmod +x ~/Desktop/quality_analyzer.desktop
```

---

## Testing Installation

### Test with Sample Data

1. Launch application
2. Click "📁 Upload CSV" under Plant 1
3. Select `sample_plant_1.csv`
4. Click "📁 Upload CSV" under Plant 2
5. Select `sample_plant_2.csv`
6. Click "🔬 Analyze Data"
7. Results should appear in 1-2 seconds

**Expected Result:**
- Plant 2 should have higher variance (lower quality consistency)
- P-value should be < 0.05 (significant difference)

---

## Uninstallation

### Remove Application

Simply delete the application folder:
```bash
rm -rf /path/to/quality_analyzer
```

### Remove Python Packages (Optional)

```bash
pip uninstall customtkinter pandas matplotlib scipy numpy reportlab
```

### Remove Python (Full Uninstall)

**Windows:** Control Panel → Programs → Uninstall Python

**macOS:** Remove `/Library/Frameworks/Python.framework/`

**Linux:** `sudo apt-get purge python3`

---

## Virtual Environment (Optional - Advanced)

For isolated Python environment:

```bash
# Create virtual environment
python -m venv analyzer_env

# Activate environment
# Windows:
analyzer_env\Scripts\activate
# macOS/Linux:
source analyzer_env/bin/activate

# Install packages
pip install -r requirements.txt

# Run application
python manufacturing_quality_analyzer.py
```

---

## Support

If installation fails:

1. **Check Python version:** `python --version` (must be 3.8+)
2. **Verify pip:** `pip --version`
3. **Check internet connection** for package downloads
4. **Review error messages** in terminal
5. **Try pip upgrade:** `pip install --upgrade pip`

For persistent issues, refer to the README.md file included with the application.

---

## Next Steps

After successful installation:

1. Read `README.md` for usage instructions
2. Test with provided sample CSV files
3. Prepare your own data in CSV format
4. Run analyses and generate reports

Enjoy using the Manufacturing Quality Comparison Analyzer!

---

**Last Updated:** February 2025  
**Version:** 1.0.0  
**Status:** Production Ready
