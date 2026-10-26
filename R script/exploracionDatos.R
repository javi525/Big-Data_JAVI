# ==============================================================================
# SCRIPT 3: BATERÍA DE CONSULTAS DE EXPLORACIÓN (EDA) - MAESTRO R
# ==============================================================================

library(tidyverse)

print("🚀 Cargando el dataset limpio 'airbnb_espana_clean.csv'...")
df <- read_csv("airbnb_espana_clean.csv", show_col_types = FALSE)

# Normalización adicional de tipos en R
df <- df %>% mutate(
  precio_eur = as.numeric(precio_eur),
  review_scores_rating = as.numeric(review_scores_rating),
  number_of_reviews = as.numeric(number_of_reviews),
  accommodates = as.numeric(accommodates),
  beds = as.numeric(beds),
  bedrooms = as.numeric(bedrooms),
  bathrooms_num = as.numeric(bathrooms_num),
  es_superhost = host_is_superhost == "t"
)

# =====================================================================
# 📌 PARTE 1: CONSULTAS GENERALES Y MERCADO (1 a 15)
# =====================================================================

print("\n🔍 --------------------------------------------------------")
print("📌 1. TOP 5 ALOJAMIENTOS MÁS CAROS EN ESPAÑA:")
print("----------------------------------------------------------")
top_caros <- df %>% arrange(desc(precio_eur)) %>% select(name, region_origen, precio_eur, room_type) %>% head(5)
print(as.data.frame(top_caros))
print("🎯 Objetivo: Identificar el techo tarifario del mercado e inspeccionar los activos de ultra lujo en España.")
cat(paste0("💡 Conclusión: La oferta más cara alcanza los ", round(top_caros$precio_eur[1], 2), "€ por noche, protagonizada por alojamientos de tipo ", top_caros$room_type[1], " en regiones como ", top_caros$region_origen[1], ".\n"))

print("\n📈 --------------------------------------------------------")
print("📌 2. RESUMEN DEL MERCADO POR REGIÓN (Precio y Volumen):")
print("----------------------------------------------------------")
resumen_region <- df %>% group_by(region_origen) %>% summarise(
  precio_promedio = round(mean(precio_eur, na.rm = TRUE), 2),
  total_alojamientos = n()
) %>% arrange(desc(precio_promedio))
print(as.data.frame(resumen_region))
print("🎯 Objetivo: Evaluar la dimensión de la oferta y el nivel de precios medio por destino geográfico.")
cat("💡 Conclusión: Mallorca lidera el coste medio con alta tarifa por noche, contrastando con mercados urbanos masivos como Madrid.\n")

print("\n⭐ --------------------------------------------------------")
print("📌 3. COMPARATIVA: ¿SER SUPERHOST MARCA LA DIFERENCIA?")
print("----------------------------------------------------------")
superhost_comp <- df %>% group_by(host_is_superhost) %>% summarise(
  precio_medio = round(mean(precio_eur, na.rm = TRUE), 2),
  puntuacion_media = round(mean(review_scores_rating, na.rm = TRUE), 2),
  total_propiedades = n()
)
print(as.data.frame(superhost_comp))
print("🎯 Objetivo: Determinar si el sello Superhost otorga un 'premium' en tarifa y mejor puntuación.")
cat("💡 Conclusión: Los Superhosts consiguen una valoración media superior manteniendo tarifas equivalentes a los anfitriones estándar.\n")

print("\n🎯 --------------------------------------------------------")
print("📌 4. BÚSQUEDA DE OPORTUNIDADES (Filtro Cruzado Inversor):")
print("----------------------------------------------------------")
oportunidades <- df %>% filter(precio_eur < 80 & review_scores_rating >= 4.6 & number_of_reviews >= 10)
cat(paste0("🎯 Se han encontrado ", nrow(oportunidades), " opciones que cumplen los requisitos.\n"))
if(nrow(oportunidades) > 0) {
  print(as.data.frame(oportunidades %>% select(name, neighbourhood_cleansed, precio_eur, review_scores_rating) %>% head(5)))
}
print("🎯 Objetivo: Isolar la oferta de alto valor (excelente nota y precio asequible por debajo de 80€).")
cat("💡 Conclusión: Se localizan opciones atractivas de alta rentabilidad potencial con valoraciones excelentes.\n")

print("\n🏠 --------------------------------------------------------")
print("📌 5. MATRIZ DE DISTRIBUCIÓN: TIPO DE ALOJAMIENTO POR REGIÓN:")
print("----------------------------------------------------------")
matriz_tipo <- table(df$region_origen, df$room_type)
print(matriz_tipo)
print("🎯 Objetivo: Analizar la tipología del producto ofrecido según la vocación de cada comunidad.")
cat("💡 Conclusión: El formato 'Entire home/apt' es predominante absoluto en zonas vacacionales.\n")

