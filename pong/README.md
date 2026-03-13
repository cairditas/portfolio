# Pong Game

A classic Pong game implementation using Python, Pygame, and Pygbag for browser deployment.

## Features

- **Classic Gameplay**: Player vs Computer Pong match
- **Scoring System**: Track player score, computer score, and high score
- **Level Progression**: Ball speed increases with each level
- **Smart AI**: Computer opponent with occasional mistakes for balanced gameplay
- **Game Over System**: Game ends after 5 losses with option to continue
- **Visual Design**: Clear game border and dashed center line
- **Browser Compatible**: Runs in web browser using Pygbag

## Installation

1. Clone or download this project
2. Navigate to the project directory
3. Create and activate virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

### Local Development
```bash
python src/main.py
```

### Web Deployment
```bash
pygbag build
```
Then serve the `build/web` directory with your preferred web server.

## Controls

- **Up Arrow / W**: Move paddle up
- **Down Arrow / S**: Move paddle down
- **Mouse**: Click YES/NO buttons when prompted

## Game Rules

1. Use your paddle (blue) to hit the ball back to the computer (red)
2. Score points when the ball passes the computer's paddle
3. Each score increases the level and ball speed
4. Game ends after 5 losses (ball passes your paddle)
5. Choose to continue or start a new game after game over

## Project Structure

```
pong/
├── src/
│   ├── pong/
│   │   ├── __init__.py
│   │   └── game.py          # Main game logic
│   └── main.py              # Entry point
├── assets/                  # Game assets (empty for now)
├── tests/                   # Test files (empty for now)
├── venv/                    # Virtual environment
├── index.html               # Web page template
├── pygbag.toml             # Pygbag configuration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Configuration

The game can be configured by modifying constants in `src/pong/core/config.py`:

- `WindowConfig`: Window dimensions and FPS settings
- `GameAreaConfig`: Game playing area size and position  
- `PaddleConfig`: Paddle dimensions and movement speed
- `BallConfig`: Ball size, speed, and physics parameters
- `AIConfig`: Computer opponent difficulty settings
- `GameRulesConfig`: Scoring and game rules

## Technologies Used

- **Python 3.11**: Programming language
- **Pygame**: Game development library
- **Pygbag**: Python to WebAssembly compiler for browser deployment

## License

MIT License
