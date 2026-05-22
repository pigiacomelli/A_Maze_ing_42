from maze.maze import Maze

from generator.dfs_generator import (
    DFSGenerator,
)

from solver.bfs_solver import BFSSolver

from exporter.hex_exporter import (
    HexExporter,
)


def main() -> None:
    print("Program started")

    maze = Maze(10, 12)

    generator = DFSGenerator(
        maze,
        seed=42,
    )

    generator.generate()

    solver = BFSSolver(maze)

    path = solver.solve(
        (0, 0),
        (9, 9),
    )

    path_string = (
        solver.path_to_string(path)
    )

    print("Shortest path:")
    print(path_string)

    exporter = HexExporter(maze)

    exporter.export(
        output_file="maze.txt",
        entry=(0, 0),
        exit_=(9, 9),
        shortest_path=path_string,
    )

    print("Maze exported successfully")


if __name__ == "__main__":
    main()