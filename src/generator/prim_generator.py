import random

from generator.dfs_generator import DFSGenerator
from maze.cell import Cell
from maze.directions import Direction
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
