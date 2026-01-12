"""
Unit tests for TimeoutCalculator (Feature 008 - T002).

Tests the adaptive timeout calculation system to reduce timeout failures
from 11.5% to <2%.

Production Issue: Fixed 240s timeout insufficient for complex files.
Solution: Dynamic timeouts based on file size.
"""

import pytest
import tempfile
from pathlib import Path
from codeindex.utils.timeout_calculator import TimeoutCalculator, calculate_timeout


class TestTimeoutCalculatorBasicCalculations:
    """Test basic timeout calculations with various line counts."""

    def test_timeout_empty_file_returns_base(self):
        """Test that empty file (0 lines) returns base timeout."""
        calc = TimeoutCalculator(base=120, scale=10)
        assert calc.calculate_for_lines(0) == 120

    def test_timeout_small_file_adds_minimal_extra(self):
        """Test that small file gets minimal extra time."""
        calc = TimeoutCalculator(base=120, scale=10)
        # 50 lines = base + (50/100)*10 = 120 + 5 = 125
        assert calc.calculate_for_lines(50) == 125

    def test_timeout_medium_file_scales_linearly(self):
        """Test that medium file timeout scales linearly."""
        calc = TimeoutCalculator(base=120, scale=10)
        # 1000 lines = base + (1000/100)*10 = 120 + 100 = 220
        assert calc.calculate_for_lines(1000) == 220

    def test_timeout_large_file_returns_scaled(self):
        """Test that large file gets appropriately scaled timeout."""
        calc = TimeoutCalculator(base=120, scale=10)
        # 5000 lines = base + (5000/100)*10 = 120 + 500 = 620
        # But capped at max_timeout=600
        assert calc.calculate_for_lines(5000) == 600  # Capped

    def test_timeout_very_large_file_capped(self):
        """Test that very large file is capped at max_timeout."""
        calc = TimeoutCalculator(base=120, scale=10, max_timeout=600)
        # 10000 lines would calculate to 1120, but capped at 600
        assert calc.calculate_for_lines(10000) == 600

    def test_timeout_respects_minimum(self):
        """Test that very small calculations respect min_timeout."""
        calc = TimeoutCalculator(base=100, scale=10, min_timeout=150)
        # 0 lines would be 100, but min is 150
        assert calc.calculate_for_lines(0) == 150


class TestTimeoutCalculatorEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_timeout_negative_lines_treated_as_zero(self):
        """Test that negative line counts are normalized to 0."""
        calc = TimeoutCalculator(base=120, scale=10)
        assert calc.calculate_for_lines(-100) == 120
        assert calc.calculate_for_lines(-1) == 120

    def test_timeout_zero_lines(self):
        """Test explicit zero line count."""
        calc = TimeoutCalculator(base=120, scale=10)
        assert calc.calculate_for_lines(0) == 120

    def test_timeout_one_line(self):
        """Test single line file."""
        calc = TimeoutCalculator(base=120, scale=10)
        # 1 line = base + (1/100)*10 = 120.1 → 120
        assert calc.calculate_for_lines(1) == 120

    def test_timeout_exactly_100_lines(self):
        """Test exactly 100 lines (boundary case)."""
        calc = TimeoutCalculator(base=120, scale=10)
        # 100 lines = base + (100/100)*10 = 120 + 10 = 130
        assert calc.calculate_for_lines(100) == 130

    def test_timeout_float_result_rounded_down(self):
        """Test that float results are converted to integers."""
        calc = TimeoutCalculator(base=100, scale=10)
        # 55 lines = 100 + (55/100)*10 = 100 + 5.5 = 105.5 → 105
        result = calc.calculate_for_lines(55)
        assert isinstance(result, int)
        assert result == 105


