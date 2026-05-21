import customtkinter as tk
from services.partido_controller import getPartidoPorFecha
from services.equipo_controller import getTablaDeGrupo
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

        # ----------------------------------------------------------------------------

        # ----------------------------------------------------------------------------

    

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

    

    def _build_frame_grupo(self):
        header = tk.CTkFrame(self.frame_grupo, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 5))

        tk.CTkButton(header, text="<- Volver", width=100,
                     fg_color="transparent", border_width=1,
                     command=self.go_to_menu).pack(side="left")

        tk.CTkLabel(header, text="Informe 2", font=("Arial", 16, "bold")).pack(side="left", padx=20)

        
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

        self.scroll_grupo = tk.CTkScrollableFrame(self.frame_grupo)
        self.scroll_grupo.pack(fill="both", expand=True, padx=20, pady=10)

    # -----------------------------------------------------------------------------
    # tabla de grupo
    # -----------------------------------------------------------------------------

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

        cols = ["Grupo " + grupo, "PJ", "G", "E", "P", "GF", "GC", "DG", "Pts"]
        col_widths  = [220, 40, 40, 40, 40, 40, 40, 40, 50]
        col_anchors = ["w",  "center","center","center","center","center","center","center","center"]

        header_row = tk.CTkFrame(self.scroll_grupo, fg_color=("gray80", "gray30"), corner_radius=4)
        header_row.pack(fill="x", padx=5, pady=(1, 0))

        for col, width, anchor in zip(cols, col_widths, col_anchors):
            tk.CTkLabel(
                header_row, text=col, width=width, height=22, anchor=anchor,
                font=("Arial", 10, "bold")
            ).pack(side="left", padx=2, pady=1)

        # --- filas de equipos ---
        for eq in equipos:
            fila = tk.CTkFrame(self.scroll_grupo, corner_radius=4, height=28)
            fila.pack(fill="x", padx=5, pady=1)
            fila.pack_propagate(False)

            # posicion + nombre
            nombre_frame = tk.CTkFrame(fila, fg_color="transparent", width=220, height=28)
            nombre_frame.pack(side="left", padx=2, pady=1)
            nombre_frame.pack_propagate(False)

            tk.CTkLabel(nombre_frame, text=str(eq.get("posicion", "")),
                        width=24, height=22, text_color="gray",
                        font=("Arial", 10)).pack(side="left")
            tk.CTkLabel(nombre_frame, text=eq.get("pais", ""),
                        width=180, height=22, anchor="w",
                        font=("Arial", 10)).pack(side="left", padx=(4, 0))

            # stats
            stats = ["pj", "g", "e", "p", "gf", "gc", "dg", "pts"]
            for key, width in zip(stats, col_widths[1:]):
                valor = eq.get(key, 0)
                es_pts = key == "pts"
                tk.CTkLabel(
                    fila,
                    text=str(valor),
                    width=width,
                    height=22,
                    anchor="center",
                    font=("Arial", 10, "bold") if es_pts else ("Arial", 10)
                ).pack(side="left", padx=2, pady=1)

    # -----------------------------------------------------------------------------
    # busquedas
    # -----------------------------------------------------------------------------

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

    # -----------------------------------------------------------------------------
    # partidos por fecha
    # -----------------------------------------------------------------------------

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

    # -----------------------------------------------------------------------------
    # nav
    # -----------------------------------------------------------------------------

    def go_to_menu(self):
        self.frame_fecha.pack_forget()
        self.frame_grupo.pack_forget()
        self.frame_menu.pack(fill="both", expand=True)

    def go_to_informe_por_fecha(self):
        self.frame_menu.pack_forget()
        self.frame_fecha.pack(fill="both", expand=True)

    def go_to_informe_por_grupo(self):
        self.frame_menu.pack_forget()
        # Cargar el grupo por defecto al entrar
        self.buscar_tabla_de_grupo(self.combo_grupo.get())
        self.frame_grupo.pack(fill="both", expand=True)

    def go_to_informe_por_equipo(self):
        pass

    def go_to_informe_siguiente_partido(self):
        pass

    def go_to_informe_all_grupos(self):
        pass

    def volver(self):
        self.root.back_to_main(self)