import tkinter as tk
import random
import tkinter.messagebox as messagebox

class Minesweeper:
    def __init__(self, master, rows, cols, num_mines):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]  # ボードの初期化
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]  # ボタンの初期化
        self.game_over = False  # ゲームの状態

        self.create_widgets()  # GUIの作成
        self.place_mines()  # 地雷の配置
        self.calculate_numbers()  # 数字の計算

    def create_widgets(self):
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # ボタンの配置
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(self.frame, width=2, command=lambda r=row, c=col: self.click(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

        # ウィンドウのサイズを調整
        self.master.geometry(f"{self.cols * 30}x{self.rows * 30}")

    def place_mines(self):
        mines_placed = 0
        # 地雷の配置
        while mines_placed < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if self.board[row][col] != -1:
                self.board[row][col] = -1
                mines_placed += 1

    def calculate_numbers(self):
        # 各セルの数字の計算
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    continue
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if 0 <= row + dr < self.rows and 0 <= col + dc < self.cols and self.board[row + dr][col + dc] == -1:
                            count += 1
                self.board[row][col] = count

    def click(self, row, col):
        if self.game_over:
            return
        button = self.buttons[row][col]
        button.config(state="disabled")
        if self.board[row][col] == -1:
            # 地雷に当たった場合
            button.config(text="X", relief=tk.SUNKEN)
            self.game_over = True
            self.reveal_board()
            messagebox.showinfo("Game Over", "You hit a mine! Game Over.")
        else:
            count = self.board[row][col]
            if count == 0:
                button.config(relief=tk.SUNKEN)
                self.reveal_empty(row, col)
            else:
                button.config(text=str(count), relief=tk.SUNKEN)

    def reveal_empty(self, row, col):
        # 空のセルを再帰的に開く
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r = row + dr
                c = col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    button = self.buttons[r][c]
                    if button["state"] == "normal":
                        self.click(r, c)

    def reveal_board(self):
        # ボード全体を表示する
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == -1:
                    self.buttons[row][col].config(text="X", relief=tk.SUNKEN)

def main():
    root = tk.Tk()
    root.title("Minesweeper")
    rows = 10
    cols = 10
    num_mines = 10
    game = Minesweeper(root, rows, cols, num_mines)
    root.mainloop()

if __name__ == "__main__":
    main()
