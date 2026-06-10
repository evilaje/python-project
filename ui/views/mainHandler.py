import customtkinter as tk
from ui.views.reportHandler import *
from ui.views.resultsHandler import *
from ui.views.configHandler import *
from models.partido import Partido as PartidoModel

import models.equipo as equipo
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from utils.fecha_utils import *

class MainFrame(tk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        torneoAcivo = isTorneoActivo()
        boton_activo, config_abierto = "normal" if torneoAcivo else "disabled", "normal" if not torneoAcivo else "disabled"

        #DESACTIVAR
        '''descomentar sgte linea para habilitar todos los botones ni bollo'''
        #boton_activo, config_abierto = "normal", "normal"

        #prueba datepicker

        self.btn1 = tk.CTkButton(self, text="Configuración del Torneo", height=50, command=self.ir_a_config)
        self.btn1.configure(state=config_abierto) #lo contrario al resto
        self.btn1.pack(pady=10, padx=10, fill="x")

        self.btn2 = tk.CTkButton(self, text="Registro de Resultados", height=50, command=self.ir_a_result)
        self.btn2.configure(state=boton_activo)
        self.btn2.pack(pady=10, padx=10, fill="x")

        self.btn3 = tk.CTkButton(self, text="Emisión de Informes", height=50, command=self.ir_a_report)
        self.btn3.configure(state=boton_activo)
        self.btn3.pack(pady=10, padx=10, fill="x")

        tk.CTkButton(self, text="Salir", height=50, command=root.destroy).pack(pady=10, padx=10, fill="x")

        # Panel: siguiente partido global
        self.next_panel = tk.CTkFrame(self, corner_radius=6, border_width=1, fg_color=("gray20", "gray15"))
        self.next_panel.pack(pady=(12, 8), padx=10, fill="x")

        header = tk.CTkFrame(self.next_panel, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(12, 0))

        self.next_title = tk.CTkLabel(header, text="Siguiente Partido", font=tk.CTkFont(size=14, weight="bold"))
        self.next_title.pack(side="left")

        self.next_status = tk.CTkLabel(header, text="Cargando...", text_color="gray")
        self.next_status.pack(side="right")

        self.next_card_container = tk.CTkFrame(self.next_panel, fg_color="transparent")
        self.next_card_container.pack(fill="x", padx=10, pady=(8, 12))

        # iniciar actualización periódica
        self.update_next_match()

    def ir_a_config(self):
        config_frame = TorneoConfigFrame(self.root, self)
        print("aparece esto: ", config_frame)
        self.root.show_frame(self, config_frame)

    def ir_a_report(self):
        report_frame = TorneoReportFrame(self.root, self)
        self.root.show_frame(self, report_frame)

    def ir_a_result(self):
        print("Cambiando a anotacion de partidos")
        result_frame = TorneoResultFrame(self.root, self)
        self.root.show_frame(self, result_frame)

    def habilitar_botones(self):
        self.btn2.configure(state="normal")
        self.btn3.configure(state="normal")
        self.btn1.configure(state="disabled", text="Configuración Cerrada")

    def update_next_match(self):
        # Busca partido actualmente en curso (inicio <= ahora <= inicio+2h) o siguiente si no hay ninguno
        partidos = PartidoModel.getPartidosPendientes() or []

        ahora = datetime.now()

        current = None
        upcoming = None
        futuros = []

        for p in partidos:
            fecha = p.get("fecha")
            hora = p.get("hora", "00:00")
            if not fecha:
                continue
            try:
                dt = datetime.strptime(f"{fecha} {hora}", "%d/%m/%Y %H:%M")
            except Exception:
                continue

            if dt <= ahora <= dt + timedelta(hours=2):
                current = (dt, p)
                break

            if dt > ahora:
                futuros.append((dt, p))

        if not current and futuros:
            futuros.sort(key=lambda x: x[0])
            upcoming = futuros[0]

        if current:
            status = "Actualmente jugandose"
            partido = current[1]
        elif upcoming:
            status = "Siguiente partido"
            partido = upcoming[1]
        else:
            self.next_status.configure(text="No hay próximos partidos")
            self._render_next_match_card(None)
            self.after(60000, self.update_next_match)
            return

        self.next_status.configure(text=status)
        self._render_next_match_card(partido)

        # programar siguiente actualización cada 30 segundos para estar seguros de detectar inicio
        self.after(30000, self.update_next_match)

    def _render_next_match_card(self, partido):
        for widget in self.next_card_container.winfo_children():
            widget.destroy()

        if not partido:
            tk.CTkLabel(self.next_card_container,
                        text="No hay próximos partidos.",
                        text_color="gray").pack(pady=20, anchor="w")
            return

        card = tk.CTkFrame(self.next_card_container, corner_radius=8, border_width=1,
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

        eq1 = equipo.getEquipo(partido.get("idEquipo1"))
        eq2 = equipo.getEquipo(partido.get("idEquipo2"))
        local_nombre = eq1.get("pais") if eq1 else partido.get("idEquipo1") or "Por definir"
        visitante_nombre = eq2.get("pais") if eq2 else partido.get("idEquipo2") or "Por definir"

        for nombre_equipo in [local_nombre, visitante_nombre]:
            fila_eq = tk.CTkFrame(equipos_col, fg_color="transparent")
            fila_eq.pack(anchor="w", pady=4)
            tk.CTkFrame(fila_eq, width=24, height=16, corner_radius=2,
                        fg_color=("gray70", "gray40")).pack(side="left", padx=(0, 8))
            tk.CTkLabel(fila_eq, text=nombre_equipo,
                        font=("Arial", 13, "bold"), anchor="w").pack(side="left")

        tk.CTkLabel(mid_row, text=partido.get("hora", ""),
                    font=("Arial", 26, "bold")).pack(side="right", padx=10)
