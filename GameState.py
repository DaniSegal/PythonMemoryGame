import enum

class GameState(enum.Enum):
    PLAYER_SELECTION = 1
    SINGLE_PLAYER = 2
    TIME_ATTACK_MODE = 3
    TWO_PLAYERS = 4
    GAME_OVER = 5
    