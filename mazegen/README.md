# MazeGenerator

## Description
This is the class responsible for generating a maze.

To generate a maze, a `Grid` object must be provided. This `Grid` object stores `Cell` objects, which represents each position of the maze.

Two coordinates must be provided as well, representing the entry position and the exit position.

A few algorithms are present into this package. Depth-first search (DFS), Kruskal, Hunt-and-Kill and Prim. Each of them implement an adaptation of its original version in order to generate a random maze.

You also must specify whether you want a perfect or non-perfect maze. A perfect maze means that there is no *loops* inside the maze, whereas the non-perfect maze has *loops*.

In this package, a *loop* is a sequence of at least four `Cell` where the first and the last `Cell` of this sequence are the same. To be a loop, every cell in this sequence must be different, except for the first and the last ones.

It means that for a given initial position, you can walk through the maze and get back to that initial given position (without moving backwards).

Finally, a *seed* may be specified to allow reproducible mazes.

## Documentation

Properties:

- `grid: list[list[Cell]]`: is a 2D matrix that holds `Cell`objects. Each `Cell` represents a position in the maze.
- `algorithm: MazeAlgorithm`: selected algorithm to generate the maze.
- `is_perfect: bool`: whether the maze is perfect or not.
- `entry: tuple[int, int]`: coordinates to the entry of the maze.
- `exit: tuple[int, int]`: coordinates to the exit of the maze.
- `shortest_path: str`: string that contains the cardinal coordinates to the shortest path from entry to exit.
- `shortest_path_cells: list[Cell]`: a list of the `Cell` representing the shortest path.

Methods:

- `generate() -> None`: it executes the selected algorithm to create the maze and save its shortest path
- `export() -> str`: it creates *height* lines where each line has *width* characters where each character represents the encoding of a given cell. Possible values for each character are hexadecimal digit that encodes information about walls in that particular cell. More details bellow. Besides those encodings, the second to last line is a tuple that refers to the entry coordinates. The last line is also a tuple but this one refers to the exit coordinates.


## Example
Creating a 50x50 perfect maze with `Prim`'s algorithm, using a seed with value 1 and checking for walls on the top-left cell:

```.py
from mazegen import MazeGenerator
from mazegen.grid import Grid
from mazegen.algorithms import Prim
from mazegen.direction import Direction

grid = Grid(50, 50)
entry = (0, 0)
exit = (49, 49)
generator = MazeGenerator(
    grid,
    entry,
    exit,
    Prim(),
    True,
    1
)
top_left = generator.grid.get_cell(0, 0)

if top_left is None:
    raise Exception("invalid cell position")

if top_left.has_wall(Direction.EAST):
    print("It has east wall!")
if top_left.has_wall(Direction.South):
    print("It has south wall!")
```

## Encoding cells
It was mentioned that `export` method returns a string with hexadecimal digits that encodes wall information of a given cell.

A cell can have a `NORTH`, `EAST`, `SOUTH` and `WEST` wall. Each of this values are represented by a bit.

`NORTH` is represent by `0b0001` (1), `EAST` is represented by `0b0010` (2), `SOUTH` by `0b0100` (4) and `WEST` by `0b1000` (8).

If a cell has, for example, `NORTH` and `SOUTH` walls, then the number that encodes information about wall of this cell is `0b0001 + 0b0100 = 0b0101` (5), so 5 tells us that a given cell has `NORTH` and `SOUTH` walls.


If another cell has the number `f` as wall encoding, we can check its binary representation, which is `0b1111` that is equivalent to `0b1000 + 0b0100 + 0b0010 + 0b0001` = `WEST + SOUTH + EAST + NORTH`. In other words, it has walls in every direction.
