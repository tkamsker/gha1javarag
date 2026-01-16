# Production Setup Guide

**Problem**: `codeindex: command not found` on production server

**Root Cause**: Package not installed or virtual environment not activated

---

## Quick Fix (Production Server)

```bash
# Navigate to project directory
cd /home/tkamsker/development/Iteration20/gha1javarag

# Check if virtual environment exists
ls -la | grep venv

# If .venv exists, activate it
source .venv/bin/activate

# Verify activation (should show path to .venv)
which python
# Should output: /home/tkamsker/development/Iteration20/gha1javarag/.venv/bin/python

# Check if codeindex is installed
which codeindex

# If not installed, install the package
pip install -e .

# Verify installation
codeindex --version

# Now you can use codeindex
codeindex status
```

---

## Full Setup from Scratch (If Needed)

### Step 1: Check Python Version

```bash
python3 --version
# Should be Python 3.8+

# If not available
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Step 2: Navigate to Project

```bash
cd /home/tkamsker/development/Iteration20/gha1javarag

# Verify you're in the right place
ls -la | grep -E "setup.py|requirements.txt|src"
```

### Step 3: Create Virtual Environment (If Missing)

```bash
# Check if .venv exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists"
fi

# Or use the setup script
./step1.sh
```

### Step 4: Activate Virtual Environment

```bash
source .venv/bin/activate

# Verify activation
echo $VIRTUAL_ENV
# Should output: /home/tkamsker/development/Iteration20/gha1javarag/.venv
```

### Step 5: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### Step 6: Verify Installation

```bash
# Check if codeindex is available
which codeindex
# Should output: /home/tkamsker/development/Iteration20/gha1javarag/.venv/bin/codeindex

# Check version
codeindex --version

# Test help command
codeindex --help
```

---

## Common Issues

### Issue 1: "No module named 'codeindex'"

**Cause**: Package not installed

**Fix**:
```bash
cd /home/tkamsker/development/Iteration20/gha1javarag
source .venv/bin/activate
pip install -e .
```

### Issue 2: "command not found: codeindex"

**Cause**: Virtual environment not activated

**Fix**:
```bash
source .venv/bin/activate
which codeindex  # Verify
```

### Issue 3: Wrong virtual environment

**Cause**: Using `venv/` instead of `.venv/`

**Fix**:
```bash
# Check which directories exist
ls -la | grep venv

# If both exist, use .venv (correct)
source .venv/bin/activate

# If only venv exists (old), recreate
rm -rf venv
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Issue 4: Permission denied

**Cause**: Script files not executable

**Fix**:
```bash
chmod +x *.sh
```

### Issue 5: setup.py not found

**Cause**: Not in project root directory

**Fix**:
```bash
cd /home/tkamsker/development/Iteration20/gha1javarag
ls -la setup.py  # Verify
```

---

## Using with Shell Scripts

All shell scripts automatically activate the virtual environment. You can use them without manual activation:

### Method 1: Use Shell Scripts (Recommended)

```bash
# These scripts activate .venv automatically
./run-cuco.sh --yes /path/to/cuco-ui-admin
./step1.sh
./step2.sh myproject
```

### Method 2: Use with-venv.sh Wrapper

```bash
# Run any command in virtual environment
./with-venv.sh codeindex status
./with-venv.sh codeindex search "test"
./with-venv.sh pytest tests/
```

### Method 3: Manual Activation

```bash
# Activate once per terminal session
source .venv/bin/activate

# Then run commands normally
codeindex status
codeindex search "test"

# Deactivate when done
deactivate
```

---

## Persistent Activation (Add to .bashrc)

If you want `codeindex` always available on production:

```bash
# Edit .bashrc
nano ~/.bashrc

# Add at the end:
# Auto-activate codeindex virtual environment
if [ -d "/home/tkamsker/development/Iteration20/gha1javarag/.venv" ]; then
    source /home/tkamsker/development/Iteration20/gha1javarag/.venv/bin/activate
fi

# Save and reload
source ~/.bashrc

# Now codeindex is always available
codeindex status
```

**Warning**: This activates the venv globally in all terminals. May conflict with other Python projects.

---

## Alternative: Create Alias

More flexible than .bashrc activation:

```bash
# Edit .bashrc
nano ~/.bashrc

# Add alias
alias codeindex='/home/tkamsker/development/Iteration20/gha1javarag/.venv/bin/codeindex'

# Save and reload
source ~/.bashrc

# Now you can use codeindex from anywhere
cd /tmp
codeindex status  # Works!
```

---

## Verification Checklist

Run these commands to verify everything is set up correctly:

```bash
# 1. Check project directory
cd /home/tkamsker/development/Iteration20/gha1javarag
pwd
# Should output: /home/tkamsker/development/Iteration20/gha1javarag

# 2. Check virtual environment exists
ls -la .venv/
# Should show bin/, lib/, etc.

# 3. Activate virtual environment
source .venv/bin/activate

# 4. Verify Python path
which python
# Should output: .../gha1javarag/.venv/bin/python

# 5. Verify pip path
which pip
# Should output: .../gha1javarag/.venv/bin/pip

# 6. Check installed packages
pip list | grep codeindex
# Should show: codeindex (editable)

# 7. Verify codeindex command
which codeindex
# Should output: .../gha1javarag/.venv/bin/codeindex

# 8. Test codeindex
codeindex --version
codeindex --help

# 9. Check services
./check-services.sh

# 10. Test full status
codeindex status
```

---

## Production Deployment Checklist

Before running `codeindex` commands on production:

- [ ] Project directory exists: `/home/tkamsker/development/Iteration20/gha1javarag`
- [ ] Virtual environment exists: `.venv/`
- [ ] Virtual environment activated: `source .venv/bin/activate`
- [ ] Package installed: `pip install -e .`
- [ ] Command available: `which codeindex`
- [ ] Ollama running: `curl http://localhost:11434/api/tags`
- [ ] Weaviate running: `curl http://localhost:8080/v1/meta`
- [ ] Scripts executable: `chmod +x *.sh`

---

## Quick Reference

### One-Time Setup (Run Once)

```bash
cd /home/tkamsker/development/Iteration20/gha1javarag
./step1.sh
```

### Before Each Session

```bash
cd /home/tkamsker/development/Iteration20/gha1javarag
source .venv/bin/activate
```

### Using Commands

```bash
# Option 1: After activation
codeindex status

# Option 2: Without activation (use wrapper)
./with-venv.sh codeindex status

# Option 3: Use shell scripts (auto-activate)
./run-cuco.sh --yes /path/to/project
```

---

## Troubleshooting Commands

```bash
# Check if virtual environment is activated
echo $VIRTUAL_ENV
# Should output path to .venv

# Check Python location
which python
# Should be in .venv/bin/

# Check installed packages
pip list

# Reinstall package
pip install -e . --force-reinstall

# Check for errors
pip install -e . -v  # Verbose output

# Verify setup.py exists
ls -la setup.py

# Check Python version
python --version

# Test import manually
python -c "import codeindex; print(codeindex.__file__)"
```

---

## Contact for Help

If issues persist, provide this diagnostic output:

```bash
echo "=== DIAGNOSTIC INFO ==="
echo "Working directory: $(pwd)"
echo "Python path: $(which python)"
echo "Virtual env: $VIRTUAL_ENV"
echo "Pip path: $(which pip)"
echo "Codeindex path: $(which codeindex)"
echo ""
echo "=== PACKAGE INFO ==="
pip list | grep codeindex
echo ""
echo "=== PYTHON VERSION ==="
python --version
echo ""
echo "=== DIRECTORY CONTENTS ==="
ls -la | head -20
```
