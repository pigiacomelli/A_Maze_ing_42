from maze.cell import Cell
from maze.directions import (
    Direction,
    DIRECTION_OFFSETS,
    get_opposite_direction,
)


class Maze:
    """
    Represents the complete maze grid.
    """

    def __init__(
        self,
        width: int,
        height: int,
    ) -> None:
        self.width = width
        self.height = height

        self.grid: list[list[Cell]] = [
            [
                Cell(x, y)
                for x in range(width)
            ]
            for y in range(height)
        ]

    def is_within_bounds(
        self,
        x: int,
        y: int,
    ) -> bool:
        """
        Check if coordinates are inside maze bounds.
        """

        return (
            0 <= x < self.width
            and 0 <= y < self.height
        )

    def get_cell(
        self,
        x: int,
        y: int,
    ) -> Cell:
        """
        Return cell at given coordinates.
        """

        return self.grid[y][x]

    def get_neighbors(
        self,
        cell: Cell,
    ) -> list[tuple[Direction, Cell]]:
        """
        Return all valid neighboring cells.
        """

        neighbors: list[
            tuple[Direction, Cell]
        ] = []

        for (
            direction,
            (dx, dy),
        ) in DIRECTION_OFFSETS.items():
            nx = cell.x + dx
            ny = cell.y + dy

            if self.is_within_bounds(nx, ny):
                neighbor = self.get_cell(nx, ny)

                neighbors.append(
                    (direction, neighbor)
                )

        return neighbors

    def get_unvisited_neighbors(
        self,
        cell: Cell,
    ) -> list[tuple[Direction, Cell]]:
        """
        Return only unvisited neighbors.
        """

        neighbors = self.get_neighbors(cell)

        return [
            (direction, neighbor)
            for direction, neighbor in neighbors
            if not neighbor.is_visited()
        ]

    def remove_wall_between(
        self,
        current: Cell,
        neighbor: Cell,
        direction: Direction,
    ) -> None:
        """
        Remove walls between two adjacent cells.
        """

        current.remove_wall(direction)

        opposite = get_opposite_direction(
            direction
        )

        neighbor.remove_wall(opposite)

    def reset_visited(self) -> None:
        """
        Reset visited state for all cells.
        """

        for row in self.grid:
            for cell in row:
                cell.reset_visited()

    def iter_cells(self) -> list[Cell]:
        """
        Return flat list of all cells.
        """

        return [
            cell
            for row in self.grid
            for cell in row
        ]

    def __repr__(self) -> str:
        """
        Debug representation.
        """

        return (
            f"Maze("
            f"width={self.width}, "
            f"height={self.height}"
            f")"
        )