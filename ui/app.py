import customtkinter as tk
from ui.views.mainHandler import *

class App(tk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Placeholder nombre")
        self.geometry("800x600")

        self.main_frame = MainFrame(self)
        self.main_frame.pack(pady=20, padx=60, fill="both", expand=True)  

    def show_frame(self, frame_actual, frame_nuevo):
        frame_actual.pack_forget()
        frame_nuevo.pack(pady = 20, padx = 20, fill = "both", expand = True)

    def back_to_main(self, frame_actual):
        frame_actual.pack_forget()
        self.main_frame.pack(pady = 20, padx = 20, fill = "both", expand = True)
