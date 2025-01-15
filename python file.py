import pygame
import sys
import heapq

pygame.init()

# Screen settings with dynamic window size
WIDTH, HEIGHT = 900, 600  # Default dimensions
if len(sys.argv) > 2:  # Check for custom dimensions passed as command-line arguments
    try:
        WIDTH = int(sys.argv[1])
        HEIGHT = int(sys.argv[2])
    except ValueError:
        print("Invalid dimensions. Using default window size.")

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Bank Transaction Shortest Path Finder")

# Updated Colors
BACKGROUND_COLOR = (207, 240, 255)
NODE_COLOR = (118, 195, 255)
SELECTED_NODE_COLOR = (3, 96, 178)
HIGHLIGHTED_PATH_COLOR = (88, 236, 58)
UNHIGHLIGHTED_PATH_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
OUTSIDE_TEXT_COLOR = (30, 16, 129)

# Graph structure (nodes and edges)
nodes_original = {
    "ICICI_Bank": (400, 100),
    "State_Bank_of_India": (200, 300),
    "HDFC_Bank": (400, 300),
    "Axis_Bank": (600, 300),
    "Kotak_Mahindra_Bank": (400, 500),
    "Bank_of_Baroda": (100, 100),
    "Yes_Bank": (700, 100),
    "Federal_Bank": (700, 500)
}

edges = {
    "ICICI_Bank": [("State_Bank_of_India", 150), ("HDFC_Bank", 200), ("Axis_Bank", 300), ("Bank_of_Baroda", 250), ("Yes_Bank", 200)],
    "State_Bank_of_India": [("ICICI_Bank", 150), ("HDFC_Bank", 100), ("Bank_of_Baroda", 300)],
    "HDFC_Bank": [("State_Bank_of_India", 100), ("ICICI_Bank", 200), ("Axis_Bank", 150), ("Kotak_Mahindra_Bank", 200)],
    "Axis_Bank": [("ICICI_Bank", 300), ("HDFC_Bank", 150), ("Kotak_Mahindra_Bank", 250), ("Yes_Bank", 150)],
    "Kotak_Mahindra_Bank": [("HDFC_Bank", 200), ("Axis_Bank", 250), ("Federal_Bank", 300)],
    "Bank_of_Baroda": [("ICICI_Bank", 250), ("State_Bank_of_India", 300)],
    "Yes_Bank": [("ICICI_Bank", 200), ("Axis_Bank", 150), ("Federal_Bank", 350)],
    "Federal_Bank": [("Kotak_Mahindra_Bank", 300), ("Yes_Bank", 350)]
}

# Function to center nodes based on window size
def center_nodes(window_width, window_height):
    offset_x = (window_width - 800) // 2  # 800 is the original width of the graph layout
    offset_y = (window_height - 600) // 2  # 600 is the original height of the graph layout
    return {node: (x + offset_x, y + offset_y) for node, (x, y) in nodes_original.items()}

nodes = center_nodes(WIDTH, HEIGHT)

# Function to find the shortest path using Dijkstra's algorithm
def dijkstra(graph, start, end):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        visited.add(node)
        if node == end:
            return path, cost
        for (neighbor, weight) in graph[node]:
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))
    return [], 0

# Initial settings
source = None
destination = None
final_transaction_path = []
final_transaction_cost = 0

# Font settings
font = pygame.font.SysFont("Arial", 22)
small_font = pygame.font.SysFont("Arial", 18)

clock = pygame.time.Clock()
running = True

# Button settings
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 40
reset_button_rect = pygame.Rect(WIDTH - BUTTON_WIDTH - 10, 10, BUTTON_WIDTH, BUTTON_HEIGHT)

# Node dimensions
NODE_WIDTH, NODE_HEIGHT = 140, 40

while running:
    screen.fill(BACKGROUND_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            reset_button_rect = pygame.Rect(WIDTH - BUTTON_WIDTH - 10, 10, BUTTON_WIDTH, BUTTON_HEIGHT)
            nodes = center_nodes(WIDTH, HEIGHT)  # Recalculate node positions
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if reset_button_rect.collidepoint(pos):
                source = None
                destination = None
                final_transaction_path = []
                final_transaction_cost = 0
            else:
                for node, coord in nodes.items():
                    node_rect = pygame.Rect(coord[0] - NODE_WIDTH // 2, coord[1] - NODE_HEIGHT // 2, NODE_WIDTH, NODE_HEIGHT)
                    if node_rect.collidepoint(pos):
                        if source is None:
                            source = node
                        elif destination is None:
                            destination = node
                            selected_path, total_cost = dijkstra(edges, source, destination)
                            final_transaction_path = selected_path
                            final_transaction_cost = total_cost

    # Draw edges and weights
    for start_node, neighbors in edges.items():
        start_pos = nodes[start_node]
        for end_node, weight in neighbors:
            end_pos = nodes[end_node]
            color = HIGHLIGHTED_PATH_COLOR if (start_node in final_transaction_path and end_node in final_transaction_path) else UNHIGHLIGHTED_PATH_COLOR
            pygame.draw.line(screen, color, start_pos, end_pos, 3)
            mid_x = (start_pos[0] + end_pos[0]) // 2
            mid_y = (start_pos[1] + end_pos[1]) // 2 - 20
            weight_text = small_font.render(f"Rs. {weight}", True, OUTSIDE_TEXT_COLOR)
            screen.blit(weight_text, (mid_x - weight_text.get_width() // 2, mid_y - weight_text.get_height() // 2))

    # Draw nodes
    for node, pos in nodes.items():
        color = SELECTED_NODE_COLOR if node in [source, destination] else NODE_COLOR
        node_rect = pygame.Rect(pos[0] - NODE_WIDTH // 2, pos[1] - NODE_HEIGHT // 2, NODE_WIDTH, NODE_HEIGHT)
        pygame.draw.rect(screen, color, node_rect, border_radius=5)
        pygame.draw.rect(screen, UNHIGHLIGHTED_PATH_COLOR, node_rect, width=2, border_radius=5)
        node_text = font.render(node, True, TEXT_COLOR)
        screen.blit(node_text, (node_rect.centerx - node_text.get_width() // 2, node_rect.centery - node_text.get_height() // 2))

    # Draw transaction path
    if final_transaction_path:
        transaction_text = " -> ".join(final_transaction_path)
        transaction_display = font.render(f"Transaction Path: {transaction_text} | Total Cost: Rs. {final_transaction_cost}", True, OUTSIDE_TEXT_COLOR)
        screen.blit(transaction_display, (20, HEIGHT - 40))

    # Draw reset button
    pygame.draw.rect(screen, NODE_COLOR, reset_button_rect, border_radius=5)
    reset_text = font.render("Reset", True, TEXT_COLOR)
    screen.blit(reset_text, (reset_button_rect.centerx - reset_text.get_width() // 2, reset_button_rect.centery - reset_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
