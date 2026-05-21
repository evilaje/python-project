import customtkinter as tk
from datetime import datetime
from services.partido_controller import *
from models.partido import *
from models.equipo import Equipo
from CTkMessagebox import CTkMessagebox


class TorneoResultFrame(tk.CTkFrame):
    def __init__(self, root, main_frame):
        super().__init__(root)
        self.root = root
        self.main_frame = main_frame

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.vista_resultados()


    def volver(self):
        self.root.back_to_main(self)

    
    def _get_partidos_pendientes(self):
        # select de los partidos que ya pasaron/ ya se pueden cargar
        partidos = Partido.getAllPartidos() or []
        ahora = datetime.now()
        pendientes = []

        for p in partidos:
            # Filtrar por goles sin asignar
            sin_goles = (
                p.get("golesT1", 0) == 0 and
                p.get("golesT2", 0) == 0 and
                p.get("penalesT1", 0) == 0 and
                p.get("penalesT2", 0) == 0
            )

            # Filtrar por fecha y hora posterior a ahora
            try:
                dt_partido = datetime.strptime(
                    f"{p['fecha']} {p['hora']}", "%d/%m/%Y %H:%M"
                )
                cargable = dt_partido < ahora
            except (ValueError, KeyError):
                cargable = False

            if sin_goles and cargable:
                pendientes.append(p)

        return pendientes

    def _label_partido(self, partido):
        """Genera el texto que se muestra en el combobox para cada partido.""" 

        aux = Equipo("", None, None, None)
        aux.id = partido.get("idEquipo1")
        eq1 = aux.getAbreviatura()

        aux.id = partido.get("idEquipo2")
        eq2 = aux.getAbreviatura()

        fecha = partido.get("fecha", "")
        hora = partido.get("hora", "")
        return f"{eq1} vs {eq2} ({fecha} {hora})"

    def seleccionar_partido(self, value=None):
        """Se llama cuando el usuario elige un partido del combobox."""
        label = value or self.combo_partidos.get()
        # Buscar el partido que corresponde al label seleccionado
        partido = next(
            (p for p in self._partidos_pendientes if self._label_partido(p) == label),
            None
        )
        if partido:
            self._partido_seleccionado = partido
            # Limpiar campos al cambiar de partido
            self.cleanInputs([
                self.input_goles_t1, self.input_goles_t2,
                self.input_penales_t1, self.input_penales_t2
            ])

    def guardar_resultado(self):
        if not hasattr(self, "_partido_seleccionado") or not self._partido_seleccionado:
            CTkMessagebox(title="Error", message="Selecciona un partido primero", icon="cancel")
            return

        goles_t1 = self.input_goles_t1.get().strip()
        goles_t2 = self.input_goles_t2.get().strip()
        penales_t1 = self.input_penales_t1.get().strip()
        penales_t2 = self.input_penales_t2.get().strip()

        if not goles_t1 or not goles_t2 or not penales_t1 or not penales_t2:
            CTkMessagebox(title="Error", message="Todos los campos son obligatorios", icon="cancel")
            return

        # Validar que sean numeros enteros no negativos
        try:
            goles_t1 = int(goles_t1)
            goles_t2 = int(goles_t2)
            penales_t1 = int(penales_t1)
            penales_t2 = int(penales_t2)
            if any(v < 0 for v in [goles_t1, goles_t2, penales_t1, penales_t2]):
                raise ValueError
        except ValueError:
            CTkMessagebox(title="Error", message="Los goles deben ser numeros enteros positivos", icon="cancel")
            return

        partido_id = self._partido_seleccionado.get("id")
        resultado = guardarResultado(partido_id, goles_t1, goles_t2, penales_t1, penales_t2)

        if resultado[0]:
            CTkMessagebox(title="Exito", message=resultado[1], icon="check")
            # Refrescar el combobox sin el partido ya cargado
            self._refrescar_combo()
            self._partido_seleccionado = None
        else:
            CTkMessagebox(title="Error", message=resultado[1], icon="cancel")

    def _refrescar_combo(self):
        """Recarga los partidos pendientes y actualiza el combobox."""
        self._partidos_pendientes = self._get_partidos_pendientes()
        labels = [self._label_partido(p) for p in self._partidos_pendientes]
        self.combo_partidos.configure(values=labels)
        self.combo_partidos.set("")
        self.cleanInputs([
            self.input_goles_t1, self.input_goles_t2,
            self.input_penales_t1, self.input_penales_t2
        ])

 
    def vista_resultados(self):
        tk.CTkButton(
            self, text="Volver", width=100,
            fg_color="transparent", border_width=1,
            command=self.volver
        ).grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        tk.CTkLabel(
            self, text="Cargar Resultados",
            font=tk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=1, columnspan=2, pady=(20, 0), sticky="n")

        # Combobox de partidos pendientes
        tk.CTkLabel(
            self, text="Seleccionar partido:"
        ).grid(row=1, column=0, padx=(40, 0), sticky="e")

        self._partidos_pendientes = self._get_partidos_pendientes()
        partido_labels = [self._label_partido(p) for p in self._partidos_pendientes]

        self.combo_partidos = tk.CTkComboBox(
            self,
            values=partido_labels,
            width=300,
            command=self.seleccionar_partido
        )
        self.combo_partidos.set("")
        self.combo_partidos.grid(row=1, column=1, columnspan=2, pady=(20, 10), sticky="w")

        tk.CTkLabel(self, text="Goles Equipo 1").grid(
            row=2, column=0, padx=(40, 10), pady=(20, 5), sticky="e"
        )
        self.input_goles_t1 = tk.CTkEntry(self, placeholder_text="0", width=120)
        self.input_goles_t1.grid(row=2, column=1, padx=(0, 20), pady=(20, 5), sticky="w")

        tk.CTkLabel(self, text="Goles Equipo 2").grid(
            row=2, column=2, padx=(20, 10), pady=(20, 5), sticky="e"
        )
        self.input_goles_t2 = tk.CTkEntry(self, placeholder_text="0", width=120)
        self.input_goles_t2.grid(row=2, column=3, padx=(0, 40), pady=(20, 5), sticky="w")

        tk.CTkLabel(self, text="Penales Equipo 1").grid(
            row=3, column=0, padx=(40, 10), pady=5, sticky="e"
        )
        self.input_penales_t1 = tk.CTkEntry(self, placeholder_text="0", width=120)
        self.input_penales_t1.grid(row=3, column=1, padx=(0, 20), pady=5, sticky="w")

        tk.CTkLabel(self, text="Penales Equipo 2").grid(
            row=3, column=2, padx=(20, 10), pady=5, sticky="e"
        )
        self.input_penales_t2 = tk.CTkEntry(self, placeholder_text="0", width=120)
        self.input_penales_t2.grid(row=3, column=3, padx=(0, 40), pady=5, sticky="w")

        tk.CTkButton(
            self, text="Guardar Resultado", width=220,
            fg_color="#29ABE2",
            command=self.guardar_resultado
        ).grid(row=4, column=1, columnspan=2, pady=(30, 10))

   

    def cleanInputs(self, inputs):
        for entry in inputs:
            entry.delete(0, "end")