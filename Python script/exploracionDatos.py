# ============================================================
# 📊 SCRIPT MAESTRO AIRBNB ESPAÑA - VERSIÓN TOTAL Y DEFINITIVA
# ============================================================

import numpy as np
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.colheader_justify", "left")

print("🚀 Cargando el dataset limpio 'airbnb_espana_clean.csv'...")
df = pd.read_csv("airbnb_espana_clean.csv", low_memory=False)

# Normalización de tipos numéricos
df["precio_eur"] = pd.to_numeric(df["precio_eur"], errors="coerce")
df["review_scores_rating"] = pd.to_numeric(
    df["review_scores_rating"], errors="coerce"
)
df["number_of_reviews"] = pd.to_numeric(
    df["number_of_reviews"], errors="coerce"
)
df["accommodates"] = pd.to_numeric(df["accommodates"], errors="coerce")
df["beds"] = pd.to_numeric(df["beds"], errors="coerce")
df["bedrooms"] = pd.to_numeric(df["bedrooms"], errors="coerce")
df["bathrooms_num"] = pd.to_numeric(df["bathrooms_num"], errors="coerce")
df["es_superhost"] = df["host_is_superhost"].eq("t")


# ============================================================
# 📌 PARTE 1: CONSULTAS GENERALES Y MERCADO (1 a 15)
# ============================================================

print("\n🔍 --------------------------------------------------------")
print("📌 1. TOP 5 ALOJAMIENTOS MÁS CAROS EN ESPAÑA:")
print("----------------------------------------------------------")
top_caros = df.sort_values(by="precio_eur", ascending=False)[
    ["name", "region_origen", "precio_eur", "room_type"]
].head(5)
print(top_caros.to_string(index=False))
print(
    "🎯 Objetivo: Identificar el techo tarifario del mercado e inspeccionar los"
    " activos de ultra lujo en España."
)
print(
    "💡 Conclusión: La oferta más cara alcanza los "
    + str(round(top_caros["precio_eur"].iloc[0], 2))
    + "€ por noche, protagonizada por alojamientos de tipo "
    + str(top_caros["room_type"].iloc[0])
    + " en regiones como "
    + str(top_caros["region_origen"].iloc[0])
    + "."
)

print("\n📈 --------------------------------------------------------")
print("📌 2. RESUMEN DEL MERCADO POR REGIÓN (Precio y Volumen):")
print("----------------------------------------------------------")
resumen_region = (
    df.groupby("region_origen")
    .agg(
        precio_promedio=("precio_eur", "mean"),
        total_alojamientos=("id", "count"),
    )
    .round(2)
    .sort_values(by="precio_promedio", ascending=False)
)
print(resumen_region)
print(
    "🎯 Objetivo: Evaluar la dimensión de la oferta y el nivel de precios"
    " medio por destino geográfico."
)
print(
    "💡 Conclusión: Mallorca lidera el coste medio con "
    + str(resumen_region.loc["Mallorca", "precio_promedio"])
    + "€/noche y "
    + str(resumen_region.loc["Mallorca", "total_alojamientos"])
    + " alojamientos, contrastando con Madrid que acumula "
    + str(resumen_region.loc["Mad", "total_alojamientos"])
    + " anuncios con un precio medio de "
    + str(resumen_region.loc["Mad", "precio_promedio"])
    + "€."
)

print("\n⭐ --------------------------------------------------------")
print("📌 3. COMPARATIVA: ¿SER SUPERHOST MARCA LA DIFERENCIA?")
print("----------------------------------------------------------")
superhost_comp = (
    df.groupby("host_is_superhost")
    .agg(
        precio_medio=("precio_eur", "mean"),
        puntuacion_media=("review_scores_rating", "mean"),
        total_propiedades=("id", "count"),
    )
    .round(2)
)
print(superhost_comp)
print(
    "🎯 Objetivo: Determinar si el sello Superhost otorga un 'premium' en"
    " tarifa y mejor puntuación."
)
print(
    "💡 Conclusión: Los Superhosts consiguen una valoración media de "
    + str(superhost_comp.loc["t", "puntuacion_media"])
    + " frente a "
    + str(superhost_comp.loc["f", "puntuacion_media"])
    + " de los estándar, manteniendo tarifas equivalentes."
)

