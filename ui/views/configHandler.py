import customtkinter as tk
from services.torneo_controller import *
from datetime import datetime
from services.equipo_controller import *
from services.partido_controller import *
from models.equipo import Equipo
from models.partido import Partido, setEquiposFaseGrupos, asignar_fases_por_orden
# este es para los popUps, ponele un title, mensaje y icon nomas, icon acepta las palabras cancel, warning y check
from CTkMessagebox import CTkMessagebox

#constantes
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

        #inicializa
        self.eqs = Equipo.getAllEquipos() or []



        self.vista1()
        self.vista2()
        self.vista3()
        self.vista4()

        if canSkipTorneoVista():
            self.frame_torneo.grid_remove()
            self.go_to_equipos()


    def go_to_grupos(self):
        #se necesita refrescar el combobox
        self.eqs = Equipo.getAllEquipos() or []
        # solo incluir equipos que no tengan grupo asignado (placeholder)
        team_values = [e["pais"] for e in self.eqs if e.get("grupo", "") in (None, "", "placeholder")]
        self._update_team_values(team_values)

        # si entramos por primera vez, preseleccionamos el grupo A y cargamos sus equipos
        if not self.comboGrupo.get():
            self.comboGrupo.set("A")
        self.seleccionarGrupo(self.comboGrupo.get())

        self.frame_equipos.grid_remove()

        self.frame_grupos.grid(row=0, column=0, columnspan=3, rowspan=5, sticky="nsew")

    def go_to_partidos(self):
        self.frame_grupos.grid_remove()
        self.frame_partidos.grid(row=0, column=0, columnspan=3, rowspan=5, sticky="nsew")

    def go_to_grupos_from_partidos(self):
        self.frame_partidos.grid_remove()
        self.frame_grupos.grid(row=0, column=0, columnspan=3, rowspan=5, sticky="nsew")

    # esta es la funcion para cambiar de pagina
    def go_to_equipos(self):
        # grid remove borra el grid pero no el frame, entonces podes llamar grid otra vez para volver a mostrar
        self.frame_torneo.grid_remove()
        self.frame_grupos.grid_remove()
        # se habilita el grid
        self.frame_equipos.grid(row=0, column=0, columnspan=3, rowspan=5, sticky="nsew")

    def go_to_torneo(self):

        self.frame_equipos.grid_remove()
        self.vista1()
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

        if dt_inicio > dt_fin:
            CTkMessagebox(title="Error", message="La fecha de inicio no puede ser posterior a la fecha de fin", icon="cancel")
            return

        cargarTorneo(nombre, fecha_inicio, fecha_fin)
        CTkMessagebox(title="Exito", message="Torneo guardado correctamente", icon="check")

        #RECARGA LA VISTA (NO SE QUE IMPACTO TIENE ESTO EN MEMORIA O EN GENERAL)
        self.go_to_torneo()

    def guardar_equipos(self):
        pais = self.paisInput.get().strip().capitalize()
        abv = self.abvInput.get().strip().upper()
        pref = self.prefixInput.get().strip()
        conf = self.confInput.get().strip().capitalize()

        #validaciones de campos vacios
        if not pais or not abv or not pref or not conf:
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios", icon="cancel")
            return
        resultado = cargarEquipo(pais, abv, pref, conf)
        if (resultado[0]):
            CTkMessagebox(title="Exito", message=resultado[1], icon="check")
            #limpieza de campos
            self.cleanInputs([self.paisInput, self.abvInput, self.prefixInput, self.confInput])
            # refrescar listado de equipos para que los combos muestren al nuevo equipo
            self.eqs = Equipo.getAllEquipos() or []
            team_values = [e["pais"] for e in self.eqs if e.get("grupo", "") in (None, "", "placeholder")]
            self._update_team_values(team_values)
            self.comboGrupo.set("A")
        else:
            CTkMessagebox(title="Error", message=resultado[1], icon="cancel")
            return

    def guardar_grupos(self):
        grupo = self.comboGrupo.get().strip()

        paises = [
            self.combo_team1.get().strip(),
            self.combo_team2.get().strip(),
            self.combo_team3.get().strip(),
            self.combo_team4.get().strip()
        ]

        # este guardar grupo hace todas las validaciones y devuelve el mensaje de error que toca
        resultado = guardarGrupo(grupo, paises)
        valido, mensaje, grupo_equipos = resultado

        if not valido:
            # Si ya ya habia equipos en el grupo salen como puestos e incambiables
            if grupo_equipos:
                self._set_team_boxes(grupo_equipos, enabled=False)
            CTkMessagebox(title="Error", message=mensaje, icon="warning")
            return

        CTkMessagebox(title="Éxito", message=mensaje, icon="check")

        # refrescar lista de equipos y actualizar comboboxes para que el cambio sea visible
        self.eqs = Equipo.getAllEquipos() or []
        team_values = [e["pais"] for e in self.eqs if e.get("grupo", "") in (None, "", "placeholder")]
        self._update_team_values(team_values)

        # asegurar que el grupo guardado quede seleccionado y sus cajas actualizadas
        try:
            self.comboGrupo.set(grupo)
            self.seleccionarGrupo(grupo)
        except Exception:
            pass

    def guardar_partidos(self):
        fecha = self.input_partido1.get().strip()
        hora = self.input_partido2.get().strip()
        lugar = self.input_partido3.get().strip()

        #validacion de fechas
        torneo_ini, torneo_fin = getRangoTorneo()[0], getRangoTorneo()[1]
        print(f"{torneo_ini} \n {torneo_fin}")
        if not (torneo_ini is None or torneo_fin is None):
            t_ini = datetime.strptime(torneo_ini, "%d/%m/%Y")
            t_fin = datetime.strptime(torneo_fin, "%d/%m/%Y")
            f = datetime.strptime(fecha, "%d/%m/%Y")

            if (f < t_ini or f > t_fin):
                msj = f"La fecha ingresada es invalida, debe ser de {torneo_ini} a {torneo_fin}"
                CTkMessagebox(title="Error", message=msj, icon="cancel")
                return


        if not fecha or not hora or not lugar:
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios", icon="cancel")
            return


        cargarPartido(fecha, hora, lugar)
        CTkMessagebox(title="Exito", message="Partidos guardados correctamente", icon="check")

    def seleccionarGrupo(self, value=None):
        grupo = value.strip() if isinstance(value, str) else self.comboGrupo.get().strip()
        if not grupo:
            return

        # Carga todos los equipos registrados y si no hay entonces una lista vacia nomas
        equipos = self.eqs or []
        # solo mostrar en las opciones los equipos sin grupo asignado
        team_values = [e["pais"] for e in equipos if e.get("grupo", "") in (None, "", "placeholder")]

        # Actualiza las opciones disponibles en los 4 combos de equipos
        self._update_team_values(team_values)

        # Filtra los equipos que ya pertenecen al grupo
        grupo_equipos = [e["pais"] for e in equipos if e.get("grupo", "") == grupo]

        # Si el grupo ya tiene 4 equipos, muestra los combos deshabilitado
        # Si tiene menos de 4, los deja habilitados para seguir asignando
        # cambiable totalmente porque no pense demasiado en esto
        self._set_team_boxes(grupo_equipos, enabled=(len(grupo_equipos) != 4))


    def _update_team_values(self, team_values):
        # Aplica la misma lista de opciones a los 4 combos ed equipo
        for combo in [self.combo_team1, self.combo_team2, self.combo_team3, self.combo_team4]:
            combo.configure(values=team_values)

    def _validar_grupos_completos(self):
        equipos = Equipo.getAllEquipos() or []
        if len(equipos) > 48:
            return False, "Solo se pueden cargar hasta 48 equipos."

        grupos = {}
        for eq in equipos:
            grupo = str(eq.get("grupo", "")).strip().upper()
            if grupo in (None, "", "PLACEHOLDER"):
                continue
            grupos.setdefault(grupo, []).append(eq)

        grupos_necesarios = [chr(ord("A") + i) for i in range(12)]
        if sorted(grupos.keys()) != grupos_necesarios:
            return False, "Deben existir 12 grupos completos (A-L)."

        for grupo, miembros in grupos.items():
            if len(miembros) != 4:
                return False, f"El grupo {grupo} debe tener exactamente 4 equipos."

        return True, None

    def _validar_partidos(self):
        partidos = Partido.getAllPartidos() or []
        if len(partidos) != 104:
            return False, "Deben haber 104 partidos cargados."

        for partido in partidos:
            fecha = partido.get("fecha", "").strip()
            hora = partido.get("hora", "").strip()
            try:
                datetime.strptime(f"{fecha} {hora}", "%d/%m/%Y %H:%M")
            except Exception:
                return False, "Todos los partidos deben tener fecha y hora válidas."

        return True, None

    def _set_team_boxes(self, nombres, enabled=True):
        combos = [self.combo_team1, self.combo_team2, self.combo_team3, self.combo_team4]

        for index, combo in enumerate(combos):
            # cambio a normal un rato para que se ponga el texto por que fokin tkinter es mierda
            combo.configure(state="normal")

            if index < len(nombres) and nombres[index]:
                combo.set(nombres[index])
            else:
                combo.set("")

            combo.configure(state=("normal" if enabled else "disabled"))

    def cerrar_config(self):
        grupos_ok, grupo_msg = self._validar_grupos_completos()
        if not grupos_ok:
            CTkMessagebox(title="Error", message=grupo_msg, icon="warning")
            return

        partidos_ok, partidos_msg = self._validar_partidos()
        if not partidos_ok:
            CTkMessagebox(title="Error", message=partidos_msg, icon="warning")
            return

        if not Partido.ordenar_partidos_por_fecha_y_reasignar_ids():
            CTkMessagebox(title="Error", message="Error al ordenar y reasignar partidos.", icon="cancel")
            return

        if not asignar_fases_por_orden():
            CTkMessagebox(title="Error", message="Error al asignar fases a los partidos.", icon="cancel")
            return

        if not activarTorneo():
            CTkMessagebox(title="Error", message="No se pudo activar el torneo.", icon="cancel")
            return

        set_result = setEquiposFaseGrupos()
        if set_result is None:
            CTkMessagebox(title="Error", message="No se pudieron asignar los equipos de fase de grupos.", icon="cancel")
            return

        CTkMessagebox(title="Exito", message="configuracion cerrada", icon="check")
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

        #desactivar carga si ya hay torneo
        nombre = None
        ini = None
        fin = None
        #sirve para definir mas tarde el estado de los inputs
        estado_inputs = "normal"

        #COMENTAR ESTE BLOQUE PARA FUNCIONAMIENTO ANTIGUO
        if torneoExits():
            #obtenemos la data del torneo
            t = getTorneo(1)
            nombre = t["nombre"]
            ini = t["inicio"]
            fin = t["fin"]
            estado_inputs = "disabled"


        tk.CTkButton(
            self.frame_torneo, text="go back", width=100,
            fg_color="transparent", border_width=1,
            command=self.volver
        ).grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        self.input_nombre = tk.CTkEntry(self.frame_torneo, placeholder_text="Nombre del Torneo", width=200)
        #cargar el nombre del torneo y luego desactivar el campo
        if nombre:
            self.input_nombre.configure(state="normal")
            self.input_nombre.delete(0, "end")
            self.input_nombre.insert(0, nombre)
            self.input_nombre.configure(state=estado_inputs)

        self.input_nombre.grid(row=0, column=1, pady=(40, 10))

        self.input_fecha_inicio = tk.CTkEntry(self.frame_torneo, placeholder_text="Fecha de Inicio DD/MM/AAAA", width=200)

        if ini:
            self.input_fecha_inicio.configure(state="normal")
            self.input_fecha_inicio.delete(0, "end")
            self.input_fecha_inicio.insert(0, ini)
            self.input_fecha_inicio.configure(state=estado_inputs)


        self.input_fecha_inicio.grid(row=1, column=1, pady=10)

        self.input_fecha_fin = tk.CTkEntry(self.frame_torneo, placeholder_text="Fecha de Final DD/MM/AAAA", width=200)

        if fin:
            self.input_fecha_fin.configure(state="normal")
            self.input_fecha_fin.delete(0, "end")
            self.input_fecha_fin.insert(0, fin)
            self.input_fecha_fin.configure(state=estado_inputs)

        self.input_fecha_fin.grid(row=2, column=1, pady=10)

        tk.CTkButton(
            self.frame_torneo, text="Guardar Torneo", width=200,
            fg_color="#29ABE2",
            command=self.guardar_data_torneo
        ).grid(row=3, column=1, pady=(20, 10))

        tk.CTkButton(
            self.frame_torneo, text="Equipos ->", width=110,
            fg_color="#29ABE2", border_width=0,
            command=self.go_to_equipos
        ).grid(row=2, column=2, padx=20, sticky="e")


    def vista2(self):

        # frame 2, se crea sendo transparente para que no se muestre hasta que se toque
        self.frame_equipos = tk.CTkFrame(self, fg_color="transparent")
        # no se hace grid todavia, se muestra solo cuando se llama go_to_grupos
        self.frame_equipos.grid_columnconfigure(0, weight=1)
        self.frame_equipos.grid_columnconfigure(1, weight=2)
        self.frame_equipos.grid_columnconfigure(2, weight=1)
        self.frame_equipos.grid_rowconfigure(0, weight=1)
        self.frame_equipos.grid_rowconfigure(1, weight=1)
        self.frame_equipos.grid_rowconfigure(2, weight=1)
        self.frame_equipos.grid_rowconfigure(3, weight=1)
        self.frame_equipos.grid_rowconfigure(4, weight=1)
        self.frame_equipos.grid_rowconfigure(5, weight=1)
        self.frame_equipos.grid_rowconfigure(6, weight=1)

        #header
        tk.CTkButton(
            self.frame_equipos, text="<- Torneo", width=100,
            fg_color="transparent", border_width=1,
            command=self.go_to_torneo
        ).grid(row=0, column=0, padx=20, pady=(20,0), sticky="nw")

        tk.CTkLabel(
            self.frame_equipos,
            text="Configuracion de Equipos"
        ).grid(row = 0, column = 1, pady=(20, 0), sticky="n")

        #body

        #aca estoy probando disposiciones nomas xd
        tk.CTkLabel(self.frame_equipos,
            text="Ingrese el Pais"
            ).grid(row=2, column=0, padx=(80, 0))

        self.paisInput = tk.CTkEntry(self.frame_equipos, placeholder_text="Pais", width=200)
        self.paisInput.grid(row=2, column=1, pady= (20, 40))

        #abreviatura
        tk.CTkLabel(self.frame_equipos,
            text="Ingrese la abreviatura"
            ).grid(row=3, column=0, padx=(80, 0))

        self.abvInput = tk.CTkEntry(self.frame_equipos, placeholder_text="Abreviatura", width=100)
        self.abvInput.grid(row=3, column=1, pady= (20, 40))

        #prefij
        tk.CTkLabel(self.frame_equipos,
            text="Ingrese el prefijo telefonico"
            ).grid(row=4, column=0, padx=(80, 0))

        self.prefixInput = tk.CTkEntry(self.frame_equipos, placeholder_text="Prefijo +000", width=100)
        self.prefixInput.grid(row=4, column=1, pady= (20, 40))

        #Confederacion
        tk.CTkLabel(self.frame_equipos,
            text="Ingrese la confederacion"
            ).grid(row=5, column=0, padx=(80, 0))
        #tengo entendido que esto debe ser un valor fijo para q no haya algo tipo Conmebol y conmebol pero equis
        #lo ideal seria un combo box
        self.confInput = tk.CTkEntry(self.frame_equipos, placeholder_text="Ingrese la confederacion", width=200)
        self.confInput.grid(row=5, column=1, pady= (20, 40))


        tk.CTkButton(
            self.frame_equipos, text="Guardar Equipos", width=200,
            fg_color="#29ABE2",
            command=self.guardar_equipos
        ).grid(row=6, column=1, pady=(20, 10))

        tk.CTkButton(
            self.frame_equipos, text="Grupos ->", width=110,
            fg_color="transparent", border_width=0,
            command=self.go_to_grupos  # proxima vista
        ).grid(row=6, column=2, padx=20, sticky="e")


    def vista3(self):
        self.frame_grupos = tk.CTkFrame(self, fg_color="transparent")

        # configurar grid interno para posicionamiento: columna 0 = zona izquierda,
        # columna 1 = columna central (donde van los 4 comboBoxes), columna 2 = derecha
        self.frame_grupos.grid_columnconfigure(0, weight=1)
        self.frame_grupos.grid_columnconfigure(1, weight=3)
        self.frame_grupos.grid_columnconfigure(2, weight=1)
        for i in range(6):
            self.frame_grupos.grid_rowconfigure(i, weight=1)

        tk.CTkButton(
            self.frame_grupos, text="<- Equipos", width=100,
            fg_color="transparent", border_width=1,
            command=self.go_to_equipos
        ).grid(row=0, column=0, padx=20, pady=(20,0), sticky="nw")

        tk.CTkLabel(
            self.frame_grupos,
            text="Configuracion de grupos"
        ).grid(row=0, column=1, sticky="n", pady=(10,0))


        tk.CTkLabel(
            self.frame_grupos,
            text="Seleccione el grupo:"
        ).grid(row=1, column=0, padx=(20, 10), pady=(0, 4), sticky="s")

        # el combo de grupos queda en la columna izquierda pero alineado hacia el centro (hacia la derecha)
        self.comboGrupo = tk.CTkComboBox(
            self.frame_grupos,
            values=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
            command=self.seleccionarGrupo
        )
        self.comboGrupo.grid(row=2, column=0, padx=(20, 40), sticky="e")

        #  ComboBoxes en la columna central cargadas con los equipos disponibles (sin grupo)
        equipos = self.eqs or []
        team_values = [e["pais"] for e in equipos if e.get("grupo", "") in (None, "", "placeholder")]

        self.combo_team1 = tk.CTkComboBox(self.frame_grupos, values=team_values)
        self.combo_team1.grid(row=1, column=1, padx=10, pady=(0, 5), sticky="ew")
        self.combo_team1.set("")

        self.combo_team2 = tk.CTkComboBox(self.frame_grupos, values=team_values)
        self.combo_team2.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.combo_team2.set("")

        self.combo_team3 = tk.CTkComboBox(self.frame_grupos, values=team_values)
        self.combo_team3.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.combo_team3.set("")

        self.combo_team4 = tk.CTkComboBox(self.frame_grupos, values=team_values)
        self.combo_team4.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        self.combo_team4.set("")

        tk.CTkButton(
            self.frame_grupos,
            text="GuardarGrupo",
            fg_color="#29B6F6",
            hover_color="#0288D1",
            text_color="#01547a",
            command=self.guardar_grupos
        ).grid(row=5, column=1, padx=10, pady=(10, 0), sticky="ew")


        tk.CTkButton(
            self.frame_grupos, text="Partidos ->", width=110,
            fg_color="transparent", border_width=0,
            command=self.go_to_partidos
        ).grid(row=5, column=2, padx=20, sticky="e")



    def vista4(self):
        self.frame_partidos = tk.CTkFrame(self, fg_color="transparent")

        self.frame_partidos.grid_columnconfigure(0, weight=1)
        self.frame_partidos.grid_columnconfigure(1, weight=2)
        self.frame_partidos.grid_columnconfigure(2, weight=1)
        self.frame_partidos.grid_rowconfigure(0, weight=1)
        self.frame_partidos.grid_rowconfigure(1, weight=1)
        self.frame_partidos.grid_rowconfigure(2, weight=1)
        self.frame_partidos.grid_rowconfigure(3, weight=1)
        self.frame_partidos.grid_rowconfigure(4, weight=1)
        self.frame_partidos.grid_rowconfigure(5, weight=1)

        # --- Botón volver a Grupos ---
        tk.CTkButton(
            self.frame_partidos, text="<- Grupos", width=100,
            fg_color="transparent", border_width=1,
            command=self.go_to_grupos_from_partidos
        ).grid(row=0, column=0, padx=20, pady=(20, 0), sticky="nw")

        tk.CTkLabel(
            self.frame_partidos,
            text="Configuracion de Partidos"
        ).grid(row=0, column=1, pady=(20, 0), sticky="n")

        # fecha
        tk.CTkLabel(self.frame_partidos,
            text="Campo 1"
        ).grid(row=2, column=0, padx=(80, 0))

        self.input_partido1 = tk.CTkEntry(self.frame_partidos, placeholder_text="fecha", width=200)
        self.input_partido1.grid(row=2, column=1, pady=(20, 10))

        # hora
        tk.CTkLabel(self.frame_partidos,
            text="Campo 2"
        ).grid(row=3, column=0, padx=(80, 0))

        self.input_partido2 = tk.CTkEntry(self.frame_partidos, placeholder_text="hora", width=200)
        self.input_partido2.grid(row=3, column=1, pady=10)

        # lugar
        tk.CTkLabel(self.frame_partidos,
            text="Campo 3"
        ).grid(row=4, column=0, padx=(80, 0))

        self.input_partido3 = tk.CTkEntry(self.frame_partidos, placeholder_text="lugar", width=200)
        self.input_partido3.grid(row=4, column=1, pady=10)

        # guardar
        tk.CTkButton(
            self.frame_partidos, text="Guardar Partidos", width=200,
            fg_color="#29ABE2",
            command=self.guardar_partidos
        ).grid(row=5, column=1, pady=(20, 10))

        # cerrar config
        tk.CTkButton(
            self.frame_partidos, text="Cerrar Configuracion", width=180,
            fg_color="#e05252", hover_color="#b33a3a",
            command=self.cerrar_config
        ).grid(row=5, column=2, padx=20, sticky="e")


    def cleanInputs(self, inputs):
        for input in inputs:
            input.delete(0, "end")
