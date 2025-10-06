import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create temporary directory for tests that expect a temp_dir fixture."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