print("\n🎯 --------------------------------------------------------")
print("📌 4. BÚSQUEDA DE OPORTUNIDADES (Filtro Cruzado Inversor):")
print("----------------------------------------------------------")
oportunidades = df.loc[
    df["precio_eur"].lt(80)
    & df["review_scores_rating"].ge(4.6)
    & df["number_of_reviews"].ge(10)
].copy()
print(
    "🎯 Se han encontrado "
    + str(len(oportunidades))
    + " opciones que cumplen los requisitos."
)
if not oportunidades.empty:
  print(
      oportunidades[[
          "name",
          "neighbourhood_cleansed",
          "precio_eur",
          "review_scores_rating",
      ]]
      .head(5)
      .to_string(index=False)
  )
print(
    "🎯 Objetivo: Isolar la oferta de alto valor (excelente nota y precio"
    " asequible por debajo de 80€)."
)
print(
    "💡 Conclusión: Se localizan "
    + str(len(oportunidades))
    + " opciones atractivas que combinan precios inferiores a 80€ con"
    " valoraciones medias superiores a 4.6."
)

print("\n🏠 --------------------------------------------------------")
print("📌 5. MATRIZ DE DISTRIBUCIÓN: TIPO DE ALOJAMIENTO POR REGIÓN:")
print("----------------------------------------------------------")
matriz_tipo = pd.crosstab(df["region_origen"], df["room_type"])
print(matriz_tipo)
print(
    "🎯 Objetivo: Analizar la tipología del producto ofrecido según la"
    " vocación de cada comunidad."
)
print(
    "💡 Conclusión: El formato 'Entire home/apt' es predominante en zonas"
    " vacacionales, mientras las capitales concentran más habitaciones"
    " privadas."
)

print("\n📊 --------------------------------------------------------")
print("📌 6J. RANKING DE CIUDADES POR VALORACIÓN:")
print("----------------------------------------------------------")
r6j = (
    df.groupby("region_origen")
    .agg(
        puntuacion_media=("review_scores_rating", "mean"),
        precio_medio=("precio_eur", "mean"),
        total_oferta=("id", "count"),
    )
    .round(2)
    .sort_values(by="puntuacion_media", ascending=False)
)
print(r6j)
print(
    "🎯 Objetivo: Clasificar los destinos según la satisfacción media de los"
    " huéspedes."
)
print(
    "💡 Conclusión: El País Vasco encabeza la satisfacción con "
    + str(r6j.loc["Pv", "puntuacion_media"])
    + " de nota media."
)

print("\n🏢 --------------------------------------------------------")
print("📌 7J. CONCENTRACIÓN DE MERCADO: TOP ANFITRIONES POR REGIÓN:")
print("----------------------------------------------------------")
r7j = (
    df.groupby(["region_origen", "host_id", "host_name"])
    .agg(
        total_propiedades=("id", "count"), precio_promedio=("precio_eur", "mean")
    )
    .reset_index()
    .sort_values(by="total_propiedades", ascending=False)
    .head(10)
)
print(r7j.to_string(index=False))
print(
    "🎯 Objetivo: Detectar la presencia de grandes gestores multipropiedad"
    " por región."
)
print(
    "💡 Conclusión: El principal gestor concentra "
    + str(r7j["total_propiedades"].iloc[0])
    + " alojamientos bajo una misma titularidad."
)

print("\n📍 --------------------------------------------------------")
print("📌 8J. RESUMEN POR BARRIO/VECINDARIO (Capacidad y Precio):")
print("----------------------------------------------------------")
r8j = (
    df.groupby(["region_origen", "neighbourhood_cleansed"])
    .agg(
        total_alojamientos=("id", "count"),
        precio_medio=("precio_eur", "mean"),
        capacidad_promedio=("accommodates", "mean"),
        puntuacion_media=("review_scores_rating", "mean"),
    )
    .round(2)
    .sort_values(by="total_alojamientos", ascending=False)
    .head(10)
)
print(r8j)
print(
    "🎯 Objetivo: Localizar los epicentros de densidad de oferta en el ámbito"
    " micro-local."
)
print(
    "💡 Conclusión: El barrio con mayor oferta acumula "
    + str(r8j["total_alojamientos"].iloc[0])
    + " unidades a un precio medio de "
    + str(r8j["precio_medio"].iloc[0])
    + "€."
)

print("\n🛏️ --------------------------------------------------------")
print("📌 9J. RATIO DE CAMAS Y DORMITORIOS POR CAPACIDAD:")
print("----------------------------------------------------------")
r9j = (
    df.groupby("room_type")
    .agg(
        capacidad_media=("accommodates", "mean"),
        dormitorios_promedio=("bedrooms", "mean"),
        camas_promedio=("beds", "mean"),
        precio_medio=("precio_eur", "mean"),
    )
    .round(2)
)
print(r9j)
print(
    "🎯 Objetivo: Analizar la configuración arquitectónica según el formato"
    " de alquiler."
)
print(
    "💡 Conclusión: Las viviendas enteras ofrecen una media de "
    + str(r9j.loc["Entire home/apt", "capacidad_media"])
    + " plazas con "
    + str(r9j.loc["Entire home/apt", "dormitorios_promedio"])
    + " dormitorios."
)

