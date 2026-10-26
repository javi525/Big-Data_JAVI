# ==============================================================================
# SCRIPT 2: PREPROCESAMIENTO AVANZADO DE DATOS (VERSIÓN R)
# ==============================================================================

library(tidyverse)

# 1. Fijar directorio de trabajo con barras normales '/'
setwd("C:/Users/5/Desktop/JAVI/R")

print("🧹 Iniciando la fase avanzada de preprocesamiento de datos en R...")

# 2. Rutas absolutas explícitas usando barras normales '/'
archivo_entrada <- "C:/Users/5/Desktop/JAVI/R/airbnb_espana_master.csv"
archivo_salida  <- "C:/Users/5/Desktop/JAVI/R/airbnb_espana_clean.csv"

# Cargar dataset maestro
df <- read_csv(archivo_entrada, show_col_types = FALSE)
filas_iniciales <- nrow(df)

# =====================================================================
# RETO 1: LIMPIEZA DE PRECIOS Y CONVERSIÓN A EUROS
# =====================================================================
print("\n2️⃣ Limpiando precios (en Euros nativos)...")

df <- df %>% 
  mutate(
    price_original = price,
    moneda_original = "EUR",
    tipo_cambio_por_eur = 1.0,
    precio_moneda_local = as.numeric(str_replace_all(as.character(price), "[$,€]", "")),
    precio_eur = round(precio_moneda_local, 2)
  )

# =====================================================================
# RETO 2: TRATAMIENTO DE VALORES NULOS (MISSING VALUES)
# =====================================================================
print("\n3️⃣ Tratando nulos y creando variables enriquecidas...")

# Imputación por la mediana regional para bedrooms y beds
df <- df %>% 
  group_by(region_origen) %>% 
  mutate(
    bedrooms = ifelse(is.na(bedrooms), median(bedrooms, na.rm = TRUE), bedrooms),
    beds = ifelse(is.na(beds), median(beds, na.rm = TRUE), beds)
  ) %>% 
  ungroup()

# Banderas de nulos y superhost
df <- df %>% 
  mutate(
    has_no_reviews = ifelse(is.na(review_scores_rating), 1, 0),
    review_scores_rating = ifelse(is.na(review_scores_rating), 0, review_scores_rating),
    host_is_superhost = ifelse(is.na(host_is_superhost), "f", host_is_superhost)
  )

# Extracción numérica de baños desde bathrooms_text
texto_banos <- str_to_lower(coalesce(as.character(df$bathrooms_text), "1"))
df <- df %>% 
  mutate(
    bathrooms_num = as.numeric(str_extract(texto_banos, "\\d+\\.?\\d*")),
    bathrooms_num = ifelse(str_detect(texto_banos, "half") & is.na(bathrooms_num), 0.5, bathrooms_num),
    bathrooms_num = ifelse(is.na(bathrooms_num), 1.0, bathrooms_num)
  )

# =====================================================================
# RETO 3: FILTRADO DE OUTLIERS DE PRECIO [10€ - 1000€]
# =====================================================================
print("\n4️⃣ Filtrando precios de 10 a 1.000 EUR...")

nulos_precio <- sum(is.na(df$precio_eur))
inferiores <- sum(df$precio_eur < 10, na.rm = TRUE)
superiores <- sum(df$precio_eur > 1000, na.rm = TRUE)

df <- df %>% filter(precio_eur >= 10 & precio_eur <= 1000)

df <- df %>% mutate(price = precio_eur)

# Guardar dataset limpio final
write_csv(df, archivo_salida)

print(paste("📊 Filas originales:", filas_iniciales))
print(paste("❌ Sin precio válido:", nulos_precio))
print(paste("⚠️ Fuera de rango:", inferiores, "inferiores y", superiores, "superiores"))
print(paste("✅ Filas conservadas:", nrow(df)))
print(paste("🎉 Archivo limpio generado con éxito:", archivo_salida))