from maze.directions import get_opposite_direction
from maze.maze import Maze


class ValidatorError(Exception):
    pass


class MazeValidator:
    """
    Validates a generated maze structure.
    """

    def __init__(self, maze: Maze, perfect: bool = True) -> None:
        self.maze = maze
        self.perfect = perfect

    def validate(self) -> None:
        """
        Run all validations. Raises ValidatorError if invalid.
        """
        self._check_dimensions()
        self._check_borders()
        self._check_consistency()
        self._check_connectivity()
        self._check_no_3x3_open()
        if self.perfect:
            self._check_perfect_maze()

    def _check_dimensions(self) -> None:
        if self.maze.width <= 0 or self.maze.height <= 0:
            raise ValidatorError("Maze dimensions must be > 0.")

    def _check_borders(self) -> None:
        from maze.directions import Direction

        for x in range(self.maze.width):
            if not self.maze.get_cell(x, 0).has_wall(Direction.NORTH):
                raise ValidatorError(f"North border open at ({x}, 0)")
            if not self.maze.get_cell(x, self.maze.height - 1).has_wall(Direction.SOUTH):
                raise ValidatorError(f"South border open at ({x}, {self.maze.height - 1})")

        for y in range(self.maze.height):
            if not self.maze.get_cell(0, y).has_wall(Direction.WEST):
                raise ValidatorError(f"West border open at (0, {y})")
            if not self.maze.get_cell(self.maze.width - 1, y).has_wall(Direction.EAST):
                raise ValidatorError(f"East border open at ({self.maze.width - 1}, {y})")

    def _check_consistency(self) -> None:
        for cell in self.maze.iter_cells():
            for direction, neighbor in self.maze.get_neighbors(cell):
                if cell.has_wall(direction) != neighbor.has_wall(get_opposite_direction(direction)):
                    raise ValidatorError(
                        f"Inconsistent wall between {cell.get_position()} and {neighbor.get_position()}")

    def _check_connectivity(self) -> None:
        self.maze.reset_visited()
        start = next((c for c in self.maze.iter_cells() if not c.is_pattern), None)
        if not start:
            return

        stack = [start]
        start.mark_visited()
        reachable = 0

        while stack:
            curr = stack.pop()
            reachable += 1

            for direction, neighbor in self.maze.get_neighbors(curr):
                if not neighbor.is_pattern and not neighbor.is_visited() and not curr.has_wall(direction):
                    neighbor.mark_visited()
                    stack.append(neighbor)

        total_traversable = sum(1 for c in self.maze.iter_cells() if not c.is_pattern)
        if reachable != total_traversable:
            raise ValidatorError(
                f"Maze is not fully connected. Reached {reachable}/{total_traversable} traversable cells.")

    def _check_no_3x3_open(self) -> None:
        from maze.directions import Direction
        for y in range(self.maze.height - 2):
            for x in range(self.maze.width - 2):
                is_open = True
                for dy in range(3):
                    for dx in range(3):
                        cell = self.maze.get_cell(x + dx, y + dy)
                        if cell.is_pattern:
                            is_open = False
                            break
                        if dx < 2 and cell.has_wall(Direction.EAST):
                            is_open = False
                            break
                        if dy < 2 and cell.has_wall(Direction.SOUTH):
                            is_open = False
                            break
                    if not is_open:
                        break
                if is_open:
                    raise ValidatorError(f"3x3 open area detected at ({x},{y})")

    def _check_perfect_maze(self) -> None:
        total_open_walls = sum(
            1 for c in self.maze.iter_cells() if not c.is_pattern
            for d in c.walls if not c.walls[d]
        )
        edges = total_open_walls // 2
        traversable_cells = sum(1 for c in self.maze.iter_cells() if not c.is_pattern)

        if edges != traversable_cells - 1:
            raise ValidatorError(f"Maze is not perfect. Vertices: {traversable_cells}, Edges: {edges}")