print("\n💬 --------------------------------------------------------")
print("📌 10J. MÉTRICAS DE POPULARIDAD Y PRECIO:")
print("----------------------------------------------------------")
r10j = (
    df.groupby("region_origen")
    .agg(
        total_resenas=("number_of_reviews", "sum"),
        resenas_promedio_por_alojamiento=("number_of_reviews", "mean"),
        puntuacion_promedio=("review_scores_rating", "mean"),
        precio_medio=("precio_eur", "mean"),
    )
    .round(2)
)
print(r10j)
print(
    "🎯 Objetivo: Medir el volumen de interacción comercial e impacto de"
    " viajeros por región."
)
print(
    "💡 Conclusión: Madrid acumula "
    + f"{r10j.loc['Mad', 'total_resenas']:,.0f}"
    + " reseñas totales con alta tracción."
)

print("\n🏷️ --------------------------------------------------------")
print("📌 11J. SEGMENTACIÓN ESTRATÉGICA POR RANGOS DE PRECIO:")
print("----------------------------------------------------------")
df["categoria_precio"] = pd.qcut(
    df["precio_eur"], q=4, labels=["Económico", "Medio", "Premium", "Lujo"]
)
r11j = (
    df.groupby(["region_origen", "categoria_precio"], observed=True)
    .agg(
        total_alojamientos=("id", "count"),
        precio_medio=("precio_eur", "mean"),
        puntuacion_media=("review_scores_rating", "mean"),
        capacidad_media=("accommodates", "mean"),
    )
    .round(2)
)
print(r11j)
print(
    "🎯 Objetivo: Dividir el mercado en cuatro estratos socioeconómicos por"
    " cuantiles."
)
print(
    "💡 Conclusión: El segmento de Lujo dispara las tarifas superando"
    " ampliamente la media general del mercado."
)

print("\n🔄 --------------------------------------------------------")
print("📌 12J. ÍNDICE DE ROTACIÓN Y ÉXITO COMERCIAL:")
print("----------------------------------------------------------")
r12j = (
    df.groupby(["region_origen", "room_type"])
    .agg(
        propiedades_totales=("id", "count"),
        suma_resenas=("number_of_reviews", "sum"),
        media_resenas_por_anuncio=("number_of_reviews", "mean"),
        porcentaje_superhosts=("es_superhost", lambda x: round(x.mean() * 100, 2)),
    )
    .round(2)
    .sort_values(by="media_resenas_por_anuncio", ascending=False)
)
print(r12j.head(10))
print(
    "🎯 Objetivo: Evaluar la frecuencia de ocupación y rotación estimada de"
    " huéspedes."
)
print(
    "💡 Conclusión: La categoría líder registra una media de "
    + str(r12j["media_resenas_por_anuncio"].iloc[0])
    + " reseñas por anuncio."
)

print("\n📉 --------------------------------------------------------")
print("📌 13J. ANÁLISIS DE DISPERSIÓN Y VOLATILIDAD DE PRECIOS:")
print("----------------------------------------------------------")
r13j = (
    df.groupby(["region_origen", "neighbourhood_cleansed"])
    .agg(
        oferta_total=("id", "count"),
        precio_medio=("precio_eur", "mean"),
        precio_mediano=("precio_eur", "median"),
        desviacion_estandar_precio=("precio_eur", "std"),
    )
    .round(2)
    .sort_values(by="desviacion_estandar_precio", ascending=False)
)
print(r13j.head(10))
print(
    "🎯 Objetivo: Medir la variabilidad de precios intrabarrio para"
    " cuantificar la heterogeneidad."
)
print(
    "💡 Conclusión: El barrio más volátil registra una desviación de "
    + str(r13j["desviacion_estandar_precio"].iloc[0])
    + "€, justificando el uso analítico de la mediana."
)

