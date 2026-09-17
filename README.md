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
| ANIMATIONS   | Play animations? (True\|False).                        | ANIMATIONS=False     |
| ALGORITHM    | Generation algorithm (DFS\|Kruskal\|HuntAndKill\|Prim) | ALGORITHM=DFS        |

## **Maze Generation Algorithms**

### **The Chosen Algorithms**

While a standard implementation requires only one algorithm, this project features an **Advanced Display & Strategy Option** via the optional ALGORITHM config key. We implemented four distinct strategies:

* **Kruskal's Algorithm:** Uses a disjoint-set (UnionFind) data structure to organically merge a forest of disconnected paths.  
* **Hunt-and-Kill:** Alternates between a random walk and a linear scan, optimizing the scan by traversing a flattened 1D list of cells.  
* **Prim's Algorithm (Default):** Grows a single minimum spanning tree outward from a starting node.  
* **Depth-First Search (DFS):** Recursively carves long, winding corridors.

### **Why We Chose Them**

We selected **Prim's Algorithm** as the primary/default strategy because it natively prevents disjoint islands, operating strictly on a frontier of active cells. By using a priority queue (min-heap) with randomized edge weights, it produces highly unpredictable, branching mazes that look organic. The addition of the other three algorithms was chosen to compare generation efficiency and visual styles, providing maximum flexibility.

## **Reusable Code**

The architecture was built with high cohesion and strict Object-Oriented Principles, making several components highly reusable:

* **The Grid and Cell classes:** These handle standard 2D spatial awareness, bitwise wall management, and neighbor lookups. They can be reused for any grid-based game, pathfinding visualizer, or board state tracker.  
* **The Solver class:** By leveraging hashable objects and flat dict\[Cell, Cell\] mappings instead of rigid 2D arrays, the BFS solver is completely decoupled from the generation logic. It can be dropped into any project that implements a compatible node graph to find the shortest path in $O(1)$ lookup time.

## **Team and Project Management**

### **Roles**

* **dode-lim:** Focused on the core generation algorithms (DFS, Kruskal's), configuration parsing with regex, and implementing the 42 pattern matrix reservation.  
* **lbalderr:** Focused on the advanced pathfinding (Solver class), bitwise wall manipulation, Prim's/Hunt-and-Kill algorithms, and the localized geometric sliding windows (3x3 open area prevention).

### **Planning & Evolution**

Our anticipated plan was to sequentially build the grid, apply an MST algorithm, and then write a simple solver. However, the plan evolved significantly when we hit performance bottlenecks and strict edge cases. Originally, we used nested 2D matrices for path tracking, but this became cumbersome. We pivoted mid-project to refactor our Cell objects to be natively hashable, allowing us to map paths in flat dictionaries, which drastically accelerated our BFS and Prim's implementations.

### **What Worked Well vs. What Could Be Improved**

* **Worked well:** Abstracting the algorithms behind a MazeAlgorithm protocol interface allowed us to swap and test different generation strategies without breaking the main MazeGenerator.  
* **To improve:** Early on, managing the geometric checks for loop creation caused a few recursive headaches. A more robust unit-testing suite during the initial phase would have caught the 3x3 open-area edge cases much sooner.

### **Tools Used**

* **Environment:** macOS with Visual Studio Code (utilizing custom keybindings and unified terminals).  
* **Version Control:** Git and GitHub for branch management and collaborative pair programming.  
* **Quality Assurance:** mypy for enforcing static typing, and flake8 (with flake8-docstrings) to guarantee strict PEP 8 formatting and compliant docstrings across the entire codebase.

## **Resources**

### **References**

* [Wikipedia: Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm?utm_source=gemini)  
* *Mazes for Programmers* by Jamis Buck (Concept references for Hunt-and-Kill and Kruskal's disjoint sets).  
* Python Official Documentation (collections.deque, heapq, re, dataclasses).

### **AI Usage**

Artificial Intelligence was utilized primarily as an architectural review and refactoring assistant throughout the project:

* **Memory Optimization:** Used AI to help refactor nested 2D array lookups in the BFS and Prim's solver into flat, hashable dictionaries, reducing memory footprint and improving readability.  
* **Geometric Validations:** Assisted in mapping out the exact bounding-box arithmetic required for the sliding-window validation to prevent $3 \\times 3$ open areas.  
* **Linting & Style:** Leveraged for formatting docstrings to perfectly comply with flake8-docstrings rules.

## Resources
* [Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
* [The Buckblog](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
* [Profeesor Elle](https://professor-l.github.io/mazes/)
