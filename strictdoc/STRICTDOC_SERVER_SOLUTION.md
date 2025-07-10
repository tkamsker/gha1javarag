# StrictDoc Server Solution

## Problem Analysis

The error you encountered indicates that there's a malformed SDoc file (`CucoSett.gwt.sdoc`) with syntax errors. The specific error is:

```
Expected 'MID' or 'UID' or '(?!^UID)(?!^RELATIONS)[A-Z]+[A-Z_0-9]*' or 'RELATIONS:' or '\n' or EOF => 'er... <<< *[/REQUIREM'
```

This suggests the file has invalid syntax around line 12.

## Solution Overview

I've created three scripts to solve this issue:

### 1. `copy_sdoc_files.sh` - Copy Existing Files
This script copies all existing SDoc files to the `output/requirements` directory:

```bash
./strictdoc/copy_sdoc_files.sh
```

### 2. `run_server.sh` - Simple Server Runner
This script runs the StrictDoc server with proper setup:

```bash
./strictdoc/run_server.sh
```

### 3. `setup_strictdoc_server.sh` - Comprehensive Solution
This script provides validation, fixing, and server management:

```bash
./strictdoc/setup_strictdoc_server.sh [command]
```

Commands:
- `validate` - Validate all SDoc files
- `fix` - Fix common syntax issues
- `create-sample` - Create sample files
- `help` - Show help

## Quick Start

### Option 1: Simple Approach
```bash
# Copy existing files
./strictdoc/copy_sdoc_files.sh

# Run server
./strictdoc/run_server.sh
```

### Option 2: Comprehensive Approach
```bash
# Validate and fix files, then run server
./strictdoc/setup_strictdoc_server.sh
```

### Option 3: Manual Fix
```bash
# Just validate files
./strictdoc/setup_strictdoc_server.sh validate

# Fix syntax issues
./strictdoc/setup_strictdoc_server.sh fix

# Run server
./strictdoc/run_server.sh
```

## Expected Results

After running the solution:

1. **Server Access**: http://localhost:5111
2. **Requirements Directory**: `output/requirements/`
3. **Valid SDoc Files**: All files will be properly formatted
4. **Sample Files**: Created if no valid files exist

## File Structure

```
strictdoc/
├── copy_sdoc_files.sh          # Copy existing files
├── run_server.sh               # Simple server runner
├── setup_strictdoc_server.sh   # Comprehensive solution
├── STRICTDOC_SERVER_SOLUTION.md # This file
└── venv2/                      # Virtual environment

output/
└── requirements/               # Server document root
    ├── sample.sdoc            # Auto-created if needed
    ├── cuco.sdoc             # Copied from strictdoc/reqdoc/
    └── *.sdoc                # Other SDoc files
```

## Troubleshooting

### If you get "Virtual environment not found":
```bash
cd strictdoc
python3 -m venv venv2
source venv2/bin/activate
pip install strictdoc
```

### If you get syntax errors:
```bash
./strictdoc/setup_strictdoc_server.sh fix
```

### If no files are found:
```bash
./strictdoc/setup_strictdoc_server.sh create-sample
```

## Next Steps

1. Choose your preferred approach (simple or comprehensive)
2. Run the appropriate script
3. Access the server at http://localhost:5111
4. The server will serve documents from `output/requirements/`

The solution handles:
- ✅ File validation and fixing
- ✅ Directory setup
- ✅ Virtual environment activation
- ✅ Sample file creation
- ✅ Error handling
- ✅ Multiple usage options 