class TestTimeoutCalculatorCustomConfiguration:
    """Test custom configuration parameters."""

    def test_timeout_custom_base(self):
        """Test custom base timeout."""
        calc = TimeoutCalculator(base=100, scale=10)
        assert calc.calculate_for_lines(0) == 100

    def test_timeout_custom_scale(self):
        """Test custom scale factor."""
        calc = TimeoutCalculator(base=100, scale=20)
        # 100 lines = 100 + (100/100)*20 = 100 + 20 = 120
        assert calc.calculate_for_lines(100) == 120

    def test_timeout_custom_scale_high_value(self):
        """Test high scale factor."""
        calc = TimeoutCalculator(base=100, scale=50)
        # 100 lines = 100 + (100/100)*50 = 100 + 50 = 150
        assert calc.calculate_for_lines(100) == 150

    def test_timeout_custom_min_timeout(self):
        """Test custom minimum timeout."""
        calc = TimeoutCalculator(base=50, scale=5, min_timeout=100)
        # 0 lines would be 50, but min is 100
        assert calc.calculate_for_lines(0) == 100

    def test_timeout_custom_max_timeout(self):
        """Test custom maximum timeout."""
        calc = TimeoutCalculator(base=100, scale=10, max_timeout=300)
        # 5000 lines would be 600, but max is 300
        assert calc.calculate_for_lines(5000) == 300

    def test_timeout_aggressive_scaling(self):
        """Test aggressive scaling for large files."""
        calc = TimeoutCalculator(base=60, scale=30, max_timeout=900)
        # 1000 lines = 60 + (1000/100)*30 = 60 + 300 = 360
        assert calc.calculate_for_lines(1000) == 360

    def test_timeout_conservative_scaling(self):
        """Test conservative scaling (slow growth)."""
        calc = TimeoutCalculator(base=200, scale=5, max_timeout=400)
        # 1000 lines = 200 + (1000/100)*5 = 200 + 50 = 250
        assert calc.calculate_for_lines(1000) == 250


class TestTimeoutCalculatorValidation:
    """Test parameter validation."""

    def test_timeout_negative_base_raises_error(self):
        """Test that negative base timeout raises ValueError."""
        with pytest.raises(ValueError, match="base must be non-negative"):
            TimeoutCalculator(base=-10)

    def test_timeout_negative_scale_raises_error(self):
        """Test that negative scale raises ValueError."""
        with pytest.raises(ValueError, match="scale must be non-negative"):
            TimeoutCalculator(scale=-5)

    def test_timeout_negative_min_raises_error(self):
        """Test that negative min_timeout raises ValueError."""
        with pytest.raises(ValueError, match="min_timeout must be non-negative"):
            TimeoutCalculator(min_timeout=-20)

    def test_timeout_max_less_than_min_raises_error(self):
        """Test that max_timeout < min_timeout raises ValueError."""
        with pytest.raises(ValueError, match="max_timeout.*must be >= min_timeout"):
            TimeoutCalculator(min_timeout=300, max_timeout=100)

    def test_timeout_valid_edge_case_min_equals_max(self):
        """Test that min_timeout == max_timeout is valid."""
        calc = TimeoutCalculator(min_timeout=200, max_timeout=200)
        # All timeouts should be exactly 200
        assert calc.calculate_for_lines(0) == 200
        assert calc.calculate_for_lines(1000) == 200
        assert calc.calculate_for_lines(10000) == 200


