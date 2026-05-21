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

        # ---------------------------------------------------------------------------
        # submenu de opciones
        self.frame_menu = tk.CTkFrame(self, fg_color="transparent")
        self.frame_menu.pack(fill="both", expand=True)

        tk.CTkLabel(self.frame_menu, text="Resultados", font=("Arial", 20, "bold")).pack(pady=20)
        tk.CTkButton(self.frame_menu, text="Partidos por fecha", command=self.go_to_informe_por_fecha).pack(pady=10)
        tk.CTkButton(self.frame_menu, text="Tabla de Grupo", command=self.go_to_informe_por_grupo).pack(pady=10)
        tk.CTkButton(self.frame_menu, text="Informe de equipo", command=self.go_to_informe_por_equipo).pack(pady=10)
        tk.CTkButton(self.frame_menu, text="Siguiente partido de equipo", command=self.go_to_informe_siguiente_partido).pack(pady=10)
        tk.CTkButton(self.frame_menu, text="Tabla de todos los grupos", command=self.go_to_informe_all_grupos).pack(pady=10)
        tk.CTkButton(self.frame_menu, text="Volver", command=self.volver).pack(pady=10)

        # ----------------------------------------------------------------------------
        # informe por fecha
        self.frame_fecha = tk.CTkFrame(self, fg_color="transparent")
        self._build_frame_fecha()

        # ----------------------------------------------------------------------------
        # informe por grupo
        self.frame_grupo = tk.CTkFrame(self, fg_color="transparent")
        self._build_frame_grupo()

        # ----------------------------------------------------------------------------
        # informe por equipo
        self.frame_equipo = tk.CTkFrame(self, fg_color="transparent")
        self._build_frame_equipo()

        # ----------------------------------------------------------------------------
        # informe siguiente partido de equipo
        self.frame_siguiente = tk.CTkFrame(self, fg_color="transparent")
        self._build_frame_siguiente()

        # ----------------------------------------------------------------------------
        # informe todos los grupos
        self.frame_all_grupos = tk.CTkFrame(self, fg_color="transparent")
        self._build_frame_all_grupos()

    # =============================================================================
    # BUILD: frame_fecha
    # =============================================================================

    def _build_frame_fecha(self):

        header = tk.CTkFrame(self.frame_fecha, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 5))

        tk.CTkButton(header, text="<- Volver", width=100,
                     fg_color="transparent", border_width=1,
                     command=self.go_to_menu).pack(side="left")

        tk.CTkLabel(header, text="Informe 1", font=("Arial", 16, "bold")).pack(side="left", padx=20)

        # input de la fecha
        input_row = tk.CTkFrame(self.frame_fecha, fg_color="transparent")
        input_row.pack(fill="x", padx=20, pady=5)

        tk.CTkLabel(input_row, text="Fecha ingresada:").pack(side="left")
        self.input_fecha = tk.CTkEntry(input_row, placeholder_text="DD/MM/AAAA", width=150)
        self.input_fecha.pack(side="left", padx=10)
        tk.CTkButton(input_row, text="Buscar", width=80, command=self.buscar_partidos_por_fecha).pack(side="left")

        tk.CTkLabel(self.frame_fecha, text="Formato modelo", text_color="gray").pack(anchor="w", padx=20)

        # scrollable donde aparecen los partidos
        self.scroll_fecha = tk.CTkScrollableFrame(self.frame_fecha)
        self.scroll_fecha.pack(fill="both", expand=True, padx=20, pady=10)

    # =============================================================================
    # BUILD: frame_grupo
    # =============================================================================

    def _build_frame_grupo(self):
        # --- header ---
        header = tk.CTkFrame(self.frame_grupo, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 5))

        tk.CTkButton(header, text="<- Volver", width=100,
                     fg_color="transparent", border_width=1,
                     command=self.go_to_menu).pack(side="left")

        tk.CTkLabel(header, text="Informe 2", font=("Arial", 16, "bold")).pack(side="left", padx=20)

        # --- fila: selector de grupo + fecha de emision ---
        input_row = tk.CTkFrame(self.frame_grupo, fg_color="transparent")
        input_row.pack(fill="x", padx=20, pady=5)

        tk.CTkLabel(input_row, text="Grupo:").pack(side="left")

        self.combo_grupo = tk.CTkComboBox(
            input_row,
            values=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
            width=80,
            command=self.buscar_tabla_de_grupo
        )
        self.combo_grupo.set("A")
        self.combo_grupo.pack(side="left", padx=10)

        self.label_fecha_emision = tk.CTkLabel(
            input_row,
            text=f"Fecha de emisión del informe: {datetime.today().strftime('%d/%m/%Y')}",
            text_color="gray"
        )
        self.label_fecha_emision.pack(side="left", padx=20)

        tk.CTkLabel(self.frame_grupo, text="Formato modelo", text_color="gray").pack(anchor="w", padx=20)

        # --- tabla scrollable ---
        self.scroll_grupo = tk.CTkScrollableFrame(self.frame_grupo)
        self.scroll_grupo.pack(fill="both", expand=True, padx=20, pady=10)

    # =============================================================================
    # RENDER: tabla de grupo
    # =============================================================================

    def _render_tabla_grupo(self, grupo, equipos):
        """
        grupo: str  "A", "B", etc.
        equipos: lista de dicts con estructura:
        {
            "posicion": 1,
            "pais":     "Ucrania",
            "pj": 3, "g": 2, "e": 1, "p": 0,
            "gf": 5, "gc": 3, "dg": 2, "pts": 7
        }
        """
        for widget in self.scroll_grupo.winfo_children():
            widget.destroy()

        if not equipos:
            tk.CTkLabel(self.scroll_grupo, text="Sin datos para este grupo.", text_color="gray").pack(pady=20)
            return

        # --- cabecera de la tabla ---
        cols = ["Grupo " + grupo, "PJ", "G", "E", "P", "GF", "GC", "DG", "Pts"]
        col_widths  = [220, 40, 40, 40, 40, 40, 40, 40, 50]
        col_anchors = ["w",  "center","center","center","center","center","center","center","center"]

        header_row = tk.CTkFrame(self.scroll_grupo, fg_color=("gray80", "gray30"), corner_radius=4)
        header_row.pack(fill="x", padx=5, pady=(4, 0))

        for col, width, anchor in zip(cols, col_widths, col_anchors):
            tk.CTkLabel(
                header_row, text=col, width=width, anchor=anchor,
                font=("Arial", 11, "bold")
            ).pack(side="left", padx=2, pady=4)

        # --- filas de equipos ---
        for eq in equipos:
            fila = tk.CTkFrame(self.scroll_grupo, corner_radius=4)
            fila.pack(fill="x", padx=5, pady=2)

            # posicion + nombre
            nombre_frame = tk.CTkFrame(fila, fg_color="transparent", width=220)
            nombre_frame.pack(side="left", padx=2, pady=6)
            nombre_frame.pack_propagate(False)

            tk.CTkLabel(nombre_frame, text=str(eq.get("posicion", "")),
                        width=24, text_color="gray").pack(side="left")
            tk.CTkLabel(nombre_frame, text=eq.get("pais", ""),
                        anchor="w").pack(side="left", padx=(4, 0))

            # stats
            stats = ["pj", "g", "e", "p", "gf", "gc", "dg", "pts"]
            for key, width in zip(stats, col_widths[1:]):
                valor = eq.get(key, 0)
                es_pts = key == "pts"
                tk.CTkLabel(
                    fila,
                    text=str(valor),
                    width=width,
                    anchor="center",
                    font=("Arial", 12, "bold") if es_pts else ("Arial", 12)
                ).pack(side="left", padx=2, pady=6)

    # =============================================================================
    # LOGICA: busquedas
    # =============================================================================

    def buscar_partidos_por_fecha(self):
        fecha = self.input_fecha.get().strip()
        if not fecha:
            self._render_partidos([])
            return

        partidos = getPartidoPorFecha(fecha)
        if not partidos:
            self._render_partidos([])
            return

        self._render_partidos(partidos)

    def buscar_tabla_de_grupo(self, value=None):
        grupo = value or self.combo_grupo.get()
        if not grupo:
            return

        # Actualizar fecha de emision al momento de la consulta
        self.label_fecha_emision.configure(
            text=f"Fecha de emisión del informe: {datetime.today().strftime('%d/%m/%Y')}"
        )

        equipos = getTablaDeGrupo(grupo)
        self._render_tabla_grupo(grupo, equipos or [])

    # =============================================================================
    # RENDER: partidos por fecha (sin cambios)
    # =============================================================================

    def _render_partidos(self, partidos):
        """
        partidos: lista de dicts con estructura:
        {
            "fecha":     "miercoles 08 test año",
            "hora":      "06:07",
            "local":     "Pharloom",
            "visitante": "Niger",
            "fase":      "Octavos de final",
            "lugar":     "Bilewater"
        }
        """
        for widget in self.scroll_fecha.winfo_children():
            widget.destroy()

        fecha_actual = None

        for p in partidos:
            if p["fecha"] != fecha_actual:
                fecha_actual = p["fecha"]
                tk.CTkLabel(self.scroll_fecha, text=fecha_actual,
                            fg_color=("gray85", "gray25"),
                            corner_radius=4,
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

    # =============================================================================
    # BUILD + RENDER: informe por equipo
    # =============================================================================

    def _build_frame_equipo(self):
        header = tk.CTkFrame(self.frame_equipo, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 5))

        tk.CTkButton(header, text="<- Volver", width=100,
                     fg_color="transparent", border_width=1,
                     command=self.go_to_menu).pack(side="left")

        tk.CTkLabel(header, text="Informe 3", font=("Arial", 16, "bold")).pack(side="left", padx=20)

        # fila: selector de equipo + fecha de emision
        input_row = tk.CTkFrame(self.frame_equipo, fg_color="transparent")
        input_row.pack(fill="x", padx=20, pady=5)

        tk.CTkLabel(input_row, text="Equipo:").pack(side="left")

        equipos = Equipo.getAllEquipos() or []
        equipo_names = [e["pais"] for e in equipos]

        self.combo_equipo = tk.CTkComboBox(
            input_row,
            values=equipo_names,
            width=180,
            command=self.buscar_informe_equipo
        )
        self.combo_equipo.set(equipo_names[0] if equipo_names else "")
        self.combo_equipo.pack(side="left", padx=10)

        self.label_fecha_emision_equipo = tk.CTkLabel(
            input_row,
            text=f"Fecha de emisión del informe: {datetime.today().strftime('%d/%m/%Y')}",
            text_color="gray"
        )
        self.label_fecha_emision_equipo.pack(side="left", padx=20)

        tk.CTkLabel(self.frame_equipo, text="Formato modelo", text_color="gray").pack(anchor="w", padx=20)

        self.scroll_equipo = tk.CTkScrollableFrame(self.frame_equipo)
        self.scroll_equipo.pack(fill="both", expand=True, padx=20, pady=10)

    def _render_informe_equipo(self, partidos, clasificacion=None):
        """
        partidos: lista de dicts con estructura:
        {
            "fecha":      "28/09/2025",
            "fase":       "Fase de Grupos",
            "local":      "Marruecos",
            "visitante":  "España",
            "golesLocal": 2,
            "golesVisit": 0
        }
        clasificacion: str opcional, ej: "Clasificado a Octavos de Final"
        """
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
                tk.CTkLabel(
                    self.scroll_equipo,
                    text=linea,
                    anchor="w",
                    font=("Arial", 12)
                ).pack(fill="x", padx=5, pady=2, anchor="w")

        # clasificacion en bold al final, si la hay
        if clasificacion:
            tk.CTkLabel(
                self.scroll_equipo,
                text=clasificacion,
                anchor="w",
                font=("Arial", 12, "bold")
            ).pack(fill="x", padx=5, pady=(10, 2), anchor="w")

    def buscar_informe_equipo(self, value=None):
        equipo = value or self.combo_equipo.get()
        if not equipo:
            return

        self.label_fecha_emision_equipo.configure(
            text=f"Fecha de emisión del informe: {datetime.today().strftime('%d/%m/%Y')}"
        )

        resultado = getPartidosPorEquipo(equipo)
        # getPartidosPorEquipo devuelve un dict: {"partidos": [...], "clasificacion": str|None}
        # o directamente una lista si no hay clasificacion, adaptate a lo que devuelva tu controller
        if isinstance(resultado, dict):
            partidos = resultado.get("partidos", [])
            clasificacion = resultado.get("clasificacion", None)
        else:
            partidos = resultado or []
            clasificacion = None

        self._render_informe_equipo(partidos, clasificacion)

    

    # =============================================================================
    # BUILD + RENDER: informe siguiente partido (informe 4)
    # =============================================================================

    def _build_frame_siguiente(self):
        header = tk.CTkFrame(self.frame_siguiente, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 5))

        tk.CTkButton(header, text="<- Volver", width=100,
                     fg_color="transparent", border_width=1,
                     command=self.go_to_menu).pack(side="left")

        tk.CTkLabel(header, text="Informe 4", font=("Arial", 16, "bold")).pack(side="left", padx=20)

        # fila: selector de equipo + fecha de emision
        input_row = tk.CTkFrame(self.frame_siguiente, fg_color="transparent")
        input_row.pack(fill="x", padx=20, pady=5)

        tk.CTkLabel(input_row, text="Equipo:").pack(side="left")

        equipos = Equipo.getAllEquipos() or []
        equipo_names = [e["pais"] for e in equipos]

        self.combo_equipo_siguiente = tk.CTkComboBox(
            input_row,
            values=equipo_names,
            width=180,
            command=self.buscar_siguiente_partido
        )
        self.combo_equipo_siguiente.set(equipo_names[0] if equipo_names else "")
        self.combo_equipo_siguiente.pack(side="left", padx=10)

        self.label_fecha_siguiente = tk.CTkLabel(
            input_row,
            text=f"Fecha : {datetime.today().strftime('%d/%m/%Y')}",
            text_color="gray"
        )
        self.label_fecha_siguiente.pack(side="left", padx=20)

        tk.CTkLabel(self.frame_siguiente, text="Formato modelo", text_color="gray").pack(anchor="w", padx=20)

        # contenedor donde se monta la card del partido
        self.container_siguiente = tk.CTkFrame(self.frame_siguiente, fg_color="transparent")
        self.container_siguiente.pack(fill="both", expand=True, padx=20, pady=10)

    def _render_siguiente_partido(self, partido):
        """
        partido: dict con estructura:
        {
            "torneo":    "Copa Mundial Sub-20 de la FIFA Chile 2025™",
            "fase":      "Octavos de final",
            "lugar":     "Estadio Fiscal",
            "fecha":     "08/10/2025",
            "hora":      "20:00",
            "local":     "PAR",
            "visitante": "NOR"
        }
        O None si no hay próximo partido.
        """
        for widget in self.container_siguiente.winfo_children():
            widget.destroy()

        if not partido:
            tk.CTkLabel(
                self.container_siguiente,
                text="No hay próximos partidos para este equipo.",
                text_color="gray"
            ).pack(pady=40)
            return

        # card principal
        card = tk.CTkFrame(self.container_siguiente, corner_radius=8, border_width=1,
                           border_color=("gray75", "gray35"))
        card.pack(fill="x", padx=5, pady=5)

        # --- fila superior: torneo+fase a la izquierda, fecha a la derecha ---
        top_row = tk.CTkFrame(card, fg_color="transparent")
        top_row.pack(fill="x", padx=14, pady=(12, 4))

        info_col = tk.CTkFrame(top_row, fg_color="transparent")
        info_col.pack(side="left", fill="x", expand=True)

        tk.CTkLabel(info_col,
                    text=partido.get("torneo", ""),
                    font=("Arial", 11),
                    anchor="w").pack(anchor="w")

        fase_lugar = partido.get("fase", "")
        if partido.get("lugar"):
            fase_lugar += f"  ·  {partido['lugar']}"

        tk.CTkLabel(info_col,
                    text=fase_lugar,
                    font=("Arial", 10),
                    text_color="gray",
                    anchor="w").pack(anchor="w")

        tk.CTkLabel(top_row,
                    text=partido.get("fecha", ""),
                    font=("Arial", 10),
                    text_color="gray").pack(side="right", anchor="n")

        # separador
        sep = tk.CTkFrame(card, height=1, fg_color=("gray80", "gray35"))
        sep.pack(fill="x", padx=14, pady=(4, 0))

        # --- fila central: equipos + hora ---
        mid_row = tk.CTkFrame(card, fg_color="transparent")
        mid_row.pack(fill="x", padx=14, pady=14)

        # columna equipos (izquierda)
        equipos_col = tk.CTkFrame(mid_row, fg_color="transparent")
        equipos_col.pack(side="left", fill="y")

        for nombre_equipo in [partido.get("local", ""), partido.get("visitante", "")]:
            fila_eq = tk.CTkFrame(equipos_col, fg_color="transparent")
            fila_eq.pack(anchor="w", pady=4)

            # banderita placeholder (cuadradito de color) — reemplazala por CTkImage si tenes banderas
            tk.CTkFrame(fila_eq, width=24, height=16,
                        corner_radius=2,
                        fg_color=("gray70", "gray40")).pack(side="left", padx=(0, 8))

            tk.CTkLabel(fila_eq,
                        text=nombre_equipo,
                        font=("Arial", 13, "bold"),
                        anchor="w").pack(side="left")

        # hora (derecha, centrada verticalmente)
        tk.CTkLabel(mid_row,
                    text=partido.get("hora", ""),
                    font=("Arial", 26, "bold")).pack(side="right", padx=10)

    def buscar_siguiente_partido(self, value=None):
        equipo = value or self.combo_equipo_siguiente.get()
        if not equipo:
            return

        self.label_fecha_siguiente.configure(
            text=f"Fecha : {datetime.today().strftime('%d/%m/%Y')}"
        )

        partido = getSiguientePartido(equipo)
        self._render_siguiente_partido(partido)

    # =============================================================================
    # informe todos los grupos 
    # =============================================================================

    def _build_frame_all_grupos(self):
        header = tk.CTkFrame(self.frame_all_grupos, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 5))

        tk.CTkButton(header, text="<- Volver", width=100,
                     fg_color="transparent", border_width=1,
                     command=self.go_to_menu).pack(side="left")

        tk.CTkLabel(header, text="Informe 5", font=("Arial", 16, "bold")).pack(side="left", padx=20)

        self.label_fecha_all_grupos = tk.CTkLabel(
            self.frame_all_grupos,
            text=f"Fecha de emisión del Informe: {datetime.today().strftime('%d/%m/%Y')}",
            text_color="gray",
            anchor="w"
        )
        self.label_fecha_all_grupos.pack(anchor="w", padx=20, pady=(0, 2))

        tk.CTkLabel(self.frame_all_grupos, text="Formato modelo",
                    text_color="gray", anchor="w").pack(anchor="w", padx=20)

        # un unico scroll con todos los grupos apilados
        self.scroll_all_grupos = tk.CTkScrollableFrame(self.frame_all_grupos)
        self.scroll_all_grupos.pack(fill="both", expand=True, padx=20, pady=10)

    def _render_all_grupos(self):
        for widget in self.scroll_all_grupos.winfo_children():
            widget.destroy()

        grupos = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

        # cabecera de columnas reutilizable
        cols        = ["", "PJ", "G", "E", "P", "GF", "GC", "DG", "Pts"]
        col_widths  = [220, 36, 36, 36, 36, 36, 36, 36, 44]
        col_anchors = ["w", "center","center","center","center","center","center","center","center"]

        for grupo in grupos:
            equipos = getTablaDeGrupo(grupo) or []

            # no mostrar grupos vacios
            if not equipos:
                continue

            # --- titulo del grupo ---
            tk.CTkLabel(
                self.scroll_all_grupos,
                text=f"Grupo {grupo}",
                font=("Arial", 11, "bold"),
                anchor="w"
            ).pack(fill="x", padx=5, pady=(14, 0))

            # --- cabecera de columnas ---
            header_row = tk.CTkFrame(self.scroll_all_grupos,
                                     fg_color=("gray80", "gray30"), corner_radius=4)
            header_row.pack(fill="x", padx=5, pady=(2, 0))

            for col, width, anchor in zip(cols, col_widths, col_anchors):
                tk.CTkLabel(
                    header_row, text=col, width=width, anchor=anchor,
                    font=("Arial", 9, "bold")
                ).pack(side="left", padx=1, pady=2)

            # --- filas de equipos ---
            for eq in equipos:
                fila = tk.CTkFrame(self.scroll_all_grupos, corner_radius=3, height=24)
                fila.pack(fill="x", padx=5, pady=1)
                fila.pack_propagate(False)

                # posicion + nombre
                nombre_frame = tk.CTkFrame(fila, fg_color="transparent", width=220, height=24)
                nombre_frame.pack(side="left", padx=1)
                nombre_frame.pack_propagate(False)

                tk.CTkLabel(nombre_frame, text=str(eq.get("posicion", "")),
                            width=20, text_color="gray",
                            font=("Arial", 9)).pack(side="left")
                tk.CTkLabel(nombre_frame, text=eq.get("pais", ""),
                            anchor="w", font=("Arial", 9)).pack(side="left", padx=(3, 0))

                # stats
                stats = ["pj", "g", "e", "p", "gf", "gc", "dg", "pts"]
                for key, width in zip(stats, col_widths[1:]):
                    es_pts = key == "pts"
                    tk.CTkLabel(
                        fila,
                        text=str(eq.get(key, 0)),
                        width=width,
                        anchor="center",
                        font=("Arial", 9, "bold") if es_pts else ("Arial", 9)
                    ).pack(side="left", padx=1)

    def go_to_menu(self):
        self.frame_fecha.pack_forget()
        self.frame_grupo.pack_forget()
        self.frame_equipo.pack_forget()
        self.frame_siguiente.pack_forget()
        self.frame_all_grupos.pack_forget()
        self.frame_menu.pack(fill="both", expand=True)

    def go_to_informe_por_fecha(self):
        self.frame_menu.pack_forget()
        self.frame_fecha.pack(fill="both", expand=True)

    def go_to_informe_por_grupo(self):
        self.frame_menu.pack_forget()
        self.buscar_tabla_de_grupo(self.combo_grupo.get())
        self.frame_grupo.pack(fill="both", expand=True)

    def go_to_informe_por_equipo(self):
        self.frame_menu.pack_forget()
        self.buscar_informe_equipo(self.combo_equipo.get())
        self.frame_equipo.pack(fill="both", expand=True)

    def go_to_informe_siguiente_partido(self):
        self.frame_menu.pack_forget()
        self.buscar_siguiente_partido(self.combo_equipo_siguiente.get())
        self.frame_siguiente.pack(fill="both", expand=True)

    def go_to_informe_all_grupos(self):
        self.frame_menu.pack_forget()
        self.label_fecha_all_grupos.configure(
            text=f"Fecha de emisión del Informe: {datetime.today().strftime('%d/%m/%Y')}"
        )
        self._render_all_grupos()
        self.frame_all_grupos.pack(fill="both", expand=True)

    def volver(self):
        self.root.back_to_main(self)