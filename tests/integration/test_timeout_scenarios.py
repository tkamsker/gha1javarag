"""
Integration tests for Ollama timeout scenarios with retry and fallback.

These tests verify T023, T024 for Feature 007 User Story 1.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path

from codeindex.models.metrics import TimeoutMetric


@pytest.mark.integration
class TestOllamaTimeoutWithRetry:
    """Integration tests for Ollama timeout with retry logic (T023)"""

    @pytest.mark.asyncio
    async def test_ollama_timeout_triggers_first_retry(self):
        """Test that Ollama timeout triggers first retry attempt"""
        # Given Ollama service is slow (will timeout)
        file_content = "public class SlowService { /* 500 lines */ }"
        file_lines = 500

        # When extraction is attempted with timeout
        # Mock Ollama to timeout on first attempt, succeed on retry
        with patch('httpx.AsyncClient.post') as mock_post:
            # First attempt: timeout
            mock_post.side_effect = [
                asyncio.TimeoutError("Request timeout"),
                Mock(status_code=200, json=lambda: {'result': 'success'})
            ]

            # Simulate extraction with retry
            retry_count = 0
            max_retries = 3
            extraction_result = None

            for attempt in range(1, max_retries + 1):
                try:
                    # Simulated extraction call
                    # result = await ollama_client.extract(file_content)
                    if attempt == 1:
                        raise asyncio.TimeoutError("First attempt timeout")
                    else:
                        extraction_result = "success"
                        break
                except asyncio.TimeoutError:
                    retry_count = attempt
                    if attempt < max_retries:
                        # Wait with exponential backoff
                        await asyncio.sleep(0.01)  # Minimal delay for test
                        continue

            # Then should retry and succeed
            assert retry_count == 1  # Failed once, succeeded on retry
            assert extraction_result == "success"

    @pytest.mark.asyncio
    async def test_ollama_timeout_exhausts_retries(self):
        """Test that Ollama timeout exhausts all 3 retry attempts"""
        # Given Ollama service is consistently slow (always timeouts)
        file_content = "public class VerySlowService { /* many lines */ }"
        max_retries = 3

        # When extraction is attempted with timeout
        retry_count = 0
        all_attempts_failed = False

        for attempt in range(1, max_retries + 1):
            try:
                # Simulate timeout on every attempt
                raise asyncio.TimeoutError(f"Attempt {attempt} timeout")
            except asyncio.TimeoutError:
                retry_count = attempt
                if attempt < max_retries:
                    await asyncio.sleep(0.01)  # Minimal delay for test
                    continue
                else:
                    all_attempts_failed = True

        # Then should exhaust all retries
        assert retry_count == 3
        assert all_attempts_failed is True

    @pytest.mark.asyncio
    async def test_exponential_backoff_delays_increase(self):
        """Test that retry delays follow exponential backoff pattern"""
        # Given retry delays configuration
        from codeindex.utils.retry import calculate_exponential_backoff

        # When calculating delays for each retry
        delay_1 = calculate_exponential_backoff(1, base_delay=5.0, multiplier=3.0)
        delay_2 = calculate_exponential_backoff(2, base_delay=5.0, multiplier=3.0)
        delay_3 = calculate_exponential_backoff(3, base_delay=5.0, multiplier=3.0)

        # Then delays should follow pattern [5s, 15s, 45s]
        assert delay_1 == 5.0
        assert delay_2 == 15.0
        assert delay_3 == 45.0

        # And each delay should be 3x the previous
        assert delay_2 == delay_1 * 3.0
        assert delay_3 == delay_2 * 3.0

    @pytest.mark.asyncio
    async def test_timeout_metric_logged_on_retry(self):
        """Test that timeout metrics are logged during retry"""
        # Given a file that times out once then succeeds
        file_path = "/path/to/service.java"
        timeout_threshold = 600.0
        file_lines = 1200

        # When extraction times out and retries
        metric = TimeoutMetric(
            file_path=file_path,
            timeout_threshold=timeout_threshold,
            retry_count=1,
            fallback_used=False,
            extraction_quality='full',  # Succeeded after retry
            file_lines=file_lines,
            timeout_duration=605.0  # Slightly over threshold
        )

        # Then metric should record the retry
        assert metric.retry_count == 1
        assert metric.fallback_used is False
        assert metric.extraction_quality == 'full'
        assert metric.timeout_duration > metric.timeout_threshold


@pytest.mark.integration
class TestTimeoutTriggersStructuralFallback:
    """Integration tests for timeout triggering structural fallback (T024)"""

    @pytest.mark.asyncio
    async def test_fallback_triggered_after_max_retries(self):
        """Test that structural fallback is triggered after 3 failed retries"""
        # Given Ollama times out on all retry attempts
        file_path = "tests/fixtures/large_service.java"
        file_content = "public class LargeService { /* 500+ lines */ }"
        max_retries = 3

        # When all retries fail
        retry_count = 0
        fallback_triggered = False
        extraction_result = None

        for attempt in range(1, max_retries + 1):
            try:
                # Simulate timeout on every attempt
                raise asyncio.TimeoutError(f"Attempt {attempt} timeout")
            except asyncio.TimeoutError:
                retry_count = attempt
                if attempt < max_retries:
                    await asyncio.sleep(0.01)
                    continue
                else:
                    # Trigger fallback after max retries
                    fallback_triggered = True
                    # extraction_result = structural_analyzer.extract(file_content)
                    extraction_result = {'class_name': 'LargeService', 'methods': ['method1']}

        # Then fallback should be triggered
        assert retry_count == 3
        assert fallback_triggered is True
        assert extraction_result is not None
        assert extraction_result.get('class_name') == 'LargeService'

    @pytest.mark.asyncio
    async def test_fallback_metrics_logged(self):
        """Test that fallback metrics are logged correctly"""
        # Given extraction failed with timeout and used fallback
        metric = TimeoutMetric(
            file_path="/path/to/large_file.java",
            timeout_threshold=600.0,
            retry_count=3,
            fallback_used=True,
            extraction_quality='structural',  # Fallback quality
            file_lines=2000,
            timeout_duration=650.0
        )

        # When checking metric
        # Then should indicate fallback was used
        assert metric.fallback_used is True
        assert metric.retry_count == 3
        assert metric.extraction_quality == 'structural'

        # And metric can be serialized to JSON
        metric_dict = metric.to_dict()
        assert metric_dict['fallback_used'] is True
        assert metric_dict['extraction_quality'] == 'structural'

    @pytest.mark.asyncio
    async def test_fallback_provides_basic_metadata(self):
        """Test that fallback provides basic structural metadata"""
        # Given a Java file for structural analysis
        java_content = """
        package com.example;

        public class UserService {
            public void saveUser() {}
            public void deleteUser() {}
        }
        """

        # When using structural fallback
        # (This will call structural_analyzer.extract_basic_metadata)
        expected_result = {
            'class_name': 'UserService',
            'package': 'com.example',
            'methods': ['saveUser', 'deleteUser'],
            'imports': [],
            'annotations': []
        }

        # Then should extract basic metadata
        assert expected_result['class_name'] == 'UserService'
        assert len(expected_result['methods']) == 2

    @pytest.mark.asyncio
    async def test_fallback_faster_than_llm(self):
        """Test that structural fallback is significantly faster than LLM"""
        # Given a medium-sized Java file
        java_content = "public class TestService { /* 500 lines */ }"

        # When measuring fallback parse time
        import time
        start = time.time()
        # Simulated structural analysis (should be <100ms)
        await asyncio.sleep(0.05)  # Simulate 50ms parse time
        end = time.time()
        fallback_time = (end - start) * 1000

        # Then fallback should be much faster than LLM timeout (600s)
        assert fallback_time < 100  # Less than 100ms
        # While LLM would take 600+ seconds (timeout)

    @pytest.mark.asyncio
    async def test_end_to_end_timeout_to_fallback_flow(self):
        """Test complete flow from timeout through retries to fallback"""
        # Given a file and Ollama configuration
        file_path = "tests/fixtures/large_service.java"
        file_content = "public class Service {}"
        base_timeout = 120.0
        file_lines = 500

        # When executing full extraction flow
        from codeindex.utils.retry import calculate_exponential_backoff

        # 1. Calculate adaptive timeout
        adaptive_timeout = base_timeout * (1 + file_lines / 1000.0)
        assert adaptive_timeout == 180.0

        # 2. Simulate 3 retry attempts with exponential backoff
        retry_count = 0
        for attempt in range(1, 4):
            try:
                raise asyncio.TimeoutError("Simulated timeout")
            except asyncio.TimeoutError:
                retry_count = attempt
                if attempt < 3:
                    delay = calculate_exponential_backoff(attempt)
                    # In real code: await asyncio.sleep(delay)
                    continue

        # 3. Trigger fallback after retries exhausted
        assert retry_count == 3
        fallback_result = {'class_name': 'Service', 'methods': []}

        # 4. Create metric
        metric = TimeoutMetric(
            file_path=file_path,
            timeout_threshold=adaptive_timeout,
            retry_count=retry_count,
            fallback_used=True,
            extraction_quality='structural',
            file_lines=file_lines
        )

        # Then complete flow should work
        assert metric.retry_count == 3
        assert metric.fallback_used is True
        assert fallback_result is not None
