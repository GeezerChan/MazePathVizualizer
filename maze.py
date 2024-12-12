import pygame
import random
import heapq
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20  # Grid size
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # A* Path
GREEN = (0, 255, 0)  # Start
RED = (255, 0, 0)  # End
YELLOW = (255, 255, 0)  # A* Explored
ORANGE = (255, 165, 0)  # IDS Path
PINK = (255, 105, 180)  # BFS Path
PURPLE = (128, 0, 128)  # Overlap of A*, IDS, BFS

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver: A*, IDS, BFS")

clock = pygame.time.Clock()

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    def draw(self, screen, color=None):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        if color:
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

        if self.walls["top"]:
            pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls["right"]:
            pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls["bottom"]:
            pygame.draw.line(screen, WHITE, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls["left"]:
            pygame.draw.line(screen, WHITE, (x, y), (x, y + CELL_SIZE), 2)

    def __lt__(self, other):
        return (self.row, self.col) < (other.row, other.col)

# Create grid of cells
grid = [[Cell(row, col) for col in range(COLS)] for row in range(ROWS)]

def remove_wall(current, next_cell):
    dx = current.col - next_cell.col
    dy = current.row - next_cell.row
    if dx == 1:  # Left
        current.walls["left"] = False
        next_cell.walls["right"] = False
    elif dx == -1:  # Right
        current.walls["right"] = False
        next_cell.walls["left"] = False
    if dy == 1:  # Above
        current.walls["top"] = False
        next_cell.walls["bottom"] = False
    elif dy == -1:  # Below
        current.walls["bottom"] = False
        next_cell.walls["top"] = False

def generate_maze():
    stack = []
    current = grid[0][0]
    current.visited = True

    while True:
        neighbors = [cell for cell in get_neighbors_unvisited(current)]
        if neighbors:
            next_cell = random.choice(neighbors)
            remove_wall(current, next_cell)
            next_cell.visited = True
            stack.append(current)
            current = next_cell
            draw_grid()
            pygame.time.delay(15)
        elif stack:
            random.shuffle(stack)
            current = stack.pop()
            draw_grid()
        else:
            break
    create_extra_paths()

def create_extra_paths():
    for _ in range(30):  # Add 30 random openings
        row = random.randint(0, ROWS - 2)
        col = random.randint(0, COLS - 2)
        direction = random.choice(["right", "bottom"])
        if direction == "right" and col < COLS - 1:
            grid[row][col].walls["right"] = False
            grid[row][col + 1].walls["left"] = False
        elif direction == "bottom" and row < ROWS - 1:
            grid[row][col].walls["bottom"] = False
            grid[row + 1][col].walls["top"] = False

def get_neighbors_unvisited(cell):
    """
    Returns the list of unvisited neighboring cells for maze generation.
    """
    row, col = cell.row, cell.col
    neighbors = []
    if row > 0 and not grid[row - 1][col].visited:  # Check above
        neighbors.append(grid[row - 1][col])
    if row < ROWS - 1 and not grid[row + 1][col].visited:  # Check below
        neighbors.append(grid[row + 1][col])
    if col > 0 and not grid[row][col - 1].visited:  # Check left
        neighbors.append(grid[row][col - 1])
    if col < COLS - 1 and not grid[row][col + 1].visited:  # Check right
        neighbors.append(grid[row][col + 1])
    return neighbors

def bfs(start, end):
    queue = [(start, [start])]
    while queue:
        current, path = queue.pop(0)
        if current == end:
            return path
        for neighbor in get_neighbors(current):
            if neighbor not in path:
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
                neighbor.draw(screen, PINK)
                pygame.display.flip()
                pygame.time.delay(10)
    return None

def a_star(start, end):
    def heuristic(a, b):
        return abs(a.row - b.row) + abs(a.col - b.col)

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                neighbor.draw(screen, YELLOW)
                pygame.display.flip()
                pygame.time.delay(10)
    return None

def iterative_deepening(start, end):
    def dfs(depth, current, path):
        if depth == 0:
            return None
        if current == end:
            return path
        for neighbor in get_neighbors(current):
            if neighbor not in path:
                new_path = path + [neighbor]
                result = dfs(depth - 1, neighbor, new_path)
                if result:
                    return result
        return None

    depth = 1
    while True:
        path = dfs(depth, start, [start])
        if path:
            return path
        depth += 1

def get_neighbors(cell):
    neighbors = []
    row, col = cell.row, cell.col
    if row > 0 and not grid[row - 1][col].walls["bottom"]:
        neighbors.append(grid[row - 1][col])
    if row < ROWS - 1 and not grid[row + 1][col].walls["top"]:
        neighbors.append(grid[row + 1][col])
    if col > 0 and not grid[row][col - 1].walls["right"]:
        neighbors.append(grid[row][col - 1])
    if col < COLS - 1 and not grid[row][col + 1].walls["left"]:
        neighbors.append(grid[row][col + 1])
    return neighbors

def draw_grid(path_a_star=None, path_ids=None, path_bfs=None):
    screen.fill(BLACK)
    for row in grid:
        for cell in row:
            cell.draw(screen)
    if path_a_star:
        for cell in path_a_star:
            cell.draw(screen, BLUE)
    if path_ids:
        for cell in path_ids:
            if cell in path_a_star:
                cell.draw(screen, PURPLE)
            else:
                cell.draw(screen, ORANGE)
    if path_bfs:
        for cell in path_bfs:
            if cell in path_a_star or cell in path_ids:
                cell.draw(screen, PURPLE)
            else:
                cell.draw(screen, PINK)
    grid[0][0].draw(screen, GREEN)
    grid[ROWS - 1][COLS - 1].draw(screen, RED)
    pygame.display.flip()

generate_maze()

start = grid[0][0]
end = grid[ROWS - 1][COLS - 1]

# Measure A* Time
start_time = time.time()
path_a_star = a_star(start, end)
a_star_time = time.time() - start_time

# Measure IDS Time
start_time = time.time()
path_ids = iterative_deepening(start, end)
ids_time = time.time() - start_time

# Measure BFS Time
start_time = time.time()
path_bfs = bfs(start, end)
bfs_time = time.time() - start_time

# Print out times and color feedback in the terminal
print(f"A* Search Time (Blue): {a_star_time:.4f}s")
print(f"IDS Time (Orange): {ids_time:.4f}s")
print(f"BFS Time (Pink): {bfs_time:.4f}s")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_grid(path_a_star, path_ids, path_bfs)
    clock.tick(30)

pygame.quit()
