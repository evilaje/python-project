class Equipo:
    def __init__(self, id, pais, abv, prefix, conf, grupo):
        self.id = id
        self.pais = pais
        self.abreviatura = abv
        self.prefijo = prefix
        self.confederacion = conf
        self.grupo = grupo

        # self.saveEquipo()


    # bs para guardar la data en un archivo
    # podemos usar el identificador para encontrar el lugar
    def saveEquipo(self, filename="../files/equipos.txt"):
        with open(filename, 'a') as file:

            # mirar si ya existe el id que se metio en er archivo
            # ese print hay que cambiar por una ventana de error o algo despues
            for line in file:
                if line.startswith(f"{self.id},"):
                    print(f"ID {self.id} ya existe. El equipo no se va a guardar.")
                    return

            file.write(f"{self.id},{self.pais},{self.abreviatura},{self.prefijo},{self.confederacion},{self.grupo}\n")
