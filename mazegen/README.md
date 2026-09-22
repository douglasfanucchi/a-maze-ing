# MazeGenerator

## Description
This is the class responsible for generating a maze.

To generate a maze, a `Width` and `Height` must be provided, these are the number of cells inthe horizontal and vertical directions, respectively. Internally, a `Grid` object will store `Cell` objects which represent each position of the maze.

Two coordinates (x: int > 0, y: int > 0) must be provided as well, representing the entry position and the exit position.

A few algorithms are present in this package. Depth-first search (DFS), Kruskal, Hunt-and-Kill and Prim. Each of them implement an adaptation of its original version in order to generate a random maze.

You also must specify whether you want a perfect or non-perfect maze. A perfect maze means that there is no *loops* inside the maze, whereas the non-perfect maze has *loops*.

In this package, a loop is a sequence of at least four Cell objects that begins and ends on the exact same cell, with all intermediate cells being unique. Practically, this means you can depart from an initial position and eventually return to it without reversing direction or retracing your steps.

Finally, a *seed* may be specified to reproduce the same exact maze every time.

## Documentation

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


## Example
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

## Encoding cells
It was mentioned that `export` method returns a string with hexadecimal digits that encodes wall information of a given cell.

A cell can have a `NORTH`, `EAST`, `SOUTH` and `WEST` wall. Each of this values are represented by a bit.

`NORTH` is represent by `0b0001` (1), `EAST` is represented by `0b0010` (2), `SOUTH` by `0b0100` (4) and `WEST` by `0b1000` (8).

If a cell has, for example, `NORTH` and `SOUTH` walls, then the number that encodes information about wall of this cell is `0b0001 + 0b0100 = 0b0101` (5), so 5 tells us that a given cell has `NORTH` and `SOUTH` walls.


If another cell has the number `f` as wall encoding, we can check its binary representation, which is `0b1111` that is equivalent to `0b1000 + 0b0100 + 0b0010 + 0b0001` = `WEST + SOUTH + EAST + NORTH`. In other words, it has walls in every direction.
