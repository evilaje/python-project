import customtkinter as tk

#comando del btn1
"""validar que no se pueda abrir mas de una vez"""
def open_torneo_config(root):
    window = tk.CTkToplevel(root)
    window.after(10, window.lift) #levanta por encima de la ventana princpal, asi se muestra arriba
    window.title("Configuración del Torneo")
    window.geometry("600x400")

    label = tk.CTkLabel(window, text="Placeholder")
    label.pack(pady=20, padx=20)

    btnGrupo = tk.CTkButton(window, text="Grupos")
    btnGrupo.pack(pady=10)

    btnEquipos = tk.CTkButton(window, text="Equipos")
    btnEquipos.pack(pady=10)

    btnCalendario = tk.CTkButton(window, text="Calendario")
    btnCalendario.pack(pady=10)

    # Este boton es importante de ver, en teoria cuando se le de click ya no se tiene que poder
    # acceder a esta ventana en especifico, ya no se tiene que poder cambiar la configuracion del torneo
    # y cuando se toque este boton recien se va a habilitar el btn2 en main
    # capaz necesitemos un txt con estados que hay que mantener al cerrar la app

    # para habilitar este boton tienen que haber 104 partidos, 48 equipos y 12 grupos segun el reglamento 
    btnCerrarConfig = tk.CTkButton(window, text="Cerrar Configuración")
    btnCerrarConfig.pack(pady=10)

    close_btn = tk.CTkButton(window, text="Salir", command=window.destroy)
    close_btn.pack(pady=10)

