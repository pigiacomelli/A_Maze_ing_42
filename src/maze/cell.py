from dataclasses import dataclass, field

from maze.directions import Direction


@dataclass(eq=False)
class Cell:
    """
    Represents a single maze cell.

    Each cell contains:
    - coordinates
    - wall states
    - visited flag
    """

    x: int
    y: int

    visited: bool = False

    walls: dict[Direction, bool] = field(
        default_factory=lambda: {
            Direction.NORTH: True,
            Direction.EAST: True,
            Direction.SOUTH: True,
            Direction.WEST: True,
        }
    )

    def remove_wall(
        self,
        direction: Direction,
    ) -> None:
        """
        Remove a wall in a given direction.

        False means:
            wall removed / passage open
        """

        self.walls[direction] = False

    def add_wall(
        self,
        direction: Direction,
    ) -> None:
        """
        Add a wall in a given direction.

        True means:
            wall exists
        """

        self.walls[direction] = True

    def has_wall(
        self,
        direction: Direction,
    ) -> bool:
        """
        Check if a wall exists
        in a given direction.
        """

        return self.walls[direction]

    def mark_visited(self) -> None:
        """
        Mark cell as visited.
        """

        self.visited = True

    def reset_visited(self) -> None:
        """
        Reset visited state.
        """

        self.visited = False

    def is_visited(self) -> bool:
        """
        Return visited state.
        """

        return self.visited

    def get_position(self) -> tuple[int, int]:
        """
        Return cell coordinates.
        """

        return (self.x, self.y)

    def __repr__(self) -> str:
        """
        Debug representation.
        """

        return (
            f"Cell("
            f"x={self.x}, "
            f"y={self.y}, "
            f"visited={self.visited}"
            f")"
        )
