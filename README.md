# 🚗 EDA — Plataforma de Transporte Urbano 2024

**Análisis Exploratorio de Datos** sobre 15,000 registros de viajes de una plataforma de movilidad urbana.  
El objetivo es identificar patrones de demanda, comportamiento de tarifas y calidad del servicio para apoyar decisiones de negocio.

---

## 📌 Contexto del Problema

Una plataforma de transporte urbano necesita entender:
- ¿Cuándo y dónde se concentra la demanda?
- ¿Qué tipo de vehículo genera más revenue?
- ¿Cómo varía la calidad del servicio según hora y zona?
- ¿Dónde están las anomalías y oportunidades de optimización?

---

## 🛠️ Stack Tecnológico

| Herramienta | Uso |
|-------------|-----|
| Python 3.10+ | Lenguaje principal |
| pandas | Limpieza, transformación y análisis |
| numpy | Cálculos estadísticos |
| matplotlib | Visualizaciones base |
| seaborn | Gráficas estadísticas avanzadas |

---

## 📂 Estructura del Proyecto

```
eda-transporte-urbano/
│
├── generar_dataset.py          # Generador del dataset sintético realista
├── eda_transporte_urbano.py    # Script principal de análisis (10 secciones)
├── viajes_urbanos_2024.csv     # Dataset generado (15,000 registros)
│
└── graficas/
    ├── 01_demanda_temporal.png
    ├── 02_heatmap_demanda.png
    ├── 03_evolucion_semanal.png
    ├── 04_matriz_OD.png
    ├── 05_revenue_por_zona.png
    ├── 06_distribucion_tarifas.png
    ├── 07_revenue_mensual.png
    ├── 08_distancia_vs_tarifa.png
    ├── 09_calificaciones.png
    ├── 10_pago_vs_calificacion.png
    ├── 11_tasa_cancelacion.png
    ├── 12_outliers.png
    └── 13_correlaciones.png
```

---

## 📊 Dataset

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `viaje_id` | str | Identificador único del viaje |
| `fecha_inicio` | datetime | Fecha y hora de inicio |
| `hora` | int | Hora del día (0–23) |
| `zona_origen` | str | Zona de recogida |
| `zona_destino` | str | Zona de destino |
| `tipo_vehiculo` | str | Moto / Carro / Premium / Camión |
| `distancia_km` | float | Kilómetros recorridos |
| `duracion_min` | float | Duración en minutos |
| `tarifa_cop` | float | Tarifa en pesos colombianos |
| `metodo_pago` | str | Efectivo / Tarjeta / App / Nequi / Daviplata |
| `calificacion` | float | Calificación del servicio (1–5 ★) |
| `cancelado` | bool | Si el viaje fue cancelado |
| `factor_demanda` | float | Multiplicador de precio pico |

**El dataset incluye suciedad intencional** para practicar limpieza: valores nulos en calificación, zona_destino, metodo_pago y tarifa_cop, además de outliers en distancia.

---

## 🔍 Estructura del Análisis

### 1. Auditoría Inicial
- Inspección de tipos, nulos y duplicados
- Estadísticas descriptivas completas

### 2. Limpieza y Transformación
- Separación de viajes cancelados
- Imputación por mediana/moda segmentada por grupo
- Eliminación de outliers extremos (3×IQR)
- Feature engineering: franja horaria, día de semana, revenue/km, trimestre

### 3. Análisis de Demanda Temporal
- Distribución por hora del día con marcadores de precio pico
- Heatmap hora × día de semana
- Tendencia semanal con media móvil de 4 semanas

### 4. Análisis Geográfico
- Matriz Origen–Destino completa (10×10 zonas)
- Revenue y tarifa promedio por zona

### 5. Análisis de Tarifas y Revenue
- Distribución de tarifas por tipo de vehículo
- Revenue mensual por segmento
- Relación distancia–tarifa con impacto del precio pico

### 6. Calidad del Servicio
- Calificaciones por tipo de vehículo y franja horaria
- Calificación vs método de pago
- Tasa de cancelación horaria

### 7. Detección de Outliers
- Análisis IQR para distancia, tarifa y duración

### 8. Correlaciones
- Matriz de correlaciones de Pearson entre variables numéricas

---

## 📈 Hallazgos Principales

### Demanda
- **45%** de los viajes ocurren en dos franjas: 07–09h y 17–20h
- Los **lunes** son el día de mayor demanda; el fin de semana muestra menor volumen pero mayor tarifa promedio

### Revenue
- El tipo **Carro** genera el mayor revenue total (~45% del total)
- La zona **Poblado** lidera en revenue; **Centro** en tarifa promedio por viaje
- Revenue promedio por km: **COP 3,332**

### Calidad
- Calificación global: **4.14 ★ / 5.00**
- El **44.8%** de los viajes recibe calificación máxima (★5)
- Las franjas de precio pico muestran las calificaciones más bajas → posible área de mejora operacional

### Cancelaciones
- Tasa de cancelación global: **~5%**, aceptable para el sector
- Variabilidad horaria sugiere investigar correlación con tiempos de espera

---

## 💡 Recomendaciones de Negocio

1. **Reforzar disponibilidad de conductores** en franjas pico (07–09h, 17–20h) para reducir tiempo de espera y cancelaciones
2. **Programa de incentivos en horas pico** vinculado a calificación para mejorar calidad en momentos de alta demanda
3. **Estrategia diferenciada fin de semana**: los usuarios muestran menor sensibilidad al precio → oportunidad para promocionar servicio Premium
4. **Concentrar flotilla en zonas Centro y Poblado** durante horas pico dado su alto volumen y revenue
5. **Investigar outliers de tarifa** (7% de viajes): pueden indicar errores en el sistema de tarifas o viajes de larga distancia sin categoría propia

---

## 🚀 Cómo Ejecutar

```bash
# 1. Clonar el repositorio
git clone https://github.com/ricardosequeda/eda-transporte-urbano
cd eda-transporte-urbano

# 2. Instalar dependencias
pip install pandas numpy matplotlib seaborn

# 3. Generar el dataset
python generar_dataset.py

# 4. Ejecutar el análisis completo
python eda_transporte_urbano.py

# Las gráficas se guardan automáticamente en ./graficas/
```

---

## 👤 Autor

**Ricardo Javier Sequeda Goez**  
Data Analyst | Business Intelligence | Python & SQL  
📧 Ricardojgoez@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/ricardosequeda)

---

*Dataset sintético generado con distribuciones estadísticas realistas basadas en patrones típicos de plataformas de movilidad urbana en Colombia.*
