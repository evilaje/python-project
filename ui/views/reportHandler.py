from customtkinter import *

def open_report_handler(root):
    window = CTkToplevel(root)
    window.after(10, window.lift) #levanta por encima de la ventana princpal, asi se muestra arribaS
    window.title("teas")
    window.geometry("600x400")
