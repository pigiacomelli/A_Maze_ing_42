import random

from maze.cell import Cell
from maze.maze import Maze
from maze.directions import Direction


class DFSGenerator:
    """
    Generate mazes using
    Recursive Backtracking DFS.
    """

    def __init__(
        self,
        maze: Maze,
        seed: int | None = None,
    ) -> None:
        self.maze = maze

        self.random = random.Random(seed)

    def generate(self) -> None:
        """
        Start maze generation.
        """

        start = self.maze.get_cell(0, 0)

        self._dfs(start)

    def _dfs(
        self,
        current: Cell,
    ) -> None:
        """
        Recursive DFS generation.
        """

        current.mark_visited()

        neighbors = (
            self.maze.get_unvisited_neighbors(
                current
            )
        )

        self.random.shuffle(neighbors)

        for (
            direction,
            neighbor,
        ) in neighbors:
            if neighbor.is_visited():
                continue

            self.maze.remove_wall_between(
                current,
                neighbor,
                direction,
            )

            self._dfs(neighbor)

    def reset(self) -> None:
        """
        Reset maze visited state.
        """

        self.maze.reset_visited()