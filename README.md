# 🧩 Sudoku Game (Python)

A simple Sudoku game built in Python.  
The game generates a playable Sudoku puzzle, allows user input, and checks for valid moves and completion.

This project is great for practicing Python fundamentals such as:
- 2D lists
- Functions
- Loops and conditionals
- Input validation
- Game logic


## 🎮 Features

- Generates a valid Sudoku puzzle
- Allows players to fill in numbers
- Prevents invalid moves
- Checks for puzzle completion
- Text-based interface (terminal/console)


## 📂 Project Structure
- main.py # code for the graphical interface
- sudoku.py # all the logic (backtracking/recursion) lies here
- README.md

## 🕹️ How to Play
1. The Sudoku board will be displayed in the terminal.
2. Enter your move when prompted:
    - Row number (1–9)
    - Column number (1–9)
    - Value (1–9)
3. The game will:
    - Reject invalid moves
    - Update the board for valid moves
4. Fill all empty cells correctly to win 🎉

## ✅ Rules
1. Each number 1–9 must appear once per row
2. Each number 1–9 must appear once per column
3. Each number 1–9 must appear once per 3×3 subgrid
