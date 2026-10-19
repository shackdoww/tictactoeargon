"""Tic-Tac-Toe with local two-player and computer modes (Tkinter)."""
import random
import tkinter as tk

LINES = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))


def result(board):
    for a,b,c in LINES:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    return "Draw" if all(board) else None


def minimax(board, bot_turn):
    outcome = result(board)
    if outcome:
        return {"O": 1, "X": -1, "Draw": 0}[outcome]
    scores = []
    for i, value in enumerate(board):
        if not value:
            board[i] = "O" if bot_turn else "X"
            scores.append(minimax(board, not bot_turn))
            board[i] = ""
    return max(scores) if bot_turn else min(scores)


class TicTacToe:
    def __init__(self, root):
        self.root = root
        root.title("Tic-Tac-Toe")
        root.resizable(False, False)
        controls = tk.Frame(root, pady=10)
        controls.pack()
        tk.Label(controls, text="Mode:").pack(side=tk.LEFT, padx=5)
        self.mode = tk.StringVar(value="bot")
        tk.OptionMenu(controls, self.mode, "bot", "two players",
                      command=lambda _: self.reset()).pack(side=tk.LEFT)
        tk.Label(controls, text="Difficulty:").pack(side=tk.LEFT, padx=5)
        self.difficulty = tk.StringVar(value="Easy")
        tk.OptionMenu(controls, self.difficulty, "Easy", "Hard",
                      command=lambda _: self.reset()).pack(side=tk.LEFT)

        self.status = tk.Label(root, font=("Arial", 16), pady=8)
        self.status.pack()
        frame = tk.Frame(root, padx=12, pady=8)
        frame.pack()
        self.buttons = []
        for i in range(9):
            button = tk.Button(frame, text="", font=("Arial", 28, "bold"),
                               width=4, height=2, command=lambda n=i: self.play(n))
            button.grid(row=i//3, column=i%3, padx=3, pady=3)
            self.buttons.append(button)
        tk.Button(root, text="Restart Game", font=("Arial", 12),
                  command=self.reset).pack(pady=(5, 15))
        self.pending = None
        self.reset()

    def reset(self):
        if self.pending is not None:
            self.root.after_cancel(self.pending)
            self.pending = None
        self.board = [""] * 9
        self.player = "X"
        self.over = False
        self.status.config(text="Your turn (X)" if self.mode.get() == "bot"
                           else "Player X's turn")
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL)

    def play(self, index):
        if self.over or self.board[index] or (self.mode.get() == "bot" and self.player == "O"):
            return
        self.place(index)
        if not self.over and self.mode.get() == "bot":
            self.status.config(text="Bot is thinking...")
            self.pending = self.root.after(350, self.bot_move)

    def place(self, index):
        mark = self.player
        self.board[index] = mark
        color = "blue" if mark == "X" else "red"
        self.buttons[index].config(text=mark, state=tk.DISABLED, disabledforeground=color)
        outcome = result(self.board)
        if outcome:
            self.over = True
            if outcome == "Draw":
                message = "It's a draw!"
            elif self.mode.get() == "bot":
                message = "You win!" if outcome == "X" else "Bot wins!"
            else:
                message = f"Player {outcome} wins!"
            self.status.config(text=message)
            for button in self.buttons:
                button.config(state=tk.DISABLED)
            return
        self.player = "O" if mark == "X" else "X"
        self.status.config(text=f"Player {self.player}'s turn")

    def bot_move(self):
        self.pending = None
        if self.over or self.mode.get() != "bot":
            return
        available = [i for i, mark in enumerate(self.board) if not mark]
        if self.difficulty.get() == "Easy":
            choice = random.choice(available)
        else:
            best = -2
            choices = []
            for i in available:
                self.board[i] = "O"
                score = minimax(self.board, False)
                self.board[i] = ""
                if score > best:
                    best, choices = score, [i]
                elif score == best:
                    choices.append(i)
            choice = random.choice(choices)
        self.place(choice)
        if not self.over:
            self.status.config(text="Your turn (X)")


if __name__ == "__main__":
    window = tk.Tk()
    TicTacToe(window)
    window.mainloop()
