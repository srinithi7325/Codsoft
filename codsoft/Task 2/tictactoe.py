import traceback
import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.current_player = 'X'
        self.board = [''] * 9
        self.buttons = []

        # Create 3x3 grid of buttons
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.window, text='', font=('Arial', 20), width=5, height=2,
                                  command=lambda x=i*3+j: self.button_click(x))
                button.grid(row=i, column=j)
                self.buttons.append(button)

    def button_click(self, index):
        if self.board[index] == '' and self.current_player == 'X':
            self.board[index] = 'X'
            self.buttons[index].config(text='X')
            if self.check_winner('X'):
                messagebox.showinfo("Game Over", "Player X wins!")
                self.reset_board()
            elif '' not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_board()
            else:
                self.current_player = 'O'
                self.ai_move()

    def ai_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ''
                if score > best_score:
                    best_score = score
                    best_move = i
        if best_move is not None:
            self.board[best_move] = 'O'
            self.buttons[best_move].config(text='O')
            if self.check_winner('O'):
                messagebox.showinfo("Game Over", "AI (O) wins!")
                self.reset_board()
            elif '' not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_board()
            else:
                self.current_player = 'X'

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner('O'):
            return 1
        if self.check_winner('X'):
            return -1
        if '' not in board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ''
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ''
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, player):
        # Check rows
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] == player:
                return True
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] == player:
                return True
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] == player:
            return True
        if self.board[2] == self.board[4] == self.board[6] == player:
            return True
        return False

    def reset_board(self):
        self.board = [''] * 9
        self.current_player = 'X'
        for button in self.buttons:
            button.config(text='')

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    print("Starting Tic-Tac-Toe game...")
    try:
        game = TicTacToe()
        print("Tkinter window created, entering mainloop...")
        game.run()
    except Exception as e:
        print("Error occurred:", e)
        import traceback
        traceback.print_exc()