print("\n🛋️ --------------------------------------------------------")
print("📌 14J. RATIOS DE CONFORT ESPACIAL (Camas y Baños por Huésped):")
print("----------------------------------------------------------")
df["ratio_camas_pax"] = df["beds"] / df["accommodates"].replace(0, 1)
df["ratio_banos_pax"] = df["bathrooms_num"] / df["accommodates"].replace(0, 1)
df["precio_por_plaza"] = df["precio_eur"] / df["accommodates"].replace(0, 1)
r14j = (
    df.groupby("room_type")
    .agg(
        capacidad_media=("accommodates", "mean"),
        ratio_medio_camas_pax=("ratio_camas_pax", "mean"),
        ratio_medio_banos_pax=("ratio_banos_pax", "mean"),
        precio_por_plaza=("precio_por_plaza", "mean"),
    )
    .round(2)
)
print(r14j)
print(
    "🎯 Objetivo: Calcular los índices de comodidad física e higiene por"
    " plaza comercializada."
)
print(
    "💡 Conclusión: El ratio de camas por huésped en viviendas enteras se"
    " sitúa en "
    + str(r14j.loc["Entire home/apt", "ratio_medio_camas_pax"])
    + "."
)

print("\n🏆 --------------------------------------------------------")
print("📌 15J. PERFIL DE RENDIMIENTO: SUPERHOST VS ESTÁNDAR:")
print("----------------------------------------------------------")
r15j = (
    df.groupby("host_is_superhost")
    .agg(
        total_anuncios=("id", "count"),
        precio_promedio=("precio_eur", "mean"),
        precio_mediano=("precio_eur", "median"),
        puntuacion_calidad=("review_scores_rating", "mean"),
        volumen_medio_resenas=("number_of_reviews", "mean"),
        capacidad_alojamiento_media=("accommodates", "mean"),
    )
    .round(2)
)
print(r15j)
print(
    "🎯 Objetivo: Contrastar métricas globales entre anfitriones consolidados"
    " y estándar."
)
print(
    "💡 Conclusión: Los Superhosts acumulan una media de "
    + str(r15j.loc["t", "volumen_medio_resenas"])
    + " reseñas por anuncio frente a "
    + str(r15j.loc["f", "volumen_medio_resenas"])
    + " de los estándar."
)


# ============================================================
# 🥇 RANKINGS ESPECIALES (1J al 5J)
# ============================================================

print("\n🥇 ========================================================")
print("🏆 RANKING 1J: TOP 5 CHOLLOS MEJOR VALORADOS (Calidad/Precio):")
print("============================================================")
df["precio_por_persona"] = df["precio_eur"] / df["accommodates"].fillna(1)
chollos_1j = df.loc[
    df["review_scores_rating"].ge(4.8) & df["number_of_reviews"].ge(20)
].sort_values(by="precio_por_persona", ascending=True)[
    [
        "name",
        "region_origen",
        "neighbourhood_cleansed",
        "precio_por_persona",
        "precio_eur",
        "review_scores_rating",
    ]
].head(5)
print(chollos_1j.to_string(index=False))
print(
    "🎯 Objetivo: Filtrar las mejores opciones atendiendo al coste ponderado"
    " por plaza."
)
print(
    "💡 Conclusión: El número 1 ofrece un coste por persona de solo "
    + str(round(chollos_1j["precio_por_persona"].iloc[0], 2))
    + "€ por noche con valoración de "
    + str(chollos_1j["review_scores_rating"].iloc[0])
    + "."
)

print("\n💎 --------------------------------------------------------")
print("🏆 RANKING 2J: TOP 5 ALOJAMIENTOS MÁS EXCLUSIVOS / LUJO:")
print("----------------------------------------------------------")
lujo_2j = df.sort_values(by="precio_eur", ascending=False)[
    [
        "name",
        "region_origen",
        "neighbourhood_cleansed",
        "precio_eur",
        "room_type",
        "accommodates",
    ]
].head(5)
print(lujo_2j.to_string(index=False))
print(
    "🎯 Objetivo: Aislar las propiedades de más alta gama del ecosistema"
    " español."
)
print(
    "💡 Conclusión: El alojamiento más costoso alcanza "
    + str(round(lujo_2j["precio_eur"].iloc[0], 2))
    + "€ por noche en "
    + str(lujo_2j["region_origen"].iloc[0])
    + "."
)

print("\n🔥 --------------------------------------------------------")
print("🏆 RANKING 3J: TOP 5 ALOJAMIENTOS MÁS POPULARES / DEMANDADOS:")
print("----------------------------------------------------------")
populares_3j = df.sort_values(by="number_of_reviews", ascending=False)[
    [
        "name",
        "region_origen",
        "neighbourhood_cleansed",
        "number_of_reviews",
        "review_scores_rating",
        "precio_eur",
    ]
].head(5)
print(populares_3j.to_string(index=False))
print(
    "🎯 Objetivo: Destacar las propiedades con mayor tracción histórica de"
    " huéspedes."
)
print(
    "💡 Conclusión: El anuncio líder acumula "
    + str(populares_3j["number_of_reviews"].iloc[0])
    + " reseñas con nota de "
    + str(populares_3j["review_scores_rating"].iloc[0])
    + "."
)