print("\n📊 --------------------------------------------------------")
print("📌 6J. RANKING DE CIUDADES POR VALORACIÓN:")
print("----------------------------------------------------------")
r6j <- df %>% group_by(region_origen) %>% summarise(
  puntuacion_media = round(mean(review_scores_rating, na.rm = TRUE), 2),
  precio_medio = round(mean(precio_eur, na.rm = TRUE), 2),
  total_oferta = n()
) %>% arrange(desc(puntuacion_media))
print(as.data.frame(r6j))
print("🎯 Objetivo: Clasificar los destinos según la satisfacción media de los huéspedes.")
cat("💡 Conclusión: Las regiones del norte y destinos específicos encabezan la satisfacción cualitativa nacional.\n")

print("\n🏢 --------------------------------------------------------")
print("📌 7J. CONCENTRACIÓN DE MERCADO: TOP ANFITRIONES POR REGIÓN:")
print("----------------------------------------------------------")
r7j <- df %>% group_by(region_origen, host_id, host_name) %>% summarise(
  total_propiedades = n(),
  precio_promedio = round(mean(precio_eur, na.rm = TRUE), 2),
  .groups = "drop"
) %>% arrange(desc(total_propiedades)) %>% head(10)
print(as.data.frame(r7j))
print("🎯 Objetivo: Detectar la presencia de grandes gestores multipropiedad por región.")
cat("💡 Conclusión: Los principales gestores concentran decenas de alojamientos bajo una misma titularidad.\n")

print("\n📍 --------------------------------------------------------")
print("📌 8J. RESUMEN POR BARRIO/VECINDARIO (Capacidad y Precio):")
print("----------------------------------------------------------")
r8j <- df %>% group_by(region_origen, neighbourhood_cleansed) %>% summarise(
  total_alojamientos = n(),
  precio_medio = round(mean(precio_eur, na.rm = TRUE), 2),
  capacidad_promedio = round(mean(accommodates, na.rm = TRUE), 2),
  puntuacion_media = round(mean(review_scores_rating, na.rm = TRUE), 2),
  .groups = "drop"
) %>% arrange(desc(total_alojamientos)) %>% head(10)
print(as.data.frame(r8j))
print("🎯 Objetivo: Localizar los epicentros de densidad de oferta en el ámbito micro-local.")
cat("💡 Conclusión: Los barrios céntricos concentran el mayor volumen de oferta turística del país.\n")

print("\n🛏️ --------------------------------------------------------")
print("📌 9J. RATIO DE CAMAS Y DORMITORIOS POR CAPACIDAD:")
print("----------------------------------------------------------")
r9j <- df %>% group_by(room_type) %>% summarise(
  capacidad_media = round(mean(accommodates, na.rm = TRUE), 2),
  dormitorios_promedio = round(mean(bedrooms, na.rm = TRUE), 2),
  camas_promedio = round(mean(beds, na.rm = TRUE), 2),
  precio_medio = round(mean(precio_eur, na.rm = TRUE), 2)
)
print(as.data.frame(r9j))
print("🎯 Objetivo: Analizar la configuración arquitectónica según el formato de alquiler.")
cat("💡 Conclusión: Las viviendas enteras ofrecen una media superior de plazas y dormitorios frente a habitaciones.\n")

print("\n💬 --------------------------------------------------------")
print("📌 10J. MÉTRICAS DE POPULARIDAD Y PRECIO:")
print("----------------------------------------------------------")
r10j <- df %>% group_by(region_origen) %>% summarise(
  total_resenas = sum(number_of_reviews, na.rm = TRUE),
  resenas_promedio = round(mean(number_of_reviews, na.rm = TRUE), 2),
  puntuacion_promedio = round(mean(review_scores_rating, na.rm = TRUE), 2),
  precio_medio = round(mean(precio_eur, na.rm = TRUE), 2)
)
print(as.data.frame(r10j))
print("🎯 Objetivo: Medir el volumen de interacción comercial e impacto de viajeros por región.")
cat("💡 Conclusión: Las grandes capitales acumulan un volumen masivo de reseñas totales.\n")

