import subprocess
import sys
from pathlib import Path

import pytest

from config.validator import validate_config
from mazegen import MazeGenerator
from maze.validator import MazeValidator


ROOT_DIR = Path(__file__).resolve().parents[1]


def run_app(config: Path) -> subprocess.CompletedProcess[str]:
    """
    Run the CLI with a temporary config file.
    """

    return subprocess.run(
        [sys.executable, "a_maze_ing.py", str(config)],
        cwd=ROOT_DIR,
        input="q\n",
        text=True,
        capture_output=True,
        timeout=10,
    )


def write_config(tmp_path: Path, content: str) -> Path:
    """
    Write a temporary config file.
    """

    config = tmp_path / "config.txt"
    config.write_text(content, encoding="utf-8")
    return config


def base_config(tmp_path: Path, **overrides: str) -> str:
    """
    Return a valid config with optional value overrides.
    """

    values = {
        "WIDTH": "10",
        "HEIGHT": "8",
        "ENTRY": "0,0",
        "EXIT": "9,7",
        "OUTPUT_FILE": str(tmp_path / "maze.txt"),
        "PERFECT": "True",
        "SEED": "1",
    }
    values.update(overrides)

    return "\n".join(f"{key}={value}" for key, value in values.items()) + "\n"


def assert_clean_config_error(
    result: subprocess.CompletedProcess[str],
    message: str,
) -> None:
    """
    Assert the CLI failed with a config error and no traceback.
    """

    output = result.stdout + result.stderr
    assert result.returncode == 1
    assert "Configuration error:" in output
    assert message in output
    assert "Traceback" not in output


def test_invalid_width_is_clean_config_error(tmp_path: Path) -> None:
    config = write_config(tmp_path, base_config(tmp_path, WIDTH="abc"))

    result = run_app(config)

    assert_clean_config_error(result, "WIDTH must be an integer")


def test_invalid_height_is_clean_config_error(tmp_path: Path) -> None:
    config = write_config(tmp_path, base_config(tmp_path, HEIGHT="no"))

    result = run_app(config)

    assert_clean_config_error(result, "HEIGHT must be an integer")


def test_invalid_seed_is_clean_config_error(tmp_path: Path) -> None:
    config = write_config(tmp_path, base_config(tmp_path, SEED="abc"))

    result = run_app(config)

    assert_clean_config_error(result, "SEED must be an integer")


def test_invalid_perfect_value_is_rejected(tmp_path: Path) -> None:
    config = write_config(tmp_path, base_config(tmp_path, PERFECT="maybe"))

    result = run_app(config)

    assert_clean_config_error(result, "PERFECT must be True or False")


def test_invalid_algorithm_is_rejected_cleanly(tmp_path: Path) -> None:
    config = write_config(tmp_path, base_config(tmp_path, ALGORITHM="kruskal"))

    result = run_app(config)

    assert_clean_config_error(result, "ALGORITHM must be dfs or prim")


def test_missing_algorithm_defaults_to_dfs(tmp_path: Path) -> None:
    raw = {
        "WIDTH": "10",
        "HEIGHT": "8",
        "ENTRY": "0,0",
        "EXIT": "9,7",
        "OUTPUT_FILE": str(tmp_path / "maze.txt"),
        "PERFECT": "True",
        "SEED": "1",
    }

    config = validate_config(raw)

    assert config.algorithm == "dfs"


def test_mazegen_facade_supports_prim() -> None:
    generator = MazeGenerator(10, 10, seed=1, algorithm="prim")

    maze = generator.generate()

    MazeValidator(maze).validate()


def test_mazegen_facade_rejects_invalid_algorithm() -> None:
    with pytest.raises(ValueError, match="algorithm must be dfs or prim"):
        MazeGenerator(10, 10, algorithm="kruskal")


def test_entry_on_pattern_cell_stops_before_export(tmp_path: Path) -> None:
    output_file = tmp_path / "maze.txt"
    config = write_config(
        tmp_path,
        base_config(
            tmp_path,
            WIDTH="30",
            HEIGHT="20",
            ENTRY="11,7",
            EXIT="0,0",
            OUTPUT_FILE=str(output_file),
            SEED="1",
        ),
    )

    result = run_app(config)
    output = result.stdout + result.stderr

    assert result.returncode == 1
    assert "Validation error:" in output
    assert "falls on a pattern cell" in output
    assert "Traceback" not in output
    assert not output_file.exists()


def test_exit_on_pattern_cell_stops_before_export(tmp_path: Path) -> None:
    output_file = tmp_path / "maze.txt"
    config = write_config(
        tmp_path,
        base_config(
            tmp_path,
            WIDTH="30",
            HEIGHT="20",
            ENTRY="0,0",
            EXIT="11,7",
            OUTPUT_FILE=str(output_file),
            SEED="1",
        ),
    )

    result = run_app(config)
    output = result.stdout + result.stderr

    assert result.returncode == 1
    assert "Validation error:" in output
    assert "falls on a pattern cell" in output
    assert "Traceback" not in output
    assert not output_file.exists()
