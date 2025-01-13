# 2048 Game

A Python implementation of the popular 2048 game using Pygame.
![image alt](https://github.com/ishimweemmanuel/2048/blob/f2c758557b00270a61a53937649c770a5036c76f/Screenshot%202025-01-13%20134039.png}

## How to Play

1. Install the requirements:
```
pip install -r requirements.txt
```

2. Run the game:
```
python game_2048.py
```

## Game Rules

1. Use arrow keys to move tiles:
   - ↑ (Up Arrow): Move tiles up
   - ↓ (Down Arrow): Move tiles down
   - ← (Left Arrow): Move tiles left
   - → (Right Arrow): Move tiles right

2. When two tiles with the same number touch, they merge into one tile with the sum of their values.

3. After each move, a new tile with a value of either 2 or 4 appears in a random empty cell.

4. The goal is to create a tile with the number 2048.

5. The game ends when there are no more possible moves (the grid is full and no adjacent tiles can be merged).

## Features

- Smooth animations
- Score tracking
- Modern UI design
- Game over detection
- Responsive grid layout
