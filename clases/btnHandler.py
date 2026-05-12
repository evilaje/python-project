import customtkinter as tk

#comando del btn1
def open_torneo_config(root):
    window = tk.CTkToplevel(root)
    window.title("Configuración del Torneo")
    window.geometry("600x400")

    label = tk.CTkLabel(window, text="Test")
    label.pack(pady=20, padx=20)

    close_btn = tk.CTkButton(window, text="Cerrar", command=window.destroy)
    close_btn.pack(pady=10)



#comando del btn2


#comando del btn3