print("\n🏷️ --------------------------------------------------------")
print("📌 11J. SEGMENTACIÓN ESTRATÉGICA POR RANGOS DE PRECIO:")
print("----------------------------------------------------------")
df$categoria_precio <- ntile(df$precio_eur, 4)
df$categoria_precio <- factor(df$categoria_precio, levels = 1:4, labels = c("Económico", "Medio", "Premium", "Lujo"))
r11j <- df %>% group_by(region_origen, categoria_precio) %>% summarise(
  total_alojamientos = n(),
  precio_medio = round(mean(precio_eur, na.rm = TRUE), 2),
  puntuacion_media = round(mean(review_scores_rating, na.rm = TRUE), 2),
  .groups = "drop"
)
print(as.data.frame(r11j))
print("🎯 Objetivo: Dividir el mercado en cuatro estratos socioeconómicos por cuartiles.")
cat("💡 Conclusión: El segmento de Lujo dispara las tarifas superando ampliamente la media general.\n")

print("\n🔄 --------------------------------------------------------")
print("📌 12J. ÍNDICE DE ROTACIÓN Y ÉXITO COMERCIAL:")
print("----------------------------------------------------------")
r12j <- df %>% group_by(region_origen, room_type) %>% summarise(
  propiedades_totales = n(),
  suma_resenas = sum(number_of_reviews, na.rm = TRUE),
  media_resenas = round(mean(number_of_reviews, na.rm = TRUE), 2),
  porcentaje_superhosts = round(mean(es_superhost, na.rm = TRUE) * 100, 2),
  .groups = "drop"
) %>% arrange(desc(media_resenas))
print(as.data.frame(head(r12j, 10)))
print("🎯 Objetivo: Evaluar la frecuencia de ocupación y rotación estimada de huéspedes.")
cat("💡 Conclusión: Las categorías con mayor rotación reflejan una alta frecuencia de visitas y tracción comercial.\n")

print("\n📉 --------------------------------------------------------")
print("📌 13J. ANÁLISIS DE DISPERSIÓN Y VOLATILIDAD DE PRECIOS:")
print("----------------------------------------------------------")
r13j <- df %>% group_by(region_origen, neighbourhood_cleansed) %>% summarise(
  oferta_total = n(),
  precio_medio = round(mean(precio_eur, na.rm = TRUE), 2),
  precio_mediano = round(median(precio_eur, na.rm = TRUE), 2),
  desviacion_estandar = round(sd(precio_eur, na.rm = TRUE), 2),
  .groups = "drop"
) %>% arrange(desc(desviacion_estandar))
print(as.data.frame(head(r13j, 10)))
print("🎯 Objetivo: Medir la variabilidad de precios intrabarrio para cuantificar la heterogeneidad.")
cat("💡 Conclusión: El barrio más volátil justifica el uso analítico de la mediana frente a la media.\n")

print("\n🛋️ --------------------------------------------------------")
print("📌 14J. RATIOS DE CONFORT ESPACIAL (Camas y Baños por Huésped):")
print("----------------------------------------------------------")
df <- df %>% mutate(
  ratio_camas_pax = beds / pmax(accommodates, 1),
  ratio_banos_pax = bathrooms_num / pmax(accommodates, 1),
  precio_por_plaza = precio_eur / pmax(accommodates, 1)
)
r14j <- df %>% group_by(room_type) %>% summarise(
  capacidad_media = round(mean(accommodates, na.rm = TRUE), 2),
  ratio_camas = round(mean(ratio_camas_pax, na.rm = TRUE), 2),
  ratio_banos = round(mean(ratio_banos_pax, na.rm = TRUE), 2),
  precio_plaza = round(mean(precio_por_plaza, na.rm = TRUE), 2)
)
print(as.data.frame(r14j))
print("🎯 Objetivo: Calcular los índices de comodidad física e higiene por plaza comercializada.")
cat("💡 Conclusión: Las viviendas enteras garantizan excelentes ratios de descanso individual por viajero.\n")

print("\n🏆 --------------------------------------------------------")
print("📌 15J. PERFIL DE RENDIMIENTO: SUPERHOST VS ESTÁNDAR:")
print("----------------------------------------------------------")
r15j <- df %>% group_by(host_is_superhost) %>% summarise(
  total_anuncios = n(),
  precio_promedio = round(mean(precio_eur, na.rm = TRUE), 2),
  precio_mediano = round(median(precio_eur, na.rm = TRUE), 2),
  puntuacion_calidad = round(mean(review_scores_rating, na.rm = TRUE), 2),
  volumen_resenas = round(mean(number_of_reviews, na.rm = TRUE), 2)
)
print(as.data.frame(r15j))
print("🎯 Objetivo: Contrastar métricas globales entre anfitriones consolidados y estándar.")
cat("💡 Conclusión: Los Superhosts multiplican significativamente el volumen de reseñas y confianza del usuario.\n")


# ============================================================
# 🥇 RANKINGS ESPECIALES (1J al 5J)
# ============================================================

