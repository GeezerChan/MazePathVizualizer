# MazePathVizualizer

CPSC481 Project

A Python-based maze visualizer and solver that implements three different pathfinding algorithms: A\* Search, Breadth-First Search (BFS), and Iterative Deepening Search (IDS). The visualizer allows you to generate mazes and see how each algorithm navigates the maze in real-time.

### Features

A\* Search: Uses a heuristic (Manhattan distance) for fast and efficient pathfinding.
BFS: Explores all possible paths to guarantee the shortest path.
IDS: Combines the depth-first search approach with iterative deepening for pathfinding in deep mazes.
Real-time Visualization: Shows how each algorithm explores the maze step by step.

### Requirements

Python 3.x
Pygame (for visualization)

### Installation

1. **Clone the Repository**

   Clone this repository to your local machine using:

   ```bash
   https://github.com/GeezerChan/MazePathVizualizer.git
   ```

2. **Install Pygame(if needed)**

``` pip install -r requirements.txt ```
OR
``` pip install pygame ```

Alterate way to install if you have different version of python

``` py -m pip install pygame ```

3. **Run maze.py**

``` python3 maze.py ```
OR
``` python maze.py ```
