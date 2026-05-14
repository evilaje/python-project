from models.partido import *

def cargarPartido(fecha:str, hora:str, lugar:str, idT1:int, idT2:int):
    #validaciones hechas en los controllers/front, por eso aca na de na
    partido:Partido = Partido(fecha, hora, lugar, idT1, idT2)
    partido.savePartido()
    
# testeo
# p1 = Partido("14/05/2026", "12:00", "La nueva Olla", 0, 0)
# p1.savePartido()
