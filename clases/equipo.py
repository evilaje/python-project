class Equipo:
    def __init__(self, id, pais, abv, prefix, conf, grupo):
        self.id = id
        self.pais = pais
        self.abreviatura = abv
        self.prefijo = prefix
        self.confederacion = conf
        self.grupo = grupo

        # self.saveEquipo("equipos.txt")


    # bs para guardar la data en un archivo
    # podemos usar el identificador para encontrar el lugar
    def saveEquipo(self, file):
          pass