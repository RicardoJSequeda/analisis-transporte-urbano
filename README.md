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

Evidenias
<img width="1799" height="629" alt="01_demanda_temporal" src="https://github.com/user-attachments/assets/960cc6ba-393d-42d2-88b3-6b6a052867b9" />
<img width="1876" height="629" alt="02_heatmap_demanda" src="https://github.com/user-attachments/assets/d469371b-1d2d-46d2-a617-9a6ac19c5ff6" />

<img width="1279" height="605" alt="10_pago_vs_calificacion" src="https://github.com/user-attachments/assets/f1411970-e177-4189-aacb-59839e388369" />
<img width="1800" height="759" alt="07_revenue_mensual" src="https://github.com/user-attachments/assets/5817e527-40cb-454e-b9ea-89db3f4a51f0" />
<img width="1799" height="1315" alt="06_distribucion_tarifas" src="https://github.com/user-attachments/assets/b524faa7-5c67-4529-bc14-c12e24695567" />
<img width="1796" height="759" alt="05_revenue_por_zona" src="https://github.com/user-attachments/assets/c7dd71a1-8db5-4cda-92c8-0b744cc262d8" />
<img width="1451" height="1149" alt="04_matriz_OD" src="https://github.com/user-attachments/assets/e970b92f-b435-41d6-b0d1-f92aed66be79" />
<img width="1157" height="1019" alt="13_correlaciones" src="https://github.com/user-attachments/assets/edf7f1fe-6149-4793-b2eb-6df4327990ab" />
<img width="2059" height="639" alt="12_outliers" src="https://github.com/user-attachments/assets/3c31dedc-fb3e-43fd-b069-6c4da473e314" />
<img width="1539" height="499" alt="11_tasa_cancelacion" src="https://github.com/user-attachments/assets/ada86b29-9dc4-40e4-bdc2-ac06e89b38b1" />

<img width="1210" height="759" alt="08_distancia_vs_tarifa" src="https://github.com/user-attachments/assets/b710451f-1ee6-4810-8d71-75921d11cf19" />
<img width="1799" height="759" alt="09_calificaciones" src="https://github.com/user-attachments/assets/182c9d31-f071-4d18-b3ee-4de702fa7686" />

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


## 👤 Autor

**Ricardo Javier Sequeda Goez**  
Data Analyst | Business Intelligence | Python & SQL  
📧 Ricardojgoez@gmail.com  
🔗 [LinkedIn](https://linkedin.com/in/ricardosequeda)

---

*Dataset sintético generado con distribuciones estadísticas realistas basadas en patrones típicos de plataformas de movilidad urbana en Colombia.*