print("\n🏰 --------------------------------------------------------")
print("🏆 RANKING 4J: TOP 5 ANFITRIONES CON MAYOR IMPERIO INMOBILIARIO:")
print("----------------------------------------------------------")
imperio_4j = (
    df.groupby(["host_id", "host_name", "host_is_superhost"])
    .agg(
        total_propiedades=("id", "count"),
        precio_medio_portafolio=("precio_eur", "mean"),
        nota_media_portafolio=("review_scores_rating", "mean"),
    )
    .round(2)
    .sort_values(by="total_propiedades", ascending=False)
    .head(5)
    .reset_index()
)
print(imperio_4j.to_string(index=False))
print(
    "🎯 Objetivo: Visibilizar a los mayores gestores de carteras de"
    " alojamientos."
)
print(
    "💡 Conclusión: El mayor anfitrión gestiona un total de "
    + str(imperio_4j["total_propiedades"].iloc[0])
    + " propiedades simultáneamente."
)

print("\n🏙️ --------------------------------------------------------")
print("🏆 RANKING 5J: TOP 5 BARRIOS MÁS EXCLUSIVOS (Por Precio Mediano):")
print("----------------------------------------------------------")
barrios_5j = (
    df.groupby(["region_origen", "neighbourhood_cleansed"])
    .agg(
        precio_mediano=("precio_eur", "median"),
        total_oferta=("id", "count"),
        puntuacion_promedio=("review_scores_rating", "mean"),
    )
    .round(2)
    .sort_values(by="precio_mediano", ascending=False)
    .head(5)
)
print(barrios_5j)
print(
    "🎯 Objetivo: Clasificar los distritos de mayor coste de entrada para el"
    " viajero."
)
print(
    "💡 Conclusión: El barrio más exclusivo registra un precio mediano de "
    + str(barrios_5j["precio_mediano"].iloc[0])
    + "€ por noche."
)


# ============================================================
# ⚖️ TABLAS AVANZADAS DE ESTRUCTURA Y LEY DE VIVIENDA
# ============================================================

print("\n⚖️ ========================================================")
print("📊 TABLAS AVANZADAS DE ESTRUCTURA Y LEY DE VIVIENDA:")
print("============================================================")

df["inmuebles_total_host"] = df.groupby("host_id")["id"].transform("count")


def clasificar_tramo(num):
  if num == 1:
    return "1) 1 vivienda (Particular)"
  elif 2 <= num <= 4:
    return "2) 2-4 viviendas (Pequeño bajo)"
  elif 5 <= num <= 10:
    return "3) 5-10 viviendas (Pequeño alto)"
  else:
    return "4) Más de 10 viviendas (Gran Tenedor)"


df["tramo_propietario"] = df["inmuebles_total_host"].apply(clasificar_tramo)

print("\n📌 DISTRIBUCIÓN DE LA OFERTA RESIDENCIAL - TOTAL ESPAÑA:")
conteo_tramos = df["tramo_propietario"].value_counts().sort_index()
porcentaje_tramos = (
    df["tramo_propietario"].value_counts(normalize=True) * 100
).sort_index().round(2)
tabla_dist_espana = pd.DataFrame({
    "Nº de Inmuebles": conteo_tramos,
    "% sobre el Total de la Oferta": porcentaje_tramos,
}).T
print(tabla_dist_espana)

pct_gran_tenedor = round((df["inmuebles_total_host"] >= 5).mean() * 100, 2)
print(
    f"\n📌 [Criterio Ley de Vivienda] % de la oferta en manos de propietarios"
    f" con 5+ viviendas (Gran Tenedor): {pct_gran_tenedor}%"
)

# Total España para las tablas comparativas
total_espana_s = (
    df["tramo_propietario"].value_counts(normalize=True) * 100
).round(2)
total_espana_s["5+ Inmuebles (% Ley Vivienda)"] = total_espana_s.get(
    "3) 5-10 viviendas (Pequeño alto)", 0
) + total_espana_s.get("4) Más de 10 viviendas (Gran Tenedor)", 0)
df_total_espana = pd.DataFrame(total_espana_s).T.rename(
    index={0: "✨ TOTAL ESPAÑA"}
)

