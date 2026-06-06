import os
import time
from config.models import Config
from exporter.hex_exporter import HexExporter
from generator.dfs_generator import DFSGenerator
from maze.maze import Maze
from maze.validator import MazeValidator, ValidatorError
from solver.bfs_solver import BFSSolver
from maze.directions import Direction

COLORS = [
    "\033[0m",
    "\033[94m",  # Light Blue (Default)
    "\033[95m",  # Magenta
    "\033[96m",  # Cyan
    "\033[97m",  # White
]


class TerminalUI:
    """
    Interactive Terminal UI for the Maze Generator with Retro Arcade Animations.
    """

    def __init__(self, config: Config) -> None:
        self.config = config
        self.show_path = False
        self.color_index = 1

        self.maze = Maze(config.width, config.height)
        self.path: list[Direction] = []
        self.path_string: str = ""

        # Generate the maze and perform the initial render with reveal animation
        self._generate_and_export(first_run=True)

    def _clear_terminal(self) -> None:
        """
        Clear the terminal screen completely.
        """
        os.system("clear")

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
            validator = MazeValidator(
                self.maze,
                perfect=self.config.perfect,
                entry=self.config.entry,
                exit_=self.config.exit
            )
            validator.validate()
        except ValidatorError as e:
            print(f"\n\033[91m[Validator Warning] {e}\033[0m")

        exporter = HexExporter(self.maze)
        try:
            exporter.export(
                output_file=self.config.output_file,
                entry=self.config.entry,
                exit_=self.config.exit,
                shortest_path=self.path_string,
            )
        except OSError as e:
            if first_run:
                import sys
                print(f"Export failed: {e}")
                sys.exit(1)
            else:
                print(f"\n\033[91m[Export Warning] {e}\033[0m")

    def build_base_display(self) -> list[list[str]]:
        """
        Builds the base grid layout matrix of the maze.
        """
        width = self.maze.width
        height = self.maze.height
        grid_w = width * 2 + 1
        grid_h = height * 2 + 1

        display = [[" "] * grid_w for _ in range(grid_h)]

        for y in range(height):
            for x in range(width):
                cell = self.maze.get_cell(x, y)
                cx = x * 2 + 1
                cy = y * 2 + 1

                display[cy - 1][cx - 1] = "█"
                display[cy - 1][cx + 1] = "█"
                display[cy + 1][cx - 1] = "█"
                display[cy + 1][cx + 1] = "█"

                if cell.has_wall(Direction.NORTH):
                    display[cy - 1][cx] = "█"
                if cell.has_wall(Direction.SOUTH):
                    display[cy + 1][cx] = "█"
                if cell.has_wall(Direction.WEST):
                    display[cy][cx - 1] = "█"
                if cell.has_wall(Direction.EAST):
                    display[cy][cx + 1] = "█"

                if cell.is_pattern:
                    display[cy][cx] = "█"

        return display

    def render(self, animate_reveal: bool = False) -> None:
        """
        Render the maze to the terminal, optionally row-by-row.
        """
        # Hide the cursor during rendering for a clean animation
        print("\033[?25l", end="")

        # Clear terminal completely
        self._clear_terminal()

        width = self.maze.width
        height = self.maze.height
        display = self.build_base_display()

        # Add static path if enabled
        if self.show_path and self.path:
            curr_x, curr_y = self.config.entry
            # Mark the starting cell
            display[curr_y * 2 + 1][curr_x * 2 + 1] = "."

            for d in self.path:
                if d == Direction.NORTH:
                    display[curr_y * 2][curr_x * 2 + 1] = "."
                    curr_y -= 1
                elif d == Direction.SOUTH:
                    display[curr_y * 2 + 2][curr_x * 2 + 1] = "."
                    curr_y += 1
                elif d == Direction.EAST:
                    display[curr_y * 2 + 1][curr_x * 2 + 2] = "."
                    curr_x += 1
                elif d == Direction.WEST:
                    display[curr_y * 2 + 1][curr_x * 2] = "."
                    curr_x -= 1
                display[curr_y * 2 + 1][curr_x * 2 + 1] = "."

        # Define entry and exit on the grid
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
                    line += f"\033[93m··{reset}"  # Yellow dots
                elif char == "S":
                    line += f"\033[92mSS{reset}"
                elif char == "E":
                    line += f"\033[91mEE{reset}"
                else:
                    line += "  "

            print(line)
            if animate_reveal:
                time.sleep(0.02)  # Delay of 20ms per row for a fluid visual reveal

        print("\nCommands:")
        print("  [r] Regenerate maze")
        print("  [s] Toggle/Animate shortest path")
        print("  [c] Change wall color")
        print("  [q] Quit\n")

        # Show cursor again after rendering
        print("\033[?25h", end="", flush=True)

    def get_path_display_coords(self) -> list[tuple[int, int]]:
        """
        Calculate all display coordinates (y, x) along the shortest path.
        """
        if not self.path:
            return []

        curr_x, curr_y = self.config.entry
        coords = [(curr_y * 2 + 1, curr_x * 2 + 1)]

        for d in self.path:
            if d == Direction.NORTH:
                coords.append((curr_y * 2, curr_x * 2 + 1))
                curr_y -= 1
            elif d == Direction.SOUTH:
                coords.append((curr_y * 2 + 2, curr_x * 2 + 1))
                curr_y += 1
            elif d == Direction.EAST:
                coords.append((curr_y * 2 + 1, curr_x * 2 + 2))
                curr_x += 1
            elif d == Direction.WEST:
                coords.append((curr_y * 2 + 1, curr_x * 2))
                curr_x -= 1
            coords.append((curr_y * 2 + 1, curr_x * 2 + 1))

        return coords

    def animate_pacman_run(self) -> None:
        """
        Runs the premium Pac-Man path-eating and blinking ghost animation.
        """
        if not self.path:
            return

        coords = self.get_path_display_coords()
        if not coords:
            return

        # Hide cursor during animation
        print("\033[?25l", end="")

        width = self.maze.width
        height = self.maze.height
        color = COLORS[self.color_index]
        reset = COLORS[0]

        # Step-by-step animation of Pac-Man traversing the dots
        for i in range(len(coords)):
            # Clear screen completely
            self._clear_terminal()

            # Get clean base layout of the maze
            display = self.build_base_display()

            # Draw dots that have NOT been eaten yet (from index i+1 onwards)
            for j in range(i + 1, len(coords) - 1):
                py, px = coords[j]
                display[py][px] = "."

            # Draw the path eaten by Pac-Man (positions before index i remain empty)
            for j in range(0, i):
                py, px = coords[j]
                display[py][px] = " "

            # Place Pac-Man at current position 'i'
            pac_y, pac_x = coords[i]
            # Determine which character to use based on the frame (open/closed mouth)
            pacman_char = "ᗧ" if i % 2 == 0 else "•"
            display[pac_y][pac_x] = "PAC"

            # Draw the Ghost at exit 'E' (final coordinate)
            ghost_y, ghost_x = coords[-1]
            display[ghost_y][ghost_x] = "GHOST"

            # Keep entry 'S' visible
            sy, sx = coords[0]
            if i > 0:
                display[sy][sx] = "S"

            # Print this frame
            print(f"Arcade Run ({width}x{height}) - Pacman is eating dots! 🎮\n")
            for row in display:
                line = ""
                for char in row:
                    if char == "█":
                        line += f"{color}██{reset}"
                    elif char == ".":
                        line += f"\033[93m··{reset}"  # Yellow dots
                    elif char == "PAC":
                        # Yellow Pac-Man representation
                        line += (
                            f"\033[93m{pacman_char}{pacman_char}{reset}"
                        )
                    elif char == "GHOST":
                        line += f"\033[91mᗣᗣ{reset}"  # Red Ghost (Blinky!)
                    elif char == "S":
                        line += f"\033[92mSS{reset}"
                    else:
                        line += "  "
                print(line)

            print("\nEating dot... chomp chomp! 🍬")
            time.sleep(0.08)  # Control movement speed (80ms per step)

        # ---- FINAL PHASE: GHOST MEETS PAC-MAN AND BLINKS ----
        # Blink Pac-Man and Ghost at the exit 4 times (8 transitions)
        for blink in range(8):
            self._clear_terminal()
            display = self.build_base_display()

            # Pacman and Ghost are at the exit
            pac_y, pac_x = coords[-1]

            # Toggle visibility to create blinking effect
            is_visible = (blink % 2 == 0)
            if is_visible:
                # Pac-Man and Ghost representation
                # on exit cell (left/right respectively)
                display[pac_y][pac_x] = "WIN"
            else:
                display[pac_y][pac_x] = " "

            # Print this frame
            print(f"Arcade Run ({width}x{height}) - SUCCESS! 🏆\n")
            for row in display:
                line = ""
                for char in row:
                    if char == "█":
                        line += f"{color}██{reset}"
                    elif char == "WIN":
                        # Yellow Pac-Man and red/blue blinking Ghost
                        line += f"\033[93mᗧ\033[91mᗣ{reset}"
                    else:
                        line += "  "
                print(line)

            print("\n💥 LEVEL CLEARED! 💥")
            time.sleep(0.25)  # Blinking interval (250ms)

        # Show cursor and return to normal control flow
        print("\033[?25h", end="", flush=True)

    def run(self) -> None:
        """
        Start the interactive loop.
        """
        # First render with top-to-bottom reveal animation!
        self.render(animate_reveal=True)

        while True:
            try:
                cmd = input("Command > ").strip().lower()
            except (KeyboardInterrupt, EOFError):
                break

            if cmd == "q":
                break
            elif cmd == "r":
                self._generate_and_export(first_run=False)
                self.render(animate_reveal=True)  # Animate on regeneration
            elif cmd == "s":
                self.show_path = not self.show_path
                if self.show_path:
                    self.animate_pacman_run()  # Run animation when enabled
                self.render(animate_reveal=False)
            elif cmd == "c":
                self.color_index = (self.color_index + 1) % len(COLORS)
                self.render(animate_reveal=False)

        print("\033[0mGoodbye!")
