class Torneo:
	def __init__ (self, nombre: str, inicio:str, fin:str):
		self.nombre = nombre
		self.inicio = inicio #DD/MM/AAAA
		self.fin = fin #DD/MM/AAAA

		# self.saveTorneo()


	def saveTorneo(self, filename="data/torneos.txt"):
		with open(filename, 'a+') as file:

			# mirar si ya existe el nombre que se metio en el archivo
			for line in file:
				if line.startswith(f"{self.nombre},"):
					print(f"Torneo {self.nombre} ya existe. El torneo no se va a guardar.")
					return

			file.write(f"{self.nombre},{self.inicio},{self.fin}\n")

	def editTorneo(self, inicio:str, fin:str):
		#tengo pensado que no se pueden cambiar los nombres de los torneos, solo las fechas
		self.inicio = inicio
		self.fin = fin
		#aca hay que hacer un rewrite del archivo, no se puede editar una linea especifica
		#o capaz hay otra manera, pero no se me ocurre ahora jeje igual es solo por tener esta funcion, ahora es useless
		pass


#utils
def selectTorneo(nombre, filename="data/torneos.txt"):
	with open(filename, 'r') as file:
		for line in file:
			if line.startswith(f"{nombre},"):
				return line.strip().split(",")

		print(f"Torneo {nombre} no encontrado.")
		return None
