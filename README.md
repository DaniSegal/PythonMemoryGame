
# Python Memory Game

An interactive and fun memory card game built with Pygame! This game features various game modes, including voice-controlled gameplay, where players can match cards by speaking card numbers! 

## How to Play

1. Clone the repository to your local machine:
   ```bash
   git clone <repository-url>
   ```
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure that you have the VOSK speech recognition model downloaded and accessible at `./vosk-model-small-en-us-0.15` (or modify the path in `VoiceControl.py` if necessary).
4. Run the game:
   ```bash
   python memorygame.py
   ```

## Game Modes

1. **Single Player**: Standard memory game with one player.
2. **Two Player**: Take turns with a friend to find matching cards. The player with the highest score wins!
3. **Time Attack Mode**: Match all cards within a set time limit. The time decreases with each successful round!
4. **Voice-Controlled Mode**: Use voice commands to play. Click "Speak" and say a number (e.g., "one", "two") to reveal the respective card.


## Known Issues

- Ensure the VOSK model is in the specified path (`./vosk-model-small-en-us-0.15`). Otherwise, the voice control feature won't work.
- PyAudio might require additional setup on some systems.

## Acknowledgements

- [Pygame](https://www.pygame.org/news) - For providing the graphical library.
- [VOSK](https://alphacephei.com/vosk/) - For the offline voice recognition model.

