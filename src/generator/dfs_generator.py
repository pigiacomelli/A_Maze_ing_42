import random

from maze.cell import Cell
from maze.maze import Maze


class DFSGenerator:
    """
    Generate mazes using
    Iterative Backtracking DFS.
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

        self._dfs(start)

        if not self.perfect:
            self._make_imperfect()

    def _dfs(self, start_cell: Cell) -> None:
        """
        Execute an iterative Depth-First Search to generate the maze.

        Using an iterative approach with a stack prevents RecursionError
        on large maze configurations.

        Args:
            start_cell (Cell): The starting point for the maze generation.
        """
        stack: list[Cell] = [start_cell]
        start_cell.mark_visited()

        while stack:
            current = stack[-1]
            neighbors = self.maze.get_unvisited_neighbors(current)

            valid_neighbors = [
                (direction, neighbor)
                for direction, neighbor in neighbors
                if not neighbor.is_pattern
            ]

            if valid_neighbors:
                direction, neighbor = self.random.choice(valid_neighbors)

                self.maze.remove_wall_between(current, neighbor, direction)
                neighbor.mark_visited()
                stack.append(neighbor)
            else:
                stack.pop()

    def reset(self) -> None:
        """
        Reset maze visited state.
        """

        self.maze.reset_visited()

    def _carve_pattern_42(self) -> None:
        """
        Carves the '42' pattern in the middle of the maze by marking
        specific cells as pattern cells (fully closed).
        """
        if self.maze.width < 10 or self.maze.height < 7:
            print("Warning: Maze too small for pattern '42'. Skipping.")
            return

        start_x = (self.maze.width - 7) // 2
        start_y = (self.maze.height - 5) // 2

        pattern_4 = [
            (0, 0), (0, 1), (0, 2),
            (1, 2),
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)
        ]

        pattern_2 = [
            (0, 0), (1, 0), (2, 0),
            (2, 1),
            (0, 2), (1, 2), (2, 2),
            (0, 3),
            (0, 4), (1, 4), (2, 4)
        ]

        for dx, dy in pattern_4:
            cell = self.maze.get_cell(start_x + dx, start_y + dy)
            cell.is_pattern = True
            cell.mark_visited()

        for dx, dy in pattern_2:
            cell = self.maze.get_cell(start_x + 4 + dx, start_y + dy)
            cell.is_pattern = True
            cell.mark_visited()

    def _make_imperfect(self) -> None:
        """
        Randomly remove some walls to create an imperfect maze.
        By only targeting dead-ends (cells with 3 walls), we guarantee
        no 3x3 open areas are created.
        """
        dead_ends = [
            c for c in self.maze.iter_cells()
            if not c.is_pattern and sum(c.walls.values()) == 3
        ]

        self.random.shuffle(dead_ends)
        num_to_remove = len(dead_ends) // 2

        removed = 0
        for cell in dead_ends:
            if removed >= num_to_remove:
                break

            neighbors = self.maze.get_neighbors(cell)
            self.random.shuffle(neighbors)

            for direction, neighbor in neighbors:
                if not neighbor.is_pattern and cell.has_wall(direction):
                    self.maze.remove_wall_between(cell, neighbor, direction)
                    removed += 1
                    break
