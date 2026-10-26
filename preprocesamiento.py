from pathlib import Path
import pandas as pd

CARPETA: Path = Path(__file__).resolve().parent
ARCHIVO_ENTRADA: Path = CARPETA / "airbnb_espana_master.csv"
ARCHIVO_SALIDA: Path = CARPETA / "airbnb_espana_clean.csv"

print("1. Cargando dataset maestro de España...")
df: pd.DataFrame = pd.read_csv(ARCHIVO_ENTRADA, low_memory=False)
filas_iniciales: int = len(df)

print("2. Limpiando precios (en Euros nativos)...")
df["price_original"] = df["price"]
df["moneda_original"] = "EUR"
df["tipo_cambio_por_eur"] = 1.0

# Limpieza de formato de precio (ej. '$1,250.00' o '150.00' -> 1250.0 o 150.0)
df["precio_moneda_local"] = pd.to_numeric(
    df["price"].astype("string").str.replace(r"[$,€]", "", regex=True).str.strip(),
    errors="coerce",
)
df["precio_eur"] = df["precio_moneda_local"].round(2)

print("3. Tratando nulos y creando variables enriquecidas...")
for columna in ("bedrooms", "beds"):
    df[columna] = df.groupby("region_origen")[columna].transform(
        lambda serie: serie.fillna(serie.median())
    )

df["has_no_reviews"] = df["review_scores_rating"].isna().astype(int)
df["host_is_superhost"] = df["host_is_superhost"].fillna("f")

texto_banos: pd.Series = df["bathrooms_text"].astype("string").str.lower()
df["bathrooms_num"] = pd.to_numeric(
    texto_banos.str.extract(r"(\d+\.?\d*)", expand=False), errors="coerce"
)
medio_bano: pd.Series = texto_banos.str.contains("half", na=False) & df["bathrooms_num"].isna()
df.loc[medio_bano, "bathrooms_num"] = 0.5

print("4. Filtrando precios de 10 a 1.000 EUR...")
nulos_precio: int = int(df["precio_eur"].isna().sum())
inferiores: int = int((df["precio_eur"] < 10).sum())
superiores: int = int((df["precio_eur"] > 1000).sum())
df = df.loc[df["precio_eur"].between(10, 1000)].copy()

if df.empty:
    raise ValueError("El filtro dejó cero filas: revisa los formatos de precio.")

df["price"] = df["precio_eur"]
df.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8-sig")

print(f"Filas originales: {filas_iniciales}")
print(f"Sin precio válido: {nulos_precio}")
print(f"Fuera de rango: {inferiores} inferiores y {superiores} superiores")
print(f"Filas conservadas: {len(df)}")
print(f"Archivo limpio generado: {ARCHIVO_SALIDA.name}")