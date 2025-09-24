# Rate Limiting Improvements

## Overview

The rate limiting system has been significantly improved to handle OpenAI API errors more intelligently, especially the 429 "insufficient_quota" error that was causing issues in your application.

## Key Improvements

### 1. Intelligent Error Handling

The system now distinguishes between different types of OpenAI API errors:

- **Quota Exceeded (insufficient_quota)**: When you've exceeded your OpenAI API quota
- **Rate Limit Exceeded**: When you've hit rate limits but still have quota
- **Other Errors**: Generic error handling with exponential backoff

### 2. Quota Exceeded Handling

When a quota exceeded error is detected:

- **Immediate Stop**: All API requests are stopped immediately
- **Wait Period**: The system waits for a configurable period (default: 1 hour)
- **Clear Messaging**: Provides clear error messages with billing links
- **No Retries**: Does not retry requests during the wait period

### 3. Enhanced Configuration

New configuration parameter added:

```yaml
quota_exceeded_wait_time: 3600  # 1 hour wait when quota exceeded
```

### 4. Improved Error Detection

The system now extracts error codes from OpenAI responses and handles:

- `insufficient_quota` errors
- `rate_limit_exceeded` errors  
- Generic rate limiting errors

## Configuration

### Environment-Specific Settings

The system supports different environments with appropriate rate limiting:

#### Production
```yaml
production:
  requests_per_minute: 15
  requests_per_hour: 800
  delay_between_requests: 4.0
  exponential_backoff_base: 2.0
  max_retries: 5
  quota_exceeded_wait_time: 3600  # 1 hour
```

#### Test
```yaml
test:
  requests_per_minute: 10
  requests_per_hour: 500
  delay_between_requests: 8.0
  exponential_backoff_base: 2.0
  max_retries: 5
  quota_exceeded_wait_time: 3600  # 1 hour
```

#### Emergency
```yaml
emergency:
  requests_per_minute: 5
  requests_per_hour: 200
  delay_between_requests: 10.0
  exponential_backoff_base: 2.0
  max_retries: 5
  quota_exceeded_wait_time: 7200  # 2 hours (more conservative)
```

## Usage

### Setting Environment

```bash
# For production use
export RATE_LIMIT_ENV=production

# For testing
export RATE_LIMIT_ENV=test

# For emergency situations
export RATE_LIMIT_ENV=emergency
```

### Running the Application

```bash
# Production mode
./lofalassn.sh production

# Test mode  
./lofalassn.sh test

# Emergency mode
./lofalassn.sh emergency
```

## Error Handling Flow

1. **API Request Made**: System attempts to make OpenAI API call
2. **Error Detection**: If error occurs, system analyzes error type
3. **Quota Exceeded**: If quota exceeded, stop all requests and wait
4. **Rate Limit**: If rate limit exceeded, apply exponential backoff
5. **Other Errors**: Apply standard retry logic with backoff

## Monitoring

The system provides detailed statistics:

```python
stats = rate_limiter.get_stats()
# Returns:
{
    'requests_last_minute': 5,
    'requests_last_hour': 45,
    'consecutive_failures': 0,
    'time_since_last_request': 2.5,
    'quota_exceeded': False,
    'should_continue_requests': True,
    'quota_exceeded_wait_remaining': None  # Only if quota exceeded
}
```

## Troubleshooting

### Quota Exceeded Error

If you see "QUOTA EXCEEDED" errors:

1. **Check Billing**: Visit https://platform.openai.com/account/billing
2. **Verify Plan**: Ensure your plan has sufficient quota
3. **Wait Period**: The system will automatically wait and retry
4. **Manual Reset**: You can restart the application after checking billing

### Rate Limit Errors

If you see rate limit errors (not quota):

1. **Check Configuration**: Verify your rate limiting settings
2. **Reduce Load**: Consider using more conservative settings
3. **Monitor Usage**: Check the statistics to understand your usage patterns

## Best Practices

1. **Start Conservative**: Begin with test or emergency settings
2. **Monitor Logs**: Watch for quota and rate limit warnings
3. **Plan Ahead**: Understand your OpenAI plan limits
4. **Use Appropriate Environment**: Match environment to your needs

## Testing

Run the test script to verify functionality:

```bash
python src/test_rate_limiter.py
```

This will test:
- Basic rate limiting
- Quota exceeded error handling
- Rate limit error handling
- Statistics functionality
- Wait time behavior

## OpenAI Error Reference

For more information on OpenAI API errors, see:
https://platform.openai.com/docs/guides/error-codes/api-errors

Key error codes:
- `insufficient_quota`: You've exceeded your current quota
- `rate_limit_exceeded`: You've hit rate limits
- `invalid_request_error`: Malformed request
- `authentication_error`: Invalid API key

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

