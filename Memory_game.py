# Refactoring the memory game code into a class-based approach with improved structure and logic

import pygame
import random

class Card:
    """Represents a single memory card."""
    def __init__(self, image, position):
        self.image = image
        self.rect = pygame.Rect(position[0], position[1], CardGame.CARD_SIZE, CardGame.CARD_SIZE)
        self.matched = False
        self.visible = False

    def draw(self, screen):
        """Draw the card on the screen."""
        if self.visible or self.matched:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, CardGame.CARD_COLOR, self.rect)

class CardGame:
    """Main class to manage game states and logic."""
    SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
    BACKGROUND_COLOR = (30, 30, 30)
    CARD_COLOR = (255, 255, 255)
    CARD_SIZE = 100
    CARD_GAP = 20
    BOARD_ROWS, BOARD_COLS = 4, 4

    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Memory Game')
        self.clock = pygame.time.Clock()
        self.cards = []
        self.selected_cards = []
        self.load_card_images()
        self.create_board()

    def load_card_images(self):
        """Load and return card images. For simplicity, using colored surfaces."""
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                  (255, 165, 0), (255, 20, 147), (0, 255, 255), (128, 0, 128)]
        self.card_images = [pygame.Surface((self.CARD_SIZE, self.CARD_SIZE)) for _ in range(8)]
        for i, card_image in enumerate(self.card_images):
            card_image.fill(colors[i])

    def create_board(self):
        """Create and shuffle the board with pairs of cards."""
        card_images = self.card_images * 2  # Create pairs
        random.shuffle(card_images)
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                position = (col * (self.CARD_SIZE + self.CARD_GAP) + self.CARD_GAP,
                            row * (self.CARD_SIZE + self.CARD_GAP) + self.CARD_GAP)
                card = Card(card_images.pop(), position)
                self.cards.append(card)

    def run(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def handle_click(self, position):
        """Handle card selection and match checking."""
        for card in self.cards:
            if card.rect.collidepoint(position) and not card.matched and not card.visible:
                card.visible = True
                self.selected_cards.append(card)
                if len(self.selected_cards) == 2:
                    self.check_for_match()

    def check_for_match(self):
        """Check if the selected cards are a match."""
        if self.selected_cards[0].image == self.selected_cards[1].image:
            for card in self.selected_cards:
                card.matched = True
        else:
            pygame.time.wait(500)  # Wait half a second
        for card in self.selected_cards:
            card.visible = False
        self.selected_cards.clear()

    def draw(self):
        """Draw the game components."""
        self.screen.fill(self.BACKGROUND_COLOR)
        for card in self.cards:
            card.draw(self.screen)

# Uncomment the following lines to run the game
game = CardGame()
game.run()