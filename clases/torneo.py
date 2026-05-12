class Torneo:
    def __init__ (self, nombre, inicio, fin):
        self.nombre = nombre
        self.inicio = inicio
        self.fin = fin

        # self.saveTorneo()


    def saveTorneo(self, filename="../files/torneos.txt"):
        with open(filename, 'a') as file:

            # mirar si ya existe el nombre que se metio en el archivo
            for line in file:
                if line.startswith(f"{self.nombre},"):
                    print(f"Torneo {self.nombre} ya existe. El torneo no se va a guardar.")
                    return

            file.write(f"{self.nombre},{self.inicio},{self.fin}\n")