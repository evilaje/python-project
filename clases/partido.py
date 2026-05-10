# esto se puede ampliar para guardar el minuto del gol y eso
# o que jugador metio pero idk

class Partido:
    def __init__(self, date, hora, lugar, idT1, idT2):
        self.fecha = date
        self.hora = hora
        self.lugar = lugar
        self.idEquipo1 = idT1
        self.idEquipo2 = idT2
        self.golesT1 = 0
        self.golesT2 = 0
        self.penalesT1 = 0
        self.penalesT2 = 0