print("\n📌 2. COMPARATIVA POR ZONA GEOGRÁFICA:")
tabla_geo_prop = (
    pd.crosstab(
        df["region_origen"], df["tramo_propietario"], normalize="index"
    )
    * 100
).round(2)
tabla_geo_prop["5+ Inmuebles (% Ley Vivienda)"] = tabla_geo_prop.get(
    "3) 5-10 viviendas (Pequeño alto)", 0
) + tabla_geo_prop.get("4) Más de 10 viviendas (Gran Tenedor)", 0)
tabla_geo_prop_con_total = pd.concat([df_total_espana, tabla_geo_prop])
print(tabla_geo_prop_con_total)


def agrupar_regiones(region):
  if region in ["Bcn", "Ger"]:
    return "CAT"
  elif region in ["Mal", "Sev"]:
    return "AND"
  elif region in ["Mallorca", "Menorca"]:
    return "BAL"
  else:
    return region


df["region_agrupada"] = df["region_origen"].apply(agrupar_regiones)

print("\n📌 TABLA COMPARATIVA POR ZONAS AGRUPADAS:")
tabla_agrupada = (
    pd.crosstab(
        df["region_agrupada"], df["tramo_propietario"], normalize="index"
    )
    * 100
).round(2)
tabla_agrupada["5+ Inmuebles (% Ley Vivienda)"] = tabla_agrupada.get(
    "3) 5-10 viviendas (Pequeño alto)", 0
) + tabla_agrupada.get("4) Más de 10 viviendas (Gran Tenedor)", 0)
tabla_agrupada_con_total = pd.concat([df_total_espana, tabla_agrupada])
print(tabla_agrupada_con_total)

print("\n📌 TABLA DE PRECIOS MEDIOS (€) POR TRAMO Y ZONA AGRUPADA:")
tabla_precios_tramo = (
    df.pivot_table(
        index="region_agrupada",
        columns="tramo_propietario",
        values="precio_eur",
        aggfunc="mean",
    )
    .round(2)
)
precio_total_espana = (
    df.pivot_table(
        columns="tramo_propietario", values="precio_eur", aggfunc="mean"
    )
    .round(2)
)
precio_total_espana.index = ["✨ TOTAL ESPAÑA"]
tabla_precios_tramo_con_total = pd.concat(
    [precio_total_espana, tabla_precios_tramo]
)
print(tabla_precios_tramo_con_total)

# ---------------------------------------------------------------------
# TABLA 2: TOP 3 / BOTTOM 3 DE BARRIOS
# ---------------------------------------------------------------------
df["es_gran_tenedor_agrupado"] = df["inmuebles_total_host"] >= 5
tabla_barrios_full = df.pivot_table(
    index=["region_agrupada", "neighbourhood_cleansed"],
    columns="tramo_propietario",
    values="precio_eur",
    aggfunc="mean",
)
gt_barrios = (
    df[df["es_gran_tenedor_agrupado"]]
    .groupby(["region_agrupada", "neighbourhood_cleansed"])["precio_eur"]
    .mean()
)
tabla_barrios_full["Precio Medio (5+ Inmuebles)"] = gt_barrios
tabla_barrios_full["precio_global_barrio"] = tabla_barrios_full.mean(axis=1)

lista_segmentos = []
for zona, grupo in tabla_barrios_full.groupby(level=0):
  grupo_z = grupo.droplevel(0)
  if len(grupo_z) <= 6:
    top_3 = grupo_z.sort_values(by="precio_global_barrio", ascending=False)
    bottom_3 = pd.DataFrame(columns=grupo_z.columns)
  else:
    top_3 = grupo_z.sort_values(
        by="precio_global_barrio", ascending=False
    ).head(3)
    bottom_3 = grupo_z.sort_values(
        by="precio_global_barrio", ascending=True
    ).head(3)

  top_3.index = pd.MultiIndex.from_tuples(
      [(zona, f"🔥 Top 3 Caro: {b}") for b in top_3.index]
  )
  lista_segmentos.append(top_3)

  if not bottom_3.empty:
    fila_sep_interna = pd.DataFrame(
        index=pd.MultiIndex.from_tuples(
            [(zona, "    . . . . . . . . . . . . . . . . . . . . . . . . .")]
        )
    )
    for col in bottom_3.columns:
      fila_sep_interna[col] = "..."
    lista_segmentos.append(fila_sep_interna)

    bottom_3.index = pd.MultiIndex.from_tuples(
        [(zona, f"❄️ Bottom 3 Barato: {b}") for b in bottom_3.index]
    )
    lista_segmentos.append(bottom_3)

  fila_fin_zona = pd.DataFrame(
      index=pd.MultiIndex.from_tuples(
          [(zona, "==================== FIN ZONA ====================")]
      )
  )
  for col in tabla_barrios_full.columns:
    fila_fin_zona[col] = "==="
  lista_segmentos.append(fila_fin_zona)