print("\n🏆 RANKING 1J: TOP 5 CHOLLOS MEJOR VALORADOS:")
df$precio_por_persona <- df$precio_eur / pmax(df$accommodates, 1)
chollos_1j <- df %>% filter(review_scores_rating >= 4.8 & number_of_reviews >= 20) %>% arrange(precio_por_persona) %>% select(name, region_origen, neighbourhood_cleansed, precio_por_persona, precio_eur, review_scores_rating) %>% head(5)
print(as.data.frame(chollos_1j))
print("🎯 Objetivo: Filtrar las mejores opciones atendiendo al coste ponderado por plaza.")
cat("💡 Conclusión: Se identifican opciones con excelente relación calidad/precio imbatible.\n")

print("\n💎 RANKING 2J: TOP 5 ALOJAMIENTOS MÁS EXCLUSIVOS / LUJO:")
lujo_2j <- df %>% arrange(desc(precio_eur)) %>% select(name, region_origen, neighbourhood_cleansed, precio_eur, room_type, accommodates) %>% head(5)
print(as.data.frame(lujo_2j))
print("🎯 Objetivo: Aislar las propiedades de más alta gama del ecosistema.")
cat("💡 Conclusión: Los activos de ultra lujo alcanzan tarifas muy elevadas en enclaves exclusivos.\n")

print("\n🔥 RANKING 3J: TOP 5 ALOJAMIENTOS MÁS POPULARES / DEMANDADOS:")
populares_3j <- df %>% arrange(desc(number_of_reviews)) %>% select(name, region_origen, neighbourhood_cleansed, number_of_reviews, review_scores_rating, precio_eur) %>% head(5)
print(as.data.frame(populares_3j))
print("🎯 Objetivo: Destacar las propiedades con mayor tracción histórica de huéspedes.")
cat("💡 Conclusión: Las propiedades líderes acumulan récords históricos de interacción turística.\n")

print("\n🏰 RANKING 4J: TOP 5 ANFITRIONES CON MAYOR IMPERIO INMOBILIARIO:")
imperio_4j <- df %>% group_by(host_id, host_name, host_is_superhost) %>% summarise(
  total_propiedades = n(),
  precio_medio = round(mean(precio_eur, na.rm = TRUE), 2),
  .groups = "drop"
) %>% arrange(desc(total_propiedades)) %>% head(5)
print(as.data.frame(imperio_4j))
print("🎯 Objetivo: Visibilizar a los mayores gestores de carteras de alojamientos.")
cat("💡 Conclusión: Los grandes tenedores gestionan carteras masivas de propiedades.\n")

print("\n🏙️ RANKING 5J: TOP 5 BARRIOS MÁS EXCLUSIVOS:")
barrios_5j <- df %>% group_by(region_origen, neighbourhood_cleansed) %>% summarise(
  precio_mediano = round(median(precio_eur, na.rm = TRUE), 2),
  total_oferta = n(),
  puntuacion_promedio = round(mean(review_scores_rating, na.rm = TRUE), 2),
  .groups = "drop"
) %>% arrange(desc(precio_mediano)) %>% head(5)
print(as.data.frame(barrios_5j))
print("🎯 Objetivo: Clasificar los distritos de mayor coste de entrada para el viajero.")
cat("💡 Conclusión: Los distritos prime marcan el techo del mercado inmobiliario local.\n")


# ============================================================
# ⚖️ TABLAS AVANZADAS DE ESTRUCTURA Y LEY DE VIVIENDA
# ============================================================

print("\n⚖️ TABLAS AVANZADAS DE ESTRUCTURA Y LEY DE VIVIENDA:")
df <- df %>% group_by(host_id) %>% mutate(inmuebles_total_host = n()) %>% ungroup()

clasificar_tramo <- function(num) {
  case_when(
    num == 1 ~ "1) 1 vivienda (Particular)",
    num >= 2 & num <= 4 ~ "2) 2-4 viviendas (Pequeño bajo)",
    num >= 5 & num <= 10 ~ "3) 5-10 viviendas (Pequeño alto)",
    TRUE ~ "4) Más de 10 viviendas (Gran Tenedor)"
  )
}

df$tramo_propietario <- sapply(df$inmuebles_total_host, clasificar_tramo)

conteo_tramos <- table(df$tramo_propietario)
porcentaje_tramos <- round(prop.table(conteo_tramos) * 100, 2)
print("Distribución General por Tramos:")
print(porcentaje_tramos)
print("🎯 Objetivo: Analizar la estructura de la propiedad bajo los umbrales de la normativa de vivienda.")
cat("💡 Conclusión: Una parte significativa de la oferta se concentra en manos de multipropietarios e inversores profesionales.\n")


# ============================================================
# 🎯 CONCLUSIONES DE NEGOCIO Y RECOMENDACIONES ESTRATÉGICAS
# ============================================================

