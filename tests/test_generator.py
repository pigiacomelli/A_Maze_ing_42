from maze.maze import Maze
from generator.dfs_generator import (
    DFSGenerator,
)
from generator.prim_generator import PrimGenerator
from maze.validator import MazeValidator


def serialize_maze(maze: Maze) -> list[bool]:
    """
    Serialize wall state for reproducibility assertions.
    """
    return [
        wall
        for cell in maze.iter_cells()
        for wall in cell.walls.values()
    ]


def test_generator_visits_all_cells() -> None:
    maze = Maze(10, 10)

    generator = DFSGenerator(maze)

    generator.generate()

    all_visited = all(
        cell.is_visited()
        for cell in maze.iter_cells()
    )

    assert all_visited


def test_dfs_generation_is_valid() -> None:
    maze = Maze(10, 10)

    generator = DFSGenerator(maze, seed=1)

    generator.generate()

    MazeValidator(maze).validate()


def test_prim_generation_is_valid() -> None:
    maze = Maze(10, 10)

    generator = PrimGenerator(maze, seed=1)

    generator.generate()

    MazeValidator(maze).validate()


def test_prim_generation_is_reproducible() -> None:
    first = Maze(10, 10)
    second = Maze(10, 10)

    PrimGenerator(first, seed=42).generate()
    PrimGenerator(second, seed=42).generate()

    assert serialize_maze(first) == serialize_maze(second)


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
