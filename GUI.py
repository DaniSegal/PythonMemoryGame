import pygame



class GUI:
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 700
    BACKGROUND_COLOR = (30, 30, 30)
    CARD_GAP = 20
    BOARD_ROWS, BOARD_COLS = 4, 4
    MATCH_SOUND_PATH = "applepay.mp3"
    UNMATCH_SOUND_PATH = "engineer_no01.mp3"
    RESET_BUTTON_COLOR = (50, 205, 50)
    RESET_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH - 170, SCREEN_HEIGHT//2 - 60, 150, 40)
    PLAY_AGAIN_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT//2 - 30, 150, 40)
    VOICE_CONTROL_BUTTON_RECT = pygame.Rect(150, 180, 250, 50)
    ONE_PLAYER_BUTTON_RECT = pygame.Rect(150, 250, 250, 50)
    TWO_PLAYER_BUTTON_RECT = pygame.Rect(150, 320, 250, 50)
    TIME_ATTACK_BUTTON_RECT = pygame.Rect(150, 390, 250, 50)
    SPEAK_BUTTON_COLOR = (113, 77, 198)
    SPEAK_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH - 170, SCREEN_HEIGHT//2 - 150, 150, 40)
    
    player_selection_buttons = [VOICE_CONTROL_BUTTON_RECT, ONE_PLAYER_BUTTON_RECT, TWO_PLAYER_BUTTON_RECT, TIME_ATTACK_BUTTON_RECT]
    game_over_buttons = [PLAY_AGAIN_BUTTON_RECT]
    voice_control_buttons = [SPEAK_BUTTON_RECT]

    def __init__(self, mem_game) -> None:

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 48)
        self.match_sound = pygame.mixer.Sound(self.MATCH_SOUND_PATH)
        self.unmatch_sound = pygame.mixer.Sound(self.UNMATCH_SOUND_PATH)
        self.well_done_surf = None
        self.player_turn_text_surf = None
        self.reset_button_surf = self.font.render('Reset', True, (255, 255, 255))
        self.play_again_button_surf = self.font.render('Play Again', True, (255, 255, 255))
        self.game = mem_game
        
    def draw_board(self, cards):
        self.screen.fill(self.BACKGROUND_COLOR)
        for card in cards:
            card.draw(self.screen)

    def format_time(self, seconds):
        """Format time in seconds to mm:ss format."""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def render_time(self, time_str, position):
        """Render the formatted time string to the screen at the specified position."""
        timer_surf = self.font.render(time_str, True, (255, 255, 255))
        timer_rect = timer_surf.get_rect(center=(self.SCREEN_WIDTH // 2, position))
        self.screen.blit(timer_surf, timer_rect)

    def draw_timer(self):
        time_str = self.format_time(self.game.elapsed_time)
        self.render_time(time_str, 10)  

    def draw_countdown_timer(self, elapsed_time, duration):
        seconds_left = max(duration - elapsed_time, 0)
        time_str = self.format_time(seconds_left)
        self.render_time(time_str, 50)  
        
        if seconds_left <= 0:
            return False  
        return True

    def draw_tries_counter(self):
        """Draws the tries counter on the screen."""
        tries_text = f"Tries: {self.game.match_tries_count}"
        tries_surf = self.font.render(tries_text, True, (255, 255, 255))
        # Choose an appropriate position on the screen
        self.screen.blit(tries_surf, (10, self.SCREEN_HEIGHT - 30))

    def draw_player_scores(self):
        for i, score in enumerate(self.game.player_scores):
            score_text = f"Player {i + 1} Score: {score}"
            score_surf = self.font.render(score_text, True, (255, 255, 255))
            self.screen.blit(score_surf, (10, 30 * i + 10))

    def draw_turn_indication(self):
        self.screen.blit(self.player_turn_text_surf, (self.SCREEN_WIDTH - 200, 10))
            
    def draw_reset_button(self):
        self.draw_button(self.RESET_BUTTON_RECT, 'Reset', self.RESET_BUTTON_COLOR)
        
    def draw_speak_button(self):
        self.draw_button(self.SPEAK_BUTTON_RECT, 'Speak', self.SPEAK_BUTTON_COLOR)
        
    def draw_play_again_button(self):
        self.draw_button(self.PLAY_AGAIN_BUTTON_RECT, 'Play Again', self.RESET_BUTTON_COLOR)
           
    def draw_well_done_message(self):
        """Draws the well done message."""
        well_done_text = f'Well done! You did it in {self.game.match_tries_count} tries, think you can do better?'
        self.well_done_surf = self.font.render(well_done_text, True, (255, 215, 0), self.BACKGROUND_COLOR)
        text_rect = self.well_done_surf.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2 - 50))
        self.screen.blit(self.well_done_surf, text_rect)
        
    def draw_winner_message(self, winner):
        
        winner_text = f'AND THE WINNER IS ........ PLAYER NUMBER {winner} !!!'
        self.winner_msg_surf = self.font.render(winner_text, True, (255, 215, 0), self.BACKGROUND_COLOR)
        text_rect = self.winner_msg_surf.get_rect(center=(self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT//2 - 50))
        self.screen.blit(self.winner_msg_surf, text_rect)
             
    def draw_game_over_screen(self):
        """Draws the game over screen with a message."""
        self.screen.fill(self.BACKGROUND_COLOR)  # Optional: Change to a darker shade if desired
        game_over_text = "Game over, you lost."
        game_over_surf = self.font.render(game_over_text, True, (255, 0, 0))  # Red color for the text
        # Calculate the position to center the text
        text_rect = game_over_surf.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_surf, text_rect)

        # Optionally, you can also add a button or instruction to go back to the main menu or exit.
        self.draw_play_again_button()

        pygame.display.flip()  # Update the display   
        
    def draw_amazing_screen(self):
        self.screen.fill((129, 205, 253))
        
        headline_text = "AMAZING"
        headline_surf = self.big_font.render(headline_text, True, (0,0,128))
        headline_rect = headline_surf.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 3))

        # Render the subtext
        subtext = "You did it! you won attack mode"
        subtext_surf = self.font.render(subtext, True, (0,0,128))
        subtext_rect = subtext_surf.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 3 + 40))

        # Blit the texts onto the screen
        self.screen.blit(headline_surf, headline_rect)
        self.screen.blit(subtext_surf, subtext_rect)

        self.draw_play_again_button()
        pygame.display.flip()  # Update the display
              
    def draw_button(self, rect, text, color=(255, 255, 255)):
        pygame.draw.rect(self.screen, color, rect)
        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_main_menu(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_button(self.VOICE_CONTROL_BUTTON_RECT, 'Voice Control')
        self.draw_button(self.ONE_PLAYER_BUTTON_RECT, '1 Player')
        self.draw_button(self.TWO_PLAYER_BUTTON_RECT, '2 Players')
        self.draw_button(self.TIME_ATTACK_BUTTON_RECT, 'Time Attack')  
        pygame.display.flip()