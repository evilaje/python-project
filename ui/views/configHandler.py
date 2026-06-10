import customtkinter as tk
from services.torneo_controller import *
from datetime import datetime
from services.equipo_controller import *
from services.partido_controller import *
from models.equipo import Equipo
from models.partido import Partido, setEquiposFaseGrupos, asignar_fases_por_orden
from CTkMessagebox import CTkMessagebox
from tkcalendar import DateEntry

class TorneoConfigFrame(tk.CTkFrame):
    def __init__(self, root, main_frame):
        super().__init__(root)
        self.root = root
        self.main_frame = main_frame

        # sidebar, este es el grid parent ponele
        self.grid_columnconfigure(0, weight=0)   # ancho fijo, no cambia en pantalla completa
        self.grid_columnconfigure(1, weight=1)   # container de las vistas, ocupa todo el espacio restante
        self.grid_rowconfigure(0, weight=1)

        self.eqs = Equipo.getAllEquipos() or []

        # constructor de sidebar
        self._build_sidebar()

        # constructor del container
        self.content_panel = tk.CTkFrame(self, fg_color="transparent")
        self.content_panel.grid(row=0, column=1, sticky="nsew")
        self.content_panel.grid_columnconfigure(0, weight=1)
        self.content_panel.grid_rowconfigure(0, weight=1)

        # bueno aca construimos los 4 frames que tiene la vista pero no se muestran
        # esto funciona asi -> el main frame que es el de la sidebar es estatico y no ocupa toda la ventana
        # entonces un layer por encima del main frame esta el container que muestra las vistas, entonces
        # cuando llamas una se destruye la otra y asi sucesivamente
        # uf creo que se entiende verdad pero capaz estoy loco
        self.vista1()   # Torneo
        self.vista2()   # Equipos
        self.vista3()   # Grupos
        self.vista4()   # Partidos

        # vista inicial -> la del torneo o si ya esta cargado el torneo muestra la de equipos
        if canSkipTorneoVista():
            self._show_frame(self.frame_equipos, "equipos")
        else:
            self._show_frame(self.frame_torneo, "torneo")


    # sidebar -----------------------------------------------------------------------------
    def _build_sidebar(self):
        sidebar = tk.CTkFrame(self, width=200, corner_radius=0, fg_color=("gray15", "gray10"))
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)  # mantener ancho fijo
        sidebar.grid_columnconfigure(0, weight=1)

        """
        el titulo este de menu podemos cambiar, no me cuadra del todo
        """
        tk.CTkLabel(
            sidebar,
            text="Menu",
            font=tk.CTkFont(size=22, weight="bold"),
            anchor="w",
        ).grid(row=0, column=0, padx=24, pady=(32, 20), sticky="w")

        # botones para navegar
        nav_items = [
            ("Torneo",   "torneo"),
            ("Equipos",  "equipos"),
            ("Grupos",   "grupos"),
            ("Partidos", "partidos"),
        ]

        self._nav_buttons = {}
        for i, (label, key) in enumerate(nav_items, start=1):
            btn = tk.CTkButton(
                sidebar,
                text=label,
                anchor="w",
                height=40,
                fg_color="transparent",
                hover_color=("gray25", "gray20"),
                text_color=("gray90", "gray85"),
                font=tk.CTkFont(size=14),
                command=lambda k=key: self._navigate(k),
            )
            btn.grid(row=i, column=0, padx=16, pady=4, sticky="ew")
            self._nav_buttons[key] = btn

        # bs para que no se junten todo los botones
        sidebar.grid_rowconfigure(len(nav_items) + 1, weight=1)

        # cerrar config btn
        tk.CTkButton(
            sidebar,
            text="Cerrar Config",
            anchor="w",
            height=40,
            fg_color="transparent",
            hover_color=("#5a1a1a", "#4a1010"),
            text_color=("#e05252", "#e05252"),
            font=tk.CTkFont(size=14),
            command=self.cerrar_config,
        ).grid(row=len(nav_items) + 2, column=0, padx=16, pady=(4, 8), sticky="ew")

        # go back btn
        tk.CTkButton(
            sidebar,
            text="← Volver",
            anchor="w",
            height=36,
            fg_color="transparent",
            hover_color=("gray25", "gray20"),
            text_color=("gray60", "gray55"),
            font=tk.CTkFont(size=12),
            command=self.volver,
        ).grid(row=len(nav_items) + 3, column=0, padx=16, pady=(0, 24), sticky="ew")

    def _set_active_button(self, active_key):
        """Resalta el boton activo en el sidebar."""
        for key, btn in self._nav_buttons.items():
            if key == active_key:
                btn.configure(
                    fg_color=("gray30", "gray25"),
                    text_color=("white", "white"),
                    font=tk.CTkFont(size=14, weight="bold"),
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=("gray90", "gray85"),
                    font=tk.CTkFont(size=14, weight="normal"),
                )


    # nav ---------------------------------------------------------------------------------
    def _show_frame(self, frame, key):
        """Oculta todos los frames de contenido y muestra el que llamas"""
        for f in [self.frame_torneo, self.frame_equipos, self.frame_grupos, self.frame_partidos]:
            f.grid_remove()
        frame.grid(row=0, column=0, sticky="nsew")
        self._set_active_button(key)

    def _navigate(self, key):
        if key == "torneo":
            self.go_to_torneo()
        elif key == "equipos":
            self.go_to_equipos()
        elif key == "grupos":
            self.go_to_grupos()
        elif key == "partidos":
            self.go_to_partidos()

    def go_to_torneo(self):
        self.vista1()  # recarga para reflejar estado guardado
        self._show_frame(self.frame_torneo, "torneo")

    def go_to_equipos(self):
        self._show_frame(self.frame_equipos, "equipos")

    def go_to_grupos(self):
        self.eqs = Equipo.getAllEquipos() or []
        team_values = [e["pais"] for e in self.eqs if e.get("grupo", "") in (None, "", "placeholder")]
        self._update_team_values(team_values)

        if not self.comboGrupo.get():
            self.comboGrupo.set("A")
        self.seleccionarGrupo(self.comboGrupo.get())

        self._show_frame(self.frame_grupos, "grupos")

    def go_to_partidos(self):
        self._show_frame(self.frame_partidos, "partidos")

    # esto esta aca por que hay funciones que recargan la vista y me dio paja arreglar
    def go_to_grupos_from_partidos(self):
        self.go_to_grupos()



    # gaurdado de data ---------------------------------------------------------------------------------
    def guardar_data_torneo(self):
        nombre = self.input_nombre.get().strip()
        fecha_inicio = self.input_fecha_inicio.get()   # ya viene como "DD/MM/YYYY"
        fecha_fin = self.input_fecha_fin.get()

        if not nombre or not fecha_inicio or not fecha_fin:
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios", icon="cancel")
            return

        try:
            dt_inicio = datetime.strptime(fecha_inicio, "%d/%m/%Y")
            dt_fin = datetime.strptime(fecha_fin, "%d/%m/%Y")
        except ValueError:
            CTkMessagebox(title="Error", message="Formato de fecha invalido, usa DD/MM/AAAA", icon="cancel")
            return

        if dt_inicio >= dt_fin:
            CTkMessagebox(title="Error", message="La fecha de inicio no puede ser posterior a la fecha de fin", icon="cancel")
            return

        cargarTorneo(nombre, fecha_inicio, fecha_fin)
        CTkMessagebox(title="Exito", message="Torneo guardado correctamente", icon="check")
        self.go_to_torneo()

    def guardar_equipos(self):
        pais = self.paisInput.get().strip().capitalize()
        abv = self.abvInput.get().strip().upper()
        pref = self.prefixInput.get().strip()
        conf = self.confInput.get().strip().capitalize()

        if not pais or not abv or not pref or not conf:
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios", icon="cancel")
            return

        resultado = cargarEquipo(pais, abv, pref, conf)
        if resultado[0]:
            CTkMessagebox(title="Exito", message=resultado[1], icon="check")
            self.cleanInputs([self.paisInput, self.abvInput, self.prefixInput, self.confInput])
            self.eqs = Equipo.getAllEquipos() or []
            team_values = [e["pais"] for e in self.eqs if e.get("grupo", "") in (None, "", "placeholder")]
            self._update_team_values(team_values)
            self.comboGrupo.set("A")
        else:
            CTkMessagebox(title="Error", message=resultado[1], icon="cancel")

    def guardar_grupos(self):
        grupo = self.comboGrupo.get().strip()
        paises = [
            self.combo_team1.get().strip(),
            self.combo_team2.get().strip(),
            self.combo_team3.get().strip(),
            self.combo_team4.get().strip(),
        ]

        # validar que las selecciones provengan de las opciones actuales
        equipos = self.eqs or []
        team_values = [e["pais"] for e in equipos if e.get("grupo", "") in (None, "", "placeholder")]
        for p in paises:
            if not p or p not in team_values:
                CTkMessagebox(title="Error", message="Seleccione países válidos desde la lista desplegable.", icon="warning")
                return

        resultado = guardarGrupo(grupo, paises)
        valido, mensaje, grupo_equipos = resultado

        if not valido:
            if grupo_equipos:
                self._set_team_boxes(grupo_equipos, enabled=False)
            CTkMessagebox(title="Error", message=mensaje, icon="warning")
            return

        CTkMessagebox(title="Éxito", message=mensaje, icon="check")
        self.eqs = Equipo.getAllEquipos() or []
        team_values = [e["pais"] for e in self.eqs if e.get("grupo", "") in (None, "", "placeholder")]
        self._update_team_values(team_values)

        try:
            self.comboGrupo.set(grupo)
            self.seleccionarGrupo(grupo)
        except Exception:
            pass

    def guardar_partidos(self):
        fecha = self.input_partido1.get()
        hora = self.input_partido2.get().strip()
        lugar = self.input_partido3.get().strip()


        torneo_ini, torneo_fin = getRangoTorneo()[0], getRangoTorneo()[1]
        if not (torneo_ini is None or torneo_fin is None):
            t_ini = datetime.strptime(torneo_ini, "%d/%m/%Y")
            t_fin = datetime.strptime(torneo_fin, "%d/%m/%Y")
            f = datetime.strptime(fecha, "%d/%m/%Y")
            if f < t_ini or f > t_fin:
                msj = f"La fecha ingresada es invalida, debe ser de {torneo_ini} a {torneo_fin}"
                CTkMessagebox(title="Error", message=msj, icon="cancel")
                return

        if not fecha or not hora or not lugar:
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios", icon="cancel")
            return

        resultado = cargarPartido(fecha, hora, lugar)
        if isinstance(resultado, tuple):
            ok, msg = resultado
        else:
            ok, msg = (True, "Exito")

        if not ok:
            CTkMessagebox(title="Error", message=msg, icon="cancel")
            return

        CTkMessagebox(title="Exito", message="Partidos guardados correctamente", icon="check")

    def seleccionarGrupo(self, value=None):
        grupo = value.strip() if isinstance(value, str) else self.comboGrupo.get().strip()
        if not grupo:
            return

        equipos = self.eqs or []
        team_values = [e["pais"] for e in equipos if e.get("grupo", "") in (None, "", "placeholder")]
        self._update_team_values(team_values)

        grupo_equipos = [e["pais"] for e in equipos if e.get("grupo", "") == grupo]
        self._set_team_boxes(grupo_equipos, enabled=(len(grupo_equipos) != 4))

    def _update_team_values(self, team_values):
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
            combo.configure(state="normal")
            combo.set(nombres[index] if index < len(nombres) and nombres[index] else "")
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

        set_result = setEquiposFaseGrupos()
        if set_result is None:
            CTkMessagebox(title="Error", message="No se pudieron asignar los equipos de fase de grupos.", icon="cancel")
            return

        if not asignar_fases_por_orden():
            CTkMessagebox(title="Error", message="Error al asignar fases a los partidos.", icon="cancel")
            return

        if not activarTorneo():
            CTkMessagebox(title="Error", message="No se pudo activar el torneo.", icon="cancel")
            return

        CTkMessagebox(title="Exito", message="Configuracion cerrada", icon="check")
        self.main_frame.habilitar_botones()
        self.root.back_to_main(self)

    def volver(self):
        self.root.back_to_main(self)

    #  las vistas del panel de la derecha
    #  cada frame se coloca dentro de self.content_panel pero no se hace el grid()
    #  hasta que _show_frame() diga yes

    def _make_content_frame(self):
        """Crea un frame hijo de content_panel listo para usar en grid"""
        f = tk.CTkFrame(self.content_panel, fg_color="transparent")
        f.grid_columnconfigure(0, weight=1)
        f.grid_columnconfigure(1, weight=2)
        f.grid_columnconfigure(2, weight=1)
        return f

    # torneo ---------------------------------------------------------------------------------
    def vista1(self):
        if hasattr(self, "frame_torneo"):
            self.frame_torneo.grid_remove()

        self.frame_torneo = self._make_content_frame()
        for r in range(5):
            self.frame_torneo.grid_rowconfigure(r, weight=1)

        tk.CTkLabel(
            self.frame_torneo,
            text="Configuración del Torneo",
            font=tk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, columnspan=3, pady=(32, 8), sticky="n")

        nombre = None
        ini = None
        fin = None
        estado_inputs = "normal"

        if torneoExits():
            t = getTorneo(1)
            nombre = t["nombre"]
            ini = t["inicio"]
            fin = t["fin"]
            estado_inputs = "disabled"

        # -- nombre (igual que antes) --
        self.input_nombre = tk.CTkEntry(self.frame_torneo, placeholder_text="Nombre del Torneo", width=280)
        if nombre:
            self.input_nombre.configure(state="normal")
            self.input_nombre.insert(0, nombre)
            self.input_nombre.configure(state=estado_inputs)
        self.input_nombre.grid(row=1, column=1, pady=10, sticky="ew", padx=20)

        # -- fecha inicio (DateEntry) --
        tk.CTkLabel(self.frame_torneo, text="Fecha de Inicio", anchor="e").grid(
            row=2, column=0, padx=(40, 16), sticky="e"
        )
        rango = getRangoTorneo() if torneoExits() else None
        self.input_fecha_inicio = DateEntry(
            self.frame_torneo,
            width=20,
            date_pattern="dd/mm/yyyy",
            font=("Segoe UI", 11),
            background="#1f538d",
            foreground="white",
            borderwidth=1,
            relief="flat",
        )
        if ini:
            from datetime import datetime as dt
            self.input_fecha_inicio.set_date(dt.strptime(ini, "%d/%m/%Y").date())
            self.input_fecha_inicio.configure(state=estado_inputs)
        self.input_fecha_inicio.grid(row=2, column=1, pady=10, sticky="w", padx=20)

        # -- fecha fin (DateEntry) --
        tk.CTkLabel(self.frame_torneo, text="Fecha de Fin", anchor="e").grid(
            row=3, column=0, padx=(40, 16), sticky="e"
        )
        self.input_fecha_fin = DateEntry(
            self.frame_torneo,
            width=20,
            date_pattern="dd/mm/yyyy",
            font=("Segoe UI", 11),
            background="#1f538d",
            foreground="white",
            borderwidth=1,
            relief="flat",

        )
        if fin:
            from datetime import datetime as dt
            self.input_fecha_fin.set_date(dt.strptime(fin, "%d/%m/%Y").date())
            self.input_fecha_fin.configure(state=estado_inputs)
        self.input_fecha_fin.grid(row=3, column=1, pady=10, sticky="w", padx=20)

        tk.CTkButton(
            self.frame_torneo, text="Guardar Torneo", width=200,
            fg_color="#29ABE2",
            command=self.guardar_data_torneo,
        ).grid(row=4, column=1, pady=(20, 10))

    # equios ---------------------------------------------------------------------------------
    def vista2(self):
        self.frame_equipos = self._make_content_frame()
        for r in range(8):
            self.frame_equipos.grid_rowconfigure(r, weight=1)

        tk.CTkLabel(
            self.frame_equipos,
            text="Configuración de Equipos",
            font=tk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, columnspan=3, pady=(32, 8), sticky="n")

        fields = [
            ("Pais",                    "paisInput",    "Pais"),
            ("Abreviatura",             "abvInput",     "Abreviatura"),
            ("Prefijo telefónico",      "prefixInput",  "Prefijo +000"),
            ("Confederación",           "confInput",    "Ingrese la confederacion"),
        ]

        for i, (label_text, attr, placeholder) in enumerate(fields, start=1):
            tk.CTkLabel(self.frame_equipos, text=label_text, anchor="e").grid(
                row=i, column=0, padx=(40, 16), sticky="e"
            )
            entry = tk.CTkEntry(self.frame_equipos, placeholder_text=placeholder, width=280)
            entry.grid(row=i, column=1, pady=10, sticky="ew", padx=(0, 20))
            setattr(self, attr, entry)

        tk.CTkButton(
            self.frame_equipos, text="Guardar Equipo", width=200,
            fg_color="#29ABE2",
            command=self.guardar_equipos,
        ).grid(row=len(fields) + 1, column=1, pady=(24, 10))

    # grupos ---------------------------------------------------------------------------------
    def vista3(self):
        self.frame_grupos = self._make_content_frame()
        for r in range(7):
            self.frame_grupos.grid_rowconfigure(r, weight=1)

        tk.CTkLabel(
            self.frame_grupos,
            text="Configuración de Grupos",
            font=tk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, columnspan=3, pady=(32, 8), sticky="n")

        tk.CTkLabel(self.frame_grupos, text="Seleccione el grupo:", anchor="e").grid(
            row=1, column=0, padx=(40, 16), sticky="e"
        )

        self.comboGrupo = tk.CTkComboBox(
            self.frame_grupos,
            values=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
            command=self.seleccionarGrupo,
            width=120,
        )
        self.comboGrupo.grid(row=1, column=1, padx=(0, 20), pady=8, sticky="w")

        equipos = self.eqs or []
        team_values = [e["pais"] for e in equipos if e.get("grupo", "") in (None, "", "placeholder")]

        for i, attr in enumerate(["combo_team1", "combo_team2", "combo_team3", "combo_team4"], start=2):
            combo = tk.CTkComboBox(self.frame_grupos, values=team_values, width=280)
            combo.grid(row=i, column=1, padx=(0, 20), pady=6, sticky="ew")
            combo.set("")
            setattr(self, attr, combo)

        tk.CTkButton(
            self.frame_grupos,
            text="Guardar Grupo",
            fg_color="#29B6F6",
            hover_color="#0288D1",
            text_color="#01547a",
            width=200,
            command=self.guardar_grupos,
        ).grid(row=6, column=1, padx=(0, 20), pady=(20, 10))

    # partidos ---------------------------------------------------------------------------------
    def vista4(self):
        self.frame_partidos = self._make_content_frame()
        for r in range(6):
            self.frame_partidos.grid_rowconfigure(r, weight=1)

        tk.CTkLabel(
            self.frame_partidos,
            text="Configuración de Partidos",
            font=tk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, columnspan=3, pady=(32, 8), sticky="n")

        # -- fecha (DateEntry) --
        tk.CTkLabel(self.frame_partidos, text="Fecha", anchor="e").grid(
            row=1, column=0, padx=(40, 16), sticky="e"
        )
        self.input_partido1 = DateEntry(
            self.frame_partidos,
            width=20,
            date_pattern="dd/mm/yyyy",
            font=("Segoe UI", 11),
            background="#1f538d",
            foreground="white",
            borderwidth=1,
            relief="flat",
        )
        self.input_partido1.grid(row=1, column=1, pady=10, sticky="w", padx=20)

        # -- hora y lugar siguen siendo CTkEntry --
        fields = [
            ("Hora",    "input_partido2", "HH:MM"),
            ("Lugar",   "input_partido3", "Estadio / Ciudad"),
        ]

        for i, (label_text, attr, placeholder) in enumerate(fields, start=2):
            tk.CTkLabel(self.frame_partidos, text=label_text, anchor="e").grid(
                row=i, column=0, padx=(40, 16), sticky="e"
            )
            entry = tk.CTkEntry(self.frame_partidos, placeholder_text=placeholder, width=280)
            entry.grid(row=i, column=1, pady=10, sticky="ew", padx=(0, 20))
            setattr(self, attr, entry)

        tk.CTkButton(
            self.frame_partidos, text="Guardar Partidos", width=200,
            fg_color="#29ABE2",
            command=self.guardar_partidos,
        ).grid(row=len(fields) + 2, column=1, pady=(24, 10))

    # utility --------------------------------------------------------------------------------
    def cleanInputs(self, inputs):
        for inp in inputs:
            inp.delete(0, "end")
