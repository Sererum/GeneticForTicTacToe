import numpy as np
from scipy.ndimage import convolve
from random import randint

class Field:

    SIZE_FIELD = 8
    ZERO, CROSS = 0, 1

    __game_over = False
    __win_sign = -1
    __last_move = (-1, -1)

    def __init__(self):
        size = self.SIZE_FIELD

        self.__field = np.full((2, size, size), 0)
        self.__zeros = self.__field[0]
        self.__cross = self.__field[1]

    def _set_sign(self, sign:int, row:int, col:int):
        if (self.__zeros[row][col] or self.__cross[row][col] or row == col == -1):
            #print(f"ERROR, sign is already place in {row}, {col}")
            self.__last_move = (-1, -1)
            return 1
        
        self.__field[sign][row][col] = 1
        self.__last_move = (row, col)
        self.__check_game_over(sign)
        return 0
        

    def __check_game_over(self, sign:int):
        matrix = self.__field[sign]

        kernel_h = np.array([[1, 1, 1, 1, 1]])
        kernel_v = kernel_h.T
        kernel_d1 = np.eye(5, dtype=int)
        kernel_d2 = np.fliplr(kernel_d1)

        # Применяем свёртку для каждого шаблона
        conv_h = convolve(matrix, kernel_h, mode='constant', cval=0)
        conv_v = convolve(matrix, kernel_v, mode='constant', cval=0)
        conv_d1 = convolve(matrix, kernel_d1, mode='constant', cval=0)
        conv_d2 = convolve(matrix, kernel_d2, mode='constant', cval=0)

        # Проверяем, есть ли результат свёртки, равный 5 (то есть пять единиц подряд)
        if (np.any(conv_h == 5) or np.any(conv_v == 5) or
            np.any(conv_d1 == 5) or np.any(conv_d2 == 5)):
            self.__game_over = True
            self.__win_sign = sign

    def set_cross(self, row:int, col:int):
        self._set_sign(self.CROSS, row, col)

    def set_zero(self, row:int, col:int):
        self._set_sign(self.ZERO, row, col)

    def print_field(self):
        size = self.SIZE_FIELD
        cross = self.__cross
        zeros = self.__zeros
        print("  0 1 2 3 4 5 6 7")
        for i in range(0, size):
            print(f"{i}|", end="")
            for j in range(0, size):
                sign = "X" if cross[i][j] else "O" if zeros[i][j] else " "
                print(f"{sign}", end="|")
            print()

        if self.__game_over:
            print("\nGAME IS OVER. ", end="")
            winner = "Cross" if self.__win_sign else "Zeros"
            print(f"{winner} win!")

    def game_is_over(self):
        return self.__game_over
    
    def get_win_sign(self):
        return self.__win_sign
    
    def get_field(self):
        return self.__field
    
    def get_last_move(self):
        return self.__last_move

if __name__ == "__main__":
    f = Field()

    while f.game_is_over() == False:
        f.set_cross(randint(0, 7), randint(0, 7))
        f.print_field()

        row, col = map(int, input("Your turn: ").split())
        f.set_zero(row, col)
    
    f.print_field()