import customtkinter as tk
from services.partido_controller import getPartidoPorFecha, getPartidosPorEquipo, getSiguientePartido
from services.equipo_controller import getTablaDeGrupo
from models.equipo import Equipo
from datetime import datetime


class TorneoReportFrame(tk.CTkFrame):
    def __init__(self, root, main_frame):
        super().__init__(root)
        self.root = root
        self.main_frame = main_frame

        # sidebar
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()

        self.content_panel = tk.CTkFrame(self, fg_color="transparent")
        self.content_panel.grid(row=0, column=1, sticky="nsew")
        self.content_panel.grid_columnconfigure(0, weight=1)
        self.content_panel.grid_rowconfigure(0, weight=1)

        # build de los reportes
        self._build_frame_fecha()
        self._build_frame_grupo()
        self._build_frame_equipo()
        self._build_frame_siguiente()
        self._build_frame_all_grupos()

        # vista inicial
        self._show_frame(self.frame_fecha, "fecha")


    # seidebar --------------------------------------------------------------------------------
    def _build_sidebar(self):
        sidebar = tk.CTkFrame(self, width=200, corner_radius=0, fg_color=("gray15", "gray10"))
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_columnconfigure(0, weight=1)

        tk.CTkLabel(
            sidebar,
            text="Resultados",
            font=tk.CTkFont(size=22, weight="bold"),
            anchor="w",
        ).grid(row=0, column=0, padx=24, pady=(32, 20), sticky="w")

        nav_items = [
            ("Partidos por fecha",           "fecha"),
            ("Tabla de Grupo",               "grupo"),
            ("Informe de equipo",            "equipo"),
            ("Siguiente partido",            "siguiente"),
            ("Todos los grupos",             "all_grupos"),
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

        # separar lso botones
        sidebar.grid_rowconfigure(len(nav_items) + 1, weight=1)

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
        ).grid(row=len(nav_items) + 2, column=0, padx=16, pady=(0, 24), sticky="ew")

    def _set_active_button(self, active_key):
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

    # nav --------------------------------------------------------------------------------
    def _show_frame(self, frame, key):
        for f in [self.frame_fecha, self.frame_grupo, self.frame_equipo,
                  self.frame_siguiente, self.frame_all_grupos]:
            f.grid_remove()
        frame.grid(row=0, column=0, sticky="nsew")
        self._set_active_button(key)

    def _navigate(self, key):
        if key == "fecha":
            self._show_frame(self.frame_fecha, "fecha")
        elif key == "grupo":
            self.buscar_tabla_de_grupo(self.combo_grupo.get())
            self._show_frame(self.frame_grupo, "grupo")
        elif key == "equipo":
            self.buscar_informe_equipo(self.combo_equipo.get())
            self._show_frame(self.frame_equipo, "equipo")
        elif key == "siguiente":
            self.buscar_siguiente_partido(self.combo_equipo_siguiente.get())
            self._show_frame(self.frame_siguiente, "siguiente")
        elif key == "all_grupos":
            self.label_fecha_all_grupos.configure(
                text=f"Fecha de emisión del Informe: {datetime.today().strftime('%d/%m/%Y')}"
            )
            self._render_all_grupos()
            self._show_frame(self.frame_all_grupos, "all_grupos")

    # bs para moverse entre los reportes
    def go_to_menu(self):                      self._navigate("fecha")
    def go_to_informe_por_fecha(self):         self._navigate("fecha")
    def go_to_informe_por_grupo(self):         self._navigate("grupo")
    def go_to_informe_por_equipo(self):        self._navigate("equipo")
    def go_to_informe_siguiente_partido(self): self._navigate("siguiente")
    def go_to_informe_all_grupos(self):        self._navigate("all_grupos")

    # hace el frame de la parte derecha
    def _make_content_frame(self):
        f = tk.CTkFrame(self.content_panel, fg_color="transparent")
        f.grid_columnconfigure(0, weight=1)
        f.grid_rowconfigure(0, weight=1)
        return f

    # frames de cada reporte --------------------------------------------------------------------------------
    def _build_frame_fecha(self):
        self.frame_fecha = self._make_content_frame()

        tk.CTkLabel(
            self.frame_fecha,
            text="Partidos por fecha",
            font=tk.CTkFont(size=18, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=24, pady=(28, 8))

        input_row = tk.CTkFrame(self.frame_fecha, fg_color="transparent")
        input_row.pack(fill="x", padx=24, pady=(0, 4))

        tk.CTkLabel(input_row, text="Fecha:").pack(side="left")
        self.input_fecha = tk.CTkEntry(input_row, placeholder_text="DD/MM/AAAA", width=150)
        self.input_fecha.pack(side="left", padx=10)
        tk.CTkButton(input_row, text="Buscar", width=80,
                     command=self.buscar_partidos_por_fecha).pack(side="left")

        tk.CTkLabel(self.frame_fecha, text="Formato: DD/MM/AAAA",
                    text_color="gray", anchor="w").pack(anchor="w", padx=24)

        self.scroll_fecha = tk.CTkScrollableFrame(self.frame_fecha)
        self.scroll_fecha.pack(fill="both", expand=True, padx=24, pady=10)


    def _build_frame_grupo(self):
        self.frame_grupo = self._make_content_frame()

        tk.CTkLabel(
            self.frame_grupo,
            text="Tabla de Grupo",
            font=tk.CTkFont(size=18, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=24, pady=(28, 8))

        input_row = tk.CTkFrame(self.frame_grupo, fg_color="transparent")
        input_row.pack(fill="x", padx=24, pady=(0, 4))

        tk.CTkLabel(input_row, text="Grupo:").pack(side="left")
        self.combo_grupo = tk.CTkComboBox(
            input_row,
            values=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
            width=80,
            command=self.buscar_tabla_de_grupo,
        )
        self.combo_grupo.set("A")
        self.combo_grupo.pack(side="left", padx=10)

        self.label_fecha_emision = tk.CTkLabel(
            input_row,
            text=f"Fecha de emisión: {datetime.today().strftime('%d/%m/%Y')}",
            text_color="gray",
        )
        self.label_fecha_emision.pack(side="left", padx=20)

        self.scroll_grupo = tk.CTkScrollableFrame(self.frame_grupo)
        self.scroll_grupo.pack(fill="both", expand=True, padx=24, pady=10)


    def _build_frame_equipo(self):
        self.frame_equipo = self._make_content_frame()

        tk.CTkLabel(
            self.frame_equipo,
            text="Informe de equipo",
            font=tk.CTkFont(size=18, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=24, pady=(28, 8))

        input_row = tk.CTkFrame(self.frame_equipo, fg_color="transparent")
        input_row.pack(fill="x", padx=24, pady=(0, 4))

        tk.CTkLabel(input_row, text="Equipo:").pack(side="left")

        equipos = Equipo.getAllEquipos() or []
        equipo_names = [e["pais"] for e in equipos]

        self.combo_equipo = tk.CTkComboBox(
            input_row,
            values=equipo_names,
            width=180,
            command=self.buscar_informe_equipo,
        )
        self.combo_equipo.set(equipo_names[0] if equipo_names else "")
        self.combo_equipo.pack(side="left", padx=10)

        self.label_fecha_emision_equipo = tk.CTkLabel(
            input_row,
            text=f"Fecha de emisión: {datetime.today().strftime('%d/%m/%Y')}",
            text_color="gray",
        )
        self.label_fecha_emision_equipo.pack(side="left", padx=20)

        self.scroll_equipo = tk.CTkScrollableFrame(self.frame_equipo)
        self.scroll_equipo.pack(fill="both", expand=True, padx=24, pady=10)


    def _build_frame_siguiente(self):
        self.frame_siguiente = self._make_content_frame()

        tk.CTkLabel(
            self.frame_siguiente,
            text="Siguiente partido de equipo",
            font=tk.CTkFont(size=18, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=24, pady=(28, 8))

        input_row = tk.CTkFrame(self.frame_siguiente, fg_color="transparent")
        input_row.pack(fill="x", padx=24, pady=(0, 4))

        tk.CTkLabel(input_row, text="Equipo:").pack(side="left")

        equipos = Equipo.getAllEquipos() or []
        equipo_names = [e["pais"] for e in equipos]

        self.combo_equipo_siguiente = tk.CTkComboBox(
            input_row,
            values=equipo_names,
            width=180,
            command=self.buscar_siguiente_partido,
        )
        self.combo_equipo_siguiente.set(equipo_names[0] if equipo_names else "")
        self.combo_equipo_siguiente.pack(side="left", padx=10)

        self.label_fecha_siguiente = tk.CTkLabel(
            input_row,
            text=f"Fecha: {datetime.today().strftime('%d/%m/%Y')}",
            text_color="gray",
        )
        self.label_fecha_siguiente.pack(side="left", padx=20)

        self.container_siguiente = tk.CTkFrame(self.frame_siguiente, fg_color="transparent")
        self.container_siguiente.pack(fill="both", expand=True, padx=24, pady=10)


    def _build_frame_all_grupos(self):
        self.frame_all_grupos = self._make_content_frame()

        tk.CTkLabel(
            self.frame_all_grupos,
            text="Tabla de todos los grupos",
            font=tk.CTkFont(size=18, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=24, pady=(28, 4))

        self.label_fecha_all_grupos = tk.CTkLabel(
            self.frame_all_grupos,
            text=f"Fecha de emisión: {datetime.today().strftime('%d/%m/%Y')}",
            text_color="gray",
            anchor="w",
        )
        self.label_fecha_all_grupos.pack(anchor="w", padx=24, pady=(0, 4))

        self.scroll_all_grupos = tk.CTkScrollableFrame(self.frame_all_grupos)
        self.scroll_all_grupos.pack(fill="both", expand=True, padx=24, pady=10)

    # codigo de busqueda de datos --------------------------------------------------------------------------------
    def buscar_partidos_por_fecha(self):
        fecha = self.input_fecha.get().strip()
        if not fecha:
            self._render_partidos([])
            return
        partidos = getPartidoPorFecha(fecha)
        self._render_partidos(partidos or [])

    def buscar_tabla_de_grupo(self, value=None):
        grupo = value or self.combo_grupo.get()
        if not grupo:
            return
        self.label_fecha_emision.configure(
            text=f"Fecha de emisión: {datetime.today().strftime('%d/%m/%Y')}"
        )
        equipos = getTablaDeGrupo(grupo)
        self._render_tabla_grupo(grupo, equipos or [])

    def buscar_informe_equipo(self, value=None):
        equipo = value or self.combo_equipo.get()
        if not equipo:
            return
        self.label_fecha_emision_equipo.configure(
            text=f"Fecha de emisión: {datetime.today().strftime('%d/%m/%Y')}"
        )
        resultado = getPartidosPorEquipo(equipo)
        if isinstance(resultado, dict):
            partidos = resultado.get("partidos", [])
            clasificacion = resultado.get("clasificacion", None)
        else:
            partidos = resultado or []
            clasificacion = None

        equipos_all = Equipo.getAllEquipos() or []
        equipo_obj = next(
            (e for e in equipos_all if e.get("pais", "").strip().lower() == equipo.strip().lower()), None
        )
        # Preferir la fase almacenada en el equipo (legible). Si no existe, usar la clasificación calculada.
        estado_fase = None
        if equipo_obj:
            estado_fase = equipo_obj.get("fase") or None

        # Normalizaciones simples para casos históricos/varios formatos
        if estado_fase:
            f = estado_fase.strip().lower()
            if "grup" in f:
                estado_fase = "Fase de Grupos"
            elif "clasificado" in f:
                # Mantener la forma 'Clasificado a ...' tal cual
                # capitalizar la primera letra si viene en minúsculas
                estado_fase = estado_fase[0].upper() + estado_fase[1:]
            elif "finalista" in f:
                estado_fase = "Finalista"
            elif "partido por el 3er" in f or "tercer" in f and "puesto" not in f:
                estado_fase = "Partido por el 3er puesto"
            elif "tercer" in f and "puesto" in f:
                estado_fase = "Tercer Puesto"
            elif "cuarto" in f:
                estado_fase = "Cuarto Puesto"
            elif "primer" in f:
                estado_fase = "Primer Puesto"
            elif "segundo" in f:
                estado_fase = "Segundo Puesto"
            # else: mantener la cadena tal cual

        self._render_informe_equipo(partidos, estado_fase or clasificacion)

    def buscar_siguiente_partido(self, value=None):
        equipo = value or self.combo_equipo_siguiente.get()
        if not equipo:
            return
        self.label_fecha_siguiente.configure(
            text=f"Fecha: {datetime.today().strftime('%d/%m/%Y')}"
        )
        partido = getSiguientePartido(equipo)
        self._render_siguiente_partido(partido)

    # renders de las tablas y eso --------------------------------------------------------------------------------
    def _render_tabla_grupo(self, grupo, equipos):
        for widget in self.scroll_grupo.winfo_children():
            widget.destroy()

        if not equipos:
            tk.CTkLabel(self.scroll_grupo, text="Sin datos para este grupo.",
                        text_color="gray").pack(pady=20)
            return

        cols        = ["Grupo " + grupo, "PJ", "G", "E", "P", "GF", "GC", "DG", "Pts"]
        col_widths  = [220, 40, 40, 40, 40, 40, 40, 40, 50]
        col_anchors = ["w", "center","center","center","center","center","center","center","center"]

        header_row = tk.CTkFrame(self.scroll_grupo, fg_color=("gray80", "gray30"), corner_radius=4)
        header_row.pack(fill="x", padx=5, pady=(4, 0))

        for col, width, anchor in zip(cols, col_widths, col_anchors):
            tk.CTkLabel(header_row, text=col, width=width, anchor=anchor,
                        font=("Arial", 11, "bold")).pack(side="left", padx=2, pady=4)

        for eq in equipos:
            fila = tk.CTkFrame(self.scroll_grupo, corner_radius=4)
            fila.pack(fill="x", padx=5, pady=2)

            nombre_frame = tk.CTkFrame(fila, fg_color="transparent", height=24, width=220)
            nombre_frame.pack(side="left", padx=2)
            nombre_frame.pack_propagate(False)

            tk.CTkLabel(nombre_frame, text=str(eq.get("posicion", "")),
                        width=24, text_color="gray").pack(side="left")
            tk.CTkLabel(nombre_frame, text=eq.get("pais", ""),
                        anchor="w").pack(side="left", padx=(4, 0))

            stats = ["pj", "g", "e", "p", "gf", "gc", "dg", "pts"]
            for key, width in zip(stats, col_widths[1:]):
                es_pts = key == "pts"
                tk.CTkLabel(fila, text=str(eq.get(key, 0)), width=width, anchor="center",
                            font=("Arial", 12, "bold") if es_pts else ("Arial", 12)
                            ).pack(side="left", padx=2, pady=6)

    def _render_partidos(self, partidos):
        for widget in self.scroll_fecha.winfo_children():
            widget.destroy()

        fecha_actual = None
        for p in partidos:
            if p["fecha"] != fecha_actual:
                fecha_actual = p["fecha"]
                tk.CTkLabel(self.scroll_fecha, text=fecha_actual,
                            fg_color=("gray85", "gray25"), corner_radius=4,
                            anchor="w").pack(fill="x", pady=(10, 2), padx=5)

            card = tk.CTkFrame(self.scroll_fecha, corner_radius=6)
            card.pack(fill="x", pady=3, padx=5)

            fila = tk.CTkFrame(card, fg_color="transparent")
            fila.pack(pady=(8, 2))

            tk.CTkLabel(fila, text=p["local"],     width=150, anchor="e").pack(side="left")
            tk.CTkLabel(fila, text=p["hora"],      width=60,  font=("Arial", 14, "bold")).pack(side="left")
            tk.CTkLabel(fila, text=p["visitante"], width=150, anchor="w").pack(side="left")

            tk.CTkLabel(card, text=f'{p["fase"]}  ·  {p["lugar"]}',
                        text_color="gray", font=("Arial", 11)).pack(pady=(0, 8))

    def _render_informe_equipo(self, partidos, clasificacion=None):
        for widget in self.scroll_equipo.winfo_children():
            widget.destroy()

        if not partidos:
            tk.CTkLabel(self.scroll_equipo,
                        text="Este equipo no tiene partidos jugados aún.",
                        text_color="gray").pack(pady=20, anchor="w", padx=5)
        else:
            for p in partidos:
                linea = (
                    f"{p['fecha']}  -  {p['fase']}  -  "
                    f"{p['local']} {p['golesLocal']} : {p['golesVisit']} {p['visitante']}"
                )
                tk.CTkLabel(self.scroll_equipo, text=linea, anchor="w",
                            font=("Arial", 12)).pack(fill="x", padx=5, pady=2, anchor="w")

        if clasificacion:
            tk.CTkLabel(self.scroll_equipo, text=clasificacion, anchor="w",
                        font=("Arial", 12, "bold")).pack(fill="x", padx=5, pady=(10, 2), anchor="w")

    def _render_siguiente_partido(self, partido):
        for widget in self.container_siguiente.winfo_children():
            widget.destroy()

        if not partido:
            tk.CTkLabel(self.container_siguiente,
                        text="No hay próximos partidos para este equipo.",
                        text_color="gray").pack(pady=40)
            return

        card = tk.CTkFrame(self.container_siguiente, corner_radius=8, border_width=1,
                           border_color=("gray75", "gray35"))
        card.pack(fill="x", padx=5, pady=5)

        top_row = tk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=14, pady=(12, 4))

        info_col = tk.CTkFrame(top_row, fg_color="transparent")
        info_col.pack(side="left", fill="x", expand=True)

        tk.CTkLabel(info_col, text=partido.get("torneo", ""),
                    font=("Arial", 11), anchor="w").pack(anchor="w")

        fase_lugar = partido.get("fase", "")
        if partido.get("lugar"):
            fase_lugar += f"  ·  {partido['lugar']}"
        tk.CTkLabel(info_col, text=fase_lugar, font=("Arial", 10),
                    text_color="gray", anchor="w").pack(anchor="w")

        tk.CTkLabel(top_row, text=partido.get("fecha", ""),
                    font=("Arial", 10), text_color="gray").pack(side="right", anchor="n")

        sep = tk.CTkFrame(card, height=1, fg_color=("gray80", "gray35"))
        sep.pack(fill="x", padx=14, pady=(4, 0))

        mid_row = tk.CTkFrame(card, fg_color="transparent")
        mid_row.pack(fill="x", padx=14, pady=14)

        equipos_col = tk.CTkFrame(mid_row, fg_color="transparent")
        equipos_col.pack(side="left", fill="y")

        for nombre_equipo in [partido.get("local", ""), partido.get("visitante", "")]:
            fila_eq = tk.CTkFrame(equipos_col, fg_color="transparent")
            fila_eq.pack(anchor="w", pady=4)
            tk.CTkFrame(fila_eq, width=24, height=16, corner_radius=2,
                        fg_color=("gray70", "gray40")).pack(side="left", padx=(0, 8))
            tk.CTkLabel(fila_eq, text=nombre_equipo,
                        font=("Arial", 13, "bold"), anchor="w").pack(side="left")

        tk.CTkLabel(mid_row, text=partido.get("hora", ""),
                    font=("Arial", 26, "bold")).pack(side="right", padx=10)

    def _render_all_grupos(self):
        for widget in self.scroll_all_grupos.winfo_children():
            widget.destroy()

        grupos = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
        col_widths  = [220, 40, 40, 40, 40, 40, 40, 40, 50]
        col_anchors = ["w", "center","center","center","center","center","center","center","center"]

        for grupo in grupos:
            equipos = getTablaDeGrupo(grupo) or []
            if not equipos:
                continue

            cols = ["Grupo " + grupo, "PJ", "G", "E", "P", "GF", "GC", "DG", "Pts"]

            header_row = tk.CTkFrame(self.scroll_all_grupos,
                                     fg_color=("gray80", "gray30"), corner_radius=4)
            header_row.pack(fill="x", padx=5, pady=(4, 0))

            for col, width, anchor in zip(cols, col_widths, col_anchors):
                tk.CTkLabel(header_row, text=col, width=width, anchor=anchor,
                            font=("Arial", 11, "bold")).pack(side="left", padx=2, pady=4)

            for eq in equipos:
                fila = tk.CTkFrame(self.scroll_all_grupos, corner_radius=4)
                fila.pack(fill="x", padx=5, pady=2)

                nombre_frame = tk.CTkFrame(fila, fg_color="transparent", height=24, width=220)
                nombre_frame.pack(side="left", padx=2)
                nombre_frame.pack_propagate(False)

                tk.CTkLabel(nombre_frame, text=str(eq.get("posicion", "")),
                            width=24, text_color="gray").pack(side="left")
                tk.CTkLabel(nombre_frame, text=eq.get("pais", ""),
                            anchor="w").pack(side="left", padx=(4, 0))

                stats = ["pj", "g", "e", "p", "gf", "gc", "dg", "pts"]
                for key, width in zip(stats, col_widths[1:]):
                    es_pts = key == "pts"
                    tk.CTkLabel(fila, text=str(eq.get(key, 0)), width=width, anchor="center",
                                font=("Arial", 12, "bold") if es_pts else ("Arial", 12)
                                ).pack(side="left", padx=2, pady=6)



    def volver(self):
        self.root.back_to_main(self)
