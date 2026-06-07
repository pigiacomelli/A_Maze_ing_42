from config.models import Config
from config.exceptions import ConfigError


REQUIRED_KEYS = {
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
}


def parse_int(value: str, key: str) -> int:
    """
    Parse an integer configuration value.
    """

    try:
        return int(value)
    except ValueError as exc:
        raise ConfigError(f"{key} must be an integer") from exc


def parse_position(value: str) -> tuple[int, int]:
    """
    Parse coordinates written in x,y format.
    """

    try:
        x_str, y_str = value.split(",")
        return int(x_str), int(y_str)
    except ValueError as exc:
        raise ConfigError(
            f"Invalid coordinate format: {value}"
        ) from exc


def validate_config(raw: dict[str, str]) -> Config:
    """
    Validate raw configuration values and return a Config object.
    """

    missing = REQUIRED_KEYS - raw.keys()

    if missing:
        raise ConfigError(
            f"Missing keys: {', '.join(sorted(missing))}"
        )

    width = parse_int(raw["WIDTH"], "WIDTH")
    height = parse_int(raw["HEIGHT"], "HEIGHT")

    if width <= 0:
        raise ConfigError("WIDTH must be > 0")

    if height <= 0:
        raise ConfigError("HEIGHT must be > 0")

    entry = parse_position(raw["ENTRY"])
    exit_ = parse_position(raw["EXIT"])

    if entry == exit_:
        raise ConfigError("ENTRY and EXIT cannot be equal")

    for x, y in [entry, exit_]:
        if x < 0 or y < 0:
            raise ConfigError("Coordinates cannot be negative")

        if x >= width or y >= height:
            raise ConfigError(
                "Coordinates out of maze bounds"
            )

    perfect_value = raw["PERFECT"].lower()
    if perfect_value not in {"true", "false"}:
        raise ConfigError("PERFECT must be True or False")

    perfect = perfect_value == "true"

    output_file = raw["OUTPUT_FILE"].strip()
    if not output_file:
        raise ConfigError("OUTPUT_FILE cannot be empty")

    seed_str = raw.get("SEED")
    seed = parse_int(seed_str, "SEED") if seed_str is not None else None

    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit_,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
    )
