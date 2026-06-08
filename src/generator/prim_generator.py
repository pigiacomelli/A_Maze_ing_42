import random

from generator.dfs_generator import DFSGenerator
from maze.cell import Cell
from maze.directions import Direction, get_opposite_direction
from maze.maze import Maze


class PrimGenerator(DFSGenerator):
    """
    Generate mazes using Randomized Prim's algorithm.
    """

    def __init__(
        self,
        maze: Maze,
        seed: int | None = None,
        perfect: bool = True,
    ) -> None:
        self.maze = maze
        self.perfect = perfect
        self.random = random.Random(seed)

    def generate(self) -> None:
        """
        Start maze generation.
        """
        self._carve_pattern_42()

        start = self.maze.get_cell(0, 0)
        if start.is_pattern:
            for cell in self.maze.iter_cells():
                if not cell.is_pattern:
                    start = cell
                    break

        self._prim(start)

        if not self.perfect:
            self._make_imperfect()

    def _prim(self, start_cell: Cell) -> None:
        """
        Execute Randomized Prim's algorithm to generate the maze.
        """
        frontier: list[tuple[Cell, Direction, Cell]] = []

        start_cell.mark_visited()
        self._add_frontier(start_cell, frontier)

        while frontier:
            index = self.random.randrange(len(frontier))
            current, direction, neighbor = frontier.pop(index)

            if neighbor.is_visited() or neighbor.is_pattern:
                continue

            self.maze.remove_wall_between(current, neighbor, direction)
            neighbor.mark_visited()
            self._add_frontier(neighbor, frontier)

    def _add_frontier(
        self,
        cell: Cell,
        frontier: list[tuple[Cell, Direction, Cell]],
    ) -> None:
        """
        Add unvisited non-pattern neighbors to the frontier.
        """
        for direction, neighbor in self.maze.get_neighbors(cell):
            if not neighbor.is_visited() and not neighbor.is_pattern:
                frontier.append((cell, direction, neighbor))

    def _make_imperfect(self) -> None:
        """
        Safely remove a conservative number of dead-end walls.

        Prim mazes branch differently from DFS mazes, so blindly opening
        dead-end walls can create 3x3 open areas. Each candidate wall is
        opened only if a temporary removal keeps the local 3x3 constraint.
        """
        dead_ends = [
            cell for cell in self.maze.iter_cells()
            if not cell.is_pattern and sum(cell.walls.values()) == 3
        ]

        self.random.shuffle(dead_ends)
        num_to_remove = len(dead_ends) // 3

        removed = 0
        for cell in dead_ends:
            if removed >= num_to_remove:
                break

            neighbors = self.maze.get_neighbors(cell)
            self.random.shuffle(neighbors)

            for direction, neighbor in neighbors:
                if (
                    neighbor.is_pattern
                    or not cell.has_wall(direction)
                    or not self._remove_wall_if_safe(cell, neighbor, direction)
                ):
                    continue

                removed += 1
                break

    def _remove_wall_if_safe(
        self,
        cell: Cell,
        neighbor: Cell,
        direction: Direction,
    ) -> bool:
        """
        Remove a wall only if it does not create a 3x3 open area.
        """
        self.maze.remove_wall_between(cell, neighbor, direction)

        if self._has_new_open_3x3(cell, neighbor):
            cell.add_wall(direction)
            neighbor.add_wall(get_opposite_direction(direction))
            return False

        return True

    def _has_new_open_3x3(
        self,
        cell: Cell,
        neighbor: Cell,
    ) -> bool:
        """
        Check only 3x3 windows that could include the new opening.
        """
        min_x = min(cell.x, neighbor.x)
        max_x = max(cell.x, neighbor.x)
        min_y = min(cell.y, neighbor.y)
        max_y = max(cell.y, neighbor.y)

        start_x_min = max(0, max_x - 2)
        start_x_max = min(min_x, self.maze.width - 3)
        start_y_min = max(0, max_y - 2)
        start_y_max = min(min_y, self.maze.height - 3)

        for y in range(start_y_min, start_y_max + 1):
            for x in range(start_x_min, start_x_max + 1):
                if self._is_open_3x3_at(x, y):
                    return True

        return False

    def _is_open_3x3_at(self, x: int, y: int) -> bool:
        """
        Return True if the 3x3 block at x,y is fully open.
        """
        for dy in range(3):
            for dx in range(3):
                cell = self.maze.get_cell(x + dx, y + dy)

                if cell.is_pattern:
                    return False

                if dx < 2 and cell.has_wall(Direction.EAST):
                    return False

                if dy < 2 and cell.has_wall(Direction.SOUTH):
                    return False

        return True
