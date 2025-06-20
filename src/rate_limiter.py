import asyncio
import time
import logging
from typing import Optional
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

class RateLimiter:
    """Rate limiter for OpenAI API calls"""
    
    def __init__(self, config: Optional[RateLimitConfig] = None):
        self.config = config or RateLimitConfig()
        self.request_times = []
        self.last_request_time = 0
        self.consecutive_failures = 0
        
    async def wait_if_needed(self) -> None:
        """Wait if necessary to respect rate limits"""
        current_time = time.time()
        
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
        
        # Add exponential backoff for consecutive failures
        if self.consecutive_failures > 0:
            backoff_time = self.config.delay_between_requests * (self.config.exponential_backoff_base ** self.consecutive_failures)
            logger.info(f"Applying exponential backoff: {backoff_time:.1f} seconds")
            await asyncio.sleep(backoff_time)
    
    def record_request(self) -> None:
        """Record a successful API request"""
        current_time = time.time()
        self.request_times.append(current_time)
        self.last_request_time = current_time
        self.consecutive_failures = 0
    
    def record_failure(self) -> None:
        """Record a failed API request"""
        self.consecutive_failures += 1
        logger.warning(f"API request failed. Consecutive failures: {self.consecutive_failures}")
    
    def get_stats(self) -> dict:
        """Get current rate limiting statistics"""
        current_time = time.time()
        recent_requests = [t for t in self.request_times if current_time - t < 60]
        hourly_requests = [t for t in self.request_times if current_time - t < 3600]
        
        return {
            'requests_last_minute': len(recent_requests),
            'requests_last_hour': len(hourly_requests),
            'consecutive_failures': self.consecutive_failures,
            'time_since_last_request': current_time - self.last_request_time if self.last_request_time > 0 else None
        } 