# Refactoring the memory game code into a class-based approach with improved structure and logic

import pygame

pygame.init()

import random
from GameState import GameState
from GUI import GUI
from Card import Card


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
        
    def fill_cards_deck(self):
        board_rows = self.gui.BOARD_ROWS
        board_cols = self.gui.BOARD_COLS
        card_size = Card.CARD_SIZE
        card_gap = self.gui.CARD_GAP 
        card_images = self.card_images * 2  # Create pairs
        random.shuffle(card_images)
        y_offset = 60
        for row in range(board_rows):
            for col in range(board_cols):
                position = (
                    col * (card_size + card_gap) + card_gap,
                    row * (card_size + card_gap) + card_gap + y_offset,)
                card = Card(card_images.pop(), position)
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
        self.gui.player_turn_text_surf = self.gui.FONT.render(turn_text, True, (255, 255, 255))

    def toggle_player_turn(self):
        """Toggles the turn between player 1 and player 2."""
        # if self.num_players == 2:
        #     self.current_player = (self.current_player + 1) % 2
        #     self.update_player_turn_text()
        self.current_player = (self.current_player + 1) % self.num_players
        self.update_player_turn_text()
        
    def all_matched(self):
        return self.matched_cards == 16
    
    def update_cursor(self):
        """Updates the cursor image based on its position."""
        # Change to hand cursor for all clickable items
        if (self.is_hovering(self.gui.RESET_BUTTON_RECT) or
            self.is_hovering(self.gui.PLAY_AGAIN_BUTTON_RECT) or
            any(self.is_hovering(card.rect) for card in self.cards_deck if not card.matched)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def is_hovering(self, rect):
        """Checks if the mouse is hovering over the given rectangle."""
        return rect.collidepoint(pygame.mouse.get_pos())

    def handle_click(self, position):
        if self.gui.RESET_BUTTON_RECT.collidepoint(position):
            self.reset_game()
            
        if self.all_matched() and self.gui.PLAY_AGAIN_BUTTON_RECT.collidepoint(position):
            self.reset_game()
            
        for card in self.cards_deck:
            if card.rect.collidepoint(position) and not card.matched and not card.visible:
                card.visible = True
                self.selected_cards.append(card)
                if len(self.selected_cards) == 2:
                    match_found = self.check_for_match()
                    if not match_found:
                        self.toggle_player_turn()
                    else:
                        # Update score for current player if a match is found
                        self.player_scores[self.current_player] += 1
                    self.match_tries_count += 1
                    self.selected_cards.clear()
                    
    def check_for_match(self):
        """Check if the selected cards are a match."""
        match_found = False
        if self.selected_cards[0].image == self.selected_cards[1].image:
            for card in self.selected_cards:
                card.matched = True
            self.player_scores[self.current_player] += 1  # Update score for current player
            match_found = True    
            self.gui.match_sound.play()
            self.matched_cards += 2
        else:
            self.draw_game_components()
            pygame.display.flip()
            self.gui.unmatch_sound.play()
            pygame.time.wait(500)  # Wait half a second
            for card in self.selected_cards:
                card.visible = False
        self.selected_cards.clear()
        return match_found
       
    def reset_game(self):
        """Resets the game to the initial state."""
        self.cards_deck.clear()
        self.selected_cards.clear()
        self.matched_cards = 0
        self.match_tries_count = 0
        self.player_scores = [0, 0]
        self.current_player = 0
        self.game_state = GameState.PLAYER_SELECTION
        self.update_player_turn_text()
        self.load_card_images()
        self.fill_cards_deck()
        self.start_ticks = pygame.time.get_ticks()  # Reset the timer
           
    def handle_player_selection(self, position):
        """Updated to correctly modify game_state of GameManager instance."""
        if self.gui.ONE_PLAYER_BUTTON_RECT.collidepoint(position):
            self.num_players = 1
        elif self.gui.TWO_PLAYER_BUTTON_RECT.collidepoint(position):
            self.num_players = 2
        self.game_state = GameState.PLAYING
            
    def draw_game_components(self):
        self.gui.draw_board(self.cards_deck)
        self.gui.draw_tries_counter()
        self.gui.draw_player_scores()
        self.gui.draw_turn_indication()    
        if(not self.all_matched()):
           self.gui.draw_reset_button()
            
    def run(self):
        running = True
        while running:
            self.update_cursor()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.game_state == GameState.PLAYER_SELECTION:
                        self.handle_player_selection(pygame.mouse.get_pos())
                    elif self.game_state == GameState.PLAYING:
                        self.handle_click(pygame.mouse.get_pos())

            if self.game_state == GameState.PLAYER_SELECTION:
                self.gui.draw_player_selection_screen()
            else:
                self.draw_game_components()

            if self.all_matched():
                self.gui.draw_well_done_message()
                self.gui.draw_play_again_button()

            pygame.display.flip()
            self.gui.clock.tick(60)
        pygame.quit()

# Uncomment the following lines to run the game
game = MemGame()
game.run()
