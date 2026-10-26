from pathlib import Path
import pandas as pd

# Directorio que contiene una carpeta por ciudad, cada una con su listings.csv
RUTA_BASE: Path = Path(__file__).resolve().parent / "Datos"
ARCHIVO_SALIDA: Path = Path(__file__).resolve().parent / "airbnb_espana_master.csv"

COLUMNAS_CLAVE: list[str] = [
    "id", "listing_url", "name", "host_id", "host_name", "host_is_superhost",
    "neighbourhood_cleansed", "latitude", "longitude", "room_type",
    "accommodates", "bathrooms_text", "bedrooms", "beds", "price",
    "number_of_reviews", "review_scores_rating",
]

print("Iniciando unificación de alojamientos en España...")
if not RUTA_BASE.is_dir():
    raise FileNotFoundError(f"Carpeta no encontrada: {RUTA_BASE}. Ajusta RUTA_BASE a tu ordenador.")

lista_dataframes: list[pd.DataFrame] = []
for carpeta_region in sorted(RUTA_BASE.iterdir()):
    if not carpeta_region.is_dir():
        continue
    archivo_listings: Path = carpeta_region / "listings.csv"
    if not archivo_listings.is_file():
        continue
    df_region: pd.DataFrame = pd.read_csv(archivo_listings, usecols=COLUMNAS_CLAVE, low_memory=False)
    df_region["region_origen"] = carpeta_region.name.title()
    lista_dataframes.append(df_region)
    print(f"  {carpeta_region.name}: {len(df_region)} filas")

if not lista_dataframes:
    raise ValueError(f"No se encontraron archivos listings.csv dentro de {RUTA_BASE}")

df_maestro: pd.DataFrame = pd.concat(lista_dataframes, ignore_index=True)
df_maestro = df_maestro.drop_duplicates(subset=["region_origen", "id"]).copy()

df_maestro.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8-sig")
print(f"Dataset maestro guardado: {ARCHIVO_SALIDA.name} ({len(df_maestro)} filas)")