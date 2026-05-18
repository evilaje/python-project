import customtkinter as tk
from services.torneo_controller import *
from datetime import datetime
from services.equipo_controller import *
# este es para los popUps, ponele un title, mensaje y icon nomas, icon acepta las palabras cancel, warning y check
from CTkMessagebox import CTkMessagebox


class TorneoConfigFrame(tk.CTkFrame):
    def __init__(self, root, main_frame):
        super().__init__(root)
        self.root = root
        self.main_frame = main_frame

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        """vista 1 - torneo"""
        self.vista1()

        # -----------------------------------------------------------------------------------------------

        """aca empieza la pagina 2 o vista 2 idk es lo de los grupos"""
        self.vista2()

    #----------------------------------------------------------------------------------------------------------
    """vista 3 por aca"""

    # esta es la funcion para cambiar de pagina
    def go_to_grupos(self):
        # grid remove borra el grid pero no el frame, entonces podes llamar grid otra vez para volver a mostrar
        self.frame_torneo.grid_remove()
        # se habilita el grid
        self.frame_grupos.grid(row=0, column=0, columnspan=3, rowspan=5, sticky="nsew")

    def go_to_torneo(self):
        self.frame_grupos.grid_remove()
        self.frame_torneo.grid(row=0, column=0, columnspan=3, rowspan=5, sticky="nsew")

    def guardar_data_torneo(self):
        nombre = self.input_nombre.get().strip()
        fecha_inicio = self.input_fecha_inicio.get().strip()
        fecha_fin = self.input_fecha_fin.get().strip()

        if not nombre or not fecha_inicio or not fecha_fin:
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios", icon="cancel")
            return

        try:
            dt_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
            dt_fin = datetime.strptime(fecha_fin, "%d/%m/%Y")
        except ValueError:
            CTkMessagebox(title="Error", message="Formato de fecha invalido, usa DD/MM/AAAA", icon="cancel")
            return

        hoy = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        if dt_inicio < hoy:
            CTkMessagebox(title="Error", message="La fecha de inicio no puede ser anterior a hoy", icon="cancel")
            return

        if dt_fin <= dt_inicio:
            CTkMessagebox(title="Error", message="La fecha de fin debe ser posterior a la de inicio", icon="cancel")
            return

        cargarTorneo(nombre, fecha_inicio, fecha_fin)
        CTkMessagebox(title="Exito", message="Torneo guardado correctamente", icon="check")

    def guardar_grupos(self):
        grupo = self.comboGrupo.get().strip()
        pais = self.paisInput.get().strip()
        abv = self.abvInput.get().strip()
        pref = self.prefixInput.get().strip()
        conf = self.confInput.get().strip()

        #validaciones de campos vacios
        if not grupo or not pais or not abv or not pref or not conf:
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios", icon="cancel")
            return
        resultado = cargarEquipo(pais, abv, pref, conf, grupo)
        if (resultado[0]):
            CTkMessagebox(title="Exito", message=resultado[1], icon="check")
            #limpieza de campos
            self.cleanInputs([self.paisInput, self.abvInput, self.prefixInput, self.confInput])
            self.comboGrupo.set("A")
        else:
            CTkMessagebox(title="Error", message=resultado[1], icon="cancel")
            return

    def cerrar_config(self):
        self.main_frame.habilitar_botones()
        self.root.back_to_main(self)

    def volver(self):
        self.root.back_to_main(self)

    def vista1(self):
        self.frame_torneo = tk.CTkFrame(self, fg_color="transparent")
        self.frame_torneo.grid(row=0, column=0, columnspan=3, rowspan=5, sticky="nsew")

        self.frame_torneo.grid_columnconfigure(0, weight=1)
        self.frame_torneo.grid_columnconfigure(1, weight=2)
        self.frame_torneo.grid_columnconfigure(2, weight=1)
        self.frame_torneo.grid_rowconfigure(0, weight=1)
        self.frame_torneo.grid_rowconfigure(1, weight=1)
        self.frame_torneo.grid_rowconfigure(2, weight=1)
        self.frame_torneo.grid_rowconfigure(3, weight=1)

        tk.CTkButton(
            self.frame_torneo, text="go back", width=100,
            fg_color="transparent", border_width=1,
            command=self.volver
        ).grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        self.input_nombre = tk.CTkEntry(self.frame_torneo, placeholder_text="Nombre del Torneo", width=200)
        self.input_nombre.grid(row=0, column=1, pady=(40, 10))

        self.input_fecha_inicio = tk.CTkEntry(self.frame_torneo, placeholder_text="Fecha de Inicio DD/MM/AAAA", width=200)
        self.input_fecha_inicio.grid(row=1, column=1, pady=10)

        self.input_fecha_fin = tk.CTkEntry(self.frame_torneo, placeholder_text="Fecha de Final DD/MM/AAAA", width=200)
        self.input_fecha_fin.grid(row=2, column=1, pady=10)

        tk.CTkButton(
            self.frame_torneo, text="Guardar Torneo", width=200,
            fg_color="#29ABE2",
            command=self.guardar_data_torneo
        ).grid(row=3, column=1, pady=(20, 10))

        tk.CTkButton(
            self.frame_torneo, text="Grupos ->", width=110,
            fg_color="#29ABE2", border_width=0,
            command=self.go_to_grupos
        ).grid(row=2, column=2, padx=20, sticky="e")

    def vista2(self):

        # frame 2, se crea sendo transparente para que no se muestre hasta que se toque
        # el boton de Grupos ->
        self.frame_grupos = tk.CTkFrame(self, fg_color="transparent")
        # no se hace grid todavia, se muestra solo cuando se llama go_to_grupos
        self.frame_grupos.grid_columnconfigure(0, weight=1)
        self.frame_grupos.grid_columnconfigure(1, weight=2)
        self.frame_grupos.grid_columnconfigure(2, weight=1)
        self.frame_grupos.grid_rowconfigure(0, weight=1)
        self.frame_grupos.grid_rowconfigure(1, weight=1)
        self.frame_grupos.grid_rowconfigure(2, weight=1)
        self.frame_grupos.grid_rowconfigure(3, weight=1)
        self.frame_grupos.grid_rowconfigure(4, weight=1)
        self.frame_grupos.grid_rowconfigure(5, weight=1)
        self.frame_grupos.grid_rowconfigure(6, weight=1)

        #header
        tk.CTkButton(
            self.frame_grupos, text="<- Torneo", width=100,
            fg_color="transparent", border_width=1,
            command=self.go_to_torneo
        ).grid(row=0, column=0, padx=20, pady=(20,0), sticky="nw")

        tk.CTkLabel(
            self.frame_grupos,
            text="Configuracion de Grupos"
        ).grid(row = 0, column = 1, pady=(20, 0), sticky="n")

        #body
        tk.CTkLabel(
            self.frame_grupos,
            text="Seleccione el grupo deseado:"
        ).grid(row = 1, column = 1, pady=(0, 0))

        self.comboGrupo = tk.CTkComboBox(
            self.frame_grupos,
            values = ["A", "B", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
            )
        self.comboGrupo.grid(row=1, column=1, pady=(80, 10))

        #aca estoy probando disposiciones nomas xd
        tk.CTkLabel(self.frame_grupos,
            text="Ingrese el Pais"
            ).grid(row=2, column=0, padx=(80, 0))

        self.paisInput = tk.CTkEntry(self.frame_grupos, placeholder_text="Pais", width=200)
        self.paisInput.grid(row=2, column=1, pady= (20, 40))

        #abreviatura
        tk.CTkLabel(self.frame_grupos,
            text="Ingrese la abreviatura"
            ).grid(row=3, column=0, padx=(80, 0))

        self.abvInput = tk.CTkEntry(self.frame_grupos, placeholder_text="Abreviatura", width=100)
        self.abvInput.grid(row=3, column=1, pady= (20, 40))

        #prefij
        tk.CTkLabel(self.frame_grupos,
            text="Ingrese el prefijo telefonico"
            ).grid(row=4, column=0, padx=(80, 0))

        self.prefixInput = tk.CTkEntry(self.frame_grupos, placeholder_text="Prefijo +000", width=100)
        self.prefixInput.grid(row=4, column=1, pady= (20, 40))

        #Confederacion
        tk.CTkLabel(self.frame_grupos,
            text="Ingrese la confederacion"
            ).grid(row=5, column=0, padx=(80, 0))
        #tengo entendido que esto debe ser un valor fijo para q no haya algo tipo Conmebol y conmebol pero equis
        #lo ideal seria un combo box
        self.confInput = tk.CTkEntry(self.frame_grupos, placeholder_text="Ingrese la confederacion", width=200)
        self.confInput.grid(row=5, column=1, pady= (20, 40))



        tk.CTkButton(
            self.frame_grupos, text="Guardar Grupos", width=200,
            fg_color="#29ABE2",
            command=self.guardar_grupos
        ).grid(row=6, column=1, pady=(20, 10))

        tk.CTkButton(
            self.frame_grupos, text="Equipos ->", width=110,
            fg_color="transparent", border_width=0,
            command=lambda: None  # proxima vista
        ).grid(row=6, column=2, padx=20, sticky="e")

    def cleanInputs(self, inputs):
        for input in inputs:
            input.delete(0, "end")
