# Refactoring the memory game code into a class-based approach with improved structure and logic

import pygame
import random

pygame.init()

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
    SCREEN_WIDTH, SCREEN_HEIGHT = 570, 600
    BACKGROUND_COLOR = (30, 30, 30)
    CARD_COLOR = (255, 255, 255)
    CARD_SIZE = 100
    CARD_GAP = 20
    BOARD_ROWS, BOARD_COLS = 4, 4
    FONT = pygame.font.SysFont("Arial", 24)
    MATCH_SOUND_PATH = 'applepay.mp3'
    UNMATCH_SOUND_PATH = 'engineer_no01.mp3'
    RESET_BUTTON_COLOR = (50, 205, 50)
    RESET_BUTTON_RECT = pygame.Rect(480, 10, 150, 40)
    PLAY_AGAIN_BUTTON_RECT = pygame.Rect(480, 60, 150, 40)

    def __init__(self):
        """Initialize the game."""
        # pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Memory Game')
        self.clock = pygame.time.Clock()
        self.cards = []
        self.selected_cards = []
        self.load_card_images()
        self.create_board()
        self.start_ticks = pygame.time.get_ticks()  # Timer start
        self.match_sound = pygame.mixer.Sound(self.MATCH_SOUND_PATH)  
        self.unmatch_sound = pygame.mixer.Sound(self.UNMATCH_SOUND_PATH)
        self.reset_button_surf = self.FONT.render('Reset', True, (255, 255, 255))
        self.play_again_button_surf = self.FONT.render('Play Again', True, (255, 255, 255))
        self.well_done_surf = self.FONT.render('Well done!', True, (255, 215, 0))

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
        y_offset = 60
        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                position = (col * (self.CARD_SIZE + self.CARD_GAP) + self.CARD_GAP,
                            row * (self.CARD_SIZE + self.CARD_GAP) + self.CARD_GAP + y_offset)
                card = Card(card_images.pop(), position)
                self.cards.append(card)
                
    def draw_play_again_button(self):
        """Draws the play again button."""
        pygame.draw.rect(self.screen, self.RESET_BUTTON_COLOR, self.PLAY_AGAIN_BUTTON_RECT)
        self.screen.blit(self.play_again_button_surf, (self.PLAY_AGAIN_BUTTON_RECT.x + 5, self.PLAY_AGAIN_BUTTON_RECT.y + 5))

    def draw_well_done_message(self):
        """Draws the well done message."""
        text_rect = self.well_done_surf.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2))
        self.screen.blit(self.well_done_surf, text_rect)
        
    def all_matched(self):
        return all(card.matched for card in self.cards)

    def run(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(pygame.mouse.get_pos())

            self.draw()
            self.draw_reset_button()
            
            if self.all_matched():
                self.draw_well_done_message()
                self.draw_play_again_button()
                
            # self.show_timer()  # Update to show the timer on the screen
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def handle_click(self, position):
        """Handle card selection and match checking."""
        if self.RESET_BUTTON_RECT.collidepoint(position):
            self.reset_game()
            
        if self.all_matched() and self.PLAY_AGAIN_BUTTON_RECT.collidepoint(position):
            self.reset_game()
            
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
            self.match_sound.play()
        else:
            self.draw()
            pygame.display.flip()
            self.unmatch_sound.play()
            pygame.time.wait(500)  # Wait half a second
            for card in self.selected_cards:
                card.visible = False
        self.selected_cards.clear()

    def draw(self):
        """Draw the game components."""
        self.screen.fill(self.BACKGROUND_COLOR)
        for card in self.cards:
            card.draw(self.screen)
        self.show_timer()
    
    def draw_reset_button(self):
        """Draws the reset button."""
        pygame.draw.rect(self.screen, self.RESET_BUTTON_COLOR, self.RESET_BUTTON_RECT)
        self.screen.blit(self.reset_button_surf, (self.RESET_BUTTON_RECT.x + 5, self.RESET_BUTTON_RECT.y + 5))
        
    def reset_game(self):
        """Resets the game to the initial state."""
        self.cards.clear()
        self.selected_cards.clear()
        self.create_board()
        self.start_ticks = pygame.time.get_ticks()  # Reset the timer
            
    def show_timer(self):
        """Display the elapsed time on the screen."""
        elapsed_ticks = pygame.time.get_ticks() - self.start_ticks
        elapsed_seconds = elapsed_ticks // 1000  # Convert milliseconds to seconds
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        timer_font = self.FONT
        timer_surf = timer_font.render(f'Playing Time: {minutes:02}:{seconds:02}', True, (255, 255, 255))
        self.screen.blit(timer_surf, (self.SCREEN_WIDTH//2 - timer_surf.get_width()//2, 10))

# Uncomment the following lines to run the game
game = CardGame()
game.run()
