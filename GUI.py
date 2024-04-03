import pygame


class Card:
    """Represents a single memory card."""
    def __init__(self, image, position):
        self.image = image
        self.rect = pygame.Rect(position[0], position[1], MemGame.CARD_SIZE, MemGame.CARD_SIZE)
        self.matched = False
        self.visible = False

    def draw(self, screen):
        """Draw the card on the screen."""
        if self.visible or self.matched:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, MemGame.CARD_COLOR, self.rect)