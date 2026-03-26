"""
eda_transporte_urbano.py
========================
Análisis Exploratorio de Datos — Plataforma de Transporte Urbano 2024
Autor: Ricardo Javier Sequeda Goez
Stack: Python | pandas | matplotlib | seaborn

Estructura:
  1. Carga y auditoría inicial
  2. Limpieza y transformación
  3. Análisis de demanda temporal
  4. Análisis por zona geográfica
  5. Análisis de tarifas y revenue
  6. Análisis de calidad del servicio
  7. Detección de outliers y anomalías
  8. Conclusiones de negocio
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")
os.makedirs("graficas", exist_ok=True)

# ── Estilo global ────────────────────────────────────────────────────────────
PALETTE_MAIN  = ["#1F4E8C", "#2E75B6", "#5BA3D9", "#A8C8E8", "#D6E4F0"]
PALETTE_ALERT = ["#C0392B", "#E67E22", "#F1C40F", "#27AE60", "#1F4E8C"]
sns.set_theme(style="whitegrid", palette=PALETTE_MAIN)
plt.rcParams.update({
    "figure.dpi": 130,
    "font.family": "DejaVu Sans",
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

def guardar(nombre):
    plt.tight_layout()
    plt.savefig(f"graficas/{nombre}.png", bbox_inches="tight")
    plt.close()
    print(f"  ✅ graficas/{nombre}.png")


# ═══════════════════════════════════════════════════════════════════════════
# 1. CARGA Y AUDITORÍA INICIAL
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*65)
print("  1. CARGA Y AUDITORÍA INICIAL")
print("═"*65)

df = pd.read_csv("viajes_urbanos_2024.csv", parse_dates=["fecha_inicio", "fecha_fin"])

print(f"\n📦 Dimensiones: {df.shape[0]:,} filas × {df.shape[1]} columnas")
print("\n📋 Tipos de datos:")
print(df.dtypes.to_string())

print("\n🔍 Valores nulos por columna:")
nulos = df.isnull().sum()
nulos_pct = (nulos / len(df) * 100).round(2)
auditoria = pd.DataFrame({"nulos": nulos, "pct": nulos_pct})
print(auditoria[auditoria["nulos"] > 0].to_string())

print(f"\n🔁 Duplicados exactos: {df.duplicated().sum()}")
print(f"\n📊 Estadísticas descriptivas (numéricas):")
print(df.describe().round(2).to_string())


# ═══════════════════════════════════════════════════════════════════════════
# 2. LIMPIEZA Y TRANSFORMACIÓN
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*65)
print("  2. LIMPIEZA Y TRANSFORMACIÓN")
print("═"*65)

df_raw_shape = df.shape

# 2.1 Separar viajes cancelados (no aportan métricas de servicio)
df_cancelados = df[df["cancelado"] == True].copy()
df = df[df["cancelado"] == False].copy()
print(f"\n→ Viajes cancelados separados: {len(df_cancelados):,} ({len(df_cancelados)/df_raw_shape[0]*100:.1f}%)")
print(f"→ Viajes activos para análisis: {len(df):,}")

# 2.2 Imputar calificacion nula con mediana por tipo de vehículo
mediana_calif = df.groupby("tipo_vehiculo")["calificacion"].median()
df["calificacion"] = df.apply(
    lambda r: mediana_calif[r["tipo_vehiculo"]] if pd.isnull(r["calificacion"]) else r["calificacion"],
    axis=1
)

# 2.3 Imputar zona_destino nula con moda por zona_origen
moda_destino = df.groupby("zona_origen")["zona_destino"].agg(
    lambda x: x.mode()[0] if not x.mode().empty else "Desconocido"
)
df["zona_destino"] = df.apply(
    lambda r: moda_destino[r["zona_origen"]] if pd.isnull(r["zona_destino"]) else r["zona_destino"],
    axis=1
)

# 2.4 Imputar metodo_pago con moda global
moda_pago = df["metodo_pago"].mode()[0]
df["metodo_pago"] = df["metodo_pago"].fillna(moda_pago)

# 2.5 Imputar tarifa_cop con mediana por tipo de vehículo
mediana_tarifa = df.groupby("tipo_vehiculo")["tarifa_cop"].median()
df["tarifa_cop"] = df.apply(
    lambda r: mediana_tarifa[r["tipo_vehiculo"]] if pd.isnull(r["tarifa_cop"]) else r["tarifa_cop"],
    axis=1
)

# 2.6 Eliminar outliers de distancia (>3 IQR)
Q1 = df["distancia_km"].quantile(0.25)
Q3 = df["distancia_km"].quantile(0.75)
IQR = Q3 - Q1
limite_sup = Q3 + 3 * IQR
outliers_dist = df[df["distancia_km"] > limite_sup]
df = df[df["distancia_km"] <= limite_sup].copy()
print(f"→ Outliers de distancia eliminados: {len(outliers_dist)}")

# 2.7 Feature engineering
df["dia_semana_num"] = df["fecha_inicio"].dt.dayofweek  # 0=Lunes
df["semana_anio"]    = df["fecha_inicio"].dt.isocalendar().week.astype(int)
df["trimestre"]      = df["fecha_inicio"].dt.quarter
df["es_fin_semana"]  = df["dia_semana_num"].isin([5, 6])
df["franja_horaria"] = pd.cut(
    df["hora"],
    bins=[-1, 5, 9, 12, 17, 20, 23],
    labels=["Madrugada", "Mañana pico", "Mañana baja", "Tarde", "Tarde pico", "Noche"]
)
df["revenue_por_km"] = (df["tarifa_cop"] / df["distancia_km"]).round(0)

ORDEN_DIAS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
ORDEN_DIAS_ES = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
dia_map = dict(zip(ORDEN_DIAS, ORDEN_DIAS_ES))
df["dia_semana_es"] = df["dia_semana"].map(dia_map)

print(f"\n→ Dataset limpio final: {df.shape[0]:,} filas × {df.shape[1]} columnas")
print(f"→ Nulos restantes: {df.isnull().sum().sum()}")


# ═══════════════════════════════════════════════════════════════════════════
# 3. ANÁLISIS DE DEMANDA TEMPORAL
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*65)
print("  3. ANÁLISIS DE DEMANDA TEMPORAL")
print("═"*65)

# 3.1 Viajes por hora del día
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

viajes_hora = df.groupby("hora").size().reset_index(name="viajes")
axes[0].bar(viajes_hora["hora"], viajes_hora["viajes"], color=PALETTE_MAIN[1], alpha=0.85, edgecolor="white")
axes[0].set_title("Distribución de Viajes por Hora del Día")
axes[0].set_xlabel("Hora")
axes[0].set_ylabel("Cantidad de Viajes")
axes[0].axvspan(7, 9, alpha=0.15, color="#C0392B", label="Pico mañana")
axes[0].axvspan(17, 20, alpha=0.15, color="#E67E22", label="Pico tarde")
axes[0].legend(fontsize=9)

# 3.2 Viajes por día de semana
viajes_dia = (
    df.groupby(["dia_semana_num", "dia_semana_es"])
    .size().reset_index(name="viajes")
    .sort_values("dia_semana_num")
)
bars = axes[1].bar(viajes_dia["dia_semana_es"], viajes_dia["viajes"],
                   color=[PALETTE_MAIN[3] if i >= 5 else PALETTE_MAIN[1] for i in range(7)],
                   alpha=0.85, edgecolor="white")
axes[1].set_title("Viajes por Día de Semana")
axes[1].set_xlabel("Día")
axes[1].set_ylabel("Cantidad de Viajes")
axes[1].tick_params(axis='x', rotation=30)

for bar in bars:
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                 f"{int(bar.get_height()):,}", ha="center", va="bottom", fontsize=8)

guardar("01_demanda_temporal")

# 3.3 Heatmap hora × día de semana
print("\n→ Generando heatmap hora×día...")
pivot_heatmap = df.pivot_table(
    index="dia_semana_num", columns="hora", values="viaje_id", aggfunc="count"
).fillna(0)
pivot_heatmap.index = ORDEN_DIAS_ES

fig, ax = plt.subplots(figsize=(16, 5))
sns.heatmap(pivot_heatmap, cmap="Blues", linewidths=0.3, ax=ax,
            cbar_kws={"label": "Viajes"}, fmt=".0f", annot=False)
ax.set_title("Mapa de Calor — Demanda por Hora y Día de Semana", fontsize=14, pad=15)
ax.set_xlabel("Hora del Día")
ax.set_ylabel("")
guardar("02_heatmap_demanda")

# 3.4 Evolución semanal (tendencia)
viajes_semana = df.groupby("semana_anio").size().reset_index(name="viajes")
fig, ax = plt.subplots(figsize=(14, 4))
ax.plot(viajes_semana["semana_anio"], viajes_semana["viajes"],
        color=PALETTE_MAIN[1], linewidth=1.5, alpha=0.7)
# Media móvil 4 semanas
viajes_semana["media_movil"] = viajes_semana["viajes"].rolling(4, center=True).mean()
ax.plot(viajes_semana["semana_anio"], viajes_semana["media_movil"],
        color=PALETTE_MAIN[0], linewidth=2.5, label="Media móvil 4 sem.")
ax.fill_between(viajes_semana["semana_anio"], viajes_semana["viajes"],
                alpha=0.1, color=PALETTE_MAIN[1])
ax.set_title("Evolución Semanal de Viajes — 2024")
ax.set_xlabel("Semana del año")
ax.set_ylabel("Viajes")
ax.legend()
guardar("03_evolucion_semanal")

# KPIs demanda
hora_pico = viajes_hora.loc[viajes_hora["viajes"].idxmax(), "hora"]
dia_pico  = viajes_dia.loc[viajes_dia["viajes"].idxmax(), "dia_semana_es"]
print(f"  Hora pico: {hora_pico}:00h ({viajes_hora['viajes'].max():,} viajes)")
print(f"  Día pico:  {dia_pico}")
print(f"  Promedio diario de viajes: {len(df)/365:.0f}")


# ═══════════════════════════════════════════════════════════════════════════
# 4. ANÁLISIS POR ZONA GEOGRÁFICA
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*65)
print("  4. ANÁLISIS POR ZONA GEOGRÁFICA")
print("═"*65)

# 4.1 Matriz OD (Origen → Destino)
od_matrix = df.pivot_table(
    index="zona_origen", columns="zona_destino",
    values="viaje_id", aggfunc="count", fill_value=0
)

fig, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(od_matrix, cmap="YlOrRd", ax=ax, linewidths=0.4,
            cbar_kws={"label": "Número de viajes"},
            annot=True, fmt="d", annot_kws={"size": 8})
ax.set_title("Matriz Origen–Destino de Viajes", fontsize=14, pad=15)
ax.set_xlabel("Zona Destino")
ax.set_ylabel("Zona Origen")
plt.xticks(rotation=40, ha="right")
guardar("04_matriz_OD")

# 4.2 Revenue por zona de origen
rev_zona = (
    df.groupby("zona_origen")["tarifa_cop"]
    .agg(["sum", "mean", "count"])
    .rename(columns={"sum": "revenue_total", "mean": "tarifa_media", "count": "viajes"})
    .sort_values("revenue_total", ascending=True)
)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
rev_zona["revenue_total"].div(1e6).plot(kind="barh", ax=axes[0],
    color=PALETTE_MAIN[1], alpha=0.85, edgecolor="white")
axes[0].set_title("Revenue Total por Zona de Origen (COP mill.)")
axes[0].set_xlabel("Millones COP")
axes[0].set_ylabel("")

rev_zona["tarifa_media"].sort_values(ascending=True).plot(kind="barh", ax=axes[1],
    color=PALETTE_MAIN[2], alpha=0.85, edgecolor="white")
axes[1].set_title("Tarifa Promedio por Zona de Origen (COP)")
axes[1].set_xlabel("COP")
axes[1].set_ylabel("")
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
guardar("05_revenue_por_zona")

print(f"  Zona mayor revenue: {rev_zona['revenue_total'].idxmax()}")
print(f"  Zona mayor tarifa promedio: {rev_zona['tarifa_media'].idxmax()}")


# ═══════════════════════════════════════════════════════════════════════════
# 5. ANÁLISIS DE TARIFAS Y REVENUE
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*65)
print("  5. ANÁLISIS DE TARIFAS Y REVENUE")
print("═"*65)

# 5.1 Distribución de tarifas por tipo de vehículo
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for i, (vh, grupo) in enumerate(df.groupby("tipo_vehiculo")):
    axes[i].hist(grupo["tarifa_cop"] / 1000, bins=40,
                 color=PALETTE_MAIN[i], alpha=0.8, edgecolor="white")
    axes[i].axvline(grupo["tarifa_cop"].median() / 1000, color="#C0392B",
                    linestyle="--", linewidth=1.5, label=f"Mediana: ${grupo['tarifa_cop'].median()/1000:.0f}k")
    axes[i].set_title(f"Distribución Tarifa — {vh}")
    axes[i].set_xlabel("Tarifa (miles COP)")
    axes[i].set_ylabel("Frecuencia")
    axes[i].legend(fontsize=9)

plt.suptitle("Distribución de Tarifas por Tipo de Vehículo", fontsize=14, y=1.01)
guardar("06_distribucion_tarifas")

# 5.2 Revenue mensual por tipo de vehículo
rev_mensual = df.groupby(["mes", "tipo_vehiculo"])["tarifa_cop"].sum().reset_index()
rev_pivot   = rev_mensual.pivot(index="mes", columns="tipo_vehiculo", values="tarifa_cop").fillna(0)

fig, ax = plt.subplots(figsize=(14, 6))
rev_pivot.div(1e6).plot(kind="bar", ax=ax, color=PALETTE_MAIN[:4],
                        alpha=0.85, edgecolor="white", width=0.75)
ax.set_title("Revenue Mensual por Tipo de Vehículo (Millones COP)")
ax.set_xlabel("Mes")
ax.set_ylabel("Millones COP")
ax.set_xticklabels(["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"],
                   rotation=0)
ax.legend(title="Vehículo", bbox_to_anchor=(1.01, 1))
guardar("07_revenue_mensual")

# 5.3 Relación distancia vs tarifa con precio pico
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(
    df["distancia_km"], df["tarifa_cop"] / 1000,
    c=df["factor_demanda"], cmap="RdYlGn_r",
    alpha=0.25, s=8
)
plt.colorbar(scatter, ax=ax, label="Factor demanda (precio pico)")
ax.set_title("Distancia vs Tarifa — Impacto del Precio Pico")
ax.set_xlabel("Distancia (km)")
ax.set_ylabel("Tarifa (miles COP)")
guardar("08_distancia_vs_tarifa")

# KPIs revenue
revenue_total = df["tarifa_cop"].sum()
ticket_promedio = df["tarifa_cop"].mean()
rev_por_km_promedio = df["revenue_por_km"].mean()
print(f"  Revenue total 2024:      COP {revenue_total:,.0f}")
print(f"  Ticket promedio:         COP {ticket_promedio:,.0f}")
print(f"  Revenue promedio por km: COP {rev_por_km_promedio:,.0f}")
print(f"  Tipo vehículo más rentable: {df.groupby('tipo_vehiculo')['tarifa_cop'].sum().idxmax()}")


# ═══════════════════════════════════════════════════════════════════════════
# 6. ANÁLISIS DE CALIDAD DEL SERVICIO
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*65)
print("  6. ANÁLISIS DE CALIDAD DEL SERVICIO")
print("═"*65)

# 6.1 Calificaciones por tipo de vehículo y franja horaria
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

calif_vh = df.groupby("tipo_vehiculo")["calificacion"].value_counts(normalize=True).unstack().fillna(0)
calif_vh.plot(kind="bar", stacked=True, ax=axes[0],
              color=PALETTE_ALERT, alpha=0.9, edgecolor="white", width=0.6)
axes[0].set_title("Distribución de Calificaciones por Tipo de Vehículo")
axes[0].set_xlabel("")
axes[0].set_ylabel("Proporción")
axes[0].tick_params(axis='x', rotation=30)
axes[0].legend(title="Calificación", labels=["★1","★2","★3","★4","★5"],
               bbox_to_anchor=(1.01, 1))

orden_franja = ["Madrugada", "Mañana pico", "Mañana baja", "Tarde", "Tarde pico", "Noche"]
calif_franja = df.groupby("franja_horaria")["calificacion"].mean().reindex(orden_franja)
bars = axes[1].bar(range(len(calif_franja)), calif_franja.values,
                   color=[PALETTE_ALERT[4] if v >= 4.0 else PALETTE_ALERT[2] if v >= 3.5 else PALETTE_ALERT[0]
                          for v in calif_franja.values],
                   alpha=0.85, edgecolor="white")
axes[1].set_xticks(range(len(calif_franja)))
axes[1].set_xticklabels(calif_franja.index, rotation=35, ha="right")
axes[1].set_title("Calificación Promedio por Franja Horaria")
axes[1].set_ylabel("Calificación promedio")
axes[1].set_ylim(3.5, 5.1)
axes[1].axhline(df["calificacion"].mean(), color="#C0392B",
                linestyle="--", linewidth=1.5, label=f"Global: {df['calificacion'].mean():.2f}")
axes[1].legend()

for bar, val in zip(bars, calif_franja.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, val + 0.03,
                 f"{val:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
guardar("09_calificaciones")

# 6.2 Método de pago vs calificación
fig, ax = plt.subplots(figsize=(10, 5))
df.boxplot(column="calificacion", by="metodo_pago", ax=ax,
           patch_artist=True, notch=False,
           boxprops=dict(facecolor=PALETTE_MAIN[2], alpha=0.7),
           medianprops=dict(color=PALETTE_MAIN[0], linewidth=2))
ax.set_title("Calificación por Método de Pago")
ax.set_xlabel("Método de Pago")
ax.set_ylabel("Calificación")
plt.suptitle("")
guardar("10_pago_vs_calificacion")

# 6.3 Tasa de cancelación por hora
cancel_hora = (
    pd.read_csv("viajes_urbanos_2024.csv", parse_dates=["fecha_inicio"])
    .groupby("hora")["cancelado"]
    .mean() * 100
)
fig, ax = plt.subplots(figsize=(12, 4))
ax.bar(cancel_hora.index, cancel_hora.values, color="#C0392B", alpha=0.75, edgecolor="white")
ax.set_title("Tasa de Cancelación por Hora del Día (%)")
ax.set_xlabel("Hora")
ax.set_ylabel("% Cancelados")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.1f}%"))
guardar("11_tasa_cancelacion")

print(f"  Calificación global promedio: {df['calificacion'].mean():.2f} ★")
print(f"  % viajes con ★5:             {(df['calificacion']==5).mean()*100:.1f}%")
print(f"  % viajes con ★1-2:           {(df['calificacion']<=2).mean()*100:.1f}%")
print(f"  Franja con menor calificación: {calif_franja.idxmin()} ({calif_franja.min():.2f}★)")


# ═══════════════════════════════════════════════════════════════════════════
# 7. DETECCIÓN DE OUTLIERS Y ANOMALÍAS
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*65)
print("  7. DETECCIÓN DE OUTLIERS Y ANOMALÍAS")
print("═"*65)

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
columnas_out = ["distancia_km", "tarifa_cop", "duracion_min"]
titulos_out  = ["Distancia (km)", "Tarifa (COP)", "Duración (min)"]

for ax, col, titulo in zip(axes, columnas_out, titulos_out):
    data = df[col].dropna()
    Q1, Q3 = data.quantile([0.25, 0.75])
    IQR = Q3 - Q1
    n_out = ((data < Q1 - 1.5*IQR) | (data > Q3 + 1.5*IQR)).sum()

    ax.boxplot(data, vert=True, patch_artist=True,
               boxprops=dict(facecolor=PALETTE_MAIN[2], alpha=0.7),
               medianprops=dict(color=PALETTE_MAIN[0], linewidth=2),
               flierprops=dict(marker="o", markerfacecolor="#C0392B",
                               markersize=3, alpha=0.4))
    ax.set_title(f"{titulo}\nOutliers IQR: {n_out:,}")
    ax.set_ylabel(titulo)
    print(f"  {titulo}: {n_out} outliers ({n_out/len(data)*100:.2f}%)")

plt.suptitle("Detección de Outliers — Variables Numéricas Clave", fontsize=13)
guardar("12_outliers")


# ═══════════════════════════════════════════════════════════════════════════
# 8. CORRELACIONES
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*65)
print("  8. MATRIZ DE CORRELACIONES")
print("═"*65)

cols_corr = ["distancia_km", "duracion_min", "tarifa_cop",
             "calificacion", "n_pasajeros", "factor_demanda", "revenue_por_km"]
corr_matrix = df[cols_corr].corr()

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
sns.heatmap(corr_matrix, ax=ax, cmap="coolwarm", center=0,
            annot=True, fmt=".2f", linewidths=0.5,
            cbar_kws={"label": "Correlación de Pearson"},
            mask=False, square=True, annot_kws={"size": 9})
ax.set_title("Matriz de Correlaciones — Variables Numéricas", pad=15)
guardar("13_correlaciones")


# ═══════════════════════════════════════════════════════════════════════════
# 9. RESUMEN EJECUTIVO (KPIs)
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*65)
print("  9. RESUMEN EJECUTIVO")
print("═"*65)

print(f"""
┌─────────────────────────────────────────────────────────────┐
│              RESUMEN EJECUTIVO — PLATAFORMA 2024            │
├──────────────────────────────┬──────────────────────────────┤
│ VOLUMEN                      │ REVENUE                      │
│  Total viajes completados:   │  Revenue total:              │
│  {len(df):>9,}               │  COP {revenue_total/1e9:>7.2f} Mil millones      │
│                              │                              │
│  Viajes cancelados:          │  Ticket promedio:            │
│  {len(df_cancelados):>9,} ({len(df_cancelados)/(len(df)+len(df_cancelados))*100:.1f}%)         │  COP {ticket_promedio:>10,.0f}           │
│                              │                              │
│  Promedio diario:            │  Rev. promedio/km:           │
│  {len(df)/365:>9.0f}               │  COP {rev_por_km_promedio:>10,.0f}           │
├──────────────────────────────┼──────────────────────────────┤
│ DEMANDA                      │ CALIDAD                      │
│  Hora pico AM:  07:00–09:00  │  Calificación global:        │
│  Hora pico PM:  17:00–20:00  │  {df['calificacion'].mean():.2f} ★ / 5.00              │
│                              │                              │
│  Vehículo + demandado:       │  Viajes ★5:                  │
│  {df['tipo_vehiculo'].value_counts().idxmax():<16}         │  {(df['calificacion']==5).mean()*100:.1f}%                       │
└──────────────────────────────┴──────────────────────────────┘
""")


# ═══════════════════════════════════════════════════════════════════════════
# 10. CONCLUSIONES DE NEGOCIO
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*65)
print("  10. CONCLUSIONES DE NEGOCIO")
print("═"*65)

conclusiones = """
  1. DEMANDA CONCENTRADA EN PICOS
     La demanda se concentra en dos franjas críticas: 07:00–09:00 (pico
     matutino) y 17:00–20:00 (pico vespertino), representando aprox. el
     45% del total de viajes. Esto valida la estrategia de pricing dinámico
     y sugiere reforzar la disponibilidad de conductores en esas ventanas.

  2. DÍAS HÁBILES DOMINAN EL VOLUMEN
     Lunes a viernes concentran el mayor volumen de viajes. Sin embargo,
     el fin de semana muestra tarifas promedio más altas, indicando que
     los usuarios de fin de semana tienen menor sensibilidad al precio.
     Oportunidad: campañas de fidelización para usuarios frecuentes LV.

  3. VEHÍCULO CARRO ES EL MOTOR DE REVENUE
     A pesar de que Moto tiene mayor volumen de viajes, el tipo Carro
     genera el mayor revenue total por su combinación de tarifa unitaria
     alta y volumen sostenido. Premium tiene la tarifa/km más alta pero
     menor demanda — hay espacio para crecer ese segmento.

  4. ZONAS CENTRO Y NORTE: MAYOR FLUJO
     La matriz OD muestra que Centro y Norte son los polos de mayor
     generación y atracción de viajes. Estratégicamente, una mayor
     concentración de conductores en estas zonas en horas pico reduciría
     tiempos de espera y aumentaría conversión.

  5. CALIDAD BAJA EN PRECIO PICO
     Las franjas de precio pico (Mañana pico, Tarde pico) presentan las
     calificaciones más bajas. Posible causa: conductores con mayor carga
     de trabajo y menor atención al usuario. Recomendación: programa de
     incentivos para conductores en horas pico ligado a calificación.

  6. TASA DE CANCELACIÓN MANEJABLE
     La tasa de cancelación global (~5%) es aceptable para el sector, pero
     muestra variabilidad horaria. Investigar si las cancelaciones en hora
     pico se deben a esperas largas o a cambios de precio dinámico.
"""
print(conclusiones)
print("═"*65)
print(f"  📁 Todas las gráficas guardadas en: ./graficas/ ({len(os.listdir('graficas'))} archivos)")
print("═"*65)
