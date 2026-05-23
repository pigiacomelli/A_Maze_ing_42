import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))


from maze.maze import Maze

from generator.dfs_generator import (
    DFSGenerator,
)

from solver.bfs_solver import BFSSolver

from exporter.hex_exporter import (
    HexExporter,
)

from config.parser import parse_config_file
from config.validator import validate_config
from config.exceptions import ConfigError


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <config_file>")
        sys.exit(1)

    print("Program started")

    try:
        raw_config = parse_config_file(sys.argv[1])
        config = validate_config(raw_config)
    except ConfigError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    maze = Maze(config.width, config.height)

    generator = DFSGenerator(
        maze,
        seed=42,
    )

    generator.generate()

    solver = BFSSolver(maze)

    path = solver.solve(
        config.entry,
        config.exit,
    )

    path_string = (
        solver.path_to_string(path)
    )

    print("Shortest path:")
    print(path_string)

    exporter = HexExporter(maze)

    exporter.export(
        output_file=config.output_file,
        entry=config.entry,
        exit_=config.exit,
        shortest_path=path_string,
    )

    print("Maze exported successfully")


if __name__ == "__main__":
    main()