class TestTimeoutCalculatorFileBasedCalculation:
    """Test file-based timeout calculation."""

    def test_timeout_for_small_file(self, tmp_path):
        """Test timeout calculation for small file."""
        # Create file with 50 non-empty lines
        file_path = tmp_path / "small.java"
        file_path.write_text("\n".join([f"line {i}" for i in range(50)]))

        calc = TimeoutCalculator(base=120, scale=10)
        timeout = calc.calculate_for_file(file_path)

        # 50 lines = 120 + (50/100)*10 = 125
        assert timeout == 125

    def test_timeout_for_large_file(self, tmp_path):
        """Test timeout calculation for large file."""
        # Create file with 2000 non-empty lines
        file_path = tmp_path / "large.java"
        file_path.write_text("\n".join([f"line {i}" for i in range(2000)]))

        calc = TimeoutCalculator(base=120, scale=10)
        timeout = calc.calculate_for_file(file_path)

        # 2000 lines = 120 + (2000/100)*10 = 320
        assert timeout == 320

    def test_timeout_for_file_with_empty_lines(self, tmp_path):
        """Test that empty lines are not counted."""
        # Create file with 100 lines, half empty
        lines = []
        for i in range(100):
            if i % 2 == 0:
                lines.append(f"line {i}")
            else:
                lines.append("")  # Empty line

        file_path = tmp_path / "sparse.java"
        file_path.write_text("\n".join(lines))

        calc = TimeoutCalculator(base=120, scale=10)
        timeout = calc.calculate_for_file(file_path)

        # Only 50 non-empty lines = 120 + (50/100)*10 = 125
        assert timeout == 125

    def test_timeout_for_file_with_whitespace_lines(self, tmp_path):
        """Test that whitespace-only lines are not counted."""
        lines = [
            "public class Test {",
            "    ",  # Whitespace only
            "    void method() {",
            "\t\t",  # Tabs only
            "    }",
            "",  # Empty
            "}",
        ]

        file_path = tmp_path / "whitespace.java"
        file_path.write_text("\n".join(lines))

        calc = TimeoutCalculator(base=120, scale=10)
        timeout = calc.calculate_for_file(file_path)

        # Only 4 non-empty, non-whitespace lines
        # 4 lines ≈ 120 (base, minimal scaling)
        assert timeout == 120

    def test_timeout_file_not_found_returns_base(self):
        """Test that non-existent file returns base timeout."""
        calc = TimeoutCalculator(base=120, scale=10)
        timeout = calc.calculate_for_file(Path("/nonexistent/file.java"))

        assert timeout == 120  # Base timeout fallback

    def test_timeout_file_permission_error_returns_base(self, tmp_path):
        """Test that unreadable file returns base timeout."""
        file_path = tmp_path / "unreadable.java"
        file_path.write_text("content")
        file_path.chmod(0o000)  # Remove all permissions

        try:
            calc = TimeoutCalculator(base=120, scale=10)
            timeout = calc.calculate_for_file(file_path)

            # Should fall back to base timeout
            assert timeout == 120
        finally:
            # Restore permissions for cleanup
            file_path.chmod(0o644)

    def test_timeout_unicode_file(self, tmp_path):
        """Test timeout calculation for file with unicode characters."""
        file_path = tmp_path / "unicode.java"
        file_path.write_text(
            "// Comment with émojis 😀\n"
            "public class Test {\n"
            "    String name = \"Café\";\n"
            "}\n",
            encoding='utf-8'
        )

        calc = TimeoutCalculator(base=120, scale=10)
        timeout = calc.calculate_for_file(file_path)

        # 4 non-empty lines
        assert timeout == 120


class TestTimeoutCalculatorConvenienceFunction:
    """Test the convenience function."""

    def test_calculate_timeout_default_config(self, tmp_path):
        """Test convenience function with default configuration."""
        file_path = tmp_path / "test.java"
        file_path.write_text("\n".join([f"line {i}" for i in range(100)]))

        timeout = calculate_timeout(file_path)

        # Default: base=120, scale=10
        # 100 lines = 120 + (100/100)*10 = 130
        assert timeout == 130

    def test_calculate_timeout_custom_config(self, tmp_path):
        """Test convenience function with custom configuration."""
        file_path = tmp_path / "test.java"
        file_path.write_text("\n".join([f"line {i}" for i in range(100)]))

        timeout = calculate_timeout(file_path, base=100, scale=20)

        # Custom: base=100, scale=20
        # 100 lines = 100 + (100/100)*20 = 120
        assert timeout == 120


