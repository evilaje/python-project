import customtkinter as tk

class GruposView(tk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")

        self.controller = controller

        tk.CTkButton(
            self,
            text="<- Torneo",
            command=controller.go_to_torneo
        ).grid(row=0, column=0)

        tk.CTkLabel(
            self,
            text="Configuración de Grupos"
        ).grid(row=0, column=1)

        tk.CTkButton(
            self,
            text="Guardar Grupos",
            command=controller.guardar_grupos
        ).grid(row=3, column=1)
