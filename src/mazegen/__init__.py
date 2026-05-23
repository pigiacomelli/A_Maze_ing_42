from maze.maze import Maze
from generator.dfs_generator import DFSGenerator
from solver.bfs_solver import BFSSolver


class MazeGenerator:
    """
    Reusable Facade for Maze Generation and Solving.
    """

    def __init__(
        self, width: int, height: int, seed: int | None = None, perfect: bool = True
    ) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.maze = Maze(width, height)

    def generate(self) -> Maze:
        """
        Generate the maze and return the Maze instance.
        """
        generator = DFSGenerator(self.maze, seed=self.seed, perfect=self.perfect)
        generator.generate()
        return self.maze

    def shortest_path(self, start: tuple[int, int], end: tuple[int, int]) -> str:
        """
        Solve the maze and return the shortest path string.
        """
        solver = BFSSolver(self.maze)
        path = solver.solve(start, end)
        return solver.path_to_string(path)
