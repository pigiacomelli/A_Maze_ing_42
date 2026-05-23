import sys
from pathlib import Path

from config.parser import parse_config_file
from config.validator import validate_config
from config.exceptions import ConfigError

sys.path.insert(0, str(Path(__file__).parent / "src"))


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <config_file>")
        sys.exit(1)

    print("Program started")

    try:
        raw_config = parse_config_file(sys.argv[1])
        config = validate_config(raw_config)
    except ConfigError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    from ui.app import TerminalUI

    ui = TerminalUI(config)
    ui.run()


if __name__ == "__main__":
    main()
