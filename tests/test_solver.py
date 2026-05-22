from maze.maze import Maze
from maze.directions import Direction
from solver.bfs_solver import BFSSolver


def test_solver_finds_path() -> None:
    maze = Maze(2, 1)

    left = maze.get_cell(0, 0)
    right = maze.get_cell(1, 0)

    maze.remove_wall_between(
        left,
        right,
        Direction.EAST,
    )

    solver = BFSSolver(maze)

    path = solver.solve(
        (0, 0),
        (1, 0),
    )

    assert path == [Direction.EAST]


def test_path_to_string() -> None:
    maze = Maze(1, 1)

    solver = BFSSolver(maze)

    result = solver.path_to_string(
        [
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
        ]
    )

    assert result == "NES"