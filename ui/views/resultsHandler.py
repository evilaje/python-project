import customtkinter as tk
from datetime import datetime
from services.partido_controller import *
from models.partido import *
from models.equipo import Equipo, getEquipo
from models.torneo import getTorneo, avanzarFase, setFaseTorneo
from CTkMessagebox import CTkMessagebox
from services.equipo_controller import isParaguayGanador


class TorneoResultFrame(tk.CTkFrame):
    def __init__(self, root, main_frame):
        super().__init__(root)
        self.root = root
        self.main_frame = main_frame

        self._partido_seleccionado = None
        self._item_activo = None  # tupla (frame, label) del ítem resaltado

        # ── Layout raíz: sidebar | contenido ──────────────────────────────────
        self.grid_columnconfigure(0, weight=0)   # sidebar (ancho fijo)
        self.grid_columnconfigure(1, weight=1)   # panel derecho
        self.grid_rowconfigure(0, weight=1)

        self._avanzar_fase_si_corresponde()
        self._build_sidebar()
        self._build_panel_derecho()

    # ══════════════════════════════════════════════════════════════════════════
    #  SIDEBAR
    # ══════════════════════════════════════════════════════════════════════════

    def _build_sidebar(self):
        self.sidebar = tk.CTkFrame(self, width=220, corner_radius=0,
                                   fg_color=("gray15", "gray10"))
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(1, weight=1)

        tk.CTkLabel(
            self.sidebar,
            text="Partidos:",
            font=tk.CTkFont(size=18, weight="bold"),
            anchor="w",
        ).grid(row=0, column=0, padx=24, pady=(24, 10), sticky="w")

        self.scroll_partidos = tk.CTkScrollableFrame(
            self.sidebar, fg_color="transparent"
        )
        self.scroll_partidos.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self.scroll_partidos.grid_columnconfigure(0, weight=1)

        tk.CTkButton(
            self.sidebar,
            text="← Volver",
            anchor="w",
            height=36,
            fg_color="transparent",
            hover_color=("gray25", "gray20"),
            text_color=("gray60", "gray55"),
            font=tk.CTkFont(size=12),
            command=self.volver,
        ).grid(row=2, column=0, padx=16, pady=(0, 24), sticky="ew")

        self._cargar_lista_partidos()

    def _cargar_lista_partidos(self):
        """Destruye y recrea todos los ítems de la lista de partidos."""
        for widget in self.scroll_partidos.winfo_children():
            widget.destroy()
        self._item_activo = None

        self._partidos_pendientes = self._get_partidos_pendientes()

        if not self._partidos_pendientes:
            print("NO se han encontrao partidos")
            tk.CTkLabel(
                self.scroll_partidos,
                text="Sin partidos\npendientes",
                text_color="gray",
                anchor="w",
                justify="left",
            ).grid(row=0, column=0, padx=16, pady=16, sticky="w")
            self._mostrar_placeholder_vacio()
            return

        # ancho disponible dentro del scroll (sidebar 220 - padx 8*2 - scrollbar ~16)
        WRAP = 172

        for i, partido in enumerate(self._partidos_pendientes):
            texto = self._label_partido(partido)

            # Frame clicable — soporta wraplength a través del CTkLabel hijo
            item_frame = tk.CTkFrame(
                self.scroll_partidos,
                fg_color="transparent",
                corner_radius=6,
                cursor="hand2",
            )
            item_frame.grid(row=i, column=0, padx=4, pady=2, sticky="ew")
            item_frame.grid_columnconfigure(0, weight=1)

            item_label = tk.CTkLabel(
                item_frame,
                text=texto,
                anchor="w",
                justify="left",
                wraplength=WRAP,
                font=tk.CTkFont(size=12),
                text_color=("gray90", "gray85"),
                padx=8,
                pady=6,
            )
            item_label.grid(row=0, column=0, sticky="ew")

            # Bind en frame Y label para cubrir toda el área clicable
            for w in (item_frame, item_label):
                w.bind("<Button-1>",
                       lambda e, p=partido, f=item_frame, l=item_label:
                       self._on_partido_click(p, f, l))
                w.bind("<Enter>",
                       lambda e, f=item_frame: f.configure(fg_color=("gray25", "gray20")))
                w.bind("<Leave>",
                       lambda e, f=item_frame:
                       None if (self._item_activo and f is self._item_activo[0])
                       else f.configure(fg_color="transparent"))

        # Seleccionar automáticamente el partido más próximo
        self.after(50, self._seleccionar_partido_proximo)

    def _seleccionar_partido_proximo(self):
        """Selecciona y resalta el partido más próximo en la lista."""
        if not self._partidos_pendientes:
            return

        partido_proximo = self._get_partido_mas_proximo(self._partidos_pendientes)
        if partido_proximo is None:
            partido_proximo = self._partidos_pendientes[0]

        # Buscar el índice en la lista para encontrar el frame/label correspondiente
        idx = self._partidos_pendientes.index(partido_proximo)
        items = list(self.scroll_partidos.winfo_children())

        # Los items son CTkFrame, uno por partido
        if idx < len(items):
            item_frame = items[idx]
            # El label es el primer hijo del frame
            children = item_frame.winfo_children()
            if children:
                item_label = children[0]
                self._on_partido_click(partido_proximo, item_frame, item_label)

    def _get_partido_mas_proximo(self, partidos):
        """Devuelve el partido con fecha/hora más próxima a ahora (o el primero si no hay fechas)."""
        ahora = datetime.now()
        mejor = None
        menor_diff = None

        for p in partidos:
            try:
                dt = datetime.strptime(f"{p['fecha']} {p['hora']}", "%d/%m/%Y %H:%M")
                diff = abs((dt - ahora).total_seconds())
                if menor_diff is None or diff < menor_diff:
                    menor_diff = diff
                    mejor = p
            except (ValueError, KeyError):
                continue

        return mejor if mejor is not None else (partidos[0] if partidos else None)

    def _on_partido_click(self, partido, frame, lbl):
        # Desresaltar el anterior
        if self._item_activo:
            prev_frame, prev_lbl = self._item_activo
            prev_frame.configure(fg_color="transparent")
            prev_lbl.configure(
                text_color=("gray90", "gray85"),
                font=tk.CTkFont(size=12, weight="normal"),
            )
        # Resaltar el nuevo
        frame.configure(fg_color=("gray30", "gray25"))
        lbl.configure(
            text_color=("white", "white"),
            font=tk.CTkFont(size=12, weight="bold"),
        )
        self._item_activo = (frame, lbl)
        self._partido_seleccionado = partido
        self._mostrar_partido(partido)
        self.cleanInputs([
            self.input_goles_t1, self.input_goles_t2,
            self.input_penales_t1, self.input_penales_t2,
        ])

    # ══════════════════════════════════════════════════════════════════════════
    #  panel de la derecha
    # ══════════════════════════════════════════════════════════════════════════

    def _build_panel_derecho(self):
        panel = tk.CTkFrame(self, fg_color="transparent")
        panel.grid(row=0, column=1, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_columnconfigure(1, weight=1)
        panel.grid_rowconfigure(9, weight=1)

        self.label_nombre_partido = tk.CTkLabel(
            panel,
            text="Selecciona un partido",
            font=tk.CTkFont(size=16, weight="bold"),
            text_color=("gray60", "gray50"),
            anchor="w",
            justify="left",
            wraplength=400,  # se actualiza dinámicamente en _on_panel_resize
        )
        self.label_nombre_partido.grid(
            row=0, column=0, columnspan=2, padx=32, pady=(24, 4), sticky="ew"
        )
        # Actualizar wraplength cuando el panel cambie de tamaño
        panel.bind("<Configure>", self._on_panel_resize)

        sep = tk.CTkFrame(panel, height=1, fg_color=("gray75", "gray30"))
        sep.grid(row=1, column=0, columnspan=2, padx=32, pady=(0, 18), sticky="ew")

        self.label_eq1 = tk.CTkLabel(
            panel,
            text="Equipo 1",
            font=tk.CTkFont(size=15, weight="bold"),
            anchor="w",
        )
        self.label_eq1.grid(row=2, column=0, columnspan=2, padx=32, pady=(0, 8), sticky="w")

        tk.CTkLabel(panel, text="Goles", anchor="w").grid(
            row=3, column=0, padx=(32, 8), sticky="w"
        )
        tk.CTkLabel(panel, text="Penales", anchor="w").grid(
            row=3, column=1, padx=(0, 32), sticky="w"
        )

        self.input_goles_t1 = tk.CTkEntry(panel, placeholder_text="0", width=140)
        self.input_goles_t1.grid(row=4, column=0, padx=(32, 8), pady=(4, 12), sticky="w")

        self.input_penales_t1 = tk.CTkEntry(panel, placeholder_text="0", width=140)
        self.input_penales_t1.grid(row=4, column=1, padx=(0, 32), pady=(4, 12), sticky="w")

        sep2 = tk.CTkFrame(panel, height=1, fg_color=("gray80", "gray25"))
        sep2.grid(row=5, column=0, columnspan=2, padx=32, pady=(0, 12), sticky="ew")

        self.label_eq2 = tk.CTkLabel(
            panel,
            text="Equipo 2",
            font=tk.CTkFont(size=15, weight="bold"),
            anchor="w",
        )
        self.label_eq2.grid(row=6, column=0, columnspan=2, padx=32, pady=(0, 8), sticky="w")

        tk.CTkLabel(panel, text="Goles", anchor="w").grid(
            row=7, column=0, padx=(32, 8), sticky="w"
        )
        tk.CTkLabel(panel, text="Penales", anchor="w").grid(
            row=7, column=1, padx=(0, 32), sticky="w"
        )

        self.input_goles_t2 = tk.CTkEntry(panel, placeholder_text="0", width=140)
        self.input_goles_t2.grid(row=8, column=0, padx=(32, 8), pady=(4, 16), sticky="w")

        self.input_penales_t2 = tk.CTkEntry(panel, placeholder_text="0", width=140)
        self.input_penales_t2.grid(row=8, column=1, padx=(0, 32), pady=(4, 16), sticky="w")

        # Guardar referencia al panel para poder manipular el placeholder
        self._panel_derecho = panel

        # Label de "no hay partidos", oculto por defecto
        self._label_no_partidos = tk.CTkLabel(
            panel,
            text="No hay partidos disponibles",
            font=tk.CTkFont(size=16),
            text_color=("gray55", "gray45"),
            anchor="center",
            justify="center",
        )

        tk.CTkButton(
            panel,
            text="Guardar Resultado",
            height=40,
            width=220,
            fg_color="#29ABE2",
            hover_color="#1a8abf",
            command=self.guardar_resultado,
        ).grid(row=10, column=0, padx=32, pady=(0, 24), sticky="w")

    def _mostrar_placeholder_vacio(self):
        """Oculta el contenido normal del panel derecho y muestra el mensaje de sin partidos."""
        # Ocultar widgets de contenido
        self.label_nombre_partido.grid_remove()
        self.label_eq1.grid_remove()
        self.label_eq2.grid_remove()

        # Mostrar el label centrado ocupando todo el espacio disponible
        self._label_no_partidos.grid(
            row=0, column=0, columnspan=2,
            padx=32, pady=32,
            sticky="nsew",
        )
        self._panel_derecho.grid_rowconfigure(0, weight=1)

    def _ocultar_placeholder_vacio(self):
        """Restaura el contenido normal del panel derecho."""
        self._label_no_partidos.grid_remove()
        self._panel_derecho.grid_rowconfigure(0, weight=0)
        self.label_nombre_partido.grid()
        self.label_eq1.grid()
        self.label_eq2.grid()

    def _on_panel_resize(self, event):
        # Descuenta los padx=32 de cada lado
        wrap = max(100, event.width - 64)
        self.label_nombre_partido.configure(wraplength=wrap)

    def _mostrar_partido(self, partido):
        # Asegurarse de que el placeholder esté oculto
        self._ocultar_placeholder_vacio()

        equipo1 = getEquipo(partido.get("idEquipo1")) if partido.get("idEquipo1") else None
        equipo2 = getEquipo(partido.get("idEquipo2")) if partido.get("idEquipo2") else None

        abrev_eq1 = equipo1.get("abreviatura") if equipo1 else None
        nombre_eq1 = equipo1.get("pais") if equipo1 else None

        abrev_eq2 = equipo2.get("abreviatura") if equipo2 else None
        nombre_eq2 = equipo2.get("pais") if equipo2 else None

        abrev_eq1 = abrev_eq1 or partido.get("idEquipo1") or "Equipo 1"
        nombre_eq1 = nombre_eq1 or (f"Equipo {partido.get('idEquipo1')}" if partido.get('idEquipo1') else "Equipo 1")
        abrev_eq2 = abrev_eq2 or partido.get("idEquipo2") or "Equipo 2"
        nombre_eq2 = nombre_eq2 or (f"Equipo {partido.get('idEquipo2')}" if partido.get('idEquipo2') else "Equipo 2")

        fase = partido.get("fase", "")
        fecha = partido.get("fecha", "")
        hora = partido.get("hora", "")
        lugar = partido.get("lugar", "")

        linea1 = f"{abrev_eq1} vs {abrev_eq2}"
        partes_linea2 = []
        if fase:
            partes_linea2.append(fase)
        if fecha or hora:
            partes_linea2.append(f"{fecha} {hora}".strip())
        if lugar:
            partes_linea2.append(lugar)
        titulo = linea1
        if partes_linea2:
            titulo += "\n" + "  ·  ".join(partes_linea2)

        self.label_nombre_partido.configure(
            text=titulo,
            text_color=("gray85", "gray80"),
        )
        self.label_eq1.configure(text=nombre_eq1)
        self.label_eq2.configure(text=nombre_eq2)

    # ══════════════════════════════════════════════════════════════════════════
    #  cambios en los archivos/get data
    # ══════════════════════════════════════════════════════════════════════════

    def _get_partidos_pendientes(self):
        partidos = Partido.getAllPartidos() or []
        ahora = datetime.now()
        pendientes = []
        current_phase = self._get_fase_actual()

        for p in partidos:
            if not self._partido_en_fase_actual(p, current_phase):
                continue
            pendiente_por_jugar = not p.get("jugado", False)
            try:
                dt_partido = datetime.strptime(
                    f"{p['fecha']} {p['hora']}", "%d/%m/%Y %H:%M"
                )
                #descomenta esta linea papu cargable = dt_partido < ahora y comenta la sgte xd
                cargable = True
            except (ValueError, KeyError):
                cargable = False
            if pendiente_por_jugar and cargable:
                pendientes.append(p)

        return pendientes

    def _get_fase_actual(self):
        torneo = getTorneo(1)
        if torneo and torneo.get("fase"):
            return torneo.get("fase")
        return "Fase de Grupos"

    def _partido_en_fase_actual(self, partido, fase_actual):
        fase_partido = partido.get("fase", "Fase de Grupos")
        if fase_actual == "16avos de Final":
            return fase_partido in ("16avos de Final", "Eliminatorias")
        return fase_partido == fase_actual

    def _fase_completada(self, partidos, fase, total):
        fase_matches = [p for p in partidos if (p.get("fase") == fase and p.get("jugado") == True)]
        return len(fase_matches) == total

    def _fase_estan_asignados_los_equipos(self, partidos, fase, total):
        fase_matches = [p for p in partidos if p.get("fase") == fase]
        if len(fase_matches) != total:
            return False
        return all(p.get("idEquipo1") and p.get("idEquipo2") for p in fase_matches)

    def _avanzar_fase_si_corresponde(self):
        print("avanzar si corresponde")
        partidos = Partido.getAllPartidos() or []
        current_phase = self._get_fase_actual()

        if self._fase_completada(partidos, "Fase de Grupos", 72):
            equipos_ya_asignados = self._fase_estan_asignados_los_equipos(partidos, "16avos de Final", 16)
            if not equipos_ya_asignados:
                avanzarFase()
                setEliminatorias()
                if current_phase != "16avos de Final":
                    setFaseTorneo("16avos de Final")
                CTkMessagebox(title="Info", message="Dieciseisavos de Final configurados.", icon="check")

        if self._fase_completada(partidos, "16avos de Final", 16):
            equipos_ya_asignados = self._fase_estan_asignados_los_equipos(partidos, "Octavos de Final", 8)
            if not equipos_ya_asignados:
                setOctavos()
                if current_phase != "Octavos de Final":
                    setFaseTorneo("Octavos de Final")
                CTkMessagebox(title="Info", message="Octavos de Final configurados.", icon="check")

        if self._fase_completada(partidos, "Octavos de Final", 8):
            equipos_ya_asignados = self._fase_estan_asignados_los_equipos(partidos, "Cuartos de Final", 4)
            if not equipos_ya_asignados:
                setCuartos()
                if current_phase != "Cuartos de Final":
                    setFaseTorneo("Cuartos de Final")
                CTkMessagebox(title="Info", message="Cuartos de Final configurados.", icon="check")

        if self._fase_completada(partidos, "Cuartos de Final", 4):
            equipos_ya_asignados = self._fase_estan_asignados_los_equipos(partidos, "Semifinal", 2)
            if not equipos_ya_asignados:
                setSemis()
                if current_phase != "Semifinal":
                    setFaseTorneo("Semifinal")
                CTkMessagebox(title="Info", message="Semifinales configurados.", icon="check")

        if self._fase_completada(partidos, "Semifinal", 2):
            equipos_ya_asignados_tercer = self._fase_estan_asignados_los_equipos(partidos, "Tercer Puesto", 1)
            if not equipos_ya_asignados_tercer:
                setFinal()
                if current_phase != "Tercer Puesto":
                    setFaseTorneo("Tercer Puesto")
                CTkMessagebox(title="Info", message="Partido por el Tercer Puesto disponible.", icon="check")

        if self._fase_completada(partidos, "Tercer Puesto", 1):
            if current_phase != "Final":
                setFaseTorneo("Final")
            CTkMessagebox(title="Info", message="Final configurada.", icon="check")

    def _label_partido(self, partido):
        aux = Equipo("", None, None, None)
        aux.id = partido.get("idEquipo1")
        eq1 = aux.getAbreviatura() or "???"
        aux.id = partido.get("idEquipo2")
        eq2 = aux.getAbreviatura() or "???"
        fecha = partido.get("fecha", "")
        hora = partido.get("hora", "")
        return f"{eq1} vs {eq2}\n{fecha} {hora}".strip()

    def guardar_resultado(self):
        if not self._partido_seleccionado:
            CTkMessagebox(title="Error", message="Selecciona un partido primero", icon="cancel")
            return

        goles_t1 = self.input_goles_t1.get().strip()
        goles_t2 = self.input_goles_t2.get().strip()
        penales_t1 = self.input_penales_t1.get().strip()
        penales_t2 = self.input_penales_t2.get().strip()

        if not goles_t1 or not goles_t2:
            CTkMessagebox(title="Error", message="Los goles de ambos equipos son obligatorios", icon="cancel")
            return

        if (penales_t1 and not penales_t2) or (penales_t2 and not penales_t1):
            CTkMessagebox(title="Error", message="Completa ambos campos de penales o deja los dos vacíos", icon="cancel")
            return

        #verificar q en caso d empate los penales no se vayan vacios
        if self._partido_seleccionado.get("fase") != "Fase de Grupos":
            if goles_t1 == goles_t2:
                if penales_t1 == penales_t2 or (not penales_t1 and not penales_t2):
                    CTkMessagebox(title="Error", message="No se puede empatar en la tanda de penales", icon="cancel")
                    return


        if not penales_t1 and not penales_t2:
            penales_t1 = "0"
            penales_t2 = "0"

        try:
            goles_t1 = int(goles_t1)
            goles_t2 = int(goles_t2)
            penales_t1 = int(penales_t1)
            penales_t2 = int(penales_t2)
            if any(v < 0 for v in [goles_t1, goles_t2, penales_t1, penales_t2]):
                raise ValueError
        except ValueError:
            CTkMessagebox(title="Error", message="Los goles y penales deben ser números enteros positivos", icon="cancel")
            return

        partido_id = self._partido_seleccionado.get("id")
        resultado = guardarResultado(partido_id, goles_t1, goles_t2, penales_t1, penales_t2)

        if resultado[0]:
            CTkMessagebox(title="Exito", message=resultado[1], icon="check")
            self._avanzar_fase_si_corresponde()
            self._partido_seleccionado = None
            self._cargar_lista_partidos()
            self.cleanInputs([
                self.input_goles_t1, self.input_goles_t2,
                self.input_penales_t1, self.input_penales_t2,
            ])
        else:
            CTkMessagebox(title="Error", message=resultado[1], icon="cancel")

    def volver(self):
        self._check_paraguay_ganador()
        self.root.back_to_main(self)

    def cleanInputs(self, inputs):
        for entry in inputs:
            entry.delete(0, "end")

    def _check_paraguay_ganador(self):
        if isParaguayGanador():
            self._mostrar_video_ganador()

    def _mostrar_video_ganador(self):
        import  os

        ventana = tk.CTkToplevel(self.root)
        ventana.title("PARAGUAY CAMPEOON!!!!!1")
        ventana.geometry("640x400")
        ventana.grab_set()  # bloquea la ventana principal hasta cerrar esta

        label = tk.CTkLabel(ventana, text="🇵🇾 ¡PARAGUAY GANO EL TORNEO PAPAAAA! 🇵🇾",
                            font=tk.CTkFont(size=22, weight="bold"))
        label.pack(pady=20)
        rutaVid = get_path("assets", "py_campeon.mp4")

        if os.path.exists(rutaVid):
            os.startfile(rutaVid)
        else:
            print("NO SE PUDO REPRODUCIR EL VIDEO")
