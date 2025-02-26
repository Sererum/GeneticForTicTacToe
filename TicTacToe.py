import tkinter as tk
from Field import Field
from Player import Player
import random

class TicTacToe:

    SIZE_FIELD = 8

    def __init__(self, root, weights:list[int]):
        self.__init_visual(root)
        self.__init_functional(weights)

    def __init_visual(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.buttons = [[None for _ in range(self.SIZE_FIELD)] for _ in range(self.SIZE_FIELD)]
        self.__create_board()

    def __init_functional(self, weights:list[int]):
        self.field = Field()

        self.me, self.evil = Player.CROSS, Player.ZERO
        self.player = Player(self.evil, 8, weights)

        if random.random() < 0.5:
            row, col = self.player.get_move()
            self.field.set_zero(row, col)
            self.current_player = "O"
            self.__on_button_click_visual(row, col)
            

    def __create_board(self):
        for row in range(self.SIZE_FIELD):
            for col in range(self.SIZE_FIELD):
                button = tk.Button(self.root, text="", width=2, height=1, font=('Helvetica', 40), bg="lightgray",
                                   command=lambda r=row, c=col: self.on_button_click(r, c))
                button.grid(row=row, column=col)
                self.current_player = "X"
                self.buttons[row][col] = button

    def on_button_click(self, row, col):
        self.__on_button_click_visual(row, col)
        self.__on_button_click_funcional(row, col)

    def __on_button_click_visual(self, row, col):
        for button_row in self.buttons:
            for button in button_row:
                button["bg"] = "lightgray"
        
        button = self.buttons[row][col]
        if button["text"] == "":
            button["text"] = self.current_player
            button["bg"] = "green"
            print(f"Кнопка нажата: ({row}, {col}), Игрок: {self.current_player}")
            self.current_player = "O" if self.current_player == "X" else "X"

    def __on_button_click_funcional(self, row, col):
        self.field.set_cross(row, col)
        if self.field.game_is_over():
            self.__show_winner("Вы")
            return
            
        row, col = self.player.get_move(self.field.get_last_move())
        self.field.set_zero(row, col)
        self.__on_button_click_visual(row, col)
        if self.field.game_is_over():
            self.__show_winner("Компьютер")
            return

    def __show_winner(self, player):
        print(f"Игрок {player} победил!")
        winner_label = tk.Label(self.root, bg="black", fg="white", text=f"Игрок {player} победил!", font=("Arial", 40))
        winner_label.grid(row=0, column=0, columnspan=8, rowspan=8)

if __name__ == "__main__":
    weights = list(map(int, input("Input weights: ").split()))
    root = tk.Tk()
    game = TicTacToe(root, weights)
    root.mainloop()
