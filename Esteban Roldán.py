import tkinter as tk
import random

# --- Clases lógicas --- #

class Barco:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.hundido = False

class Tablero:
    def __init__(self, tamaño=5):
        self.tamaño = tamaño
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

# --- Clase principal con interfaz gráfica PvP --- #
class JuegoBatallaNaval:
    def __init__(self, root):
        self.root = root
        self.root.title("Batalla Naval PvP")

        self.tamaño = 5
        self.barcos_por_jugador = 3

        self.jugador1_tablero = Tablero(self.tamaño)
        self.jugador2_tablero = Tablero(self.tamaño)

        self.jugador1_botones = []
        self.jugador2_botones = []

        self.estado = "colocando1"
        self.barcos_colocados = 0

        self.turno = 1

        self.mensaje = tk.Label(root, text="Jugador 1: Coloca tus barcos")
        self.mensaje.grid(row=0, column=0, columnspan=12)

        self.crear_tableros()

        self.boton_turno = tk.Button(root, text="Pasar turno", command=self.pasar_turno)
        self.boton_turno.grid(row=self.tamaño + 3, column=0, columnspan=12)

    def crear_tableros(self):
        for i in range(self.tamaño):
            fila_botones_j1 = []
            fila_botones_j2 = []
            for j in range(self.tamaño):
                b1 = tk.Button(self.root, text="~", width=3, command=lambda i=i, j=j: self.accion_jugador(1, i, j))
                b1.grid(row=i + 1, column=j)
                fila_botones_j1.append(b1)

                b2 = tk.Button(self.root, text="~", width=3, command=lambda i=i, j=j: self.accion_jugador(2, i, j))
                b2.grid(row=i + 1, column=j + self.tamaño + 3)
                fila_botones_j2.append(b2)

            self.jugador1_botones.append(fila_botones_j1)
            self.jugador2_botones.append(fila_botones_j2)

        tk.Label(self.root, text="Jugador 1").grid(row=self.tamaño + 2, column=1, columnspan=4)
        tk.Label(self.root, text="Jugador 2").grid(row=self.tamaño + 2, column=self.tamaño + 4, columnspan=4)

        # Línea divisoria
        for i in range(1, self.tamaño + 1):
            separador = tk.Label(self.root, text="|", width=1)
            separador.grid(row=i, column=self.tamaño + 1)

    def accion_jugador(self, jugador, fila, col):
        if self.estado.startswith("colocando"):
            if (jugador == 1 and self.estado == "colocando1") and self.jugador1_tablero.colocar_barco(fila, col):
                self.jugador1_botones[fila][col].config(text="B", bg="blue")
                self.barcos_colocados += 1
                if self.barcos_colocados == self.barcos_por_jugador:
                    self.estado = "colocando2"
                    self.barcos_colocados = 0
                    self.ocultar_tablero(self.jugador1_botones)
                    self.mensaje.config(text="Jugador 2: Coloca tus barcos")
            elif (jugador == 2 and self.estado == "colocando2") and self.jugador2_tablero.colocar_barco(fila, col):
                self.jugador2_botones[fila][col].config(text="B", bg="green")
                self.barcos_colocados += 1
                if self.barcos_colocados == self.barcos_por_jugador:
                    self.estado = "jugando"
                    self.ocultar_tablero(self.jugador2_botones)
                    self.mensaje.config(text="Turno de Jugador 1: Dispara")

        elif self.estado == "jugando":
            if self.turno == 1 and jugador == 2:
                if (fila, col) not in self.jugador2_tablero.disparos:
                    resultado = self.jugador2_tablero.recibir_disparo(fila, col)
                    self.jugador2_botones[fila][col].config(text="X" if resultado == "tocado" else "O",
                                                           bg="red" if resultado == "tocado" else "gray")
                    if self.jugador2_tablero.todos_hundidos():
                        self.mensaje.config(text="¡Jugador 1 gana!")
                        self.estado = "final"
                    else:
                        self.turno = 2
                        self.ocultar_tablero(self.jugador2_botones)
                        self.mensaje.config(text="Turno de Jugador 2: Dispara")
            elif self.turno == 2 and jugador == 1:
                if (fila, col) not in self.jugador1_tablero.disparos:
                    resultado = self.jugador1_tablero.recibir_disparo(fila, col)
                    self.jugador1_botones[fila][col].config(text="X" if resultado == "tocado" else "O",
                                                           bg="red" if resultado == "tocado" else "gray")
                    if self.jugador1_tablero.todos_hundidos():
                        self.mensaje.config(text="¡Jugador 2 gana!")
                        self.estado = "final"
                    else:
                        self.turno = 1
                        self.ocultar_tablero(self.jugador1_botones)
                        self.mensaje.config(text="Turno de Jugador 1: Dispara")

    def ocultar_tablero(self, botones):
        for fila in botones:
            for b in fila:
                if b["text"] == "B":
                    b.config(text="~", bg="SystemButtonFace")

    def pasar_turno(self):
        if self.estado == "jugando":
            if self.turno == 1:
                self.mostrar_tablero(self.jugador2_botones)
                self.mensaje.config(text="Turno de Jugador 2: Dispara")
            elif self.turno == 2:
                self.mostrar_tablero(self.jugador1_botones)
                self.mensaje.config(text="Turno de Jugador 1: Dispara")

    def mostrar_tablero(self, botones):
        for fila in botones:
            for b in fila:
                if b["bg"] == "red" or b["bg"] == "gray":
                    continue
                b.config(text="~", bg="SystemButtonFace")

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoBatallaNaval(root)
    root.mainloop()
