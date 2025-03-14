import pyray as pyr
from math import floor

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
    def __init__(
        self,
        x: int,
        y: int,
        tipo: TipoCelula = TipoCelula.VAZIO,
        fill_level: float = 0.0,
    ):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.fill_level = fill_level

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
        return f"Célula({self.x=}, {self.y=}, {self.tipo=}, {self.cor=}, {self.fill_level=})"


GRID_CELULAS = [
    [Cell(x=i * CELL_SIZE, y=j * CELL_SIZE) for j in range(ROWS + 1)]
    for i in range(COLUMNS + 1)
]


def get_vizinhos(cell: Cell):
    nro_col = int(cell.x / CELL_SIZE)
    nro_lin = int(cell.y / CELL_SIZE)

    vizinhos = [
        (nro_col - 1, nro_lin),
        (nro_col + 1, nro_lin),
        (nro_col, nro_lin + 1),
        (nro_col, nro_lin - 1),
    ]  # A esquerda, A direita, Abaixo e Acima

    return {
        key: val
        for key, val in zip(["L", "R", "D", "U"], vizinhos)
        if 0 <= val[0] <= COLUMNS - 1 and 0 <= val[1] <= ROWS - 1
    }


def fluxo_de_liquidos(cell: Cell):
    vizinhos = get_vizinhos(cell)

    if cell.fill_level < 1.0:
        espaco_celula = 1.0 - cell.fill_level

        if "U" in vizinhos.keys():
            vizinho = GRID_CELULAS[vizinhos["U"][0]][vizinhos["U"][1]]
            if vizinho.tipo == TipoCelula.LIQUIDO and vizinho.fill_level > 0.0:
                transfer = min(espaco_celula, vizinho.fill_level)

                vizinho.fill_level = vizinho.fill_level - transfer
                cell.fill_level = cell.fill_level + transfer

            elif "L" in vizinhos.keys():
                vizinho = GRID_CELULAS[vizinhos["L"][0]][vizinhos["L"][1]]
                if vizinho.tipo == TipoCelula.LIQUIDO and vizinho.fill_level > 0.0:
                    transfer = (cell.fill_level + vizinho.fill_level) / 2

                    vizinho.fill_level = transfer
                    cell.fill_level = transfer

                elif "R" in vizinhos.keys():
                    vizinho = GRID_CELULAS[vizinhos["R"][0]][vizinhos["R"][1]]
                    if vizinho.tipo == TipoCelula.LIQUIDO and vizinho.fill_level > 0.0:
                        transfer = (cell.fill_level + vizinho.fill_level) / 2

                        vizinho.fill_level = transfer
                        cell.fill_level = transfer

    return None


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

        if (0.0 <= pyr.get_mouse_position().x <= float(WIDTH)) and (
            0.0 <= pyr.get_mouse_position().y <= float(HEIGHT)
        ):
            if pyr.is_mouse_button_down(pyr.MouseButton.MOUSE_BUTTON_LEFT):
                GRID_CELULAS[x_cell_mouse][y_cell_mouse].tipo = TipoCelula.SOLIDO
            if pyr.is_mouse_button_down(pyr.MouseButton.MOUSE_BUTTON_MIDDLE):
                GRID_CELULAS[x_cell_mouse][y_cell_mouse].tipo = TipoCelula.VAZIO
                GRID_CELULAS[x_cell_mouse][y_cell_mouse].fill_level = 0.0
            if (
                pyr.is_mouse_button_down(pyr.MouseButton.MOUSE_BUTTON_RIGHT)
                and GRID_CELULAS[x_cell_mouse][y_cell_mouse].tipo != TipoCelula.SOLIDO
            ):
                GRID_CELULAS[x_cell_mouse][y_cell_mouse].tipo = TipoCelula.LIQUIDO
                GRID_CELULAS[x_cell_mouse][y_cell_mouse].fill_level = 1.0

        print(
            GRID_CELULAS[x_cell_mouse][y_cell_mouse].tipo,
            GRID_CELULAS[x_cell_mouse][y_cell_mouse].fill_level,
        )

        for row in GRID_CELULAS:
            for cell in row:
                fluxo_de_liquidos(cell)

                # Atualiza o tipo da célula após o fluxo
                if cell.tipo != TipoCelula.SOLIDO:
                    if cell.fill_level >= 0.0001:
                        cell.tipo = TipoCelula.LIQUIDO
                    if cell.fill_level < 0.0001:
                        cell.tipo = TipoCelula.VAZIO

                if cell.tipo == TipoCelula.LIQUIDO:
                    pyr.draw_rectangle(
                        cell.x,
                        cell.y + int(CELL_SIZE * round(1 - cell.fill_level, 2)),
                        CELL_SIZE - 1,
                        CELL_SIZE - int(CELL_SIZE * round(1 - cell.fill_level, 2)),
                        cell.cor,
                    )
                else:
                    pyr.draw_rectangle(
                        cell.x, cell.y, CELL_SIZE - 1, CELL_SIZE - 1, cell.cor
                    )

        pyr.end_drawing()

    pyr.close_window()


if __name__ == "__main__":
    main()
