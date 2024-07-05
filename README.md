# Wino Hunter

Wino Hunter is a simple arcade-style game built using Pygame, where the player controls a police car to shoot down falling beer sprites while avoiding collisions and collecting health power-ups.

## Features

- **Player Control**: Use arrow keys to move the police car (left, right, up, down).
- **Shooting Mechanic**: Press spacebar to shoot bullets at falling beer sprites.
- **Enemy Variety**: Beer sprites fall from the top of the screen, requiring multiple hits to destroy.
- **Health Power-ups**: Collect health icons to restore player health.
- **Score Tracking**: Gain points by shooting down beer sprites.
- **Particle Effects**: Visual effects when enemies are destroyed.
- **Game Over Screen**: Displays when player health reaches zero, allowing for restart or quit options.

## Setup and Installation

1. **Prerequisites**:
   - Python 3.x
   - Pygame library (`pip install pygame`)

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/Cloud1590/wineo-hunter.git
   cd wineo-hunter

## Installation

To run Wino Hunter, you'll need to install the required dependencies listed in `requirements.txt`. You can install them using pip:

```bash
pip install -r requirements.txt
```
   
3. **Run the Game**:
   ```bash
   python3 WinoHunter.py
   
4. **Controls**:

Use arrow keys to move the police car.
Press spacebar to shoot bullets.

5. **Game Over**:

When player health reaches zero, a game over screen appears.
Click "Restart" to play again or "Quit" to exit.

---------------------------------------------------------------
To build the executable for your system, use the following command:
```
pyinstaller --onefile --add-data "assets/*:assets" WinoHunter.py
```

macos building:
```
pyinstaller --onefile --windowed --add-data "assets/:assets" --icon "assets/icon.png" WinoHunter.py
```

**Contributing**
*Contributions are welcome! Fork the repository and submit pull requests for any improvements or fixes.*


