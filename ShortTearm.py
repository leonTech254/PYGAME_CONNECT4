import pygame
import sys
import time
import random

# Constants for the GUI
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
CELL_SIZE = 100
GRID_ROWS = 6
GRID_COLS = 7
DISC_RADIUS = CELL_SIZE // 2 - 5

class Connect4Board:
    def __init__(self):
        self.grid = [[' ' for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

    def display_board(self):
        for row in self.grid:
            print('|'.join(row))
            print('-' * (GRID_COLS * 2 - 1))

    def is_valid_move(self, col):
        return 0 <= col < GRID_COLS and self.grid[0][col] == ' '

    def make_move(self, col, player):
        for row in range(GRID_ROWS - 1, -1, -1):
            if self.grid[row][col] == ' ':
                self.grid[row][col] = player
                return True
        return False  # Column is full

    def check_winner(self, player):
        # Check horizontally
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS - 3):
                if all(self.grid[row][col + i] == player for i in range(4)):
                    return True

        # Check vertically
        for row in range(GRID_ROWS - 3):
            for col in range(GRID_COLS):
                if all(self.grid[row + i][col] == player for i in range(4)):
                    return True

        # Check diagonally (down-right)
        for row in range(GRID_ROWS - 3):
            for col in range(GRID_COLS - 3):
                if all(self.grid[row + i][col + i] == player for i in range(4)):
                    return True

        # Check diagonally (up-right)
        for row in range(3, GRID_ROWS):
            for col in range(GRID_COLS - 3):
                if all(self.grid[row - i][col + i] == player for i in range(4)):
                    return True

        return False

    def is_full(self):
        return all(self.grid[0][col] != ' ' for col in range(GRID_COLS))


class ShortTermAgent:
    def __init__(self, player):
        self.player = player

    def make_move(self, board):
        # Simple heuristic: choose a random valid move
        valid_moves = [col for col in range(GRID_COLS) if board.is_valid_move(col)]
        return random.choice(valid_moves)


class Connect4Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Connect 4")
        self.clock = pygame.time.Clock()

        self.board = Connect4Board()
        self.human_player = 'R'
        self.computer_player = 'Y'
        self.current_player = self.human_player  # Start with human player
        self.game_over = False
        self.winner = None
        self.short_term_agent = ShortTermAgent(self.computer_player)

    def run(self):
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.current_player == self.human_player:
                col = event.pos[0] // CELL_SIZE
                self.make_move(col)
            elif event.type == pygame.KEYDOWN and self.current_player == self.human_player:
                if pygame.K_1 <= event.key <= pygame.K_7:
                    col = event.key - pygame.K_1
                    self.make_move(col)

    def make_move(self, col):
        if self.current_player == self.human_player:
            # Human player's move
            if self.board.is_valid_move(col):
                if self.board.make_move(col, self.human_player):
                    if self.board.check_winner(self.human_player):
                        self.winner = self.human_player
                        self.game_over = True
                    elif self.board.is_full():
                        self.winner = 'Draw'
                        self.game_over = True
                    else:
                        self.current_player = self.computer_player
                        # Computer agent makes a move
                        self.make_move(-1)  # -1 as a placeholder for computer move
        else:
            # Computer agent's move
            computer_move = self.short_term_agent.make_move(self.board)
            if self.board.is_valid_move(computer_move):
                if self.board.make_move(computer_move, self.computer_player):
                    if self.board.check_winner(self.computer_player):
                        self.winner = self.computer_player
                        self.game_over = True
                    elif self.board.is_full():
                        self.winner = 'Draw'
                        self.game_over = True
                    else:
                        self.current_player = self.human_player

    def update(self):
        # Add any game logic updates here
        pass

    def draw(self):
        self.screen.fill((255, 255, 255))  # White background

        # Draw grid lines
        for row in range(GRID_ROWS + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (0, row * CELL_SIZE), (SCREEN_WIDTH, row * CELL_SIZE), 2)
        for col in range(GRID_COLS + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (col * CELL_SIZE, 0), (col * CELL_SIZE, SCREEN_HEIGHT), 2)

        # Draw discs on the board
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                if self.board.grid[row][col] == 'R':
                    color = (255, 0, 0)  # Red for player 'R'
                elif self.board.grid[row][col] == 'Y':
                    color = (255, 255, 0)  # Yellow for player 'Y'
                else:
                    continue  # Skip empty cells
                pygame.draw.circle(self.screen, color, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), DISC_RADIUS)

        # Display winner message
        if self.winner is not None:
            font = pygame.font.Font(None, 36)
            if self.winner == 'Draw':
                text = font.render("It's a Draw!", True, (0, 0, 0))
            else:
                text = font.render(f"Player {self.winner} wins!", True, (0, 0, 0))
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()

            # Add a delay before exiting
            time.sleep(2)
            pygame.quit()
            sys.exit()

        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    game = Connect4Game()
    game.run()
