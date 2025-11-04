import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from click.testing import CliRunner
from cli import cli


def test_cli_config_smoke():
    runner = CliRunner()
    result = runner.invoke(cli, ["config"])  # should not require network
    assert result.exit_code == 0
    assert "Effective Configuration" in result.output

