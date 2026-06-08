from maze.maze import Maze
from generator.dfs_generator import DFSGenerator
from generator.prim_generator import PrimGenerator
from solver.bfs_solver import BFSSolver


class MazeGenerator:
    """
    Reusable Facade for Maze Generation and Solving.
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None = None,
        perfect: bool = True,
        algorithm: str = "dfs",
    ) -> None:
        algorithm = algorithm.strip().lower()
        if algorithm not in {"dfs", "prim"}:
            raise ValueError("algorithm must be dfs or prim")

        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.algorithm = algorithm
        self.maze = Maze(width, height)

    def generate(self) -> Maze:
        """
        Generate the maze and return the Maze instance.
        """
        generator: DFSGenerator | PrimGenerator
        if self.algorithm == "prim":
            generator = PrimGenerator(
                self.maze,
                seed=self.seed,
                perfect=self.perfect,
            )
        else:
            generator = DFSGenerator(
                self.maze,
                seed=self.seed,
                perfect=self.perfect,
            )
        generator.generate()
        return self.maze

    def shortest_path(self, start: tuple[int, int], end: tuple[int, int]) -> str:
        """
        Solve the maze and return the shortest path string.
        """
        solver = BFSSolver(self.maze)
        path = solver.solve(start, end)
        return solver.path_to_string(path)