tabla_barrios_resumida = pd.concat(lista_segmentos)
if "precio_global_barrio" in tabla_barrios_resumida.columns:
  tabla_barrios_resumida = tabla_barrios_resumida.drop(
      columns=["precio_global_barrio"]
  )

print("\n📊 TABLA 2: TOP 3 Y BOTTOM 3 DE BARRIOS POR ZONA:")
print(tabla_barrios_resumida.to_string())


# ============================================================
# 🔥 NUEVO CRUCES DE ACTUALIDAD: PROFESIONALIZACIÓN VS TAMAÑO DE ANUNCIO
# ============================================================
print("\n🔥 ========================================================")
print("💡 NUEVO CRUCE EXTRA (Actualidad - Profesionalización vs Oferta):")
print("============================================================")
print(
    "Analizamos cómo la 'profesionalización' (anfitriones con múltiples"
    " inmuebles)\nse concentra según el tipo de alojamiento (Habitación privada"
    " vs Alojamiento entero):\n"
)

# Creamos una columna binaria de profesionalización (Gran Tenedor vs Particular)
df["es_profesional"] = df["inmuebles_total_host"].ge(5)

cruge_actualidad = (
    df.groupby(["room_type", "es_profesional"])
    .agg(
        total_anuncios=("id", "count"),
        precio_medio=("precio_eur", "mean"),
        puntuacion_media=("review_scores_rating", "mean"),
    )
    .round(2)
)
print(cruge_actualidad)

# Renombramos el índice booleano para mayor claridad visual
cruge_actualidad_vista = cruge_actualidad.reset_index()
cruge_actualidad_vista["Perfil Anfitrión"] = cruge_actualidad_vista[
    "es_profesional"
].map({True: "Profesional (5+ inmuebles)", False: "Particular (1-4 inmuebles)"})

print(
    "\n💡 Conclusión analítica: Permite demostrar si el"
    " fenómeno del 'gran tenedor'\n"
    "en Airbnb domina más en viviendas completas (apartamentos turísticos"
    " puros)\n"
    "o si también invade el mercado de habitaciones compartidas.\n"
)


# ============================================================
# 🏅 TOP 10 ALOJAMIENTOS MÁS ECONÓMICOS Y BIEN VALORADOS
# ============================================================
print("\n🏅 ========================================================")
print("🏅 TOP 10 ALOJAMIENTOS MÁS ECONÓMICOS Y BIEN VALORADOS:")
print("============================================================")

candidatos_top = df.loc[
    df["precio_eur"].notna()
    & df["precio_eur"].gt(0)
    & df["review_scores_rating"].ge(4.5)
    & df["number_of_reviews"].ge(5)
].copy()

top_10 = candidatos_top.sort_values(
    by=["precio_eur", "review_scores_rating", "number_of_reviews"],
    ascending=[True, False, False],
).head(10)

top_10_vista = top_10.copy()


def nombre_corto(nombre: object) -> str:
  texto = str(nombre).strip() if pd.notna(nombre) else "Sin nombre"
  normalizado = texto.lower()
  if "habitación" in normalizado or "room" in normalizado:
    return "Habitación Privada"
  if "estudio" in normalizado or "studio" in normalizado:
    return "Estudio Económico"
  return texto[:22].rstrip(" -,.!")


top_10_vista["Alojamiento"] = top_10_vista["name"].map(nombre_corto)
top_10_vista["Zona"] = top_10_vista["region_origen"]
top_10_vista["Barrio"] = (
    top_10_vista["neighbourhood_cleansed"].fillna("-").str.slice(0, 18)
)
top_10_vista["Habitaciones"] = top_10_vista["bedrooms"].fillna(1).astype(int)

print(
    f"{'Alojamiento':22} {'Zona':12} {'Barrio':18} {'Hab.':>5}"
    f" {'Precio €':>9} {'Nota':>5}   ID Referencia"
)
print("-" * 95)

