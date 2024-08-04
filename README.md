# Chess Engine

## Overview
Welcome to the Chess Engine project! This repository contains a chess engine built in Python, featuring both a text-based and a graphical interface using `pygame`. The project is structured around object-oriented principles, making it modular and extensible. The chessboard, pieces, and game logic are implemented as classes, allowing for easy modification and expansion.

## Features
- **Chessboard Representation**: The `Chessboard` class handles the creation, display, and management of the board and pieces.
- **Object-Oriented Design**: Each chess piece is represented as a class inheriting from a base `Chesspiece` class. This design allows for easy extension and customization of piece behavior.
- **Move Validation**: The engine includes logic to validate moves, detect check and checkmate, and enforce the rules of chess.
- **Graphical Interface**: The project uses `pygame` to provide a graphical interface for playing chess, including rendering the board and pieces and handling user input.

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/KymaiselHunter/ChessPython.git
   cd ChessPython
   ```
2. **Install dependencies:**:
   This project requires Python 3.x and the pygame library.
   Install the necessary packages using pip:
   ```bash
   pip install pygame
   ```
## Usage
In the current state of the project, running main.py will initialize a chessboard and display it using pygame.
The code also contains several commented-out sections for testing different aspects of the engine, such as setting up a custom board, clearing the board, and testing vision and valid moves for the pieces.

The graphical interface (playGameGraphic) provides an interactive way to play chess, allowing you to move pieces on the board by clicking on them.
   ```bash
   python main.py
   ```

## Code Overview

The main file `main.py` includes:
- **Initialization and Display**: Sets up a chessboard and displays it using `pygame`.
- **Testing and Debugging**: Contains commented-out code for testing various functionalities of the chess engine.

### Main Components
- `Chesspiece`: Base class for all chess pieces, handling common attributes like coordinates, vision, and valid moves.
- `Pawn`, `King`, `Queen`, `Bishop`, `Knight`, `Rook`: Subclasses of `Chesspiece` representing different types of chess pieces with their unique behaviors and attributes.
- `Chessboard`: Manages the board, pieces, and game logic, including updating vision and valid moves for each piece.

## Future Development
- **Enhanced Graphics**: Improving the `pygame` interface with better graphics and animations.
- **Undo/Redo Feature**: Adding functionality to undo and redo moves.
## Far Future Development
- **AI Opponent**: Implementing an AI opponent using Minimax or other algorithms.

## Shoutout
Thank you for my sister, who made the art of the chess pieces!
