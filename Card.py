import pygame



class Card:
    CARD_BACK_COLOR = (255, 255, 255)
    CARD_SIZE = 100
    TEXT_COLOR = (0, 0, 0)
    
    """Represents a single memory card."""

    def __init__(self, image, position, index):
        self.image = image
        self.rect = pygame.Rect(position[0], position[1], self.CARD_SIZE, self.CARD_SIZE)
        
        
        self.index = index
        self.matched = False
        self.visible = False
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        """Draw the card on the screen."""
        if self.visible or self.matched:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(screen, self.CARD_BACK_COLOR, self.rect)
            text_surf = self.font.render(str(self.index), True, Card.TEXT_COLOR)
            text_rect = text_surf.get_rect(center=self.rect.center)
            screen.blit(text_surf, text_rect)
            
    def get_card_size(self):
        return self.CARD_SIZE