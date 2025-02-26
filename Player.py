from random import randint
from Field import Field
import numpy as np
import os

class Player:

    ZERO, CROSS = 0, 1
    INFINF = 999999
    INF = 999

    __left_border, __up_border, __right_border, __down_border = 4, 4, 0, 0

    def __init__(self, sign:int,  size_field:int, weights:list[int]):
        self.__init_w_positions(weights)

        self.__self_sign = sign
        self.__evil_sign = (1 - sign)
        self.__size_field = size_field

        self.__right_border = self.__left_border + size_field
        self.__down_border = self.__up_border + size_field
        
        self.__positions = np.full((2, size_field + 8, size_field + 8), 0)
        self.__init_weights()
        
    def __init_w_positions(self, weights:list[int]):
        self.__w_positions = {0: 0, 1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 10: -1, 11: -1, 12: -1, 13: -1, 14: -1, 15: 9999, 16: -1, 17: -1, 18: -1, 19: -1, 20: -1, 21: -1, 22: -1, 23: -1, 24: -1, 25: -1, 26: -1, 27: -1, 28: -1, 29: -1, 30: 9999, 31: 9999, 32: -1, 33: -1, 34: -1, 35: -1, 36: -1, 37: -1, 38: -1, 39: -1, 40: -1, 41: -1, 42: -1, 43: -1, 44: -1, 45: -1, 46: -1, 47: 9999, 48: -1, 49: -1, 50: -1, 51: -1, 52: -1, 53: -1, 54: -1, 55: -1, 56: -1, 57: -1, 58: -1, 59: -1, 60: 9999, 61: 9999, 62: 9999, 63: 9999, 64: -1, 65: -1, 66: -1, 67: -1, 68: -1, 69: -1, 70: -1, 71: -1, 72: -1, 73: -1, 74: -1, 75: -1, 76: -1, 77: -1, 78: -1, 79: 9999, 80: -1, 81: -1, 82: -1, 83: -1, 84: -1, 85: -1, 86: -1, 87: -1, 88: -1, 89: -1, 90: -1, 91: -1, 92: -1, 93: -1, 94: 9999, 95: 9999, 96: -1, 97: -1, 98: -1, 99: -1, 100: -1, 101: -1, 102: -1, 103: -1, 104: -1, 105: -1, 106: -1, 107: -1, 108: -1, 109: -1, 110: -1, 111: 9999, 112: -1, 113: -1, 114: -1, 115: -1, 116: -1, 117: -1, 118: -1, 119: -1, 120: 9999, 121: 9999, 122: 9999, 123: 9999, 124: 9999, 125: 9999, 126: 9999, 127: 9999, 128: -1, 129: -1, 130: -1, 131: -1, 132: -1, 133: -1, 134: -1, 135: -1, 136: -1, 137: -1, 138: -1, 139: -1, 140: -1, 141: -1, 142: -1, 143: 9999, 144: -1, 145: -1, 146: -1, 147: -1, 148: -1, 149: -1, 150: -1, 151: -1, 152: -1, 153: -1, 154: -1, 155: -1, 156: -1, 157: -1, 158: 9999, 159: 9999, 160: -1, 161: -1, 162: -1, 163: -1, 164: -1, 165: -1, 166: -1, 167: -1, 168: -1, 169: -1, 170: -1, 171: -1, 172: -1, 173: -1, 174: -1, 175: 9999, 176: -1, 177: -1, 178: -1, 179: -1, 180: -1, 181: -1, 182: -1, 183: -1, 184: -1, 185: -1, 186: -1, 187: -1, 188: 9999, 189: 9999, 190: 9999, 191: 9999, 192: -1, 193: -1, 194: -1, 195: -1, 196: -1, 197: -1, 198: -1, 199: -1, 200: -1, 201: -1, 202: -1, 203: -1, 204: -1, 205: -1, 206: -1, 207: 9999, 208: -1, 209: -1, 210: -1, 211: -1, 212: -1, 213: -1, 214: -1, 215: -1, 216: -1, 217: -1, 218: -1, 219: -1, 220: -1, 221: -1, 222: 9999, 223: 9999, 224: -1, 225: -1, 226: -1, 227: -1, 228: -1, 229: -1, 230: -1, 231: -1, 232: -1, 233: -1, 234: -1, 235: -1, 236: -1, 237: -1, 238: -1, 239: 9999, 240: 9999, 241: 9999, 242: 9999, 243: 9999, 244: 9999, 245: 9999, 246: 9999, 247: 9999, 248: 9999, 249: 9999, 250: 9999, 251: 9999, 252: 9999, 253: 9999, 254: 9999, 255: 9999}
        pos = self.__w_positions

        ind_w = 0

        for key in range(2**8):
            if pos[key] != -1:
                continue

            mask = bin(key + 2**8)[3:]
            pos[int(mask, 2)] = weights[ind_w]
            pos[int(mask[::-1], 2)] = weights[ind_w]
            ind_w += 1

    def __init_weights(self):
        size = self.__size_field
        self.__start_weights = np.full((size, size), 0.0)

        for i in range(size):
            for j in range(size):
                self.__start_weights[i][j] = min(i, j, size - i - 1, size - j - 1) / 10.0

        self.__weigths = np.full((2, size, size), 0.)

    def _check_positions(self):
        pos = self.__w_positions
        for i in range(2**8):
            mask = bin(i+2**8)[3:][::-1]
            print(f"{mask} - {pos[i]}")
            
            if pos[int(mask, 2)] != pos[int(mask[::-1], 2)]:
                print("ERROR")
                break

    def get_move(self, last_move=(-1, -1)):
        me, evil = self.__self_sign, self.__evil_sign
        weights = self.__weigths[me]
        positions = self.__positions

        if (last_move != (-1, -1)):
            positions[evil][last_move[0]+4][last_move[1]+4] = 1

        self.__update_weights()

        max_index = np.argmax(weights)
        row, col = np.unravel_index(max_index, weights.shape)
        positions[me][row+4][col+4] = 1

        return row, col

        
    def __update_weights(self):
        me, evil = self.__self_sign, self.__evil_sign
        weights = self.__weigths[me]

        for row in range(self.__up_border, self.__down_border):
            for col in range(self.__left_border, self.__right_border):
                weights[row-4][col-4] = self.__start_weights[row-4][col-4]
                weights[row-4][col-4] += self.__get_weight(me, row, col) + 1
                weights[row-4][col-4] += self.__get_weight(evil, row, col)
        

    def __get_weight(self, sign:int, row:int, col:int):
        pos = self.__positions[sign]
        if (pos[row][col]):
            return -self.INFINF

        weight = 0

        hor_np_array = pos[row, col-4:col+5]
        hor_mask = self.__get_mask_by_array(hor_np_array)
        weight += self.__w_positions[int(hor_mask, 2)]

        ver_np_array = pos[row-4:row+5, col].T
        ver_mask = self.__get_mask_by_array(ver_np_array)
        weight += self.__w_positions[int(ver_mask, 2)]

        lr_diag_array = [pos[row + i][col + i] for i in range(-4, 5)]
        lr_diag_mask = self.__get_mask_by_array(lr_diag_array)
        weight += self.__w_positions[int(lr_diag_mask, 2)]

        rl_diag_array = [pos[row + i][col - i] for i in range(-4, 5)]
        rl_diag_mask = self.__get_mask_by_array(rl_diag_array)
        weight += self.__w_positions[int(rl_diag_mask, 2)]

        return weight
        
    
    def __get_mask_by_array(self, array):
        int_array = list(map(int, array))
        str_array = list(map(str, int_array))
        mask = "".join(str_array)
        mask = mask[:4] + mask[5:]
        return mask

    def __print_weights(self, weights):
        size = self.__size_field
        for i in range(size):
            for j in range(size):
                w = round(weights[i][j], 1)
                sep = " " * (9 - len(str(w)))
                print(sep, w, sep="", end=" ")
            print()
        print()


if __name__ == "__main__":
    field = Field()

    me, evil = Player.CROSS, Player.ZERO

    weights = list(map(int, input("Input weights: ").split()))
    print(weights)
    player = Player(evil, 8, weights)

    while field.game_is_over() == False:

        row, col = player.get_move(field.get_last_move())
        field._set_sign(evil, row, col)

        field.print_field()

        row, col = map(int, input("Your turn: ").split())
        field._set_sign(me, row, col)

    field.print_field()
