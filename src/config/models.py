from dataclasses import dataclass


@dataclass
class Config:
    """
    Store validated maze generation configuration values.
    """

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None
