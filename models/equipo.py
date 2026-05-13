# le meti puntos aca para poder hacer lo de el scoreboard ese
# en teoria son 3 puntos victoria, 1 empate y 0 si pierde, eso se saca todo de partido
# tengo la idea de que se actualice automaticamente cuando se guarda un partido
class Equipo:
    def __init__(self, id, pais, abv, prefix, conf, grupo):
        self.id = id
        self.pais = pais
        self.abreviatura = abv
        self.prefijo = prefix
        self.confederacion = conf
        self.grupo = grupo
        self.puntos = 0

        # self.saveEquipo()


    # bs para guardar la data en un archivo
    # podemos usar el identificador para encontrar el lugar
    # hay que ordenar los registros por grupo para que sea mas facil encontrar los datos para el scoreboard
    # asi se busca saltando n lineas dependiendo de la cantidad de equipos por grupo y no le fuerza tanto al mierdon
    def saveEquipo(self, filename="data/equipos.txt"):
        with open(filename, 'a') as file:

            # mirar si ya existe el id que se metio en er archivo
            # ese print hay que cambiar por una ventana de error o algo despues
            for line in file:
                if line.startswith(f"{self.id},"):
                    print(f"ID {self.id} ya existe. El equipo no se va a guardar.")
                    return

            # esto busca donde escribir la linea dependiendo del grupo y si no encuentra uno igual o mayor
            # entonces pone abajo mismo
            for line in file:
                aux = line.strip().split(",")
                if aux[5] == self.grupo or (aux[5] > self.grupo):
                    if int(aux[0]) > self.id:
                        file.write(f"{self.id},{self.pais},{self.abreviatura},{self.prefijo},{self.confederacion},{self.grupo},{self.puntos}\n")
                        return
            
            file.write(f"{self.id},{self.pais},{self.abreviatura},{self.prefijo},{self.confederacion},{self.grupo},{self.puntos}\n")
