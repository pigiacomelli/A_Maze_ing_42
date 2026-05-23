from enum import Enum


class Direction(Enum):
    """
    Represents the four cardinal directions
    used inside the maze.
    """

    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"


# Coordinate movement offsets.
#
# x -> horizontal movement
# y -> vertical movement
#
# Example:
#
# NORTH => (0, -1)
#
# means:
# x stays the same
# y decreases by 1
#
DIRECTION_OFFSETS: dict[Direction, tuple[int, int]] = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}


# Opposite direction mapping.
#
# Used when removing walls between cells.
#
# Example:
#
# If current cell removes EAST wall,
# neighbor must remove WEST wall.
#
OPPOSITE_DIRECTION: dict[Direction, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}


def get_opposite_direction(
    direction: Direction,
) -> Direction:
    """
    Return the opposite direction for a given cardinal direction.

    Example:
        NORTH -> SOUTH
        EAST -> WEST

    Args:
        direction (Direction): The cardinal direction to invert.

    Returns:
        Direction: The opposite cardinal direction.
    """

    return OPPOSITE_DIRECTION[direction]


def get_direction_offset(
    direction: Direction,
) -> tuple[int, int]:
    """
    Return movement offset for a direction.

    Example:
        EAST -> (1, 0)
    """

    return DIRECTION_OFFSETS[direction]
