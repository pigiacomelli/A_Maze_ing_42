from pathlib import Path

from maze.cell import Cell
from maze.maze import Maze
from maze.directions import Direction


BIT_VALUES = {
    Direction.NORTH: 1 << 0,
    Direction.EAST: 1 << 1,
    Direction.SOUTH: 1 << 2,
    Direction.WEST: 1 << 3,
}


class HexExporter:
    """
    Export maze to hexadecimal format.
    """

    def __init__(
        self,
        maze: Maze,
    ) -> None:
        self.maze = maze

    def cell_to_hex(
        self,
        cell: Cell,
    ) -> str:
        """
        Convert single cell to hexadecimal.
        """

        value = 0

        for (
            direction,
            bit,
        ) in BIT_VALUES.items():
            if cell.has_wall(direction):
                value |= bit

        return format(value, "X")

    def maze_to_hex_grid(self) -> list[str]:
        """
        Convert entire maze grid
        into hexadecimal rows.
        """

        rows: list[str] = []

        for row in self.maze.grid:
            line = ""

            for cell in row:
                line += self.cell_to_hex(cell)

            rows.append(line)

        return rows

    def export(
        self,
        output_file: str,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        shortest_path: str,
    ) -> None:
        """
        Export maze to output file.
        """

        lines: list[str] = []

        lines.append(
            f"WIDTH={self.maze.width}"
        )

        lines.append(
            f"HEIGHT={self.maze.height}"
        )

        lines.append(
            f"ENTRY={entry[0]},{entry[1]}"
        )

        lines.append(
            f"EXIT={exit_[0]},{exit_[1]}"
        )

        lines.append(
            f"PATH={shortest_path}"
        )

        lines.append("GRID=")

        lines.extend(
            self.maze_to_hex_grid()
        )

        content = "\n".join(lines) + "\n"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
