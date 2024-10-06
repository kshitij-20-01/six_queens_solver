import pygame
import sys
import time
from typing import List, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
BOARD_SIZE = 6
SQUARE_SIZE = 80
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE
COLORS = [(238, 238, 210), (118, 150, 86)]  # Light and dark square colors

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("6-Queen Solver")

# Load and scale queen image
queen_img = pygame.image.load("queen.jpg")
queen_img = pygame.transform.scale(queen_img, (SQUARE_SIZE, SQUARE_SIZE))

def is_safe(board: List[List[int]], row: int, col: int) -> bool:
    """
    Check if it's safe to place a queen at the given position.
    
    Args:
    board (List[List[int]]): The current state of the board
    row (int): The row to check
    col (int): The column to check
    
    Returns:
    bool: True if it's safe to place a queen, False otherwise
    """
    # Check this row on left side
    for i in range(col):
        if board[row][i] == 1:
            return False
    
    # Check upper diagonal on left side
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    
    # Check lower diagonal on left side
    for i, j in zip(range(row, BOARD_SIZE, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False
    
    return True

def solve_queens(board: List[List[int]], col: int) -> bool:
    """
    Solve the 6-Queen problem using backtracking.
    
    Args:
    board (List[List[int]]): The current state of the board
    col (int): The current column being processed
    
    Returns:
    bool: True if a solution is found, False otherwise
    """
    if col >= BOARD_SIZE:
        return True
    
    for i in range(BOARD_SIZE):
        if is_safe(board, i, col):
            board[i][col] = 1
            draw_board(board)
            pygame.display.flip()
            time.sleep(0.5)  # Delay for visualization
            
            if solve_queens(board, col + 1):
                return True
            
            board[i][col] = 0
            draw_board(board)
            pygame.display.flip()
            time.sleep(0.5)  # Delay for visualization
    
    return False

def draw_board(board: List[List[int]]) -> None:
    """
    Draw the chessboard and queens.
    
    Args:
    board (List[List[int]]): The current state of the board
    """
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = COLORS[(row + col) % 2]
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
            if board[row][col] == 1:
                screen.blit(queen_img, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def main() -> None:
    """
    Main function to run the 6-Queen solver with visualization.
    """
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    
    running = True
    solving = False
    solution_found = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not solving:
                    solving = True
                    solution_found = False
                    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
                    logging.info("Starting to solve the 6-Queen problem")
        
        screen.fill((255, 255, 255))
        draw_board(board)
        
        if solving and not solution_found:
            solution_found = solve_queens(board, 0)
            solving = False
            if solution_found:
                logging.info("Solution found!")
            else:
                logging.info("No solution exists")
        
        font = pygame.font.Font(None, 36)
        if solution_found:
            text = font.render("Solution found! Press SPACE to restart", True, (0, 0, 0))
        elif solving:
            text = font.render("Solving...", True, (0, 0, 0))
        else:
            text = font.render("Press SPACE to start", True, (0, 0, 0))
        
        screen.blit(text, (10, WINDOW_SIZE - 40))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        pygame.quit()
        sys.exit(1)