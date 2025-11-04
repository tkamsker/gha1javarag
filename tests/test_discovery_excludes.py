from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from config.settings import settings
from discover.file_discovery import FileDiscovery


def test_discovery_skips_ignored_dirs(tmp_path):
    # Arrange: create tmp project structure
    src_root = tmp_path / "project"
    (src_root / "src" / "main" / "java").mkdir(parents=True)
    (src_root / "node_modules" / "lib").mkdir(parents=True)

    java_file = src_root / "src" / "main" / "java" / "Hello.java"
    java_file.write_text("class Hello {}", encoding="utf-8")

    ignored_java = src_root / "node_modules" / "lib" / "Ignored.java"
    ignored_java.write_text("class Ignored {}", encoding="utf-8")

    # Point settings to tmp source dir
    settings.java_source_dir = str(src_root)

    # Act
    discovery = FileDiscovery()
    files = discovery.discover_all_files()

    # Assert: we include Hello.java, exclude Ignored.java
    assert any(p.endswith("Hello.java") for p in files.get("java", []))
    assert not any("node_modules" in p for p in files.get("java", []))

