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
* **The Maze Generator:** It is available as a standalone module that can be imported and used in other projects, such as a Pac-Man game that uses the mazes as a playable board for building the game levels. Check the [mazegen module documentation](#-mazegen-documentation) for more details.
* **The Solver class:** By leveraging hashable objects and flat dict\[Cell, Cell\] mappings instead of rigid 2D arrays, the BFS solver is completely decoupled from the generation logic. It can be dropped into any project that implements a compatible node graph to find the shortest path in linear time.

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
