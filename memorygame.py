# Refactoring the memory game code into a class-based approach with improved structure and logic

import pygame

pygame.init()

import random
from GameState import GameState
from GUI import GUI
from Card import Card
import VoiceControl



class MemGame:

    def __init__(self):   
        pygame.display.set_caption('Memory Game')
        self.game_state = GameState.PLAYER_SELECTION
        self.player_scores = [0, 0]  # Scores for player 1 and player 2
        self.current_player = 0  # Index of the current player
        self.num_players = 1  # Default to single player game
        self.cards_deck = []
        self.card_images = []
        self.selected_cards = []
        self.gui = GUI(self)
        
        self.matched_cards = 0
        self.match_tries_count = 0
        self.load_card_images()
        self.fill_cards_deck()
        self.update_player_turn_text()

        self.time_attack_round_duration = 60
        self.clock = pygame.time.Clock()
        self.start_ticks = 0
        self.elapsed_time = 0
            
    def fill_cards_deck(self):
        board_rows = self.gui.BOARD_ROWS
        board_cols = self.gui.BOARD_COLS
        card_size = Card.CARD_SIZE
        card_gap = self.gui.CARD_GAP 
        card_images = self.card_images * 2  # Create pairs
        random.shuffle(card_images)
        y_offset = 60
        index = 1
        for row in range(board_rows):
            for col in range(board_cols):
                position = (
                    col * (card_size + card_gap) + card_gap,
                    row * (card_size + card_gap) + card_gap + y_offset,)
                card = Card(card_images.pop(), position, index)
                index += 1
                self.cards_deck.append(card)

    def load_card_images(self):
        """Load and return card images. For simplicity, using colored surfaces."""
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                  (255, 165, 0), (255, 20, 147), (0, 255, 255), (128, 0, 128)]
        self.card_images = [pygame.Surface((Card.CARD_SIZE, Card.CARD_SIZE)) for _ in range(8)]
        for i, card_image in enumerate(self.card_images):
            card_image.fill(colors[i])
    
    def update_player_turn_text(self):
        """Updates the player turn text based on the current player."""   
        # Ensuring the player turn text updates correctly
        turn_text = f"Player {self.current_player + 1}'s Turn"
        self.gui.player_turn_text_surf = self.gui.font.render(turn_text, True, (255, 255, 255))

    def toggle_player_turn(self):
        self.current_player = (self.current_player + 1) % self.num_players
        self.update_player_turn_text()
        
    def all_matched(self):
        return self.matched_cards == 16
    
    def update_cursor(self):
        should_be_hand = any(self.is_hovering(button) for button in self.get_current_buttons())

        if self.game_state != GameState.VOICE_CONTROL and self.game_state != GameState.PLAYER_SELECTION:
            if not should_be_hand:
                should_be_hand = any(self.is_hovering(card.rect) for card in self.cards_deck if not card.matched)

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if should_be_hand else pygame.SYSTEM_CURSOR_ARROW)

    def get_current_buttons(self):
        buttons = []
        if self.game_state == GameState.PLAYER_SELECTION:
            buttons.extend(self.gui.player_selection_buttons)
        if self.game_state == GameState.VOICE_CONTROL:
            buttons.extend(self.gui.voice_control_buttons)
        if self.game_state == GameState.GAME_OVER:
            buttons.extend(self.gui.game_over_buttons)

        buttons.append(self.gui.RESET_BUTTON_RECT)  # Always include the reset button

        return buttons
    
    def is_hovering(self, rect):
        """Checks if the mouse is hovering over the given rectangle."""
        return rect.collidepoint(pygame.mouse.get_pos())

    def handle_card_selection(self, position):
        for card in self.cards_deck:
            if card.rect.collidepoint(position) and not card.matched and not card.visible:
                self.make_card_visible(card)
                if len(self.selected_cards) == 2:
                    self.process_selected_cards()
                    
    def handle_voice_selection(self):
        model = VoiceControl.init_vosk_model()
        number = VoiceControl.recognize_numbers_from_mic(model)
        
        for card in self.cards_deck:
            if card.index == number and not card.matched and not card.visible:
                self.make_card_visible(card)
                if len(self.selected_cards) == 2:
                    self.process_selected_cards()
                   
    def make_card_visible(self, card):
        card.visible = True
        self.selected_cards.append(card)

    def process_selected_cards(self):
        match_found = self.check_for_match()
        if not match_found:
            self.toggle_player_turn()
        self.match_tries_count += 1
        self.selected_cards.clear()

    def check_for_match(self):
        if self.selected_cards[0].image == self.selected_cards[1].image:
            self.set_cards_as_matched()
            return True
        else:
            self.handle_no_match_found()
            return False

    def set_cards_as_matched(self):
        for card in self.selected_cards:
            card.matched = True
        self.player_scores[self.current_player] += 1
        self.gui.match_sound.play()
        self.matched_cards += 2

    def handle_no_match_found(self):
        if self.game_state == GameState.TIME_ATTACK_MODE:
            self.attack_mode_logic()
        elif self.game_state == GameState.VOICE_CONTROL:
            self.voice_control_logic()
        else:    
            self.regular_game_logic()
            
        pygame.display.flip()
        self.gui.unmatch_sound.play()
        pygame.time.wait(500)  # Wait half a second
        for card in self.selected_cards:
            card.visible = False
                 
    def reset_game(self):
        """Resets the game to the initial state."""
        self.cards_deck.clear()
        self.selected_cards.clear()
        self.matched_cards = 0
        self.match_tries_count = 0
        self.player_scores = [0, 0]
        self.current_player = 0
        self.load_card_images()
        self.fill_cards_deck()
        self.start_ticks = pygame.time.get_ticks()
        self.elapsed_time = 0
        Card.current_card_index = 0
        
        if self.game_state == GameState.PLAYER_SELECTION:
            self.update_player_turn_text()
            self.time_attack_round_duration = 60
                        
    def handle_player_selection(self, position):
        
        if self.gui.ONE_PLAYER_BUTTON_RECT.collidepoint(position):
            self.num_players = 1
            self.game_state = GameState.SINGLE_PLAYER
        elif self.gui.TWO_PLAYER_BUTTON_RECT.collidepoint(position):
            self.num_players = 2
            self.game_state = GameState.TWO_PLAYERS
        elif self.gui.TIME_ATTACK_BUTTON_RECT.collidepoint(position):
            self.num_players = 1
            self.game_state = GameState.TIME_ATTACK_MODE
        elif self.gui.VOICE_CONTROL_BUTTON_RECT.collidepoint(position):
            self.num_players = 1
            self.game_state = GameState.VOICE_CONTROL
            
        self.start_ticks = pygame.time.get_ticks()
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.process_mouse_click(event.pos)
        return True
    
    def process_mouse_click(self, mouse_pos):
        if self.game_state == GameState.PLAYER_SELECTION:
            self.handle_player_selection(mouse_pos)
            
        elif self.gui.RESET_BUTTON_RECT.collidepoint(mouse_pos):
            self.game_state = GameState.PLAYER_SELECTION
            self.reset_game()    
            
        elif self.gui.PLAY_AGAIN_BUTTON_RECT.collidepoint(mouse_pos) and self.game_state == GameState.GAME_OVER:
            self.game_state = GameState.PLAYER_SELECTION
            self.reset_game()
            
        elif self.game_state in (GameState.SINGLE_PLAYER, GameState.TIME_ATTACK_MODE, GameState.TWO_PLAYERS):
            self.handle_card_selection(mouse_pos)
            
        elif self.game_state == GameState.VOICE_CONTROL:
            if self.gui.SPEAK_BUTTON_RECT.collidepoint(mouse_pos):
                    self.handle_voice_selection()
                          
    def draw_regular_game_components(self):
        self.gui.draw_board(self.cards_deck)
        self.gui.draw_timer()
        self.gui.draw_tries_counter()
        
        if self.num_players == 2: 
            self.gui.draw_player_scores()
            self.gui.draw_turn_indication() 
               
        if(not self.all_matched()):
           self.gui.draw_reset_button()
           
    def draw_voice_control_components(self):
        self.gui.draw_board(self.cards_deck)
        self.gui.draw_timer()
        self.gui.draw_tries_counter()
        self.gui.draw_speak_button()
        if(not self.all_matched()):
           self.gui.draw_reset_button()
        
    def attack_mode_logic(self):
        
        self.gui.draw_board(self.cards_deck)
        self.gui.draw_reset_button()
        if(self.gui.draw_countdown_timer(self.elapsed_time, self.time_attack_round_duration)):
            if self.all_matched():
                if self.time_attack_round_duration == 30:
                    self.game_state = GameState.GAME_OVER
                    self.gui.draw_amazing_screen()
                else:    
                    self.time_attack_round_duration -= 5
                    self.reset_game()     
        elif self.game_state == GameState.TIME_ATTACK_MODE:
            self.game_state = GameState.GAME_OVER
            self.gui.draw_game_over_screen()
                         
    def regular_game_logic(self):
        self.draw_regular_game_components() 
        if self.all_matched():
                if self.num_players == 2:
                    winner = 1
                    if self.player_scores[0] < self.player_scores[1]: winner = 2
                    self.gui.draw_winner_message(winner)
                else: 
                    self.gui.draw_well_done_message()    
                self.game_state = GameState.GAME_OVER
                self.gui.draw_play_again_button()
                                         
    def voice_control_logic(self):
        self.draw_voice_control_components()
        if self.all_matched():
            self.game_state = GameState.GAME_OVER
            self.gui.draw_well_done_message()
            self.gui.draw_play_again_button()     
    
    def run(self):
        running = True
        while running:
            self.update_cursor()
            running = self.handle_events()
           
            if self.game_state != GameState.GAME_OVER and self.game_state != GameState.PLAYER_SELECTION:
                self.elapsed_time = int((pygame.time.get_ticks()-self.start_ticks)/1000)
                
            if self.game_state == GameState.VOICE_CONTROL:
                self.voice_control_logic()
            elif self.game_state == GameState.PLAYER_SELECTION:
                self.gui.draw_main_menu()
            elif self.game_state == GameState.TIME_ATTACK_MODE:
                self.attack_mode_logic()
            elif self.game_state != GameState.GAME_OVER:
                self.regular_game_logic() 
            self.clock.tick(60)
            
            pygame.display.flip()
            
        pygame.quit()
            
       

game = MemGame()
game.run()
