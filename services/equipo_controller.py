from models.equipo import *

def cargarEquipo(nombre:str, pais:str, codigoPais:str, telefono:str, confederacion:str, grupo:str):
    #validaciones hechas en los controllers/front, por eso aca na de na
    equipo:Equipo = Equipo(nombre, pais, codigoPais, telefono, confederacion, grupo)
    equipo.saveEquipo()