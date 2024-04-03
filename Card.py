import pygame

class Card:
    CARD_BACK_COLOR = (255, 255, 255)
    CARD_SIZE = 100

    """Represents a single memory card."""

    def __init__(self, image, position):
        self.image = image
        self.rect = pygame.Rect(position[0], position[1], self.CARD_SIZE, self.CARD_SIZE)
        self.matched = False
        self.visible = False

    def draw(self, screen):
        """Draw the card on the screen."""
        if self.visible or self.matched:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.CARD_BACK_COLOR, self.rect)
            
    def get_card_size(self):
        return self.CARD_SIZE