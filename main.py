import customtkinter as tk

from ui.app import *
from utils.cache_banderas import init_flags

init_flags("assets/banderas/")


# for i in range(0, 16):
#     aux = Partido(None, None, None)
#     aux.savePartido()
# setEquiposFaseGrupos()
# avanzarFase()
# setEliminatorias()


#todo el resto esta en las views xd

"""cambiar validaciones de fecha"""

# ventana principal
root = App()

# cargarGrupo("Hallownest", "H")

# bs que inicia la appW
root.mainloop()