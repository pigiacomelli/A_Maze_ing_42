*This project has been created as part of the 42 curriculum by ando-sou, pgiacome.*

# A-Maze-ing

## Description
A-Maze-ing is a Python project designed to generate, solve, and display random mazes. It strictly follows the constraints of the 42 curriculum (v2.1). The generator creates perfect or imperfect mazes, validates their structural integrity, visually renders them in an interactive ASCII terminal UI, and exports them in hexadecimal format. It features the mandatory "42" pattern Easter egg smoothly embedded in the generated mazes.

## Instructions
Ensure you are running **Python 3.10+**.

1. Install required dependencies:
   ```bash
   make install
   ```

2. Run the application with your configuration file:
   ```bash
   python3 a_maze_ing.py config.txt
   ```
   Or via the Makefile:
   ```bash
   make run
   ```

3. Inside the interactive UI, you can use the following commands:
   - `r` : Regenerate a new maze
   - `s` : Show/hide the shortest path solution
   - `c` : Cycle through wall colors
   - `q` : Quit the application

## Configuration format
The application uses a configuration file (e.g., `config.txt`) containing key-value pairs (`KEY=VALUE`).

### Required Keys:
- `WIDTH`: Maze width in cells. (e.g., `WIDTH=20`)
- `HEIGHT`: Maze height in cells. (e.g., `HEIGHT=15`)
- `ENTRY`: Start coordinates. (e.g., `ENTRY=0,0`)
- `EXIT`: End coordinates. (e.g., `EXIT=19,14`)
- `OUTPUT_FILE`: Hexadecimal export filename. (e.g., `OUTPUT_FILE=maze.txt`)
- `PERFECT`: Boolean indicating if the maze should be perfect (no loops) or imperfect. (e.g., `PERFECT=True`)

### Optional Keys:
- `SEED`: An integer seed for reproducible generation. (e.g., `SEED=42`)

## Code Reusability (mazegen package)
This project has been designed with modularity in mind. The core generator has been encapsulated into an installable Python package called `mazegen-*`.

You can easily reuse this package in future projects by building it via standard python packaging tools (e.g., `python -m build`) or installing it locally using:
```bash
pip install .
```

**Usage Example:**
```python
from mazegen import MazeGenerator

# Initialize the reusable generator facade
generator = MazeGenerator(width=20, height=15, perfect=True, seed=42)

# Generate the maze structure
maze = generator.generate()

# Solve the maze and get the path string
path_str = generator.shortest_path((0, 0), (19, 14))
print(f"Shortest path: {path_str}")
```

## Resources
- Python 3.10 Official Documentation: https://docs.python.org/3/
- Flake8 Linter Documentation: https://flake8.pycqa.org/
- Mypy Static Type Checker: https://mypy.readthedocs.io/
- Pytest Framework: https://docs.pytest.org/
- Maze Generation Algorithms: https://en.wikipedia.org/wiki/Maze_generation_algorithm
