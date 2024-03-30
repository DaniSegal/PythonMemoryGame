import random
import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

# Define the game board dimensions
WIDTH = 800
HEIGHT = 600
ROWS = 4
COLS = 4


class Card:
  def __init__(self, x, y, color):
    self.x = x
    self.y = y
    self.color = color
    self.flipped = False

  def draw(self, screen):
    pygame.draw.rect(screen, self.color if self.flipped else GREY, (self.x, self.y, CARD_WIDTH, CARD_HEIGHT))
    # Only draw the card face if flipped
    if self.flipped:
      # You can customize this to draw an image or text on the card face
      pass


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Game")

# Define card dimensions
CARD_WIDTH = WIDTH // COLS
CARD_HEIGHT = HEIGHT // ROWS

# Define variables
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
cards = []
picked_cards = []

# Generate card colors (duplicate each color for matching)
colors = [(x, y, z) for x in range(256) for y in range(256) for z in range(256)]
random.shuffle(colors)
colors = colors[: (ROWS * COLS) // 2] * 2


# Create card objects
for row in range(ROWS):
  for col in range(COLS):
    card = Card(col * CARD_WIDTH, row * CARD_HEIGHT, colors.pop())
    cards.append(card)


def draw_grid(screen):
  # Draw grid lines
  for row in range(ROWS + 1):
    pygame.draw.line(screen, GREY, (0, row * CARD_HEIGHT), (WIDTH, row * CARD_HEIGHT))
  for col in range(COLS + 1):
    pygame.draw.line(screen, GREY, (col * CARD_WIDTH, 0), (col * CARD_WIDTH, HEIGHT))


def check_win():
  # Check if all cards are flipped
  for card in cards:
    if not card.flipped:
      return False
  return True


def handle_clicks(pos):
  global picked_cards

  card_x = pos[0] // CARD_WIDTH
  card_y = pos[1] // CARD_HEIGHT
  card = cards[card_y * COLS + card_x]

  # Check if card is already flipped or clickable (not yet matched)
  if not card.flipped and not any(c.color == card.color and c.flipped for c in picked_cards):
    card.flipped = True
    picked_cards.append(card)
    if len(picked_cards) == 2:
      # Check if cards match
      if picked_cards[0].color == picked_cards[1].color:
        # Cards match, keep them flipped
        picked_cards = []
      else:
        # Cards don't match, flip them back after a delay
        pygame.time.delay(1000)
        for card in picked_cards:
          card.flipped = False
        picked_cards = []


def draw_text(text, x, y):
  text_surface = font.render(text, True, WHITE)
  text_rect = text_surface.get_rect(center=(x, y))
  screen.blit(text_surface, text_rect)


# Game loop
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      pos = pygame.mouse.get_pos()
      handle_clicks(pos)

  # Clear the screen
  screen.fill(BLACK)

  # Draw the grid
  draw_grid(screen)

  # Draw the cards
  for card in cards:
    card.draw(screen)

  # Check for win condition
  if check_win():
    draw_text("You win!", WIDTH // 2, HEIGHT // 2)

  # Update the display
  pygame.display.flip()
  clock.tick(60)  # Set the frame rate to 60 fps

# Quit Pygame
pygame.quit()