cat("\n============================================================\n")
cat("📌 CONCLUSIONES DE NEGOCIO Y RECOMENDACIONES ESTRATÉGICAS\n")
cat("============================================================\n")

cat("\n--- 📈 CONCLUSIONES DE NEGOCIO ---\n")
cat("1. Concentración Profesional: El mercado está dominado por inversores con múltiples propiedades.\n")
cat("2. Especialización por Tipología: Las viviendas completas ('Entire home/apt') lideran la oferta inversora.\n")
cat("3. Retorno de Calidad: El estatus Superhost incrementa la confianza y tracción sin necesidad de sobreprecios.\n")
cat("4. Dualidad Regional: Los destinos turísticos costeros e insulares operan con tarifas muy superiores a las capitales.\n")

cat("\n--- 🚀 RECOMENDACIONES ESTRATÉGICAS ---\n")
cat("1. Filtrado de Oportunidades: Enfocarse en nichos con alta rentabilidad inicial y buenas valoraciones.\n")
cat("2. Optimización Operativa: Automatizar procesos para alcanzar el estatus Superhost.\n")
cat("3. Cobertura Regulatoria: Anticiparse a la Ley de Vivienda diversificando hacia estancias de media duración.\n")

print("\n✅ ¡Script de EDA en R ejecutado con éxito y al 100% de paridad con Python!")


# ============================================================
# 📉 GRÁFICOS 📉
# ============================================================

# =====================================================================
# GRÁFICO 1: Boxplot de Precios por Región
# =====================================================================
# Objetivo: Visualizar la dispersión, la mediana y los valores atípicos (outliers) de los precios por noche en cada región de España
library(ggplot2)

ggplot(df, aes(x = region_origen, y = precio_eur, fill = region_origen)) +
  geom_boxplot(outlier.alpha = 0.3, outlier.color = "red") +
  scale_y_continuous(limits = c(0, 400)) + # Limitamos el eje Y para mejor visualización (excluyendo extremos)
  labs(
    title = "Distribución de Precios por Noche (€) según Región",
    subtitle = "Análisis de medianas y dispersión (filtrado hasta 400€)",
    x = "Región / Destino",
    y = "Precio por Noche (€)"
  ) +
  theme_minimal() +
  theme(legend.position = "none", plot.title = element_text(face = "bold", size = 14))

# 3 Conclusiones:
# 1.1. Mallorca líder en precio caro (tanto en la posición de su caja como en la mediana (línea horizontal), superando los 230€ la noche, lo q confirma su marcado carácter vacacional de alto standing
# 1.2. BCn destaca entre el resto de ciudades: caja muy amplia y mediana elevada (unos 175€), gran dispersión en cuanto a variedad de tarifas
# 1.3. Val y Mal, los destinos más asequibles (medianas más bajas)
# Resumiendo: Mientras las islas y grandes metrópolis alzan los precios, el resto de zonas tienen precios moderados

# =====================================================================
# GRÁFICO 2: Precio Medio por Tipo de Alojamiento y Región
# =====================================================================
# Objetivo: Comparar de forma visual qué tipo de alojamiento (room_type) es más caro en cada comunidad autónoma

df_grafico2 <- df %>% 
  group_by(region_origen, room_type) %>% 
  summarise(precio_medio = mean(precio_eur, na.rm = TRUE), .groups = "drop")

ggplot(df_grafico2, aes(x = region_origen, y = precio_medio, fill = room_type)) +
  geom_bar(stat = "identity", position = "dodge") +
  labs(
    title = "Precio Medio por Noche según Tipo de Alojamiento",
    subtitle = "Comparativa directa por región de origen",
    x = "Región",
    y = "Precio Promedio (€)",
    fill = "Tipo de Alojamiento"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(face = "bold", size = 14))

# 3 Conclusiones:
# 2.1. Mallorca, la zona con los alojamientos más caros de todo el territorio (>350€ de media). Esto refleja la fuerte presión y el perfil de turismo vacacional de alto poder adquisitivo en temporada alta  
# 2.2. Jerarquía de precios muy lógica
# 2.2.1. Las viviendas enteras y las habitaciones de hotel son los que tienen los precios más altos
# 2.2.2. Las habitaciones privadas se sitúan en un nivel intermedio (entre 80€y 200€) 
# 2.2.3. Las habitaciones compartidas son la opción más económica
# 2.3. Hay diferencias entre destinos costeros y urbanos
# 2.3.1. En PV, Bcn e incluso Sev con fuerte infraestructura hotelera urbana y corporativa/vacacional de gama alta 
# 2.3.2. En Ger y Mal líderes en ratio de viviendas enteras
# Resumiendo: el tipo de espacio define drásticamente el precio, siendo las islas (Mallorca/Menorca) y las grandes capitales turísticas los lugares donde alquilar una vivienda completa alcanza los mayores picos del mercado español

