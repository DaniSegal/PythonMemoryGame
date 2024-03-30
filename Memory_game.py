import pygame
import random

# Initialize Pygame
pygame.init()

# Game variables
screen_width, screen_height = 640, 480
background_color = (30, 30, 30)
card_color = (255, 255, 255)
card_size = 100
card_gap = 20
board_rows, board_cols = 4, 4
cards = []
selected_cards = []
found_pairs = []

# Pygame setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Memory Game')
clock = pygame.time.Clock()

def load_card_images():
    # Placeholder: Use solid colors for simplicity. Replace with image loading for more complexity.
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (255, 20, 147), (0, 255, 255), (128, 0, 128)]
    card_images = [pygame.Surface((card_size, card_size)) for _ in range(8)]
    for i, card_image in enumerate(card_images):
        card_image.fill(colors[i])
    return card_images

def create_board():
    card_images = load_card_images() * 2 # Create pairs
    random.shuffle(card_images)
    for row in range(board_rows):
        row_cards = []
        for col in range(board_cols):
            position = (col * (card_size + card_gap) + card_gap, 
                        row * (card_size + card_gap) + card_gap)
            card = {'rect': pygame.Rect(position[0], position[1], card_size, card_size),
                    'image': card_images.pop(),
                    'matched': False}
            row_cards.append(card)
        cards.append(row_cards)

def select_card(position):
    for row in cards:
        for card in row:
            if card['rect'].collidepoint(position) and not card['matched']:
                return card
    return None

def game_loop():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle card selection
                card = select_card(pygame.mouse.get_pos())
                if card and card not in selected_cards:
                    selected_cards.append(card)
                    if len(selected_cards) == 2:
                        # Check for a match
                        if selected_cards[0]['image'] == selected_cards[1]['image']:
                            for selected_card in selected_cards:
                                selected_card['matched'] = True
                            selected_cards.clear()
                        else:
                            pygame.time.wait(500) # Wait half a second
                            selected_cards.clear()

        screen.fill(background_color)
        
        for row in cards:
            for card in row:
                if card in selected_cards or card['matched']:
                    pygame.draw.rect(screen, (200, 200, 200), card['rect'])  # Show card or matched card
                    screen.blit(card['image'], card['rect'])
                else:
                    pygame.draw.rect(screen, card_color, card['rect'])  # Cover card
                    
        pygame.display.flip()
        clock.tick(60)

create_board()
game_loop()
pygame.quit()
