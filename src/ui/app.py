from config.models import Config
from exporter.hex_exporter import HexExporter
from generator.dfs_generator import DFSGenerator
from maze.maze import Maze
from maze.validator import MazeValidator, ValidatorError
from solver.bfs_solver import BFSSolver

COLORS = [
    "\033[0m",
    "\033[94m",
    "\033[95m",
    "\033[96m",
    "\033[97m",
]


class TerminalUI:
    """
    Interactive Terminal UI for the Maze Generator.
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        self.show_path = False
        self.color_index = 1

        self.maze = Maze(config.width, config.height)
        self.path: list = []
        self.path_string: str = ""

        self._generate_and_export(first_run=True)

    def _generate_and_export(self, first_run: bool = False) -> None:
        """
        Generate the maze, solve it, export to hex, and run validation.
        """
        self.maze = Maze(self.config.width, self.config.height)

        seed = self.config.seed if first_run else None

        generator = DFSGenerator(self.maze, seed=seed, perfect=self.config.perfect)
        generator.generate()

        solver = BFSSolver(self.maze)
        self.path = solver.solve(self.config.entry, self.config.exit)
        self.path_string = solver.path_to_string(self.path)

        try:
            validator = MazeValidator(self.maze, perfect=self.config.perfect)
            validator.validate()
        except ValidatorError as e:
            print(f"\n\033[91m[Validator Warning] {e}\033[0m")

        exporter = HexExporter(self.maze)
        exporter.export(
            output_file=self.config.output_file,
            entry=self.config.entry,
            exit_=self.config.exit,
            shortest_path=self.path_string,
        )

    def render(self) -> None:
        """
        Render the maze to the terminal.
        """
        print("\033[2J\033[H", end="")

        width = self.maze.width
        height = self.maze.height

        grid_w = width * 2 + 1
        grid_h = height * 2 + 1

        display = [[" "] * grid_w for _ in range(grid_h)]

        from maze.directions import Direction

        for y in range(height):
            for x in range(width):
                cell = self.maze.get_cell(x, y)
                cx = x * 2 + 1
                cy = y * 2 + 1

                display[cy - 1][cx - 1] = "█"
                display[cy - 1][cx + 1] = "█"
                display[cy + 1][cx - 1] = "█"
                display[cy + 1][cx + 1] = "█"

                if cell.has_wall(Direction.NORTH): display[cy - 1][cx] = "█"
                if cell.has_wall(Direction.SOUTH): display[cy + 1][cx] = "█"
                if cell.has_wall(Direction.WEST): display[cy][cx - 1] = "█"
                if cell.has_wall(Direction.EAST): display[cy][cx + 1] = "█"

                if cell.is_pattern:
                    display[cy][cx] = "█"

        if self.show_path and self.path:
            curr_x, curr_y = self.config.entry
            display[curr_y * 2 + 1][curr_x * 2 + 1] = "."
            for d in self.path:
                if d == Direction.NORTH:
                    curr_y -= 1
                elif d == Direction.SOUTH:
                    curr_y += 1
                elif d == Direction.EAST:
                    curr_x += 1
                elif d == Direction.WEST:
                    curr_x -= 1
                display[curr_y * 2 + 1][curr_x * 2 + 1] = "."

        ex, ey = self.config.entry
        display[ey * 2 + 1][ex * 2 + 1] = "S"

        xx, xy = self.config.exit
        display[xy * 2 + 1][xx * 2 + 1] = "E"

        color = COLORS[self.color_index]
        reset = COLORS[0]

        print(f"Maze ({width}x{height}) - Perfect: {self.config.perfect}\n")

        for row in display:
            line = ""
            for char in row:
                if char == "█":
                    line += f"{color}██{reset}"
                elif char == ".":
                    line += f"\033[93m..{reset}"
                elif char == "S":
                    line += f"\033[92mSS{reset}"
                elif char == "E":
                    line += f"\033[91mEE{reset}"
                else:
                    line += "  "
            print(line)

        print("\nCommands:")
        print("  [r] Regenerate maze")
        print("  [s] Toggle shortest path")
        print("  [c] Change wall color")
        print("  [q] Quit\n")

    def run(self) -> None:
        """
        Start the interactive loop.
        """
        while True:
            self.render()
            try:
                cmd = input("Command > ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                break

            if cmd == "q":
                break
            elif cmd == "r":
                self._generate_and_export(first_run=False)
            elif cmd == "s":
                self.show_path = not self.show_path
            elif cmd == "c":
                self.color_index = (self.color_index + 1) % len(COLORS)

        print("\033[0mGoodbye!")
