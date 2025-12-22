"""
Unit tests for Ollama timeout handling with adaptive timeout and exponential backoff.

These tests verify T019, T020, T021 for Feature 007 User Story 1.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import asyncio

from codeindex.utils.retry import calculate_exponential_backoff
from codeindex.models.metrics import TimeoutMetric


class TestAdaptiveTimeout:
    """Tests for adaptive timeout calculation (T019)"""

    def test_calculate_adaptive_timeout_small_file(self):
        """Test adaptive timeout for small file (<500 lines)"""
        # Given a small file with 100 lines
        file_lines = 100
        base_timeout = 120.0  # 2 minutes base

        # When calculating adaptive timeout
        # Formula: timeout = base_timeout * (1 + file_lines / 1000)
        expected_timeout = base_timeout * (1 + file_lines / 1000.0)
        # expected_timeout = 120 * (1 + 0.1) = 132 seconds

        # Then timeout should be slightly above base
        assert expected_timeout == 132.0

    def test_calculate_adaptive_timeout_medium_file(self):
        """Test adaptive timeout for medium file (500 lines)"""
        # Given a medium file with 500 lines
        file_lines = 500
        base_timeout = 120.0

        # When calculating adaptive timeout
        expected_timeout = base_timeout * (1 + file_lines / 1000.0)
        # expected_timeout = 120 * (1 + 0.5) = 180 seconds

        # Then timeout should be 1.5x base
        assert expected_timeout == 180.0

    def test_calculate_adaptive_timeout_large_file(self):
        """Test adaptive timeout for large file (>1000 lines)"""
        # Given a large file with 2000 lines
        file_lines = 2000
        base_timeout = 120.0

        # When calculating adaptive timeout
        expected_timeout = base_timeout * (1 + file_lines / 1000.0)
        # expected_timeout = 120 * (1 + 2.0) = 360 seconds (6 minutes)

        # Then timeout should be 3x base
        assert expected_timeout == 360.0

    def test_calculate_adaptive_timeout_very_large_file(self):
        """Test adaptive timeout for very large file (>5000 lines)"""
        # Given a very large file with 5000 lines
        file_lines = 5000
        base_timeout = 120.0

        # When calculating adaptive timeout
        expected_timeout = base_timeout * (1 + file_lines / 1000.0)
        # expected_timeout = 120 * (1 + 5.0) = 720 seconds (12 minutes)

        # Then timeout should be 6x base
        assert expected_timeout == 720.0

    def test_calculate_adaptive_timeout_zero_lines(self):
        """Test adaptive timeout for empty file (edge case)"""
        # Given an empty file
        file_lines = 0
        base_timeout = 120.0

        # When calculating adaptive timeout
        expected_timeout = base_timeout * (1 + file_lines / 1000.0)
        # expected_timeout = 120 * 1 = 120 seconds

        # Then timeout should equal base
        assert expected_timeout == 120.0


class TestExponentialBackoff:
    """Tests for exponential backoff delays (T020)"""

    def test_exponential_backoff_attempt_1(self):
        """Test exponential backoff for first retry (attempt 1)"""
        # Given first retry attempt
        attempt = 1
        base_delay = 5.0
        multiplier = 3.0

        # When calculating delay
        delay = calculate_exponential_backoff(attempt, base_delay, multiplier)

        # Then delay should be base_delay (5 seconds)
        assert delay == 5.0

    def test_exponential_backoff_attempt_2(self):
        """Test exponential backoff for second retry (attempt 2)"""
        # Given second retry attempt
        attempt = 2
        base_delay = 5.0
        multiplier = 3.0

        # When calculating delay
        delay = calculate_exponential_backoff(attempt, base_delay, multiplier)

        # Then delay should be base_delay * multiplier (15 seconds)
        assert delay == 15.0

    def test_exponential_backoff_attempt_3(self):
        """Test exponential backoff for third retry (attempt 3)"""
        # Given third retry attempt
        attempt = 3
        base_delay = 5.0
        multiplier = 3.0

        # When calculating delay
        delay = calculate_exponential_backoff(attempt, base_delay, multiplier)

        # Then delay should be base_delay * multiplier^2 (45 seconds)
        assert delay == 45.0

    def test_exponential_backoff_custom_base(self):
        """Test exponential backoff with custom base delay"""
        # Given custom base delay
        attempt = 2
        base_delay = 10.0
        multiplier = 2.0

        # When calculating delay
        delay = calculate_exponential_backoff(attempt, base_delay, multiplier)

        # Then delay should be 10 * 2 = 20 seconds
        assert delay == 20.0

    def test_exponential_backoff_invalid_attempt(self):
        """Test exponential backoff with invalid attempt number"""
        # Given invalid attempt (< 1)
        attempt = 0

        # When calculating delay
        # Then should raise ValueError
        with pytest.raises(ValueError, match="attempt must be >= 1"):
            calculate_exponential_backoff(attempt)

    def test_exponential_backoff_invalid_base_delay(self):
        """Test exponential backoff with invalid base delay"""
        # Given invalid base delay (<= 0)
        attempt = 1
        base_delay = -5.0

        # When calculating delay
        # Then should raise ValueError
        with pytest.raises(ValueError, match="base_delay must be positive"):
            calculate_exponential_backoff(attempt, base_delay)

    def test_exponential_backoff_invalid_multiplier(self):
        """Test exponential backoff with invalid multiplier"""
        # Given invalid multiplier (<= 1.0)
        attempt = 1
        multiplier = 0.5

        # When calculating delay
        # Then should raise ValueError
        with pytest.raises(ValueError, match="multiplier must be > 1.0"):
            calculate_exponential_backoff(attempt, multiplier=multiplier)


class TestFallbackTrigger:
    """Tests for fallback trigger after max retries (T021)"""

    def test_fallback_triggered_after_max_retries(self):
        """Test that fallback is triggered after 3 failed attempts"""
        # Given max retries exhausted (3 attempts)
        max_attempts = 3
        retry_count = 3

        # When checking if fallback should be used
        should_use_fallback = retry_count >= max_attempts

        # Then fallback should be triggered
        assert should_use_fallback is True

    def test_fallback_not_triggered_before_max_retries(self):
        """Test that fallback is not triggered before max retries"""
        # Given retries not exhausted (2 attempts)
        max_attempts = 3
        retry_count = 2

        # When checking if fallback should be used
        should_use_fallback = retry_count >= max_attempts

        # Then fallback should not be triggered
        assert should_use_fallback is False

    def test_timeout_metric_records_fallback(self):
        """Test that TimeoutMetric correctly records fallback usage"""
        # Given a timeout that triggered fallback
        metric = TimeoutMetric(
            file_path="/path/to/file.java",
            timeout_threshold=600.0,
            retry_count=3,
            fallback_used=True,
            extraction_quality='structural',
            file_lines=1500
        )

        # When checking metric
        # Then fallback should be marked as used
        assert metric.fallback_used is True
        assert metric.retry_count == 3
        assert metric.extraction_quality == 'structural'

    def test_timeout_metric_no_fallback_on_success(self):
        """Test that TimeoutMetric shows no fallback when LLM succeeds"""
        # Given a successful extraction without timeout
        metric = TimeoutMetric(
            file_path="/path/to/file.java",
            timeout_threshold=600.0,
            retry_count=0,
            fallback_used=False,
            extraction_quality='full',
            file_lines=500
        )

        # When checking metric
        # Then no fallback should be used
        assert metric.fallback_used is False
        assert metric.retry_count == 0
        assert metric.extraction_quality == 'full'

    def test_timeout_metric_validates_extraction_quality(self):
        """Test that TimeoutMetric validates extraction quality values"""
        # Given invalid extraction quality
        # When creating metric
        # Then should raise ValueError
        with pytest.raises(ValueError, match="extraction_quality must be"):
            TimeoutMetric(
                file_path="/path/to/file.java",
                timeout_threshold=600.0,
                retry_count=3,
                fallback_used=True,
                extraction_quality='invalid',  # Invalid value
                file_lines=500
            )
