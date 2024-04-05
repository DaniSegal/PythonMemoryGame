import enum

class GameState(enum.Enum):
    PLAYER_SELECTION = 1
    VOICE_CONTROL = 2
    SINGLE_PLAYER = 3
    TIME_ATTACK_MODE = 4
    TWO_PLAYERS = 5
    GAME_OVER = 6
    