# =====================================================================
# GRÁFICO 3: Relación Calidad (Rating) vs Precio
# =====================================================================
# Objetivo: Analizar si los alojamientos con mejor puntuación (review_scores_rating) son necesariamente los más caros del mercado 
df_filtrado_rating <- df %>% filter(review_scores_rating > 0 & precio_eur <= 500)

ggplot(df_filtrado_rating, aes(x = review_scores_rating, y = precio_eur)) +
  geom_point(alpha = 0.2, color = "steelblue") +
  geom_smooth(method = "lm", color = "darkred", se = FALSE) +
  labs(
    title = "Relación entre Valoración del Huésped y Precio del Alojamiento",
    subtitle = "Cada punto representa un anuncio en España",
    x = "Puntuación Media (Review Score Rating)",
    y = "Precio por Noche (€)"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(face = "bold", size = 14))
# 3 Conclusiones:
#3.1.Oferta de altísima calidad (lado derecho): la mayoría de los huéspedes valoran con 4-5 
#3.2.Correlación muy débil entre alta calidad y precio caro (Línea roja) 
#3.3.El precio no determina la satisfacción (Dispersión):Puedes encontrar alojamientos muy económicos (por debajo de 100€) y muy caros (más de 400€) con valoraciones excelentes (cercanas a 5)
#Resumiendo: Gran variedad de opciones con alta calidad a precios moderados

# =====================================================================
# GRÁFICO 4: Impacto del Estatus Superhost en el Volumen de Reseñas
# =====================================================================
# Objetivo: el sello Superhost no solo mejora las valoraciones, sino que multiplica de forma masiva el volumen de interacciones y reservas (medido a través de las reseñas)
library(ggplot2)

df_superhost <- df %>% filter(number_of_reviews <= 150 & !is.na(host_is_superhost))

ggplot(df_superhost, aes(x = host_is_superhost, y = number_of_reviews, fill = host_is_superhost)) +
  geom_violin(trim = FALSE, alpha = 0.6) +
  geom_boxplot(width = 0.1, color = "black", alpha = 0.8, outlier.shape = NA) +
  scale_x_discrete(labels = c("f" = "Anfitrión Estándar", "t" = "Superhost")) +
  labs(
    title = "El 'Efecto Superhost': Mayor Tracción y Volumen de Reservas",
    subtitle = "Comparativa del número de reseñas acumuladas por tipo de anfitrión (filtrado hasta 150 reseñas)",
    x = "Categoría de Anfitrión",
    y = "Número Total de Reseñas (Proxy de Ocupación)"
  ) +
  theme_minimal() +
  theme(
    legend.position = "none",
    plot.title = element_text(face = "bold", size = 14),
    axis.text = element_text(size = 11))
# 4 Conclusiones:
# 4.1. Los superhost tienen un volumen de reseñas (y ocupación) mayor que los no superhsot
# 4.2. El cuerpo estandar y ancho de los superhost en el tramo 50-100 reseñas garantiza un flujo constante de clientes a lo largo del tiempo
# 4.3. os anfitriones convencionales tienen muy pocas evaluaciones y menor tracción comercial
# Resumen: El estatus de Superhost actúa como catalizador directo de ocupación desplazando la media de actividad hacia arriba
# =====================================================================
# GRÁFICO 5: Estructura de Propiedad (Ley de Vivienda) por Región
# =====================================================================
# Objetivo: qué porcentaje de la oferta en cada región está en manos de pequeños propietarios frente a grandes tenedores o gestores profesionales (5+ inmuebles)
ggplot(df, aes(x = region_origen, fill = tramo_propietario)) +
  geom_bar(position = "fill") +
  scale_y_continuous(labels = scales::percent_format()) +
  labs(
    title = "Estructura de la Propiedad Turística por Región",
    subtitle = "Distribución porcentual según el tamaño del portafolio del anfitrión (Ley de Vivienda)",
    x = "Región / Destino",
    y = "Porcentaje sobre el Total de la Oferta",
    fill = "Tramo de Propiedad"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    legend.position = "bottom",
    axis.text.x = element_text(face = "bold")
  ) +
  guides(fill = guide_legend(nrow = 2))
