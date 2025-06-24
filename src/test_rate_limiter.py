#!/usr/bin/env python3
"""
Test script for the improved rate limiter
Tests quota exceeded error handling and other rate limiting features
"""

import asyncio
import time
import logging
from rate_limiter import RateLimiter, RateLimitConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockOpenAIError(Exception):
    """Mock OpenAI error for testing"""
    def __init__(self, error_type: str, message: str = ""):
        self.error_type = error_type
        self.message = message
        super().__init__(message)

class MockQuotaError(MockOpenAIError):
    """Mock quota exceeded error"""
    def __init__(self):
        super().__init__("insufficient_quota", "You exceeded your current quota, please check your plan and billing details.")

class MockRateLimitError(MockOpenAIError):
    """Mock rate limit error"""
    def __init__(self):
        super().__init__("rate_limit_exceeded", "Rate limit exceeded for requests")

async def test_rate_limiter():
    """Test the improved rate limiter functionality"""
    logger.info("Starting rate limiter tests...")
    
    # Test 1: Basic rate limiting
    logger.info("\n=== Test 1: Basic Rate Limiting ===")
    config = RateLimitConfig(
        requests_per_minute=5,
        requests_per_hour=10,
        delay_between_requests=1.0,
        max_retries=3
    )
    rate_limiter = RateLimiter(config)
    
    start_time = time.time()
    for i in range(3):
        await rate_limiter.wait_if_needed()
        rate_limiter.record_request()
        logger.info(f"Request {i+1} recorded")
    
    elapsed = time.time() - start_time
    logger.info(f"3 requests took {elapsed:.1f} seconds (expected ~2 seconds)")
    
    # Test 2: Quota exceeded error handling
    logger.info("\n=== Test 2: Quota Exceeded Error Handling ===")
    rate_limiter2 = RateLimiter(config)
    
    # Simulate quota exceeded error
    quota_error = MockQuotaError()
    rate_limiter2.record_failure(quota_error)
    
    logger.info(f"Quota exceeded: {rate_limiter2.quota_exceeded}")
    logger.info(f"Should continue requests: {rate_limiter2.should_continue_requests()}")
    
    # Test 3: Rate limit error handling (not quota)
    logger.info("\n=== Test 3: Rate Limit Error Handling ===")
    rate_limiter3 = RateLimiter(config)
    
    # Simulate rate limit error
    rate_limit_error = MockRateLimitError()
    rate_limiter3.record_failure(rate_limit_error)
    
    logger.info(f"Quota exceeded: {rate_limiter3.quota_exceeded}")
    logger.info(f"Should continue requests: {rate_limiter3.should_continue_requests()}")
    logger.info(f"Consecutive failures: {rate_limiter3.consecutive_failures}")
    
    # Test 4: Stats functionality
    logger.info("\n=== Test 4: Stats Functionality ===")
    stats = rate_limiter.get_stats()
    logger.info(f"Rate limiter stats: {stats}")
    
    # Test 5: Quota exceeded wait time
    logger.info("\n=== Test 5: Quota Exceeded Wait Time ===")
    config_short = RateLimitConfig(
        requests_per_minute=5,
        requests_per_hour=10,
        delay_between_requests=1.0,
        max_retries=3,
        quota_exceeded_wait_time=5  # 5 seconds for testing
    )
    rate_limiter4 = RateLimiter(config_short)
    
    # Trigger quota exceeded
    rate_limiter4.record_failure(MockQuotaError())
    
    logger.info("Testing wait_if_needed with quota exceeded (should wait 5 seconds)...")
    start_time = time.time()
    await rate_limiter4.wait_if_needed()
    elapsed = time.time() - start_time
    logger.info(f"Wait completed in {elapsed:.1f} seconds")
    
    logger.info("All tests completed!")

if __name__ == "__main__":
    asyncio.run(test_rate_limiter()) 