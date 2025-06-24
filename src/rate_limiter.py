import asyncio
import time
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger('java_analysis.rate_limiter')

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    requests_per_minute: int = 20  # Conservative default
    requests_per_hour: int = 1000
    delay_between_requests: float = 3.0  # Seconds
    exponential_backoff_base: float = 2.0
    max_retries: int = 5
    quota_exceeded_wait_time: int = 3600  # 1 hour wait when quota exceeded

class RateLimiter:
    """Rate limiter for OpenAI API calls with intelligent error handling"""
    
    def __init__(self, config: Optional[RateLimitConfig] = None):
        self.config = config or RateLimitConfig()
        self.request_times = []
        self.last_request_time = 0
        self.consecutive_failures = 0
        self.quota_exceeded = False
        self.quota_exceeded_time = 0
        
    async def wait_if_needed(self) -> None:
        """Wait if necessary to respect rate limits"""
        current_time = time.time()
        
        # Check if quota was exceeded recently
        if self.quota_exceeded:
            time_since_quota_exceeded = current_time - self.quota_exceeded_time
            if time_since_quota_exceeded < self.config.quota_exceeded_wait_time:
                remaining_wait = self.config.quota_exceeded_wait_time - time_since_quota_exceeded
                logger.error(f"Quota exceeded. Waiting {remaining_wait:.0f} seconds before retrying. "
                           f"Please check your OpenAI billing and plan details.")
                await asyncio.sleep(remaining_wait)
            else:
                # Reset quota exceeded flag after wait time
                self.quota_exceeded = False
                logger.info("Quota exceeded wait time completed. Resuming requests.")
        
        # Clean old request times (older than 1 hour)
        self.request_times = [t for t in self.request_times if current_time - t < 3600]
        
        # Check if we're at the hourly limit
        if len(self.request_times) >= self.config.requests_per_hour:
            wait_time = 3600 - (current_time - self.request_times[0])
            if wait_time > 0:
                logger.warning(f"Hourly rate limit reached. Waiting {wait_time:.1f} seconds")
                await asyncio.sleep(wait_time)
        
        # Check if we're at the minute limit
        recent_requests = [t for t in self.request_times if current_time - t < 60]
        if len(recent_requests) >= self.config.requests_per_minute:
            wait_time = 60 - (current_time - recent_requests[0])
            if wait_time > 0:
                logger.warning(f"Minute rate limit reached. Waiting {wait_time:.1f} seconds")
                await asyncio.sleep(wait_time)
        
        # Ensure minimum delay between requests
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.config.delay_between_requests:
            wait_time = self.config.delay_between_requests - time_since_last
            await asyncio.sleep(wait_time)
        
        # Add exponential backoff for consecutive failures (but not for quota exceeded)
        if self.consecutive_failures > 0 and not self.quota_exceeded:
            backoff_time = self.config.delay_between_requests * (self.config.exponential_backoff_base ** self.consecutive_failures)
            logger.info(f"Applying exponential backoff: {backoff_time:.1f} seconds")
            await asyncio.sleep(backoff_time)
    
    def record_request(self) -> None:
        """Record a successful API request"""
        current_time = time.time()
        self.request_times.append(current_time)
        self.last_request_time = current_time
        self.consecutive_failures = 0
    
    def record_failure(self, error: Optional[Exception] = None) -> None:
        """Record a failed API request with intelligent error handling"""
        self.consecutive_failures += 1
        
        # Handle specific OpenAI error types
        if error:
            error_str = str(error).lower()
            error_code = self._extract_error_code(error)
            
            # Check for quota exceeded error
            if ('insufficient_quota' in error_str or 
                'quota' in error_str and 'exceeded' in error_str or
                error_code == 'insufficient_quota'):
                
                self.quota_exceeded = True
                self.quota_exceeded_time = time.time()
                logger.error(f"QUOTA EXCEEDED: OpenAI API quota has been exceeded. "
                           f"Please check your billing and plan details at: "
                           f"https://platform.openai.com/account/billing")
                logger.error(f"Stopping all requests for {self.config.quota_exceeded_wait_time} seconds")
                return
            
            # Check for rate limit error (but not quota)
            elif ('rate_limit' in error_str or 
                  'too many requests' in error_str or
                  error_code == 'rate_limit_exceeded'):
                
                logger.warning(f"Rate limit exceeded. Consecutive failures: {self.consecutive_failures}")
                return
        
        # Generic failure logging
        logger.warning(f"API request failed. Consecutive failures: {self.consecutive_failures}")
    
    def _extract_error_code(self, error: Exception) -> Optional[str]:
        """Extract error code from OpenAI error response"""
        try:
            if hasattr(error, 'response') and hasattr(error.response, 'json'):
                error_data = error.response.json()
                if 'error' in error_data and 'code' in error_data['error']:
                    return error_data['error']['code']
        except:
            pass
        
        # Try to extract from error message
        error_str = str(error)
        if 'insufficient_quota' in error_str:
            return 'insufficient_quota'
        elif 'rate_limit' in error_str:
            return 'rate_limit_exceeded'
        
        return None
    
    def should_continue_requests(self) -> bool:
        """Check if we should continue making requests"""
        if self.quota_exceeded:
            current_time = time.time()
            time_since_quota_exceeded = current_time - self.quota_exceeded_time
            if time_since_quota_exceeded < self.config.quota_exceeded_wait_time:
                return False
        
        return True
    
    def get_stats(self) -> dict:
        """Get current rate limiting statistics"""
        current_time = time.time()
        recent_requests = [t for t in self.request_times if current_time - t < 60]
        hourly_requests = [t for t in self.request_times if current_time - t < 3600]
        
        stats = {
            'requests_last_minute': len(recent_requests),
            'requests_last_hour': len(hourly_requests),
            'consecutive_failures': self.consecutive_failures,
            'time_since_last_request': current_time - self.last_request_time if self.last_request_time > 0 else None,
            'quota_exceeded': self.quota_exceeded,
            'should_continue_requests': self.should_continue_requests()
        }
        
        if self.quota_exceeded:
            time_since_quota_exceeded = current_time - self.quota_exceeded_time
            remaining_wait = max(0, self.config.quota_exceeded_wait_time - time_since_quota_exceeded)
            stats['quota_exceeded_wait_remaining'] = remaining_wait
        
        return stats 