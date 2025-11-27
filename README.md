
# Traveling Salesman Problem – Interactive Python Visualizer

An interactive Python application that visualizes and solves the Traveling Salesman Problem (TSP).  
You can add, remove, and modify cities directly on a canvas and compute an efficient tour using heuristic algorithms.

Built with **Python** and **Tkinter**. No external dependencies required.

----------

##  Features

-   **Interactive UI**
    
    -   Left-click to add cities
        
    -   Right-click to remove cities
        
-   **TSP Solver**
    
    -   Nearest Neighbor heuristic
        
    -   2-Opt optimization
        
-   **Live Visualization**
    
    -   Routes drawn directly on the canvas
        
    -   Total route distance displayed
        
-   **Simple Controls**
    
    -   Solve TSP with one click
        
    -   Clear all cities instantly
        
-   **Single-file project** – easy to run and modify
    

----------

## Getting Started

### Prerequisites

-   Python 3.8 or newer
    
-   Tkinter (included with standard Python installations)
    

### Installation

Clone the repository:

git clone https://github.com/yourusername/tsp-visualizer.git  
cd tsp-visualizer

Run the application:
python tsp_ui.py

----------

## Algorithm Details

This project uses a heuristic approach optimized for interactivity and speed.

1.  **Nearest Neighbor**  
    Creates an initial tour by always visiting the closest unvisited city.
    
2.  **2-Opt Optimization**  
    Improves the route by iteratively swapping edges to reduce total distance.
    
3.  **Multiple Starts**  
    The solver tries multiple starting cities and keeps the best result.
    

This is not an exact solver, but it produces good solutions quickly and works well for visualization.

----------

## Project Structure

.  
├── tsp_ui.py  
└── README.md

----------

## Possible Extensions

-   Drag-and-drop city movement
    
-   Save and load city configurations
    
-   Exact solvers for small datasets (Brute Force, Held–Karp)
    
-   Simulated Annealing or Genetic Algorithms
    
-   Animated solving steps
    
-   Dark mode UI
    

----------

## License

MIT License

You are free to use, modify, and distribute this project.

----------

## Acknowledgements

-   Traveling Salesman Problem – classic optimization problem
-   Tkinter for lightweight GUI support
    

Happy optimizing.
