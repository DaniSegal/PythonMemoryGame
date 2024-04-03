# Refactoring the memory game code into a class-based approach with improved structure and logic

import pygame
import random
import GameState
import GUI

pygame.init()

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

    
class GameManager:
    def __init__(self, game):
        self.game = game
        self.game_state = GameState.State.PLAYER_SELECTION
        
    def draw_player_selection_screen(self):
        """Draws the player selection screen."""
        screen = self.game.screen
        screen.fill(MemGame.BACKGROUND_COLOR)
        # Note: Use self.game.one_player_button_rect as an example of how to properly reference attributes
        pygame.draw.rect(screen, (100, 200, 255), self.game.one_player_button_rect)
        pygame.draw.rect(screen, (100, 200, 255), self.game.two_player_button_rect)
            
        one_player_text = MemGame.FONT.render('1 Player', True, (255, 255, 255))
        two_player_text = MemGame.FONT.render('2 Players', True, (255, 255, 255))
        
        screen.blit(one_player_text, (self.game.one_player_button_rect.x + 50, self.game.one_player_button_rect.y + 10))
        screen.blit(two_player_text, (self.game.two_player_button_rect.x + 50, self.game.two_player_button_rect.y + 10))
        
    def handle_player_selection(self, position):
        """Updated to correctly modify game_state of GameManager instance."""
        if self.game.one_player_button_rect.collidepoint(position):
            self.game.num_players = 1
            self.game_state = GameState.State.PLAYING
        elif self.game.two_player_button_rect.collidepoint(position):
            self.game.num_players = 2
            self.game_state = GameState.State.PLAYING



class MemGame:
    """Main class to manage game states and logic."""
    SCREEN_WIDTH, SCREEN_HEIGHT = 650, 600
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
    MATCHED_CARDS = 0
    MATCH_TRIES = 0

    def __init__(self):
        """Initialize the game."""
        # pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Memory Game')
        self.player_scores = [0, 0]  # Scores for player 1 and player 2
        self.current_player = 0  # Index of the current player
        self.num_players = 1  # Default to single player game
        self.player_turn_text_surf = None
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
        self.matched_cards = 0
        self.match_tries_count = 0
        self.well_done_surf = None
        self.one_player_button_rect = pygame.Rect(150, 250, 250, 50)
        self.two_player_button_rect = pygame.Rect(150, 320, 250, 50)
        self.manager = GameManager(self)
        self.update_player_turn_text()
        

    def load_card_images(self):
        """Load and return card images. For simplicity, using colored surfaces."""
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                  (255, 165, 0), (255, 20, 147), (0, 255, 255), (128, 0, 128)]
        self.card_images = [pygame.Surface((self.CARD_SIZE, self.CARD_SIZE)) for _ in range(8)]
        for i, card_image in enumerate(self.card_images):
            card_image.fill(colors[i])
    
    def update_player_turn_text(self):
        """Updates the player turn text based on the current player."""
        turn_text = f"Player {self.current_player + 1}'s Turn"
        self.player_turn_text_surf = self.FONT.render(turn_text, True, (255, 255, 255))

    def toggle_player_turn(self):
        """Toggles the turn between player 1 and player 2."""
        if self.num_players == 2:
            self.current_player = (self.current_player + 1) % 2
            self.update_player_turn_text()

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
         # Update to generate the message dynamically with the current number of tries
        well_done_text = f'Well done! You did it in {self.match_tries_count} tries, think you can do better?'
        self.well_done_surf = self.FONT.render(well_done_text, True, (255, 215, 0), self.BACKGROUND_COLOR)
        text_rect = self.well_done_surf.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2 - 50))
        self.screen.blit(self.well_done_surf, text_rect)
        
    def all_matched(self):
        return self.matched_cards == 16
    
    def update_cursor(self):
        """Updates the cursor image based on its position."""
        # Change to hand cursor for all clickable items
        if (self.is_hovering(self.RESET_BUTTON_RECT) or
            self.is_hovering(self.PLAY_AGAIN_BUTTON_RECT) or
            any(self.is_hovering(card.rect) for card in self.cards if not card.matched)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def is_hovering(self, rect):
        """Checks if the mouse is hovering over the given rectangle."""
        return rect.collidepoint(pygame.mouse.get_pos())

    def run(self):
        running = True
        while running:
            self.update_cursor()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.manager.game_state == GameState.State.PLAYER_SELECTION:
                        self.manager.handle_player_selection(pygame.mouse.get_pos())
                    elif self.manager.game_state == GameState.State.PLAYING:
                        self.handle_click(pygame.mouse.get_pos())

            if self.manager.game_state == GameState.State.PLAYER_SELECTION:
                self.manager.draw_player_selection_screen()
            else:
                self.draw_game_components()

            if self.all_matched():
                self.draw_well_done_message()
                self.draw_play_again_button()

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
                    match_found = self.check_for_match()
                    if not match_found:
                        self.toggle_player_turn()
                    self.match_tries_count += 1
                    

    def check_for_match(self):
        """Check if the selected cards are a match."""
        match_found = False
        if self.selected_cards[0].image == self.selected_cards[1].image:
            for card in self.selected_cards:
                card.matched = True
            self.player_scores[self.current_player] += 1  # Update score for current player
            match_found = True    
            self.match_sound.play()
            self.matched_cards += 2
        else:
            self.draw_game_components()
            pygame.display.flip()
            self.unmatch_sound.play()
            pygame.time.wait(500)  # Wait half a second
            for card in self.selected_cards:
                card.visible = False
        self.selected_cards.clear()
        return match_found

    def draw_game_components(self):
        """Draw the game components."""
        self.screen.fill(self.BACKGROUND_COLOR)
        for card in self.cards:
            card.draw(self.screen)
        self.show_timer()
        
        """Draws the tries counter on the screen."""
        tries_text = f'Tries: {self.match_tries_count}'
        tries_surf = self.FONT.render(tries_text, True, (255, 255, 255))
        # Choose an appropriate position on the screen
        self.screen.blit(tries_surf, (10, self.SCREEN_HEIGHT - 30))
        
        # Draw player scores and turn indication
        for i, score in enumerate(self.player_scores):
            score_text = f"Player {i + 1} Score: {score}"
            score_surf = self.FONT.render(score_text, True, (255, 255, 255))
            self.screen.blit(score_surf, (10, 30 * i + 10))
            
        # Draw the current player's turn indication
        self.screen.blit(self.player_turn_text_surf, (self.SCREEN_WIDTH - 200, 10))

        if(not self.all_matched()): 
            pygame.draw.rect(self.screen, self.RESET_BUTTON_COLOR, self.RESET_BUTTON_RECT)
            self.screen.blit(self.reset_button_surf, (self.RESET_BUTTON_RECT.x + 5, self.RESET_BUTTON_RECT.y + 5))
        
    def reset_game(self):
        """Resets the game to the initial state."""
        self.cards.clear()
        self.selected_cards.clear()
        self.matched_cards = 0
        self.match_tries_count = 0
        self.create_board()
        self.start_ticks = pygame.time.get_ticks()  # Reset the timer
        self.player_scores = [0, 0]
        self.current_player = 0
        self.manager.game_state = GameState.State.PLAYER_SELECTION
        self.update_player_turn_text()
            
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
game = MemGame()
game.run()
