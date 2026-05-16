import customtkinter as tk
from services.partido_controller import getPartidoPorFecha

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
        #informe por fecha
        self.frame_fecha = tk.CTkFrame(self, fg_color="transparent")
        self._build_frame_fecha()

        # ----------------------------------------------------------------------------

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

        # div ahh scrollable donde se aparecen los partidos
        self.scroll_fecha = tk.CTkScrollableFrame(self.frame_fecha)
        self.scroll_fecha.pack(fill="both", expand=True, padx=20, pady=10)

    def _render_partidos(self, partidos):
        """
        partidos: lista de dicts con estructura:
        {
            "fecha": "miercoles 08 test año",
            "hora":        "06:07",
            "local":       "Pharloom",  (equipo1)
            "visitante":   "Niger",     (equipo2)
            "fase":        "Octavos de final",
            "lugar":     "Bilewater"
        }
        """
        # clear de lo que haya habido antes en el frame
        for widget in self.scroll_fecha.winfo_children():
            widget.destroy()

        fecha_actual = None

        for p in partidos:

            # separador de fecha si cambia
            if p["fecha"] != fecha_actual:
                fecha_actual = p["fecha"]
                tk.CTkLabel(self.scroll_fecha, text=fecha_actual,
                            fg_color=("gray85", "gray25"),
                            corner_radius=4,
                            anchor="w").pack(fill="x", pady=(10, 2), padx=5)

            # card del partido
            card = tk.CTkFrame(self.scroll_fecha, corner_radius=6)
            card.pack(fill="x", pady=3, padx=5)

            # fila principal -> el equipo local, hora partido, equipo visitante
            fila = tk.CTkFrame(card, fg_color="transparent")
            fila.pack(pady=(8, 2))

            tk.CTkLabel(fila, text=p["local"], width=150, anchor="e").pack(side="left")
            tk.CTkLabel(fila, text=p["hora"], width=60,  font=("Arial", 14, "bold")).pack(side="left")
            tk.CTkLabel(fila, text=p["visitante"], width=150, anchor="w").pack(side="left")

            # fila 2 -> fase y estadio
            tk.CTkLabel(card, text=f'{p["fase"]}  ·  {p["lugar"]}',
                        text_color="gray", font=("Arial", 11)).pack(pady=(0, 8))

    
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


    # funcion para volver al submenu, hay que poner en todas las vistas ngl
    def go_to_menu(self):
        self.frame_fecha.pack_forget()
        self.frame_menu.pack(fill="both", expand=True)

    def go_to_informe_por_fecha(self):
        self.frame_menu.pack_forget()
        self.frame_fecha.pack(fill="both", expand=True)

    def go_to_informe_por_grupo(self):
        pass

    def go_to_informe_por_equipo(self):
        pass

    def go_to_informe_siguiente_partido(self):
        pass

    def go_to_informe_all_grupos(self):
        pass
    

    def volver(self):
        self.root.back_to_main(self)

    