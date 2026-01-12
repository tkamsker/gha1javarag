"""
Timeout Calculator - Adaptive timeout calculation based on file complexity.

Calculates dynamic timeouts for LLM analysis based on file size and complexity,
preventing timeout failures on large files while maintaining fast processing
for small files.

Algorithm:
    timeout = base + (lines / 100) * scale
    timeout = max(min_timeout, min(timeout, max_timeout))

Example:
    >>> calc = TimeoutCalculator(base=120, scale=10)
    >>> calc.calculate_for_lines(100)    # Small file
    130  # 120 + (100/100)*10
    >>> calc.calculate_for_lines(5000)   # Large file
    600  # 120 + (5000/100)*10, capped at max_timeout

Feature 008 - T002: Adaptive Timeout Strategy
Production Issue: 11.5% timeout rate in services, 1.1% in frontend
Target: <2% timeout rate
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class TimeoutCalculator:
    """
    Calculate adaptive timeouts based on file complexity.

    The timeout scales linearly with file size, with configurable base time,
    scale factor, and min/max caps.

    Attributes:
        base: Base timeout in seconds (default: 120)
        scale: Additional seconds per 100 lines (default: 10)
        min_timeout: Minimum timeout in seconds (default: 60)
        max_timeout: Maximum timeout in seconds (default: 600)

    Examples:
        Basic usage:
        >>> calc = TimeoutCalculator()
        >>> calc.calculate_for_lines(0)      # Empty file
        120
        >>> calc.calculate_for_lines(100)    # 100 lines
        130
        >>> calc.calculate_for_lines(1000)   # 1000 lines
        220
        >>> calc.calculate_for_lines(10000)  # Very large file
        600  # Capped at max_timeout

        Custom configuration:
        >>> calc = TimeoutCalculator(base=100, scale=20, max_timeout=300)
        >>> calc.calculate_for_lines(500)
        200  # 100 + (500/100)*20

        File-based calculation:
        >>> calc = TimeoutCalculator()
        >>> timeout = calc.calculate_for_file(Path("service.java"))
        >>> print(f"Timeout: {timeout}s")
    """

    def __init__(
        self,
        base: int = 120,
        scale: int = 10,
        min_timeout: int = 60,
        max_timeout: int = 600,
    ):
        """
        Initialize TimeoutCalculator with configurable parameters.

        Args:
            base: Base timeout in seconds (default: 120)
            scale: Additional seconds per 100 lines (default: 10)
            min_timeout: Minimum timeout in seconds (default: 60)
            max_timeout: Maximum timeout in seconds (default: 600)

        Raises:
            ValueError: If parameters are invalid (negative or min > max)
        """
        if base < 0:
            raise ValueError(f"base must be non-negative, got {base}")
        if scale < 0:
            raise ValueError(f"scale must be non-negative, got {scale}")
        if min_timeout < 0:
            raise ValueError(f"min_timeout must be non-negative, got {min_timeout}")
        if max_timeout < min_timeout:
            raise ValueError(
                f"max_timeout ({max_timeout}) must be >= min_timeout ({min_timeout})"
            )

        self.base = base
        self.scale = scale
        self.min_timeout = min_timeout
        self.max_timeout = max_timeout

        logger.debug(
            f"TimeoutCalculator initialized: base={base}s, scale={scale}s/100lines, "
            f"min={min_timeout}s, max={max_timeout}s"
        )

    def calculate_for_file(self, file_path: Path) -> int:
        """
        Calculate timeout for a given file based on its line count.

        Args:
            file_path: Path to the file to analyze

        Returns:
            Calculated timeout in seconds

        Raises:
            FileNotFoundError: If file doesn't exist (returns base timeout)
            OSError: If file can't be read (returns base timeout)

        Examples:
            >>> calc = TimeoutCalculator()
            >>> timeout = calc.calculate_for_file(Path("service.java"))
            >>> print(f"Timeout: {timeout}s")
            Timeout: 250s
        """
        try:
            lines = self._count_lines(file_path)
            timeout = self.calculate_for_lines(lines)

            logger.debug(
                f"Calculated timeout for {file_path.name}: {lines} lines → {timeout}s"
            )

            return timeout

        except FileNotFoundError:
            logger.warning(
                f"File not found: {file_path}, using base timeout ({self.base}s)"
            )
            return self.base

        except OSError as e:
            logger.warning(
                f"Error reading file {file_path}: {e}, using base timeout ({self.base}s)"
            )
            return self.base

        except Exception as e:
            logger.error(
                f"Unexpected error calculating timeout for {file_path}: {e}, "
                f"using base timeout ({self.base}s)"
            )
            return self.base

    def calculate_for_lines(self, lines: int) -> int:
        """
        Calculate timeout for a given line count.

        Algorithm:
            1. Normalize negative line counts to 0
            2. Calculate extra time: (lines / 100) * scale
            3. Add base timeout
            4. Apply min/max caps
            5. Round to integer

        Args:
            lines: Number of lines in the file

        Returns:
            Calculated timeout in seconds (integer)

        Examples:
            >>> calc = TimeoutCalculator(base=120, scale=10)
            >>> calc.calculate_for_lines(0)
            120
            >>> calc.calculate_for_lines(100)
            130
            >>> calc.calculate_for_lines(1000)
            220
            >>> calc.calculate_for_lines(10000)
            600  # Capped at max_timeout
            >>> calc.calculate_for_lines(-100)
            120  # Negative treated as 0
        """
        # Normalize negative line counts to 0
        if lines < 0:
            logger.debug(f"Negative line count ({lines}) normalized to 0")
            lines = 0

        # Calculate extra time based on file size
        extra = (lines / 100) * self.scale

        # Add base timeout
        timeout = self.base + extra

        # Apply min/max caps
        timeout = max(self.min_timeout, min(timeout, self.max_timeout))

        # Round to integer
        return int(timeout)

    def _count_lines(self, file_path: Path) -> int:
        """
        Count non-empty lines in a file.

        Empty lines and lines with only whitespace are not counted,
        as they don't contribute to analysis complexity.

        Args:
            file_path: Path to the file

        Returns:
            Number of non-empty lines

        Raises:
            FileNotFoundError: If file doesn't exist
            OSError: If file can't be read

        Examples:
            >>> calc = TimeoutCalculator()
            >>> lines = calc._count_lines(Path("service.java"))
            >>> print(f"Lines: {lines}")
            Lines: 523
        """
        count = 0

        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if line.strip():  # Count only non-empty lines
                    count += 1

        return count

    def get_config(self) -> dict:
        """
        Get current configuration as a dictionary.

        Returns:
            Dictionary with base, scale, min_timeout, max_timeout

        Examples:
            >>> calc = TimeoutCalculator()
            >>> config = calc.get_config()
            >>> print(config)
            {'base': 120, 'scale': 10, 'min_timeout': 60, 'max_timeout': 600}
        """
        return {
            'base': self.base,
            'scale': self.scale,
            'min_timeout': self.min_timeout,
            'max_timeout': self.max_timeout,
        }

    def __repr__(self) -> str:
        """
        String representation of TimeoutCalculator.

        Returns:
            String representation

        Examples:
            >>> calc = TimeoutCalculator()
            >>> print(calc)
            TimeoutCalculator(base=120s, scale=10s/100lines, min=60s, max=600s)
        """
        return (
            f"TimeoutCalculator(base={self.base}s, scale={self.scale}s/100lines, "
            f"min={self.min_timeout}s, max={self.max_timeout}s)"
        )


# Convenience function for quick calculations
def calculate_timeout(file_path: Path, **kwargs) -> int:
    """
    Convenience function to calculate timeout for a file with default settings.

    Args:
        file_path: Path to the file
        **kwargs: Optional TimeoutCalculator parameters (base, scale, min_timeout, max_timeout)

    Returns:
        Calculated timeout in seconds

    Examples:
        >>> timeout = calculate_timeout(Path("service.java"))
        >>> print(f"Timeout: {timeout}s")
        Timeout: 250s

        >>> timeout = calculate_timeout(Path("dao.java"), base=100, scale=15)
        >>> print(f"Custom timeout: {timeout}s")
        Custom timeout: 325s
    """
    calc = TimeoutCalculator(**kwargs)
    return calc.calculate_for_file(file_path)
