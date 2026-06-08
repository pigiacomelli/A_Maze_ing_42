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


def test_prim_imperfect_regression_seeds_are_valid() -> None:
    cases = [
        (30, 20, 62),
        (50, 40, 10),
        (50, 40, 18),
        (50, 40, 29),
        (50, 40, 51),
        (50, 40, 85),
        (50, 40, 91),
    ]

    for width, height, seed in cases:
        maze = Maze(width, height)

        generator = PrimGenerator(maze, seed=seed, perfect=False)

        generator.generate()

        MazeValidator(maze, perfect=False).validate()


def test_prim_perfect_generation_stays_reproducible() -> None:
    first = Maze(30, 20)
    second = Maze(30, 20)

    PrimGenerator(first, seed=62, perfect=True).generate()
    PrimGenerator(second, seed=62, perfect=True).generate()

    MazeValidator(first, perfect=True).validate()
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
