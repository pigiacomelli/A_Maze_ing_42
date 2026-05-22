from maze.maze import Maze
from generator.dfs_generator import (
    DFSGenerator,
)


def test_generator_visits_all_cells() -> None:
    maze = Maze(10, 10)

    generator = DFSGenerator(maze)

    generator.generate()

    all_visited = all(
        cell.is_visited()
        for cell in maze.iter_cells()
    )

    assert all_visited


def test_reset_visited() -> None:
    maze = Maze(3, 3)

    generator = DFSGenerator(maze)

    generator.generate()

    generator.reset()

    all_reset = all(
        not cell.is_visited()
        for cell in maze.iter_cells()
    )

    assert all_reset