class TestTimeoutCalculatorProductionScenarios:
    """Test scenarios from production error analysis."""

    def test_timeout_solr_repository_file(self, tmp_path):
        """
        Test timeout for SolrPartyRepository.java (production timeout example).

        Production: Timed out at 240s (fixed timeout).
        Expected: Adaptive timeout based on file size.
        """
        # Simulate large file (~3000 lines)
        file_path = tmp_path / "SolrPartyRepository.java"
        file_path.write_text("\n".join([f"// line {i}" for i in range(3000)]))

        calc = TimeoutCalculator(base=120, scale=10, max_timeout=600)
        timeout = calc.calculate_for_file(file_path)

        # 3000 lines = 120 + (3000/100)*10 = 420
        assert timeout == 420
        assert timeout > 240  # More than old fixed timeout

    def test_timeout_phone_number_service(self, tmp_path):
        """
        Test timeout for PhoneNumberService.java (production timeout example).

        Production: Timed out at 240s.
        """
        # Simulate medium-large file (~2500 lines)
        file_path = tmp_path / "PhoneNumberService.java"
        file_path.write_text("\n".join([f"// line {i}" for i in range(2500)]))

        calc = TimeoutCalculator(base=120, scale=10)
        timeout = calc.calculate_for_file(file_path)

        # 2500 lines = 120 + (2500/100)*10 = 370
        assert timeout == 370

    def test_timeout_small_service_stays_fast(self, tmp_path):
        """
        Test that small files maintain fast timeouts.

        Important: Don't add unnecessary overhead to simple files.
        """
        # Small service file (~200 lines)
        file_path = tmp_path / "SimpleService.java"
        file_path.write_text("\n".join([f"// line {i}" for i in range(200)]))

        calc = TimeoutCalculator(base=120, scale=10)
        timeout = calc.calculate_for_file(file_path)

        # 200 lines = 120 + (200/100)*10 = 140
        assert timeout == 140
        assert timeout < 180  # Keep it fast


class TestTimeoutCalculatorConfiguration:
    """Test configuration retrieval and string representation."""

    def test_get_config(self):
        """Test get_config returns correct configuration."""
        calc = TimeoutCalculator(base=100, scale=15, min_timeout=50, max_timeout=500)
        config = calc.get_config()

        assert config == {
            'base': 100,
            'scale': 15,
            'min_timeout': 50,
            'max_timeout': 500,
        }

    def test_repr(self):
        """Test string representation."""
        calc = TimeoutCalculator(base=120, scale=10, min_timeout=60, max_timeout=600)
        repr_str = repr(calc)

        assert "TimeoutCalculator" in repr_str
        assert "base=120s" in repr_str
        assert "scale=10s/100lines" in repr_str
        assert "min=60s" in repr_str
        assert "max=600s" in repr_str


class TestTimeoutCalculatorPerformance:
    """Test performance characteristics."""

    def test_calculate_for_lines_performance(self):
        """Test that calculate_for_lines is fast."""
        import time

        calc = TimeoutCalculator()

        # Time 10000 calculations
        start = time.time()
        for i in range(10000):
            calc.calculate_for_lines(i)
        duration = time.time() - start

        # Should complete in under 0.1 seconds
        assert duration < 0.1, f"Too slow: {duration}s for 10000 calculations"

    def test_calculate_for_file_reasonable_performance(self, tmp_path):
        """Test that file-based calculation is reasonably fast."""
        import time

        # Create a medium file
        file_path = tmp_path / "test.java"
        file_path.write_text("\n".join([f"line {i}" for i in range(1000)]))

        calc = TimeoutCalculator()

        # Time 100 file calculations
        start = time.time()
        for _ in range(100):
            calc.calculate_for_file(file_path)
        duration = time.time() - start

        # Should complete in under 1 second
        assert duration < 1.0, f"Too slow: {duration}s for 100 file calculations"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
