import customtkinter as tk

class TorneoResultFrame(tk.CTkFrame):
    def __init__(self, root, main_frame):
        super().__init__(root)
        self.root = root
        self.main_frame = main_frame

        tk.CTkLabel(self, text="Resultados").pack(pady=20, padx=20)

        tk.CTkButton(self, text="test").pack(pady=10)
        tk.CTkButton(self, text="Volver", command=self.volver).pack(pady=10)

   
    def volver(self):
        self.root.back_to_main(self)