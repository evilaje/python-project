import customtkinter as tk
from ui.views.reportHandler import *
from ui.views.resultsHandler import *
from ui.views.configHandler import *

class MainFrame(tk.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        torneoAcivo = isTorneoActivo()
        boton_activo, config_abierto = "normal" if torneoAcivo else "disabled", "normal" if not torneoAcivo else "disabled"

        #DESACTIVAR
        '''descomentar sgte linea para habilitar todos los botones ni bollo'''
        #boton_acitvo, config_abierto = "normal", "normal"

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

    def ir_a_config(self):
        config_frame = TorneoConfigFrame(self.root, self)
        print("aparece esto: ", config_frame)
        self.root.show_frame(self, config_frame)

    def ir_a_report(self):
        report_frame = TorneoReportFrame(self.root, self)
        self.root.show_frame(self, report_frame)

    def ir_a_result(self):
        result_frame = TorneoResultFrame(self.root, self)
        self.root.show_frame(self, result_frame)

    def habilitar_botones(self):
        self.btn2.configure(state="normal")
        self.btn3.configure(state="normal")
        self.btn1.configure(state="disabled", text="Configuración Cerrada")
