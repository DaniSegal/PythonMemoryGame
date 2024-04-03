import pygame


class GUI:
    SCREEN_WIDTH, SCREEN_HEIGHT = 650, 600
    BACKGROUND_COLOR = (30, 30, 30)
    CARD_GAP = 20
    BOARD_ROWS, BOARD_COLS = 4, 4
    FONT = None
    MATCH_SOUND_PATH = "applepay.mp3"
    UNMATCH_SOUND_PATH = "engineer_no01.mp3"
    RESET_BUTTON_COLOR = (50, 205, 50)
    RESET_BUTTON_RECT = pygame.Rect(480, 10, 150, 40)
    PLAY_AGAIN_BUTTON_RECT = pygame.Rect(480, 60, 150, 40)
    ONE_PLAYER_BUTTON_RECT = pygame.Rect(150, 250, 250, 50)
    TWO_PLAYER_BUTTON_RECT = pygame.Rect(150, 320, 250, 50)

    def __init__(self, mem_game) -> None:

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.FONT = pygame.font.SysFont("Arial", 24)
        self.start_ticks = pygame.time.get_ticks()  # Timer start
        self.match_sound = pygame.mixer.Sound(self.MATCH_SOUND_PATH)
        self.unmatch_sound = pygame.mixer.Sound(self.UNMATCH_SOUND_PATH)
        self.well_done_surf = None
        self.player_turn_text_surf = None
        self.reset_button_surf = self.FONT.render('Reset', True, (255, 255, 255))
        self.play_again_button_surf = self.FONT.render('Play Again', True, (255, 255, 255))
        self.game = mem_game
        
        

    def draw_board(self, cards):
        self.screen.fill(self.BACKGROUND_COLOR)
        for card in cards:
            card.draw(self.screen)
        self.draw_timer()

    def draw_timer(self):
        """Display the elapsed time on the screen."""
        elapsed_ticks = pygame.time.get_ticks() - self.start_ticks
        elapsed_seconds = elapsed_ticks // 1000  # Convert milliseconds to seconds
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        timer_font = self.FONT
        timer_surf = timer_font.render(f"Playing Time: {minutes:02}:{seconds:02}", True, (255, 255, 255))
        self.screen.blit(timer_surf, (self.SCREEN_WIDTH // 2 - timer_surf.get_width() // 2, 10))

    def draw_tries_counter(self):
        """Draws the tries counter on the screen."""
        tries_text = f"Tries: {self.game.match_tries_count}"
        tries_surf = self.FONT.render(tries_text, True, (255, 255, 255))
        # Choose an appropriate position on the screen
        self.screen.blit(tries_surf, (10, self.SCREEN_HEIGHT - 30))

    def draw_player_scores(self):
        for i, score in enumerate(self.game.player_scores):
            score_text = f"Player {i + 1} Score: {score}"
            score_surf = self.FONT.render(score_text, True, (255, 255, 255))
            self.screen.blit(score_surf, (10, 30 * i + 10))

    def draw_turn_indication(self):
        self.screen.blit(self.player_turn_text_surf, (self.SCREEN_WIDTH - 200, 10))
            
    def draw_reset_button(self):
        pygame.draw.rect(self.screen, self.RESET_BUTTON_COLOR, self.RESET_BUTTON_RECT)
        self.screen.blit(self.reset_button_surf,(self.RESET_BUTTON_RECT.x + 5, self.RESET_BUTTON_RECT.y + 5),)
        
    def draw_play_again_button(self):
        """Draws the play again button."""
        pygame.draw.rect(self.screen, self.RESET_BUTTON_COLOR, self.PLAY_AGAIN_BUTTON_RECT)
        self.screen.blit(self.play_again_button_surf,(self.PLAY_AGAIN_BUTTON_RECT.x + 5, self.PLAY_AGAIN_BUTTON_RECT.y + 5),)
        
    def draw_well_done_message(self):
        """Draws the well done message."""
        well_done_text = f'Well done! You did it in {self.game.match_tries_count} tries, think you can do better?'
        self.well_done_surf = self.FONT.render(well_done_text, True, (255, 215, 0), self.BACKGROUND_COLOR)
        text_rect = self.well_done_surf.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2 - 50))
        self.screen.blit(self.well_done_surf, text_rect)

    def draw_player_selection_screen(self):
        """Draws the player selection screen."""
        screen = self.screen
        screen.fill(self.BACKGROUND_COLOR)
        # Note: Use self.game.one_player_button_rect as an example of how to properly reference attributes
        pygame.draw.rect(screen, (100, 200, 255), self.ONE_PLAYER_BUTTON_RECT)
        pygame.draw.rect(screen, (100, 200, 255), self.TWO_PLAYER_BUTTON_RECT)
            
        one_player_text = self.FONT.render('1 Player', True, (255, 255, 255))
        two_player_text = self.FONT.render('2 Players', True, (255, 255, 255))
        
        screen.blit(one_player_text, (self.ONE_PLAYER_BUTTON_RECT.x + 50, self.ONE_PLAYER_BUTTON_RECT.y + 10))
        screen.blit(two_player_text, (self.TWO_PLAYER_BUTTON_RECT.x + 50, self.TWO_PLAYER_BUTTON_RECT.y + 10))