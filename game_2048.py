import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
MINIMUM_SIZE = 600
DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 800
GRID_SIZE = 4
MIN_CELL_SIZE = 50
GRID_RATIO = 0.65  # Grid will take up 65% of the window height

# Colors
BACKGROUND = (250, 248, 239)  # Lighter background
GRID_BACKGROUND = (187, 173, 160)
EMPTY_CELL = (205, 193, 180)
FONT_COLOR = (119, 110, 101)
LIGHT_FONT = (249, 246, 242)
SUCCESS_COLOR = (0, 200, 0)
MILESTONE_COLOR = (255, 140, 0)
HEADER_COLOR = (143, 122, 102)  # New header color

# Color scheme for different numbers
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# Milestones for achievements
MILESTONES = [128, 256, 512, 1024, 2048]

class Game2048:
    def __init__(self):
        self.width = DEFAULT_WIDTH
        self.height = DEFAULT_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption('2048')
        self.reset_game()

    def reset_game(self):
        """Reset the game to initial state"""
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.score = 0
        self.highest_tile = 2
        self.milestone_messages = []
        self.message_timers = []
        self.update_sizes()
        self.add_new_tile()
        self.add_new_tile()
        self.game_over_state = False

    def update_sizes(self):
        """Update sizes based on current window dimensions"""
        min_dimension = min(self.width, self.height)
        self.header_height = min_dimension // 8  # Smaller header
        
        # Calculate cell size based on available space and desired grid ratio
        available_height = self.height - self.header_height
        desired_grid_height = self.height * GRID_RATIO
        self.cell_size = max(MIN_CELL_SIZE, int(desired_grid_height // (GRID_SIZE + 1)))
        
        # Adjust padding based on cell size
        self.cell_padding = max(5, self.cell_size // 15)  # Smaller padding between cells
        self.grid_padding = max(10, self.cell_size // 8)  # Smaller padding around grid
        
        # Update fonts
        self.title_font = pygame.font.Font(None, min_dimension // 12)
        self.header_font = pygame.font.Font(None, min_dimension // 20)
        self.score_font = pygame.font.Font(None, min_dimension // 25)
        self.message_font = pygame.font.Font(None, min_dimension // 20)

    def handle_resize(self, event):
        """Handle window resize event"""
        new_width, new_height = event.size
        # Enforce minimum window size
        self.width = max(MINIMUM_SIZE, new_width)
        self.height = max(MINIMUM_SIZE, new_height)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.update_sizes()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def update_highest_tile(self, value):
        if value > self.highest_tile:
            self.highest_tile = value
            if value in MILESTONES:
                self.milestone_messages.append({
                    'text': f'Reached {value}!',
                    'time': pygame.time.get_ticks(),
                    'color': MILESTONE_COLOR
                })

    def draw_rounded_rect(self, surface, color, rect, radius):
        """Draw a rounded rectangle"""
        pygame.draw.rect(surface, color, rect, border_radius=radius)

    def draw_tile(self, value, x, y):
        # Calculate position for centered grid
        grid_width = GRID_SIZE * self.cell_size + (GRID_SIZE - 1) * self.cell_padding
        start_x = (self.width - grid_width) // 2
        start_y = self.header_height + self.grid_padding
        
        pos_x = start_x + x * (self.cell_size + self.cell_padding)
        pos_y = start_y + y * (self.cell_size + self.cell_padding)

        # Draw tile with rounded corners
        self.draw_rounded_rect(

            self.screen,
            TILE_COLORS.get(value, TILE_COLORS[2048]),
            (pos_x, pos_y, self.cell_size, self.cell_size),
            self.cell_size // 8
        )

        if value != 0:
            text_color = FONT_COLOR if value <= 4 else LIGHT_FONT
            text = str(value)
            digit_count = len(text)
            
            # Adjust font size based on number length and cell size
            if digit_count <= 2:
                font_size = self.cell_size // 2
            elif digit_count == 3:
                font_size = self.cell_size // 2.5
            else:
                font_size = self.cell_size // 3
                
            font = pygame.font.Font(None, int(font_size))
            text_surface = font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=(pos_x + self.cell_size/2, pos_y + self.cell_size/2))
            self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BACKGROUND)
        
        # Draw title
        title = self.title_font.render('2048', True, HEADER_COLOR)
        title_rect = title.get_rect(topleft=(self.width//20, self.header_height//4))
        self.screen.blit(title, title_rect)

        # Draw score container
        score_box_width = self.width // 6  # Smaller score box
        score_box_height = self.header_height // 1.5  # Taller score box
        score_box_x = self.width - score_box_width - self.width//20
        score_box_y = self.header_height//4
        
        self.draw_rounded_rect(
            self.screen,
            GRID_BACKGROUND,
            (score_box_x, score_box_y, score_box_width, score_box_height),
            8
        )
        
        # Draw score label and value
        score_label = self.score_font.render('SCORE', True, LIGHT_FONT)
        score_value = self.header_font.render(str(self.score), True, LIGHT_FONT)
        
        score_label_rect = score_label.get_rect(centerx=score_box_x + score_box_width//2, 
                                              top=score_box_y + score_box_height//6)
        score_value_rect = score_value.get_rect(centerx=score_box_x + score_box_width//2, 
                                              top=score_box_y + score_box_height//2)
        
        self.screen.blit(score_label, score_label_rect)
        self.screen.blit(score_value, score_value_rect)

        # Draw highest tile
        highest_text = self.score_font.render(f'Highest: {self.highest_tile}', True, HEADER_COLOR)
        highest_rect = highest_text.get_rect(midtop=(self.width//2, self.header_height//3))
        self.screen.blit(highest_text, highest_rect)

        # Draw main grid background
        grid_width = GRID_SIZE * self.cell_size + (GRID_SIZE - 1) * self.cell_padding
        grid_height = grid_width
        grid_x = (self.width - grid_width) // 2
        grid_y = self.header_height + self.grid_padding
        
        self.draw_rounded_rect(
            self.screen,
            GRID_BACKGROUND,
            (grid_x - self.grid_padding//2, 
             grid_y - self.grid_padding//2,
             grid_width + self.grid_padding,
             grid_height + self.grid_padding),
            12
        )

        # Draw milestone messages
        current_time = pygame.time.get_ticks()
        y_offset = self.header_height
        remaining_messages = []
        
        for message in self.milestone_messages:
            if current_time - message['time'] < 2000:
                text = self.message_font.render(message['text'], True, message['color'])
                text_rect = text.get_rect(center=(self.width/2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += self.header_height//3
                remaining_messages.append(message)
        
        self.milestone_messages = remaining_messages

        # Draw grid
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.draw_tile(self.grid[i][j], i, j)

        # Draw game over screen if game is over
        if self.game_over_state:
            self.draw_game_over()

    def draw_game_over(self):
        """Draw game over screen with restart button"""
        # Add semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((255, 255, 255))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        font = pygame.font.Font(None, self.width // 10)
        text = font.render('Game Over!', True, FONT_COLOR)
        text_rect = text.get_rect(center=(self.width/2, self.height/2 - 50))
        self.screen.blit(text, text_rect)

        # Draw restart button
        button_width = self.width // 4
        button_height = self.height // 12
        button_x = self.width//2 - button_width//2
        button_y = self.height//2 + 20

        # Get mouse position for hover effect
        mouse_pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        button_color = (142, 122, 102)  # Default color
        
        # Change color if mouse is over button
        if button_rect.collidepoint(mouse_pos):
            button_color = (158, 138, 118)  # Lighter color on hover

        # Draw button
        self.draw_rounded_rect(
            self.screen,
            button_color,
            button_rect,
            10
        )

        # Restart text
        restart_font = pygame.font.Font(None, self.width // 20)
        restart_text = restart_font.render('Restart (R)', True, LIGHT_FONT)
        restart_rect = restart_text.get_rect(center=(self.width/2, button_y + button_height/2))
        self.screen.blit(restart_text, restart_rect)

    def move(self, direction):
        original_grid = self.grid.copy()
        merged = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

        if direction in ['UP', 'DOWN']:
            for i in range(GRID_SIZE):

                for j in range(GRID_SIZE):

                    if direction == 'UP':
                        self._move_tile(GRID_SIZE - 1 - j, i, -1, 0, merged)
                    else:  # DOWN
                        self._move_tile(j, i, 1, 0, merged)

        elif direction in ['LEFT', 'RIGHT']:
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    if direction == 'LEFT':
                        self._move_tile(i, GRID_SIZE - 1 - j, 0, -1, merged)
                    else:  # RIGHT
                        self._move_tile(i, j, 0, 1, merged)

        # Only add new tile if the grid changed
        if not np.array_equal(original_grid, self.grid):
            self.add_new_tile()

    def _move_tile(self, i, j, di, dj, merged):
        if self.grid[i][j] == 0:
            return

        value = self.grid[i][j]
        self.grid[i][j] = 0
        ni, nj = i, j

        while True:
            next_i, next_j = ni + di, nj + dj
            if not (0 <= next_i < GRID_SIZE and 0 <= next_j < GRID_SIZE):
                break
            if self.grid[next_i][next_j] == 0:
                ni, nj = next_i, next_j
            elif self.grid[next_i][next_j] == value and not merged[next_i][next_j]:
                ni, nj = next_i, next_j
                value *= 2
                self.score += value
                self.update_highest_tile(value)
                merged[ni][nj] = True
                break
            else:
                break

        self.grid[ni][nj] = value

    def game_over(self):
        # Check for any empty cells
        if 0 in self.grid:
            return False

        # Check for possible merges
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j]
                # Check right and down neighbors
                for di, dj in [(0, 1), (1, 0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
                        if self.grid[ni][nj] == value:
                            return False
        return True

def main():
    game = Game2048()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                game.handle_resize(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_over_state:
                    # Check if restart button is clicked
                    button_width = game.width // 4
                    button_height = game.height // 12
                    button_x = game.width//2 - button_width//2
                    button_y = game.height//2 + 20
                    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                    
                    if button_rect.collidepoint(event.pos):
                        game.reset_game()
                else:
                    # Handle regular game clicks
                    pos = pygame.mouse.get_pos()
                    grid_width = GRID_SIZE * game.cell_size + (GRID_SIZE - 1) * game.cell_padding
                    grid_height = grid_width
                    grid_x = (game.width - grid_width) // 2
                    grid_y = game.header_height + game.grid_padding
                    
                    if grid_x <= pos[0] <= grid_x + grid_width and \
                       grid_y <= pos[1] <= grid_y + grid_height:
                        col = (pos[0] - grid_x) // (game.cell_size + game.cell_padding)
                        row = (pos[1] - grid_y) // (game.cell_size + game.cell_padding)
                        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                            game.selected = (row, col)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over_state:
                    game.reset_game()
                elif not game.game_over_state:
                    # Arrow keys for movement
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        game.move('UP')
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        game.move('DOWN')
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        game.move('LEFT')
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        game.move('RIGHT')

        game.draw()
        
        # Check for game over
        if game.game_over() and not game.game_over_state:
            game.game_over_state = True
            
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
