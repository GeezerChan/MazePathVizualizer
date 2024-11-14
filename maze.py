import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20  # Grid size
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")

# Clock for controlling frame rate
clock = pygame.time.Clock()

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}

    def draw(self, screen):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        # Draw the cell's walls
        if self.walls["top"]:
            pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y), 2)
        if self.walls["right"]:
            pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls["bottom"]:
            pygame.draw.line(screen, WHITE, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE), 2)
        if self.walls["left"]:
            pygame.draw.line(screen, WHITE, (x, y), (x, y + CELL_SIZE), 2)

# Create grid of cells
grid = [[Cell(row, col) for col in range(COLS)] for row in range(ROWS)]

def get_neighbors(cell):
    neighbors = []
    row, col = cell.row, cell.col

    # Check each direction and add neighboring cells if they're within bounds and unvisited
    if row > 0 and not grid[row - 1][col].visited:  # Up
        neighbors.append(("top", grid[row - 1][col]))
    if row < ROWS - 1 and not grid[row + 1][col].visited:  # Down
        neighbors.append(("bottom", grid[row + 1][col]))
    if col > 0 and not grid[row][col - 1].visited:  # Left
        neighbors.append(("left", grid[row][col - 1]))
    if col < COLS - 1 and not grid[row][col + 1].visited:  # Right
        neighbors.append(("right", grid[row][col + 1]))

    return neighbors

def remove_wall(current, next_cell, direction):
    # Remove walls between current and next cell
    if direction == "top":
        current.walls["top"] = False
        next_cell.walls["bottom"] = False
    elif direction == "bottom":
        current.walls["bottom"] = False
        next_cell.walls["top"] = False
    elif direction == "left":
        current.walls["left"] = False
        next_cell.walls["right"] = False
    elif direction == "right":
        current.walls["right"] = False
        next_cell.walls["left"] = False

# Maze generation
def generate_maze():
    stack = []
    current = grid[0][0]
    current.visited = True

    while True:
        neighbors = get_neighbors(current)
        if neighbors:
            direction, next_cell = random.choice(neighbors)
            next_cell.visited = True
            stack.append(current)
            remove_wall(current, next_cell, direction)
            current = next_cell
        elif stack:
            current = stack.pop()
        else:
            break

def draw_grid():
    screen.fill(BLACK)
    for row in grid:
        for cell in row:
            cell.draw(screen)
    pygame.display.flip()

# Generate the maze
generate_maze()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_grid()
    clock.tick(30)  # Control the frame rate

pygame.quit()
