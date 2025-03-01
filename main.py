import pyray as pyr
from math import floor
import os

HEIGHT = 450
WIDTH = 900
CELL_SIZE = 15

COLUMNS = int(WIDTH / CELL_SIZE)
ROWS = int(HEIGHT / CELL_SIZE)


COR_BACKGROUND = pyr.BLACK


class TipoCelula(int):
    VAZIO = 0
    SOLIDO = 1
    LIQUIDO = 2


class Cell:
    def __init__(self, x: int, y: int, tipo: TipoCelula = TipoCelula.VAZIO):
        self.x = x
        self.y = y
        self.tipo = tipo

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, novo_tipo):
        self._tipo = novo_tipo
        if novo_tipo == TipoCelula.SOLIDO:
            self.cor = pyr.WHITE
        elif novo_tipo == TipoCelula.LIQUIDO:
            self.cor = pyr.BLUE
        else:
            self.cor = COR_BACKGROUND

    def __repr__(self):
        return f"Célula(x={self.x}, y={self.y}, tipo={self.tipo}, cor={self.cor})"


GRID_CELULAS = [
    [Cell(x=i * CELL_SIZE, y=j * CELL_SIZE) for j in range(ROWS)]
    for i in range(COLUMNS)
]

def main():
    pyr.init_window(WIDTH, HEIGHT, "Simulação")

    while not pyr.window_should_close():
        pyr.begin_drawing()

        # Grid
        for col in range(COLUMNS):
            pos = col * CELL_SIZE
            pyr.draw_line(pos, 0, pos, HEIGHT, pyr.GRAY)

        for row in range(ROWS):
            pos = row * CELL_SIZE
            pyr.draw_line(0, pos, WIDTH, pos, pyr.GRAY)

        # Desenha as celulas como sólidos ou líquidos
        x_cell_mouse = floor(pyr.get_mouse_x() / CELL_SIZE)
        y_cell_mouse = floor(pyr.get_mouse_y() / CELL_SIZE)

        if (
            (0.0 <= pyr.get_mouse_position().x <= float(WIDTH))
            and (0.0 <= pyr.get_mouse_position().y <= float(HEIGHT))
        ):
            if pyr.is_mouse_button_down(pyr.MouseButton.MOUSE_BUTTON_LEFT):
                GRID_CELULAS[x_cell_mouse][y_cell_mouse].tipo =  TipoCelula.SOLIDO
            if pyr.is_mouse_button_down(pyr.MouseButton.MOUSE_BUTTON_RIGHT):
                GRID_CELULAS[x_cell_mouse][y_cell_mouse].tipo =  TipoCelula.VAZIO
            if pyr.is_mouse_button_down(pyr.MouseButton.MOUSE_BUTTON_MIDDLE):
                GRID_CELULAS[x_cell_mouse][y_cell_mouse].tipo =  TipoCelula.LIQUIDO
                

        for row in GRID_CELULAS:
            for cell in row:
                pyr.draw_rectangle(
                    cell.x, cell.y, CELL_SIZE - 1, CELL_SIZE - 1, cell.cor
                )

        pyr.end_drawing()

    pyr.close_window()


if __name__ == "__main__":
    main()
