# Usage Guide - Rate Limited Code Analysis

## Overview

The code analysis pipeline has been updated with comprehensive rate limiting to prevent OpenAI API quota exhaustion and 429 errors.

## Running the Analysis

### Basic Usage

```bash
# Test mode (default) - Very conservative rate limiting
./Lofalassn.sh

# Or explicitly specify test mode
./Lofalassn.sh test

# Production mode - Standard rate limiting
./Lofalassn.sh production

# Emergency mode - Very restrictive rate limiting
./Lofalassn.sh emergency
```

### Mode Comparison

| Mode | Requests/Min | Requests/Hour | Delay Between Calls | Files Processed | Use Case |
|------|-------------|---------------|-------------------|-----------------|----------|
| **test** | 5 | 200 | 10 seconds | 10 files | Testing, debugging |
| **production** | 15 | 800 | 4 seconds | 30 files | Normal operation |
| **emergency** | 5 | 200 | 10 seconds | 20 files | Quota issues |

## Individual Step Execution

### Step 1: File Processing and AI Analysis

```bash
# Test mode (conservative)
python src/main_test.py

# Production mode
export RATE_LIMIT_ENV=production
python src/main.py

# Emergency mode
export RATE_LIMIT_ENV=emergency
python src/main.py
```

### Step 2: Requirements Generation

```bash
# Test mode (conservative)
export RATE_LIMIT_ENV=test
python src/step2_test.py

# Production mode
export RATE_LIMIT_ENV=production
python src/step2.py

# Emergency mode
export RATE_LIMIT_ENV=emergency
python src/step2.py
```

### Step 3: Final Processing

```bash
# Step 3 doesn't use OpenAI API, so no rate limiting needed
python src/step3.py
```

## Rate Limiting Features

### 1. Batch Processing
- **Step 1**: Processes 2-3 files per API call (instead of 1)
- **Step 2**: Processes 2-3 files per API call
- **Reduction**: ~60-70% fewer API calls

### 2. File Prioritization
- Java files (highest priority)
- JSP files
- Configuration files (XML, properties)
- Other files (lowest priority)

### 3. File Filtering
Automatically skips:
- Compiled files (.class, .jar, .war)
- System files (.DS_Store, .log)
- Package info files
- Temporary files

### 4. Content Optimization
- Limits file content to 600-800 characters
- Reduces token usage by ~70%
- Truncates large files intelligently

## Monitoring and Debugging

### Log Messages
```
INFO - Rate limit stats: 3/15 min, 45/800 hour
WARNING - Minute rate limit reached. Waiting 45.2 seconds
INFO - Applying exponential backoff: 8.0 seconds
```

### Progress Tracking
```
INFO - Progress: 6/30 files processed
INFO - Successfully analyzed batch of 3 files
```

### Error Handling
```
ERROR - Error analyzing batch (attempt 1): 429 Too Many Requests
INFO - Applying exponential backoff: 8.0 seconds
```

## Troubleshooting

### If You Still Get Rate Limit Errors

1. **Switch to Emergency Mode**:
   ```bash
   ./Lofalassn.sh emergency
   ```

2. **Check Your OpenAI Plan**:
   - Verify your current quota and limits
   - Consider upgrading your plan if needed

3. **Reduce File Count**:
   - Edit `max_files_to_process` in the analyzer classes
   - Use more restrictive file filtering

4. **Increase Delays**:
   - Modify `delay_between_requests` in config files
   - Increase `requests_per_minute` limits

### Performance Optimization

1. **Start with Test Mode**: Always test with `./Lofalassn.sh test` first
2. **Monitor Logs**: Watch for rate limit warnings
3. **Use Appropriate Mode**: Match the mode to your OpenAI plan
4. **Plan Ahead**: Large codebases may take several hours to process

## Configuration Files

### Rate Limiting Configuration
- **File**: `config/rate_limiting.yaml`
- **Purpose**: Define rate limits for different environments
- **Usage**: Set `RATE_LIMIT_ENV` environment variable

### Environment Variables
```bash
# Set rate limiting environment
export RATE_LIMIT_ENV=test

# Set OpenAI model (optional)
export OPENAI_MODEL_NAME=gpt-4-turbo-preview

# Set output directory (optional)
export OUTPUT_DIR=./output
```

## Expected Results

### Test Mode
- **Duration**: 30-60 minutes
- **Files Processed**: 10 files
- **API Calls**: ~5-10 calls
- **Success Rate**: Very high

### Production Mode
- **Duration**: 2-4 hours
- **Files Processed**: 30 files
- **API Calls**: ~15-20 calls
- **Success Rate**: High

### Emergency Mode
- **Duration**: 4-8 hours
- **Files Processed**: 20 files
- **API Calls**: ~10-15 calls
- **Success Rate**: Very high

## Best Practices

1. **Always Start with Test Mode**: Verify everything works before running production
2. **Monitor Your Quota**: Check OpenAI dashboard regularly
3. **Use Appropriate Mode**: Match mode to your plan and quota
4. **Plan for Long Runs**: Large codebases take time with rate limiting
5. **Resume Capability**: The system can be restarted and will skip processed files 