for _, row in top_10_vista.iterrows():
  id_ref = str(row.get("id", ""))
  print(
      f"{str(row['Alojamiento'])[:22]:22} "
      f"{str(row['Zona'])[:12]:12} "
      f"{str(row['Barrio'])[:18]:18} "
      f"{int(row['Habitaciones']):>5} "
      f"{row['precio_eur']:>9.2f} € "
      f"{row['review_scores_rating']:>5.2f}   {id_ref}"
  )

# ============================================================
# 📊 ANÁLISIS ESTADÍSTICO AVANZADO DE PRECIOS Y GRÁFICO CONDICIONAL
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración del entorno visual
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (17, 7)

# Función auxiliar para calcular el Rango Intercuartílico (IQR)
def iqr(x):
    return x.quantile(0.75) - x.quantile(0.25)

# 1. Resumen estadístico avanzado por región
resumen_regiones = df.groupby('region_origen')['precio_eur'].agg(
    Oferta_Total='count',
    Mediana='median',
    Media='mean',
    Desv_Estandar='std',
    Q1=lambda x: x.quantile(0.25),
    Q3=lambda x: x.quantile(0.75),
    IQR=iqr,
    P90=lambda x: x.quantile(0.90)
).reset_index().sort_values(by='Mediana', ascending=False)

# 2. Cálculo global de España para la tabla y la referencia visual
mediana_nacional = df['precio_eur'].median()
resumen_total_espana = pd.DataFrame({
    'region_origen': ['✨ TOTAL ESPAÑA'],
    'Oferta_Total': [len(df)],
    'Mediana': [mediana_nacional],
    'Media': [df['precio_eur'].mean()],
    'Desv_Estandar': [df['precio_eur'].std()],
    'Q1': [df['precio_eur'].quantile(0.25)],
    'Q3': [df['precio_eur'].quantile(0.75)],
    'IQR': [iqr(df['precio_eur'])],
    'P90': [df['precio_eur'].quantile(0.90)]
})

# Unimos el total nacional a la tabla estadística
resumen_avanzado = pd.concat([resumen_regiones, resumen_total_espana], ignore_index=True)
resumen_avanzado = resumen_avanzado.sort_values(by='Mediana', ascending=False)

# IMPRESIÓN DE LA TABLA EN CONSOLA
print("\n=== 📊 RESUMEN ESTADÍSTICO AVANZADO DE PRECIOS POR REGIÓN Y TOTAL ESPAÑA (€) ===")
print(resumen_avanzado.round(2).to_string(index=False))

# 3. Preparación de datos para el gráfico de caja (Boxplot)
df_grafico = df[df['precio_eur'] <= 600].copy()
df_grafico['region_origen_con_total'] = df_grafico['region_origen']

# Copia para asignar la etiqueta de Total España
df_total_copia = df_grafico.copy()
df_total_copia['region_origen_con_total'] = '✨ TOTAL ESPAÑA'

# Unimos los datos (la categoría de separación '   ' dejará el espacio en blanco)
df_boxplot_final = pd.concat([df_grafico, df_total_copia], ignore_index=True)

orden_regiones_originales = resumen_regiones['region_origen'].tolist()
orden_eje_x = ['✨ TOTAL ESPAÑA', '   '] + orden_regiones_originales

# 4. Creación dinámica de la paleta de colores condicional
colores_mapa = {
    '✨ TOTAL ESPAÑA': '#f39c12', # Naranja/Ámbar institucional de referencia
    '   ': 'white'                   # Espacio en blanco transparente
}

# Asignación automática: Verde si supera la mediana nacional, Rojo si está por debajo
for _, row in resumen_regiones.iterrows():
    zona = row['region_origen']
    mediana_zona = row['Mediana']
    
    if mediana_zona > mediana_nacional:
        colores_mapa[zona] = '#2ecc71'  # Verde (Por encima del Total España)
    elif mediana_zona < mediana_nacional:
        colores_mapa[zona] = '#e74c3c'  # Rojo (Por debajo del Total España)
    else:
        colores_mapa[zona] = '#f1c40f'  # Amarillo pálido (Exactamente igual)

lista_colores = [colores_mapa[cat] for cat in orden_eje_x]

# 5. Generación del Gráfico de Cajas Final
plt.figure(figsize=(17, 7))
sns.boxplot(
    data=df_boxplot_final,
    x='region_origen_con_total',
    y='precio_eur',
    order=orden_eje_x,
    palette=lista_colores
)

plt.title("Distribución de Precios por Noche: Comparativa Condicional vs. Total España (Hasta 600€)", fontsize=14, fontweight='bold')
plt.xlabel("Región / Destino", fontsize=12)
plt.ylabel("Precio por Noche (€)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()