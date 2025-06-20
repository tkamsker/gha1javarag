#!/usr/bin/env python3
"""
Test script to verify rate limiting functionality
"""
import asyncio
import time
import logging
from rate_limiter import RateLimiter, RateLimitConfig
from logger_config import setup_logging

async def test_rate_limiter():
    """Test the rate limiter functionality"""
    logger = setup_logging(level=logging.INFO)
    logger.info("Starting rate limiter test")
    
    # Create a very restrictive rate limiter for testing
    config = RateLimitConfig(
        requests_per_minute=3,  # Only 3 requests per minute
        requests_per_hour=10,   # Only 10 requests per hour
        delay_between_requests=2.0,  # 2 seconds between requests
        exponential_backoff_base=2.0,
        max_retries=3
    )
    
    rate_limiter = RateLimiter(config)
    
    logger.info("Testing rate limiter with 5 requests...")
    
    for i in range(5):
        start_time = time.time()
        logger.info(f"Request {i + 1}: Waiting for rate limiter...")
        
        await rate_limiter.wait_if_needed()
        
        # Simulate a successful API call
        rate_limiter.record_request()
        
        elapsed = time.time() - start_time
        logger.info(f"Request {i + 1}: Completed in {elapsed:.2f} seconds")
        
        # Show stats
        stats = rate_limiter.get_stats()
        logger.info(f"Stats: {stats['requests_last_minute']}/min, {stats['requests_last_hour']}/hour")
    
    logger.info("Rate limiter test completed!")

if __name__ == "__main__":
    asyncio.run(test_rate_limiter()) 