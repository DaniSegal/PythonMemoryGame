import enum

class State(enum.Enum):
    PLAYER_SELECTION = 1
    PLAYING = 2
    GAME_OVER = 3