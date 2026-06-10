"""
Descarga las banderas del torneo desde el repo hampusborgos/country-flags.

Pasos que hace el script:
  1. Baja el ZIP del repo (rama main)
  2. Extrae solo los PNG de png100px/ que necesitamos
  3. Los copia a assets/flags/ renombrados por abreviatura del torneo
  4. Borra el ZIP temporal

Requiere: requests, Pillow  →  pip install requests Pillow
"""

import requests
import os
import zipfile
import io

# Mapeo: abreviatura del torneo → código ISO del repo (carpeta png100px)
PAISES = {
    "MEX": "mx",      # México
    "RSA": "za",      # Sudáfrica
    "KOR": "kr",      # Corea del Sur
    "CZE": "cz",      # Chequia
    "CAN": "ca",      # Canadá
    "BIH": "ba",      # Bosnia y Herzegovina
    "QAT": "qa",      # Catar
    "SUI": "ch",      # Suiza
    "BRA": "br",      # Brasil
    "MAR": "ma",      # Marruecos
    "HAI": "ht",      # Haití
    "SCO": "gb-sct",  # Escocia
    "USA": "us",      # Estados Unidos
    "PAR": "py",      # Paraguay
    "AUS": "au",      # Australia
    "TUR": "tr",      # Turquía
    "GER": "de",      # Alemania
    "CUW": "cw",      # Curazao
    "CIV": "ci",      # Costa de Marfil
    "ECU": "ec",      # Ecuador
    "NED": "nl",      # Países Bajos
    "JPN": "jp",      # Japón
    "SWE": "se",      # Suecia
    "TUN": "tn",      # Túnez
    "BEL": "be",      # Bélgica
    "EGY": "eg",      # Egipto
    "IRN": "ir",      # Irán
    "NZL": "nz",      # Nueva Zelanda
    "ESP": "es",      # España
    "CPV": "cv",      # Cabo Verde
    "KSA": "sa",      # Arabia Saudita
    "URU": "uy",      # Uruguay
    "FRA": "fr",      # Francia
    "SEN": "sn",      # Senegal
    "IRQ": "iq",      # Irak
    "NOR": "no",      # Noruega
    "ARG": "ar",      # Argentina
    "ALG": "dz",      # Argelia
    "AUT": "at",      # Austria
    "JOR": "jo",      # Jordania
    "POR": "pt",      # Portugal
    "COD": "cd",      # Congo RD
    "UZB": "uz",      # Uzbekistán
    "COL": "co",      # Colombia
    "ENG": "gb-eng",  # Inglaterra
    "CRO": "hr",      # Croacia
    "GHA": "gh",      # Ghana
    "PAN": "pa",      # Panamá
}

ZIP_URL = "https://github.com/hampusborgos/country-flags/archive/refs/heads/main.zip"
OUT_DIR = "assets/flags"
FLAG_W, FLAG_H = 48, 32  # tamaño final en px (se puede cambiar)

os.makedirs(OUT_DIR, exist_ok=True)

# 1. Bajar el ZIP completo del repo
print("Descargando repo (puede tardar unos segundos)...")
r = requests.get(ZIP_URL, timeout=60)
r.raise_for_status()
print(f"ZIP descargado ({len(r.content) / 1024 / 1024:.1f} MB), convirtiendo banderas...")

# 2. Abrir el ZIP en memoria, convertir SVG → PNG con cairosvg
try:
    import cairosvg
except ImportError:
    print("\nFalta cairosvg. Instalalo con:  pip install cairosvg")
    raise SystemExit(1)

iso_a_abrev = {v: k for k, v in PAISES.items()}
ok, fail = [], []

with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
    nombres = set(zf.namelist())
    for iso, abrev in iso_a_abrev.items():
        zip_path = f"country-flags-main/svg/{iso}.svg"
        if zip_path not in nombres:
            print(f"✗ {abrev} ({iso}) — no encontrado en el ZIP")
            fail.append(abrev)
            continue

        with zf.open(zip_path) as f:
            svg_data = f.read()

        png_data = cairosvg.svg2png(bytestring=svg_data, output_width=FLAG_W, output_height=FLAG_H)
        dest = os.path.join(OUT_DIR, f"{abrev}.png")
        with open(dest, "wb") as out:
            out.write(png_data)
        print(f"✓ {abrev} ({iso})")
        ok.append(abrev)

print(f"\nGuardadas en '{OUT_DIR}': {len(ok)}/{len(PAISES)}")
if fail:
    print(f"Fallidas: {', '.join(fail)}")