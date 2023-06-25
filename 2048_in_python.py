import random
import tkinter as tk
from tkinter import messagebox


class Game2048(tk.Tk):
    def __init__(self):
        super().__init__()

        self.grid_size = 4
        self.tile_size = 100
        self.font = ('Verdana', 40, 'bold')
        self.score = 0

        self.tiles = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        self.title("2048")
        self.geometry(f"{self.grid_size * self.tile_size}x{self.grid_size * self.tile_size}")

        self.canvas = tk.Canvas(self, bg='white', width=self.grid_size * self.tile_size,
                                height=self.grid_size * self.tile_size)
        self.canvas.pack()

        self.bind('<Key>', self.key_pressed)

        self.add_tile()
        self.add_tile()
        self.draw_tiles()

        self.show_walkthrough()

    def show_walkthrough(self):
        # to display a message box with instructions for the game
        messagebox.showinfo("2048 Game", "Welcome to 2048! Use the arrow keys to move the tiles. The goal is to merge "
                                         "tiles with the same number to reach the 2048 tile. Good luck!")

    def add_tile(self):
        # to add a new tile with a value of 2 or 4 to a random empty cell
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.tiles[i][j] == 0]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.tiles[row][col] = random.choice([2, 4])

    def draw_tiles(self):
        # to draw the tiles on the canvas
        self.canvas.delete('tile')
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x = j * self.tile_size
                y = i * self.tile_size
                tile_value = self.tiles[i][j]
                color = self.get_tile_color(tile_value)
                self.canvas.create_rectangle(x, y, x + self.tile_size, y + self.tile_size, fill=color, tags='tile')
                if tile_value != 0:
                    self.canvas.create_text(x + self.tile_size // 2, y + self.tile_size // 2, text=str(tile_value),
                                            fill='black', font=self.font, tags='tile')
        self.update()  # Update the canvas

    def get_tile_color(self, value):
        # to return the color for a tile based on its value
        colors = {
            0: '#CDC1B4',
            2: '#EEE4DA',
            4: '#EDE0C8',
            8: '#F2B179',
            16: '#F59563',
            32: '#F67C5F',
            64: '#F65E3B',
            128: '#EDCF72',
            256: '#EDCC61',
            512: '#EDC850',
            1024: '#EDC53F',
            2048: '#EDC22E',
        }
        return colors.get(value, '#000000')

    def key_pressed(self, event):
        # to handle key press events
        key = event.keysym.lower()
        if key == 'left':
            self.move_left()
        elif key == 'right':
            self.move_right()
        elif key == 'up':
            self.move_up()
        elif key == 'down':
            self.move_down()
        self.add_tile()
        self.draw_tiles()
        if self.check_game_over():
            self.after(500, self.show_game_over_message)

    def move_left(self):
        # to move the tiles to the left and merge adjacent tiles
        for row in self.tiles:
            self.merge_tiles(row)
            row[:] = self.compress_tiles(row)

    def move_right(self):
        # to move the tiles to the right and merge adjacent tiles
        for row in self.tiles:
            row.reverse()
            self.merge_tiles(row)
            row[:] = self.compress_tiles(row)
            row.reverse()

    def move_up(self):
        # to move the tiles up and merge adjacent tiles
        self.transpose_tiles()
        self.move_left()
        self.transpose_tiles()

    def move_down(self):
        # to move the tiles down and merge adjacent tiles
        self.transpose_tiles()
        self.move_right()
        self.transpose_tiles()

    def merge_tiles(self, row):
        # to merge adjacent tiles with the same value
        for i in range(len(row) - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0

    @staticmethod
    def compress_tiles(row):
        # to compress the tiles by removing empty cells and shifting non-empty cells to the left
        new_row = [tile for tile in row if tile != 0]
        new_row += [0] * (len(row) - len(new_row))
        return new_row

    def transpose_tiles(self):
        # to transpose the tiles matrix (swap rows and columns)
        self.tiles = [list(row) for row in zip(*self.tiles)]

    def check_game_over(self):
        # to check if the game is over (no more valid moves)
        for row in self.tiles:
            if 2048 in row:
                return True
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.tiles[i][j] == 0:
                    return False
                if i < self.grid_size - 1 and self.tiles[i][j] == self.tiles[i + 1][j]:
                    return False
                if j < self.grid_size - 1 and self.tiles[i][j] == self.tiles[i][j + 1]:
                    return False
        return True

    def show_game_over_message(self):
        # to display a message box with the "game over" message and final score
        messagebox.showinfo("Game Over", f"Game Over! Your score is {self.score}.")


if __name__ == '__main__':
    game = Game2048()
    game.mainloop()