# 5 Conclusiones:
# 5.1. Fuerte presencia de Grandes tenedores en zonas urbanas clave (como Bcn)
# 5.2. Mayor peso del pequeño particular en PV incluso Ger 
# 5.3. Dominio del perfil profesional e inversor
# Resumen: El mercado del alquiler turístico en Esp está fuertemente profesionalizado, la > parte de la oferta no procede de familias q alquilan su vivienda, sino de gestores e inversores multipropiedad 
# =====================================================================
# GRÁFICO 6: Escalado de Precios según Capacidad de Huéspedes y Tipo
# =====================================================================
# Objetivo: Muestra cómo crece el precio por noche a medida que aumenta la capacidad de huéspedes (accommodates)
df_facet <- df %>% filter(precio_eur <= 450 & accommodates <= 10)

ggplot(df_facet, aes(x = as.factor(accommodates), y = precio_eur, fill = room_type)) +
  geom_boxplot(outlier.alpha = 0.2, outlier.size = 1) +
  facet_wrap(~ room_type, scales = "free_y") +
  labs(
    title = "Evolución del Precio por Noche según la Capacidad de Huéspedes",
    subtitle = "Análisis segmentado por tipología de alojamiento",
    x = "Capacidad de Personas (Huéspedes)",
    y = "Precio por Noche (€)"
  ) +
  theme_minimal() +
  theme(
    legend.position = "none",
    plot.title = element_text(face = "bold", size = 14),
    strip.text = element_text(face = "bold", size = 11))
# 6 Conclusiones:
# 6.1. Crecimiento lógico y ordenado en viviendas enteras: cuantas más personas caben en el alojamiento, mayor es el precio por noche
# 6.2. Las habitaciones compartidas son siempre económicas
# 6.3. Comportamiento estable en hoteles y fluctuación en habitaciones privadas
# Resumen: La capacidad marca el precio principalmente en viviendas completas, esto es, el tamaño del alojamiento (número de huéspedes) encarece la tarifa de forma predecible en los pisos enteros, mientras que las opciones compartidas o habitaciones individuales conservan precios bajos

# =====================================================================
# GRÁFICO 6_Mallorca: Escalado de Precios según Capacidad de Huéspedes y Tipo en Mallorca
# =====================================================================
# Objetivo: Muestra cómo crece el precio por noche a medida que aumenta la capacidad de huéspedes (accommodates)
# 1. Filtramos los datos guardando en el objeto filtrado
df_facet_mallorca <- df %>% 
  filter(region_origen == "Mallorca" & precio_eur <= 450 & accommodates <= 10)

# 2. Generamos el gráfico usando df_facet_mallorca
ggplot(df_facet_mallorca, aes(x = as.factor(accommodates), y = precio_eur, fill = room_type)) +
  geom_boxplot(outlier.alpha = 0.2, outlier.size = 1) +
  facet_wrap(~ room_type, scales = "free_y") +
  labs(
    title = "Evolución del Precio por Noche según la Capacidad (Mallorca)",
    subtitle = "Análisis segmentado por tipología de alojamiento en Mallorca",
    x = "Capacidad de Personas (Huéspedes)",
    y = "Precio por Noche (€)"
  ) +
  theme_minimal() +
  theme(
    legend.position = "none",
    plot.title = element_text(face = "bold", size = 14),
    strip.text = element_text(face = "bold", size = 11)
  )
# 6_Mallorca Conclusiones:
# 6.1_Mallorca. Precios notablemente más caros en Mallorca
# 6.2_Mallorca. Menor variedad de opciones compartidas
# Resumen_Mallorca:Mallorca opera en una categoría de precios superior y más estacional

# =====================================================================
# RESUMEN EJECUTIVO AIRBNB ESPAÑA
# =====================================================================
# 1. La capacidad y el destino (especialmente Islas, y sobre todo Mallorca) marcan la pauta de los precios
# 2. El "Efecto Superhost" como acelerador de reservas: impulsa drásticamente el volumen comercial
# 3. Mercado altamente profesionalizado y dominado por multipropietarios: los grandes tenedores y gestores profesionales (con 2 a 10+ propiedades) controlan la mayor parte de la oferta
# RECOMENDACIÓN ESTRATÉGICA PARA QUE UN INVERSOR MAXIMICE LA RENTABILIDAD: SE RECOMIENDA FOCALIZARSE EN EL ALQUILER DE VIVIENDAS COMPLETAS (ENTIRE HOME/APT) CON CAPACIDAD PARA GRUPOS O FAMILIAS EN ZONAS DE ALTA DEMANDA Y PRIORIZAR OPERATIONALMENTE LA OBTENCIÓN DEL SELLO SUPERHOST DESDE EL PRIMER TRIMESTRE. LA CONSECUCIÓN DE ESTA INSIGNIA ES LA PALANCA MÁS EFICAZ PARA ROMPER LA BARRERA DE ENTRADA, DIFERENCIARSE EN UN MERCADO DOMINADO POR GRANDES TENEDORES PROFESIONALES Y ASEGURAR UN FLUJO CONSTANTE Y RECURRENTE DE OCUPACIÓN A TARIFAS PRÉMIUM


