# Rate Limiting Improvements

## Overview

This project has been updated with comprehensive rate limiting to prevent OpenAI API quota exhaustion and 429 (Too Many Requests) errors.

## Key Improvements

### 1. Dedicated Rate Limiter Class
- **File**: `src/rate_limiter.py`
- **Features**:
  - Per-minute and per-hour request limits
  - Exponential backoff for failed requests
  - Minimum delay between requests
  - Request tracking and statistics

### 2. Configuration-Based Settings
- **File**: `config/rate_limiting.yaml`
- **Environments**:
  - `production`: Conservative settings (15 req/min, 800 req/hour)
  - `test`: Very conservative (10 req/min, 500 req/hour)
  - `development`: More aggressive (20 req/min, 1000 req/hour)
  - `emergency`: Very restrictive (5 req/min, 200 req/hour)

### 3. Updated Components

#### AI Analyzer (`src/ai_analyzer.py`)
- Added rate limiting to individual file analysis
- Reduced content length to minimize token usage
- Added retry logic with exponential backoff

#### Step 2 Processor (`src/step2.py`)
- Implemented batch processing (3 files per API call)
- Limited total files processed (50 max)
- Enhanced rate limiting with longer delays

#### Step 2 Test (`src/step2_test.py`)
- Very conservative settings for testing
- Limited to 5 files maximum
- 8-second delays between requests

## Usage

### Environment Configuration
Set the environment variable to control rate limiting:

```bash
# For production use
export RATE_LIMIT_ENV=production

# For testing
export RATE_LIMIT_ENV=test

# For emergency situations
export RATE_LIMIT_ENV=emergency
```

### Running with Rate Limiting

```bash
# Test the rate limiter
python src/test_rate_limiter.py

# Run step2 with conservative settings
RATE_LIMIT_ENV=test python src/step2_test.py

# Run step2 with production settings
RATE_LIMIT_ENV=production python src/step2.py
```

## Rate Limiting Features

### 1. Request Tracking
- Tracks all API requests with timestamps
- Maintains rolling windows for minute and hour limits
- Automatically cleans old request data

### 2. Exponential Backoff
- Increases delay after consecutive failures
- Base delay: 4 seconds (production)
- Exponential factor: 2.0
- Maximum retries: 5

### 3. Statistics and Monitoring
- Real-time request statistics
- Logging of rate limit events
- Progress tracking for long-running operations

## Configuration Options

### Rate Limit Settings
```yaml
production:
  requests_per_minute: 15    # Max requests per minute
  requests_per_hour: 800     # Max requests per hour
  delay_between_requests: 4.0  # Minimum seconds between requests
  exponential_backoff_base: 2.0  # Backoff multiplier
  max_retries: 5            # Maximum retry attempts
```

### Content Optimization
- Reduced content length limits (2000 chars max)
- Truncated file content to minimize tokens
- Optimized prompts for efficiency

## Monitoring and Debugging

### Log Messages
The rate limiter provides detailed logging:
```
INFO - Rate limit stats: 3/15 min, 45/800 hour
WARNING - Minute rate limit reached. Waiting 45.2 seconds
INFO - Applying exponential backoff: 8.0 seconds
```

### Statistics
```python
stats = rate_limiter.get_stats()
print(f"Requests last minute: {stats['requests_last_minute']}")
print(f"Requests last hour: {stats['requests_last_hour']}")
print(f"Consecutive failures: {stats['consecutive_failures']}")
```

## Troubleshooting

### If You Still Get Rate Limit Errors

1. **Switch to Emergency Mode**:
   ```bash
   export RATE_LIMIT_ENV=emergency
   ```

2. **Check Your OpenAI Plan**:
   - Verify your current quota and limits
   - Consider upgrading your plan if needed

3. **Reduce File Count**:
   - Edit the `max_files_to_process` setting
   - Use more restrictive file filtering

4. **Increase Delays**:
   - Modify `delay_between_requests` in the config
   - Increase `requests_per_minute` limits

### Performance Optimization

1. **Batch Processing**: Files are processed in batches to reduce API calls
2. **Content Truncation**: Large files are truncated to save tokens
3. **Priority Filtering**: Only important files are processed
4. **Skip Patterns**: Unnecessary files are automatically skipped

## Best Practices

1. **Start with Test Mode**: Always test with `RATE_LIMIT_ENV=test` first
2. **Monitor Logs**: Watch for rate limit warnings and adjust accordingly
3. **Use Appropriate Environment**: Match the environment to your OpenAI plan
4. **Plan Ahead**: Large codebases may take several hours to process
5. **Resume Capability**: The system can be restarted and will skip already processed files 