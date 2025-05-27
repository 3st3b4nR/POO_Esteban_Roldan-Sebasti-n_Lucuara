import tkinter as tk
import random

# --- Clases lógicas --- #
class Barco:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.hundido = False

class Tablero:
    def __init__(self, tamano=5):
        self.tamano = tamano
        self.barcos = []
        self.disparos = []

    def colocar_barco(self, fila, columna):
        if not self.hay_barco_en(fila, columna):
            self.barcos.append(Barco(fila, columna))
            return True
        return False

    def hay_barco_en(self, fila, columna):
        return any(b.fila == fila and b.columna == columna for b in self.barcos)

    def recibir_disparo(self, fila, columna):
        self.disparos.append((fila, columna))
        for b in self.barcos:
            if b.fila == fila and b.columna == columna:
                b.hundido = True
                return "tocado"
        return "agua"

    def todos_hundidos(self):
        return all(b.hundido for b in self.barcos)

# --- Clase principal con interfaz gráfica --- #
class JuegoPvP:
    def __init__(self, root):
        self.root = root
        self.root.title("Batalla Naval PvP")

        self.tamano = 5
        self.barcos_por_jugador = 3

        self.tableros = [Tablero(self.tamano), Tablero(self.tamano)]
        self.botones = [[], []]
        self.turno = 0  # 0 para jugador 1, 1 para jugador 2
        self.estado = "colocando"
        self.barcos_colocados = [0, 0]

        self.mensaje = tk.Label(root, text="Jugador 1: coloca tus barcos")
        self.mensaje.grid(row=0, column=0, columnspan=10)

        self.crear_tableros()

        self.boton_turno = tk.Button(root, text="Pasar turno", command=self.pasar_turno, state="disabled")
        self.boton_turno.grid(row=self.tamano + 3, column=0, columnspan=10)

    def crear_tableros(self):
        for jugador in [0, 1]:
            matriz = []
            for i in range(self.tamano):
                fila = []
                for j in range(self.tamano):
                    b = tk.Button(self.root, text="~", width=3,
                                  command=lambda i=i, j=j, jugador=jugador: self.accion(i, j, jugador))
                    b.grid(row=i + 1, column=j + (0 if jugador == 0 else self.tamano + 2))
                    fila.append(b)
                matriz.append(fila)
            self.botones[jugador] = matriz

        tk.Label(self.root, text="Tablero Jugador 1").grid(row=self.tamano + 2, column=1, columnspan=4)
        tk.Label(self.root, text="Tablero Jugador 2").grid(row=self.tamano + 2, column=self.tamano + 3, columnspan=4)

    def accion(self, fila, col, tablero_id):
        if self.estado == "colocando":
            if self.turno == tablero_id:
                if self.tableros[self.turno].colocar_barco(fila, col):
                    self.botones[self.turno][fila][col].config(text="B", bg="blue")
                    self.barcos_colocados[self.turno] += 1
                    if self.barcos_colocados[self.turno] == self.barcos_por_jugador:
                        if self.turno == 0:
                            self.turno = 1
                            self.mensaje.config(text="Jugador 2: coloca tus barcos")
                        else:
                            self.estado = "jugando"
                            self.turno = 0
                            self.ocultar_barcos()
                            self.mensaje.config(text="Jugador 1: dispara al tablero enemigo")

        elif self.estado == "jugando":
            enemigo = 1 - self.turno
            if tablero_id == enemigo and (fila, col) not in self.tableros[enemigo].disparos:
                resultado = self.tableros[enemigo].recibir_disparo(fila, col)
                if resultado == "tocado":
                    self.botones[enemigo][fila][col].config(text="X", bg="red")
                else:
                    self.botones[enemigo][fila][col].config(text="O", bg="gray")

                if self.tableros[enemigo].todos_hundidos():
                    self.estado = "final"
                    self.mensaje.config(text=f"Jugador {self.turno + 1} ha ganado!")
                else:
                    self.boton_turno.config(state="normal")

    def pasar_turno(self):
        self.turno = 1 - self.turno
        self.mensaje.config(text=f"Jugador {self.turno + 1}: dispara al tablero enemigo")
        self.boton_turno.config(state="disabled")
        self.ocultar_barcos()

    def ocultar_barcos(self):
        for jugador in [0, 1]:
            for i in range(self.tamano):
                for j in range(self.tamano):
                    b = self.botones[jugador][i][j]
                    if (i, j) in self.tableros[jugador].disparos:
                        if self.tableros[jugador].hay_barco_en(i, j):
                            b.config(text="X", bg="red")
                        else:
                            b.config(text="O", bg="gray")
                    else:
                        b.config(text="~", bg="SystemButtonFace")

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoPvP(root)
    root.mainloop()