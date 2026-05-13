# esto se puede ampliar para guardar el minuto del gol y eso
# o que jugador metio pero idk

# lo del jugador solo si es un str suelto ahi porque class jugador no tenemos xd
# un nroPartido capaz haga falta igual
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

    # muchas verificaciones
    # no puede haber un partido con la misma fecha, hora, lugar
    # hay qiue ver que un equipo no juegue dos partidos al mismo tiempo
    def savePartido(self, filename="data/partidos.txt"):
        for line in open(filename, 'r'):

            # revisar
            if self.fecha in line and self.hora in line and self.lugar in line:
                print("Ya hay un partido programado en ese espacio y tiempo")
                return
            elif self.fecha in line and self.hora in line:
                if str(self.idEquipo1) in line or str(self.idEquipo2) in line:
                    print("Uno de los equipos ya tiene un partido programado en ese espacio y tiempo")
                    return


        with open(filename, 'a') as file:
            file.write(f"{self.fecha},{self.hora},{self.lugar},{self.idEquipo1},{self.idEquipo2},{self.golesT1},{self.golesT2},{self.penalesT1},{self.penalesT2}\n")

        for line in open("data/equipos.txt", 'r'):
            if line.startswith(f"{self.idEquipo1},"):
                equipo1 = line.strip().split(",")
            elif line.startswith(f"{self.idEquipo2},"):
                equipo2 = line.strip().split(",")

        # actualizar puntos de los equipos
        if self.golesT1 > self.golesT2:
            equipo1[6] = str(int(equipo1[6]) + 3)
        elif self.golesT1 < self.golesT2:
            equipo2[6] = str(int(equipo2[6]) + 3)
        else:
            equipo1[6] = str(int(equipo1[6]) + 1)
            equipo2[6] = str(int(equipo2[6]) + 1)

        # aca un rewrite del archivo, no se si se puede editar solo una linea xd
        with open("data/equipos.txt", 'w') as file:
            for line in open("data/equipos.txt", 'r'):
                if line.startswith(f"{self.idEquipo1},"):
                    file.write(",".join(equipo1) + "\n")
                elif line.startswith(f"{self.idEquipo2},"):
                    file.write(",".join(equipo2) + "\n")
                else:
                    file.write(line)
