"""
Progress indicators for Java Codebase Indexer Pipeline.

Uses click.progressbar with ETA and rate display.
Updates every 10 seconds or 100 items (whichever is sooner) per constitution.
"""
import time
from typing import Optional, Iterable, TypeVar, Iterator
from contextlib import contextmanager
import click

T = TypeVar('T')


class ProgressTracker:
    """
    Track progress for long-running operations.

    Provides rate calculation, ETA estimation, and periodic updates.
    """

    def __init__(self, total: Optional[int] = None, label: str = "Processing"):
        """
        Initialize progress tracker.

        Args:
            total: Total number of items to process (None for unknown)
            label: Label to display in progress bar
        """
        self.total = total
        self.label = label
        self.processed = 0
        self.start_time = time.time()
        self.last_update = self.start_time

    def update(self, count: int = 1):
        """
        Update progress by count items.

        Args:
            count: Number of items processed since last update
        """
        self.processed += count

    @property
    def elapsed(self) -> float:
        """Elapsed time in seconds."""
        return time.time() - self.start_time

    @property
    def rate(self) -> float:
        """Processing rate (items per second)."""
        if self.elapsed == 0:
            return 0.0
        return self.processed / self.elapsed

    @property
    def rate_per_minute(self) -> float:
        """Processing rate (items per minute)."""
        return self.rate * 60

    @property
    def eta_seconds(self) -> Optional[float]:
        """
        Estimated time remaining in seconds.

        Returns:
            Seconds remaining, or None if total is unknown
        """
        if self.total is None or self.rate == 0:
            return None
        remaining = self.total - self.processed
        return remaining / self.rate

    def format_time(self, seconds: float) -> str:
        """
        Format seconds as HH:MM:SS.

        Args:
            seconds: Time in seconds

        Returns:
            Formatted time string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def summary(self) -> str:
        """
        Get progress summary string.

        Returns:
            Summary with elapsed time, rate, ETA
        """
        elapsed_str = self.format_time(self.elapsed)

        if self.total:
            pct = (self.processed / self.total) * 100
            progress = f"{self.processed}/{self.total} ({pct:.1f}%)"
        else:
            progress = f"{self.processed} items"

        rate_str = f"{self.rate_per_minute:.1f} items/min"

        parts = [
            f"Progress: {progress}",
            f"Elapsed: {elapsed_str}",
            f"Rate: {rate_str}"
        ]

        if self.eta_seconds:
            eta_str = self.format_time(self.eta_seconds)
            parts.append(f"ETA: {eta_str}")

        return " | ".join(parts)


@contextmanager
def progress_bar(
    iterable: Iterable[T],
    total: Optional[int] = None,
    label: str = "Processing",
    show_eta: bool = True,
    show_percent: bool = True,
    item_show_func: Optional[callable] = None
) -> Iterator[T]:
    """
    Context manager for progress bar using click.progressbar.

    Args:
        iterable: Iterable to wrap
        total: Total number of items (if known)
        label: Label to display
        show_eta: Show estimated time remaining
        show_percent: Show percentage completion
        item_show_func: Function to customize item display

    Yields:
        Items from iterable with progress tracking

    Example:
        with progress_bar(files, len(files), "Scanning files") as bar:
            for file in bar:
                process(file)
    """
    with click.progressbar(
        iterable,
        length=total,
        label=label,
        show_eta=show_eta,
        show_percent=show_percent,
        item_show_func=item_show_func,
        fill_char="█",
        empty_char="░"
    ) as bar:
        yield bar


class ThrottledProgressBar:
    """
    Progress bar that updates at most once per interval.

    Prevents excessive updates for fast operations.
    Updates every 10 seconds or 100 items per constitution.
    """

    def __init__(
        self,
        total: Optional[int] = None,
        label: str = "Processing",
        update_interval: float = 10.0,
        update_count: int = 100
    ):
        """
        Initialize throttled progress bar.

        Args:
            total: Total number of items
            label: Progress bar label
            update_interval: Minimum seconds between updates (default: 10)
            update_count: Update every N items (default: 100)
        """
        self.total = total
        self.label = label
        self.update_interval = update_interval
        self.update_count = update_count
        self.processed = 0
        self.last_update_time = time.time()
        self.last_update_count = 0
        self.tracker = ProgressTracker(total, label)
        self.bar: Optional[click.progressbar] = None

    def __enter__(self):
        """Enter context manager."""
        self.bar = click.progressbar(
            length=self.total,
            label=self.label,
            show_eta=True,
            show_percent=True if self.total else False,
            fill_char="█",
            empty_char="░"
        )
        self.bar.__enter__()
        return self

    def __exit__(self, *args):
        """Exit context manager."""
        if self.bar:
            self.bar.__exit__(*args)

    def update(self, count: int = 1):
        """
        Update progress (throttled).

        Args:
            count: Number of items processed
        """
        self.processed += count
        self.tracker.update(count)

        # Check if should update display
        elapsed = time.time() - self.last_update_time
        items_since_update = self.processed - self.last_update_count

        if elapsed >= self.update_interval or items_since_update >= self.update_count:
            if self.bar:
                self.bar.update(items_since_update)
            self.last_update_time = time.time()
            self.last_update_count = self.processed

    def finish(self):
        """Finish progress bar (show 100%)."""
        if self.bar and self.processed > self.last_update_count:
            remaining = self.processed - self.last_update_count
            self.bar.update(remaining)
