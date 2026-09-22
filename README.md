*This project has been created as part of the 42 curriculum by dode-lim, lbalderr.*

# **A-Maze-ing: Maze Generator & Solver**

## **Description**

This project is a maze generation and solving application made in Python. The goal is to programmatically generate randomized mazes that adhere to specific rules (such as the 42 school reserved center pattern and Pac-Man board playability rules) and then efficiently find the shortest path from an entry to an exit point.  
The generator produces fully connected, loop-enabled mazes that avoid large $3\times3$ open areas while guaranteeing open corners. The solver utilizes graph traversal techniques (BFS) to navigate the generated grid and output the shortest path.

## **Instructions**

### **Prerequisites**

* Python 3.10 or higher with pip.

### **Installation & Execution**

1. **Clone the repository:**  
```Bash  
   git clone <repository-url> a_maze_ing
   cd a_maze_ing
```

2. **Set up a config file:** (You can just edit the existing config.txt file) 

	Read the [Configuration File Structure](#Configuration-File-Structure) section below for more details.


From here you can either:

3. **Run the program with make**
```Bash
make run
```

or 

3. **Set up a virtual environment and activate it:**  
```Bash  
   python3 -m venv a_maze_ing_venv
   source a_maze_ing_venv/bin/activate  # Linux/macOS
```

4. **Install dependencies:**
```Bash
pip install -r requirements.txt
```

5. **Run the application:** The program is executed through the main entry point, passing the configuration file as an argument
```Bash  
   python3 a_maze_ing.py config.txt
```

## **Configuration File Structure**

The application uses a custom, regex-validated configuration parser. The file uses simple KEY=value assignment pairs.

* **Format:** Keys must start with a letter/underscore. Values must not contain spaces or \= signs.  
* **Comments:** Inline comments starting with \# are supported.

Keys marked with * are mandatory


| Key          | Description                                            | Example              |
| :----------  | :----------------------------------------------------- | :------------------- |
| WIDTH*       | Maze width (number of cells)                           | WIDTH=20             |
| HEIGHT*      | Maze height (number of cells)                          | HEIGHT=15            |
| ENTRY*       | Entry coordinates (x,y)                                | ENTRY=0,0            |
| EXIT*        | Exit coordinates (x,y)                                 | EXIT=19,14           |
| OUTPUT_FILE* | Output filename                                        | OUTPUT_FILE=maze.txt |
| PERFECT*     | Is the maze perfect? (True\|False)                     | PERFECT=False        |
| SEED         | Seed for randomness reproducibility (int)              | SEED=42              |
| ALGORITHM    | Generation algorithm (DFS\|Kruskal\|HuntAndKill\|Prim) | ALGORITHM=DFS        |

## **Maze Generation Algorithms**

### **The Chosen Algorithms**

While a standard implementation requires only one algorithm, this project features a strategy selection via the optional ALGORITHM config key. We implemented four distinct strategies:

* **Depth-First Search (DFS):** The default algorithm. Recursively carves long, winding corridors.
* **Kruskal's Algorithm:** Uses a disjoint-set (UnionFind) data structure to organically merge a forest of disconnected paths.  
* **Prim's Algorithm:** Grows a single minimum spanning tree outward from a starting node.  
* **Hunt-and-Kill:** Alternates between a random walk and a linear scan, optimizing the scan by traversing a flattened 1D list of cells.  

### **Why We Chose Them**

We selected DFS as the default strategy for its simplicity and because it generates a perfect maze with the fewest dead-ends of all the selected algorithms, making it ideal for converting it to a playable maze. The other three algorithms were chosen mainly to explore topics of Data Structures such as priority queues and disjoint-sets.

## **Reusable Code**

The architecture was built with high cohesion and strict Object-Oriented Principles, making several components highly reusable:

* **The Grid and Cell classes:** These handle standard 2D spatial awareness, bitwise wall management, and neighbor lookups. They can be reused for any grid-based game, pathfinding visualizer, or board state tracker.
* **The Maze Generator:** It is available as a standalone module that can be imported and used in other projects, such as a Pac-Man game that uses the mazes as a playable board for building the game levels. Check the [mazegen module documentation](#-MazeGenerator) for more details.
* **The Solver class:** By leveraging hashable objects and flat dict\[Cell, Cell\] mappings instead of rigid 2D arrays, the BFS solver is completely decoupled from the generation logic. It can be dropped into any project that implements a compatible node graph to find the shortest path in linear time.

## MazeGenerator

### Description
This is the class responsible for generating a maze.

To generate a maze, a `Width` and `Height` must be provided, these are the number of cells inthe horizontal and vertical directions, respectively. Internally, a `Grid` object will store `Cell` objects which represent each position of the maze.

Two coordinates (x: int > 0, y: int > 0) must be provided as well, representing the entry position and the exit position.

A few algorithms are present in this package. Depth-first search (DFS), Kruskal, Hunt-and-Kill and Prim. Each of them implement an adaptation of its original version in order to generate a random maze.

You also must specify whether you want a perfect or non-perfect maze. A perfect maze means that there is no *loops* inside the maze, whereas the non-perfect maze has *loops*.

In this package, a loop is a sequence of at least four Cell objects that begins and ends on the exact same cell, with all intermediate cells being unique. Practically, this means you can depart from an initial position and eventually return to it without reversing direction or retracing your steps.

Finally, a *seed* may be specified to allow reproducible mazes.

### Documentation

Properties:

- `grid: list[list[Cell]]`: is a 2D matrix that holds `Cell`objects. Each `Cell` represents a position in the maze.
- `algorithm: MazeAlgorithm`: selected algorithm to generate the maze.
- `is_perfect: bool`: whether the maze is perfect or not.
- `entry: tuple[int, int]`: coordinates to the entry of the maze.
- `exit: tuple[int, int]`: coordinates to the exit of the maze.
- `shortest_path: str`: string that contains the cardinal directions for the shortest path from entry to exit.
- `shortest_path_cells: list[Cell]`: a list of `Cell` objects representing the shortest path.

Methods:

- `generate() -> None`: Executes the selected algorithm to create the maze and save its shortest path
- `export() -> str`: Return a string consisting of *height* lines where each line has *width* characters and each character represents the encoding of a given cell. Each character is a hexadecimal digit that encodes information about walls in that particular cell. More details bellow. Besides those encodings, the second to last line is a tuple representing the entry coordinates, while the last line is a tuple representing the exit coordinates.


### Example
Creating a 50x50 perfect maze with `Prim`'s algorithm, using a seed with value 1 and checking for walls on the top-left cell:

```python
from mazegen import MazeGenerator
from mazegen.direction import Direction

width = 50
height = 50
entry_coords = (0, 0)
exit_coords = (49, 49)
algorithm = "Prim"
seed_value = 1
is_perfect_maze = True

generator = MazeGenerator(
    width,
    height,
    entry_coords,
    exit_coords,
    algorithm,
    is_perfect_maze,
    seed_value
)

# Execute the algorithm
generator.generate()

# Access the generated structure
top_left = generator.grid.get_cell(0, 0)
if top_left is None:
    raise Exception("invalid cell position")

if top_left.has_wall(Direction.EAST):
    print("It has east wall!")
if top_left.has_wall(Direction.SOUTH):
    print("It has south wall!")

# Access the solution
print(f"Shortest path: {generator.shortest_path}")
```

### Encoding cells
It was mentioned that `export` method returns a string with hexadecimal digits that encodes wall information of a given cell.

A cell can have a `NORTH`, `EAST`, `SOUTH` and `WEST` wall. Each of this values are represented by a bit.

`NORTH` is represent by `0b0001` (1), `EAST` is represented by `0b0010` (2), `SOUTH` by `0b0100` (4) and `WEST` by `0b1000` (8).

If a cell has, for example, `NORTH` and `SOUTH` walls, then the number that encodes information about wall of this cell is `0b0001 + 0b0100 = 0b0101` (5), so 5 tells us that a given cell has `NORTH` and `SOUTH` walls.


If another cell has the number `f` as wall encoding, we can check its binary representation, which is `0b1111` that is equivalent to `0b1000 + 0b0100 + 0b0010 + 0b0001` = `WEST + SOUTH + EAST + NORTH`. In other words, it has walls in every direction.

## **Team and Project Management**

### **Roles**

* **dode-lim:** Focused on  configuration parsing with regex, building the solver Class and architecturing the graphical features of the project.  
* **lbalderr:** Focused on researching the core generation algorithms, creating core data structures (Cell, Grid) maintaining the project architecture and OOP best practices, and validating maze constraints. 

### **Planning & Evolution**

Our initial plan was to sequentially build the grid, implement generation algorithms, write a simple solver, and then generate a visualization for the mazes. However, we decided to refactor our core structures and algorithms along the way to improve the performance and maintainability of our codebase, this ended up costing us a couple extra days but the implementation sequence and task division was well preserved.

### **What Worked Well vs. What Could Be Improved**

* **Worked well:** Abstracting the algorithms behind a MazeAlgorithm protocol interface, and more generally keeping separation of concerns, allowed us to work on separate algorithms and files, speeding up development while minimizing merge conflicts.
* **To improve:** A more detailed research and planning of the architecture early on could have avoided some refactors down the line.

### **Tools Used**

* **Tasks & Team Management:** We used a shared Google Docs for tasks planning and frequent communication through slack when one of us couldn't be physically present at the 42 campus.  
* **Version Control:** Git and GitHub for branch management and collaborative pair programming.  
* **Quality Assurance:** pytest for unit tests, along with mypy and flake8 (with flake8-docstrings) for linting and type-checking.

## **Resources**

* [Wikipedia: Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm?utm_source=gemini) 
* [Maze Generation Algorithms - An Exploration](https://professor-l.github.io/mazes/) 
* [Maze Generation: Algorithm Recap](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap) 
* *Mazes for Programmers* by Jamis Buck (Concept references for Hunt-and-Kill and Kruskal's disjoint sets). 
* Python Official Documentation (collections.deque, heapq, dataclasses).

## **AI Usage**

Artificial Intelligence (AI) was used primarily as an architectural review and refactoring assistant throughout the project for things like:

* **Memory Optimization:** AI was used to help refactor nested 2D array lookups in the BFS solver and generation algorithms into flat dictionaries by making the Cell class hashable, reducing memory footprint and improving readability.  
* **Geometric Validations:** Assisted in finding counter-examples and validation to prevent $3\times3$ open areas.  
* **Refactoring & Documentation:** Helped suggesting refactors for improving readability and generating docstrings.
