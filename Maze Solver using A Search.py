import heapq
import math

# Define the maze as a 2D list: 0 = open, 1 = wall, 'S' = start, 'G' = goal
maze = [
    ['S', 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 'G']
]

# Directions: up, down, left, right
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def heuristic(a, b, type='manhattan'):
    """Calculate heuristic distance between two points."""
    if type == 'manhattan':
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    elif type == 'euclidean':
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    else:
        raise ValueError("Invalid heuristic type. Choose 'manhattan' or 'euclidean'.")

def a_star_search(maze, start, goal, heuristic_type='manhattan'):
    """Perform A* search on the maze."""
    rows, cols = len(maze), len(maze[0])
    
    # Priority queue: (f_score, counter, node)
    open_set = []
    heapq.heappush(open_set, (0, 0, start))
    
    # Came from: to reconstruct path
    came_from = {}
    
    # g_score: cost from start to node
    g_score = {start: 0}
    
    # f_score: g_score + heuristic
    f_score = {start: heuristic(start, goal, heuristic_type)}
    
    # Closed set
    closed_set = set()
    
    counter = 0  # Tie-breaker for priority queue
    
    while open_set:
        current_f, _, current = heapq.heappop(open_set)
        
        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path
        
        closed_set.add(current)
        
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] != 1:
                if neighbor in closed_set:
                    continue
                
                tentative_g = g_score[current] + 1  # Assuming uniform cost
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal, heuristic_type)
                    counter += 1
                    heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))
    
    return None  # No path found

def visualize_maze(maze, path=None):
    """Visualize the maze in console, marking the path if provided."""
    maze_copy = [row[:] for row in maze]  # Copy to avoid modifying original
    
    if path:
        for x, y in path[1:-1]:  # Mark path except start and goal
            maze_copy[x][y] = '*'
    
    for row in maze_copy:
        print(' '.join(str(cell) for cell in row))

# Find start and goal positions
start = None
goal = None
for i in range(len(maze)):
    for j in range(len(maze[0])):
        if maze[i][j] == 'S':
            start = (i, j)
        elif maze[i][j] == 'G':
            goal = (i, j)

if start is None or goal is None:
    print("Start or goal not found in maze.")
else:
    print("Original Maze:")
    visualize_maze(maze)
    
    path = a_star_search(maze, start, goal, heuristic_type='manhattan')
    
    if path:
        print("\nShortest Path Found:")
        visualize_maze(maze, path)
        print(f"Path: {path}")
    else:
        print("\nNo path found. Goal is unreachable.")