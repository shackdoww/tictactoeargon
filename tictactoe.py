"""Simple two-player Tic-Tac-Toe game using Tkinter."""

import tkinter as tk

WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)

        self.status = tk.Label(root, font=("Arial", 16), pady=12)
        self.status.pack()

        board_frame = tk.Frame(root, padx=12, pady=8)
        board_frame.pack()
        self.buttons = []
        for index in range(9):
            button = tk.Button(
                board_frame,
                text="",
                font=("Arial", 28, "bold"),
                width=4,
                height=2,
                command=lambda i=index: self.play(i),
            )
            button.grid(row=index // 3, column=index % 3, padx=3, pady=3)
            self.buttons.append(button)

        tk.Button(root, text="Restart Game", font=("Arial", 12),
                  command=self.reset).pack(pady=(5, 15))
        self.reset()

    def reset(self):
        self.board = [""] * 9
        self.player = "X"
        self.game_over = False
        self.status.config(text="Player X's turn")
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL, fg="black")

    def play(self, index):
        if self.game_over or self.board[index]:
            return

        self.board[index] = self.player
        self.buttons[index].config(
            text=self.player,
            fg="blue" if self.player == "X" else "red",
            state=tk.DISABLED,
            disabledforeground="blue" if self.player == "X" else "red",
        )

        for line in WINNING_LINES:
            if all(self.board[i] == self.player for i in line):
                self.status.config(text=f"Player {self.player} wins!")
                self.finish()
                return

        if all(self.board):
            self.status.config(text="It's a draw!")
            self.finish()
            return

        self.player = "O" if self.player == "X" else "X"
        self.status.config(text=f"Player {self.player}'s turn")

    def finish(self):
        self.game_over = True
        for button in self.buttons:
            button.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()
