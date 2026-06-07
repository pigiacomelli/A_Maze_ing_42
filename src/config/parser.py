from config.exceptions import ConfigError


def parse_config_file(path: str) -> dict[str, str]:
    """
    Parse a KEY=VALUE configuration file into a dictionary.
    """

    config: dict[str, str] = {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError as exc:
        raise ConfigError(f"Cannot open config file: {path}") from exc

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            raise ConfigError(
                f"Invalid line {line_number}: missing '='"
            )

        key, value = line.split("=", maxsplit=1)

        key = key.strip()
        value = value.strip()

        config[key] = value

    return config
