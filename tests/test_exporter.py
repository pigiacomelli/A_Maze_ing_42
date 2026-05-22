from maze.maze import Maze
from maze.directions import Direction
from exporter.hex_exporter import (
    HexExporter,
)


def test_cell_to_hex() -> None:
    maze = Maze(1, 1)

    cell = maze.get_cell(0, 0)

    exporter = HexExporter(maze)

    assert (
        exporter.cell_to_hex(cell)
        == "F"
    )


def test_open_wall_changes_hex() -> None:
    maze = Maze(2, 1)

    left = maze.get_cell(0, 0)
    right = maze.get_cell(1, 0)

    maze.remove_wall_between(
        left,
        right,
        Direction.EAST,
    )

    exporter = HexExporter(maze)

    left_hex = exporter.cell_to_hex(left)

    right_hex = exporter.cell_to_hex(right)

    assert left_hex != "F"

    assert right_hex != "F"