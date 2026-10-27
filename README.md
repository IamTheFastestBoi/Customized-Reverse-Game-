🟢 Reversi (Othello) - Basic AI

A Customized Reversi (Othello) game made with Python and Pygame. The computer plays using a basic, location-based scoring system.

📖 About the Project

This project is a board game built with Object-Oriented Programming (OOP). The computer (AI) does not look into the future to calculate moves. Instead, it makes decisions using a static 8x8 score map.

The AI uses a "greedy" logic: It always tries to capture the best squares (like corners) and flip as many pieces as possible in its current turn.

“There is difference between my reversi game and classic game . The main difference is in classic reversi when you make a move , that move needs to change at least change one color of piece but you either pc dont need to change color when they make a move . If the position you want to make move is not occipied you are free to move . “

✨ Features

Pygame GUI: A simple and smooth graphical interface with an 8x8 grid (80x80 pixel squares).The pygame GUI was made by AI .

Rule Engine (Referee): It checks 8 different directions to find valid moves and flip the opponent's pieces correctly.

Dynamic Score Map: If the AI captures a corner, it updates the map to make the squares near that corner "safe" and valuable.

Clean Code (OOP): The code is modular and divided into classes: GameEngine, Referee, AI, and Board.

🚀 How to Install and Run

Requirements:
You need to have Python 3.x and the Pygame library installed on your computer.

Install Pygame by running this command in your terminal:

pip install pygame


Start the game:

python main_reverse.py


🎮 How to Play

You play as Black (X), and the computer plays as White (O).

When it is your turn, use your mouse to click on a valid green square to place your piece.

The computer will play its turn automatically.

When the board is completely full, the player with the most pieces wins the game.
