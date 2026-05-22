from collections import deque

from maze.cell import Cell
from maze.maze import Maze
from maze.directions import (
    Direction,
    DIRECTION_OFFSETS,
)


class BFSSolver:
    """
    Solve maze using BFS shortest path.
    """

    def __init__(
        self,
        maze: Maze,
    ) -> None:
        self.maze = maze

    def solve(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> list[Direction]:
        """
        Return shortest path between
        start and end.
        """

        self.maze.reset_visited()

        start_cell = self.maze.get_cell(
            *start
        )

        end_cell = self.maze.get_cell(
            *end
        )

        queue: deque[Cell] = deque()

        queue.append(start_cell)

        start_cell.mark_visited()

        came_from: dict[
            Cell,
            tuple[Cell, Direction]
        ] = {}

        while queue:
            current = queue.popleft()

            if current == end_cell:
                return self._reconstruct_path(
                    came_from,
                    start_cell,
                    end_cell,
                )

            for (
                direction,
                neighbor,
            ) in self.maze.get_neighbors(
                current
            ):
                if neighbor.is_visited():
                    continue

                if current.has_wall(direction):
                    continue

                neighbor.mark_visited()

                queue.append(neighbor)

                came_from[neighbor] = (
                    current,
                    direction,
                )

        return []

    def _reconstruct_path(
        self,
        came_from: dict[
            Cell,
            tuple[Cell, Direction]
        ],
        start: Cell,
        end: Cell,
    ) -> list[Direction]:
        """
        Reconstruct shortest path.
        """

        path: list[Direction] = []

        current = end

        while current != start:
            previous, direction = (
                came_from[current]
            )

            path.append(direction)

            current = previous

        path.reverse()

        return path

    def path_to_string(
        self,
        path: list[Direction],
    ) -> str:
        """
        Convert path to string format.

        Example:
            NNEESSWW
        """

        return "".join(
            direction.value
            for direction in path
        )