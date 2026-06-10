from PIL import Image
import customtkinter as ctk
import os

_cache: dict = {}

def init_flags(flags_dir: str, size: tuple = (24, 16)):
    """Llamar una sola vez al arrancar la app."""
    global _cache
    for archivo in os.listdir(flags_dir):
        if archivo.endswith(".png"):
            codigo = archivo[:-4].upper()  # "py.png" → "PY"
            ruta = os.path.join(flags_dir, archivo)
            img = Image.open(ruta).resize(size, Image.LANCZOS)
            _cache[codigo] = ctk.CTkImage(light_image=img, dark_image=img, size=size)

def get_flag(codigo_iso: str) -> ctk.CTkImage | None:
    return _cache.get((codigo_iso or "").upper())