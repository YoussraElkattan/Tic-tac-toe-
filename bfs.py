import tkinter as tk
import random
from collections import deque


class Game:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = None
        self.winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

    def start(self, player, computer):
        self.player = player
        self.computer = computer
        self.current_player = player
        player.set_game(self)
        computer.set_game(self)
        self.update_display()

    def play(self, position):
        if self.board[position] == " " and not self.is_game_over():
            self.board[position] = self.current_player.symbol
            if self.is_winner():
                self.display_winner()
            elif " " not in self.board:
                self.display_draw()
            else:
                self.current_player = self.computer if self.current_player == self.player else self.player
                self.update_display()
                if self.current_player == self.computer:
                    self.computer.make_move()

    def is_winner(self):
        for a, b, c in self.winning_combinations:
            if self.board[a] == self.board[b] == self.board[c] != " ":
                return True
        return False

    def is_game_over(self):
        return self.is_winner() or " " not in self.board

    def update_display(self):
        for i in range(9):
            buttons[i]["text"] = self.board[i]

    def display_winner(self):
        label.config(text=f"{self.current_player.symbol} wins!")
        self.disable_buttons()

    def display_draw(self):
        label.config(text="It's a draw!")
        self.disable_buttons()

    def disable_buttons(self):
        for button in buttons:
            button.config(state=tk.DISABLED)

    def reset(self):
        for i in range(9):
            self.board[i] = " "
        self.current_player = self.player
        label.config(text="")
        for button in buttons:
            button.config(state=tk.NORMAL)
        if self.current_player == self.computer:
            self.computer.make_move()
        else:
            self.update_display()

class Player:
    def __init__(self, symbol):
        self.symbol = symbol
        self.game = None

    def set_game(self, game):
        self.game = game

class Computer(Player):
    def make_move(self):
        best_move = self.bfs()
        self.game.play(best_move)

    def bfs(self):
        best_score = -float("inf")
        best_move = None

        for i in range(9):
            if self.game.board[i] == " ":
                self.game.board[i] = self.symbol
                score = self.bfs_search(self.game.board)
                self.game.board[i] = " "

                if score > best_score:
                    best_score = score
                    best_move = i

        return best_move

    def bfs_search(self, board):
        queue = deque([(board, self.symbol)])
        scores = {"X": 1, "O": -1, " ": 0}

        while queue:
            current_board, current_symbol = queue.popleft()
            if self.game.is_winner() or " " not in current_board:
                return scores[current_symbol]

            for i in range(9):
                if current_board[i] == " ":
                    next_board = list(current_board)
                    next_board[i] = "X" if current_symbol == "O" else "O"
                    queue.append((next_board, "X" if current_symbol == "O" else "O"))

        return 0


root = tk.Tk()
root.title("Tic-Tac-Toe")

buttons = [tk.Button(root, text=" ", width=10, height=3, command=lambda i=i: game.play(i)) for i in range(9)]

for i in range(9):
    row, col = divmod(i, 3)
    buttons[i].grid(row=row, column=col)

label = tk.Label(root, text="", font=('Helvetica', 20))
label.grid(row=3, column=0, columnspan=3)

game = Game()
player = Player("X")
computer = Computer("O")

game.start(player, computer)

root.mainloop()
