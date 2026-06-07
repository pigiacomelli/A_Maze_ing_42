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
* `r` : Regenerate a new maze
* `s` : Show/hide the shortest path solution
* `c` : Cycle through wall colors
* `q` : Quit the application



## Configuration format

The application uses a configuration file (e.g., `config.txt`) containing key-value pairs (`KEY=VALUE`).

### Required Keys:

* `WIDTH`: Maze width in cells. (e.g., `WIDTH=20`)
* `HEIGHT`: Maze height in cells. (e.g., `HEIGHT=15`)
* `ENTRY`: Start coordinates. (e.g., `ENTRY=0,0`)
* `EXIT`: End coordinates. (e.g., `EXIT=19,14`)
* `OUTPUT_FILE`: Hexadecimal export filename. (e.g., `OUTPUT_FILE=maze.txt`)
* `PERFECT`: Boolean indicating if the maze should be perfect (no loops) or imperfect. (e.g., `PERFECT=True`)

### Optional Keys:

* `SEED`: An integer seed for reproducible generation. (e.g., `SEED=42`)
* `ALGORITHM`: Maze generation algorithm. Accepted values are `dfs` and `prim`.
  If omitted, the application uses `dfs`. (e.g., `ALGORITHM=prim`)

## Algorithm

### Explanation

The default generation algorithm relies on an **Iterative Backtracking Depth-First Search (DFS)**.
Starting from a valid initial cell, the algorithm explores the grid by randomly selecting an unvisited neighboring cell, removing the wall between them, and pushing the new cell onto a stack. When it reaches a dead-end (a cell with no unvisited neighbors), it backtracks by popping cells from the stack until it finds a cell with unvisited neighbors.
For imperfect mazes, the algorithm subsequently identifies dead-ends and randomly removes walls to create loops, ensuring no 3x3 open areas are formed.

The bonus generator uses **Randomized Prim**. It starts from one cell, keeps a randomized frontier of neighboring cells, and repeatedly connects one unvisited frontier cell back into the growing maze. Like DFS, it creates a perfect maze by default and respects the protected "42" pattern cells.

### Justification

The DFS algorithm was selected because it naturally produces mazes with long, winding corridors and deep dead-ends, which significantly increases the complexity and visual appeal of the maze. We opted specifically for an **iterative** implementation using a stack rather than a recursive one. This design choice guarantees system stability and prevents the `RecursionError` that occurs in Python when generating very large mazes.

Use `dfs` when you want longer corridors and a classic backtracking maze feel. Use `prim` when you want a more evenly branched maze with shorter local passages.

## Advanced Features / Bonuses

* Multiple generation algorithms: Iterative DFS and Randomized Prim.
* Animation during maze rendering.
* Pac-Man shortest path animation.
* Regenerate maze from the interactive UI.
* Toggle shortest path display.
* Wall color cycling.

## Team & Project Management

### Roles

* **ando-sou (Antonin)**: Architecture design, core algorithmic implementation (DFS generator, BFS solver), pathfinding logic, and Python packaging (`mazegen` reusable module).
* **pgiacome (Pietro)**: Configuration parsing, strict validation logic (structural integrity of the maze), interactive terminal UI rendering, and Hexadecimal exporter.

### Planning & Evolution

We initially planned a strictly linear progression: parsing -> data structures -> generation -> solving -> UI.
However, we quickly realized that developing the UI earlier helped visualize bugs in the generation process. The plan evolved into an iterative cycle where the visual rendering was used as an active debugging tool alongside the algorithmic development.

### Retrospective

* **What worked well**: Our clear separation of concerns (Core Logic vs. I/O & Validation) minimized merge conflicts. Integrating `mypy` and `flake8` from day one kept the codebase robust and reliable.
* **What could be improved**: The initial time estimation for the Python packaging aspect (creating the standalone `mazegen` module) was too short.

### Tools Used

* **Version Control**: Git & GitHub.
* **Code Quality**: `flake8`, `mypy`, `pytest`.
* **Communication & Management**: Live coding sessions and asynchronous reviews.

## Code Reusability (mazegen package)

This project has been designed with modularity in mind. The core generator has been encapsulated into an installable Python package called `mazegen-*`.

You can easily reuse this package in future projects by building it via standard python packaging tools or installing it locally using:

```bash
pip install .

```

**Usage Example:**

```python
from mazegen import MazeGenerator

# Initialize the reusable generator facade
generator = MazeGenerator(
    width=20,
    height=15,
    perfect=True,
    seed=42,
    algorithm="prim",
)

# Generate the maze structure
maze = generator.generate()

# Solve the maze and get the path string
path_str = generator.shortest_path((0, 0), (19, 14))
print(f"Shortest path: {path_str}")

```

## Resources

* Python 3.10 Official Documentation: https://docs.python.org/3/
* Flake8 Linter Documentation: https://flake8.pycqa.org/
* Mypy Static Type Checker: https://mypy.readthedocs.io/
* Pytest Framework: https://docs.pytest.org/
* Maze Generation Algorithms: https://en.wikipedia.org/wiki/Maze_generation_algorithm
* **AI Usage**: Artificial Intelligence (LLMs) was strictly used to assist with writing and standardizing docstrings (PEP 257) and inline comments. AI helped ensure the documentation was clean and compliant without writing the core algorithmic logic or making architectural decisions.