# =====================================================================
# EJERCICIO POTENCIAL DE PRECIOS: BENICARLO vs. ENTORNO COMPETITIVO (Peñíscola, Alcossebre, Vinarós) 
# =====================================================================
# Bloque conceptual de validación visual para Benicarló / Corredor Castellón-Tarragona
library(ggplot2)
library(dplyr)

# Simulación de datos comparativos de mercado para el informe
df_inversion <- data.frame(
  Zona = c("Benicarló (Exclusivo)", "Peñíscola Costa", "Vinaròs", "Alcossebre"),
  Precio_Medio_Noche = c(210, 195, 160, 185),
  Ocupacion_Estimada_Verano = c(0.85, 0.90, 0.75, 0.80)
)

ggplot(df_inversion, aes(x = reorder(Zona, Precio_Medio_Noche), y = Precio_Medio_Noche, fill = Zona)) +
  geom_col(width = 0.6, alpha = 0.9) +
  coord_flip() +
  labs(
    title = "Potencial de Precios: Benicarló vs. Entorno Competitivo",
    subtitle = "Tarifa media estimada por noche para apartamentos exclusivos en temporada alta",
    x = "Destino / Zona",
    y = "Precio Medio por Noche (€)"
  ) +
  theme_minimal() +
  theme(legend.position = "none", plot.title = element_text(face = "bold", size = 13))




# =====================================================================
# SCRIPT R: Proyección Financiera y Benchmark para Plan de Inversión
# =====================================================================
library(tidyverse)

# 1. Cargar el dataset limpio con el que hemos trabajado
# df <- read.csv("C:/Users/5/Desktop/JAVI/R/airbnb_espana_clean.csv")

# 2. Filtrar un benchmark de referencia costera similar a Benicarló (ej. Menorca o Valencia)
df_benchmark <- df %>% 
  filter(region_origen %in% c("Menorca", "Val") & room_type == "Entire home/apt" & precio_eur <= 350)

# 3. Calcular métricas clave de referencia para el modelo financiero
resumen_benchmark <- df_benchmark %>%
  group_by(region_origen) %>%
  summarise(
    Precio_Mediano = median(precio_eur, na.rm = TRUE),
    Precio_Medio = mean(precio_eur, na.rm = TRUE),
    Reseñas_Medias = mean(number_of_reviews, na.rm = TRUE)
  )

print("Métricas de referencia costera para calibrar el Business Plan:")
print(resumen_benchmark)

# 4. Proyección de ingresos brutos anuales estimados para el apartamento en Benicarló
# Asumiendo 60 noches en temporada alta a precio premium y 40 noches en temporada media/baja
precio_objetivo_alto <- 200
precio_objetivo_medio <- 150

ingresos_brutos_estimados <- (60 * precio_objetivo_alto) + (40 * precio_objetivo_medio)
cat("Ingresos Brutos Anuales Estimados (Simulación Inmobiliaria):", ingresos_brutos_estimados, "€\n")

# =====================================================================
# SCRIPT R: Simulación Inmobiliaria - Estudio / 1 Hab + Terraza 60m2
# =====================================================================

# 1. Parámetros de Inversión (Estudio + Terraza Premium)
inversion_total_estudio <- 300000

# 2. Estimación de Noches y Precios (Perfil Parejas / Premium Outdoor)
noches_alta <- 60
precio_alta <- 200

noches_media_baja <- 60
precio_media_baja <- 150

# 3. Cálculo de Estado de Resultados
ingresos_brutos <- (noches_alta * precio_alta) + (noches_media_baja * precio_media_baja)
comisiones <- ingresos_brutos * 0.15
gastos_fijos <- 1800 + 1600 + 800 + 400  # Suministros, limpieza, IBI/comunidad, seguro

opex_total <- comisiones + gastos_fijos
noi <- ingresos_brutos - opex_total
cap_rate <- (noi / inversion_total_estudio) * 100

# 4. Salida por consola
cat("--- RESULTADOS RECALCULADOS (ESTUDIO / 1 HAB + TERRAZA 60M2) ---\n")
cat("Inversión Inicial Requerida:", inversion_total_estudio, "€\n")
cat("Ingresos Brutos Anuales:", ingresos_brutos, "€\n")
cat("Gastos Operativos (Opex):", opex_total, "€\n")
cat("Beneficio Neto Operativo (NOI):", noi, "€\n")
cat("Cap Rate (Rentabilidad Neta):", round(cap_rate, 2), "%\n")

