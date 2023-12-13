import pygame
import sys
import random

# Constants
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2
WINNING_LENGTH = 4

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Create the game board
board = [[EMPTY] * COLS for _ in range(ROWS)]

# Initialize Pygame window
SQUARE_SIZE = 100
WIDTH = COLS * SQUARE_SIZE
HEIGHT = (ROWS + 1) * SQUARE_SIZE
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Connect 4")

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == PLAYER1:
                pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif board[row][col] == PLAYER2:
                pygame.draw.circle(screen, YELLOW, (col * SQUARE_SIZE + SQUARE_SIZE // 2, (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

    pygame.display.flip()

def is_valid_move(column):
    return 0 <= column < COLS and board[0][column] == EMPTY

def drop_piece(column, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == EMPTY:
            board[row][column] = player
            return row

def check_winner(row, col, player):
    # Check horizontally
    for c in range(col - WINNING_LENGTH + 1, col + 1):
        if 0 <= c < COLS and board[row][c] == player:
            return True

    # Check vertically
    for r in range(row - WINNING_LENGTH + 1, row + 1):
        if 0 <= r < ROWS and board[r][col] == player:
            return True

    # Check diagonally (bottom-left to top-right)
    for i in range(WINNING_LENGTH):
        r, c = row - i, col + i
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            return True

    # Check diagonally (top-left to bottom-right)
    for i in range(WINNING_LENGTH):
        r, c = row + i, col + i
        if 0 <= r < ROWS and 0 <= c < COLS and board[r][c] == player:
            return True

    return False

def is_board_full():
    return all(cell != EMPTY for row in board for cell in row)

def get_column_from_mouse_click(pos):
    return pos[0] // SQUARE_SIZE

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER1:
            return get_column_from_mouse_click(event.pos)

        if event.type == pygame.KEYDOWN and event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7] and turn == PLAYER1:
            return int(event.unicode) - 1

def random_agent():
    return random.randint(0, COLS - 1)

def main():
    turn = random.choice([PLAYER1, PLAYER2])

    while True:
        column = None

        if turn == PLAYER1:
            column = handle_events()
        elif turn == PLAYER2:
            # Replace human input logic with random agent logic
            column = random_agent()
            while not is_valid_move(column):
                column = random_agent()

        if column is not None:
            row = drop_piece(column, turn)
            draw_board()

            if check_winner(row, column, turn):
                print(f"Player {turn} wins!")
                break
            elif is_board_full():
                print("It's a draw!")
                break

            turn = PLAYER2 if turn == PLAYER1 else PLAYER1

    pygame.time.wait(5000)  # Add a delay to see the window before exiting
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.time.wait(3000)
