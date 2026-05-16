import customtkinter as tk

class TorneoReportFrame(tk.CTkFrame):
    def __init__(self, root, main_frame):
        super().__init__(root)
        self.root = root
        self.main_frame = main_frame

        tk.CTkLabel(self, text="Informes").pack(pady=20, padx=20)

        tk.CTkButton(self, text="Volver", command=self.volver).pack(pady=10)
   
    def volver(self):
        self.root.back_to_main(self)
