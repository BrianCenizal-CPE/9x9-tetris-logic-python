# 9x9 Tetris Logic (Python)

A robust, from-scratch Tetris engine built entirely using Python lists and pure backend logic. Developed from first principles without referencing existing source code, this project focuses on algorithmic fundamentals and defensive programming.

## Key Features
-Implemented a "Future Projection" algorithm (`can_it_fit`) that validates coordinates before movement or rotation occurs, preventing piece-clipping.
-Game logic is separated from data. All 6 classic Tetrominos (O, T, S, Z, J, L) are stored in a modular `shapes.py` file with 4 rotation states each.
-Utilizes `msvcrt` for non-blocking keyboard input in a Windows console environment.
-Developed a "Buffer Flush" system to handle rapid key-spamming, ensuring the game remains synchronized even under heavy user input.
-Implements a "Pre-spawn Validation" that checks if the next random piece can legally enter the playfield before spawning.

## Technical Logic
-The game operates on a 9x9 primary playfield (list of lists).
-Each 3x3 shape container is mapped onto the 9x9 grid using an anchor-point system (X, Y).
-Uses dynamic list manipulation (`pop` and `insert`) to clear filled horizontal rows and shift the remaining stack downward.

## Project Structure
- `main.py`: The core game loop, gravity logic, and input handling.
- `shapes.py`: The data library containing all shape states and rotations.

## How to Run
1. Ensure you are on a Windows environment (for `msvcrt` support).
2. Download both `main.py` and `shapes.py` into the same folder.
3. Run the game via terminal:
   `python main.py`
