"""
generar_dataset.py
Genera un dataset realista de viajes urbanos para el proyecto EDA.
Ejecutar una sola vez: python generar_dataset.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# ── Parámetros del dataset ──────────────────────────────────────────────────
N_VIAJES = 15_000
FECHA_INICIO = datetime(2024, 1, 1)
FECHA_FIN = datetime(2024, 12, 31)

ZONAS = [
    "Centro", "Norte", "Sur", "Occidente", "Oriente",
    "Laureles", "Poblado", "Bello", "Itagüí", "Envigado"
]

TIPOS_VEHICULO = {
    "Moto":    {"peso": 0.30, "tarifa_base": 4000,  "tarifa_km": 800},
    "Carro":   {"peso": 0.45, "tarifa_base": 6000,  "tarifa_km": 1200},
    "Premium": {"peso": 0.15, "tarifa_base": 12000, "tarifa_km": 2000},
    "Camión":  {"peso": 0.10, "tarifa_base": 20000, "tarifa_km": 3500},
}

METODOS_PAGO = ["Efectivo", "Tarjeta", "App", "Nequi", "Daviplata"]

# ── Distribución de horas (picos mañana y tarde-noche) ──────────────────────
PESOS_HORA = np.array([
    0.5, 0.3, 0.2, 0.2, 0.3, 0.8,   # 0–5
    2.0, 4.5, 5.0, 3.5, 2.5, 2.2,   # 6–11
    2.8, 2.5, 2.0, 2.2, 3.0, 4.8,   # 12–17
    5.2, 4.0, 3.0, 2.5, 1.8, 1.0    # 18–23
])
PESOS_HORA = PESOS_HORA / PESOS_HORA.sum()


def generar_viaje(idx):
    # Fecha y hora
    dias_rango = (FECHA_FIN - FECHA_INICIO).days
    fecha = FECHA_INICIO + timedelta(days=random.randint(0, dias_rango))
    hora = np.random.choice(24, p=PESOS_HORA)
    minuto = random.randint(0, 59)
    dt_inicio = fecha.replace(hour=hora, minute=minuto)

    # Tipo de vehículo
    nombres_vh = list(TIPOS_VEHICULO.keys())
    pesos_vh = [v["peso"] for v in TIPOS_VEHICULO.values()]
    pesos_vh = [p / sum(pesos_vh) for p in pesos_vh]
    tipo_vh = np.random.choice(nombres_vh, p=pesos_vh)
    vh = TIPOS_VEHICULO[tipo_vh]

    # Origen y destino (distintos)
    origen = random.choice(ZONAS)
    destino = random.choice([z for z in ZONAS if z != origen])

    # Distancia y duración
    distancia_km = round(np.random.lognormal(mean=1.8, sigma=0.6), 2)
    distancia_km = max(0.5, min(distancia_km, 50.0))
    velocidad_promedio = np.random.normal(25, 8)  # km/h en ciudad
    velocidad_promedio = max(10, velocidad_promedio)
    duracion_min = round((distancia_km / velocidad_promedio) * 60)
    duracion_min = max(3, duracion_min)
    dt_fin = dt_inicio + timedelta(minutes=int(duracion_min))

    # Tarifa (con algo de variabilidad por demanda)
    factor_demanda = 1.0
    if hora in range(7, 9) or hora in range(17, 20):
        factor_demanda = np.random.uniform(1.1, 1.5)  # precio pico
    tarifa = (vh["tarifa_base"] + distancia_km * vh["tarifa_km"]) * factor_demanda
    tarifa = round(tarifa / 100) * 100  # redondear a centenas

    # Calificación (con sesgo hacia positivo)
    calificacion = np.random.choice(
        [1, 2, 3, 4, 5],
        p=[0.03, 0.05, 0.12, 0.35, 0.45]
    )

    # Pasajeros
    n_pasajeros = 1 if tipo_vh == "Moto" else np.random.choice([1, 2, 3, 4], p=[0.55, 0.25, 0.15, 0.05])

    # Método de pago
    metodo_pago = random.choice(METODOS_PAGO)

    # Cancelación (5% de viajes)
    cancelado = np.random.choice([True, False], p=[0.05, 0.95])

    return {
        "viaje_id": f"VJ{idx:06d}",
        "fecha_inicio": dt_inicio,
        "fecha_fin": dt_fin if not cancelado else None,
        "hora": hora,
        "dia_semana": fecha.strftime("%A"),
        "mes": fecha.month,
        "zona_origen": origen,
        "zona_destino": destino,
        "tipo_vehiculo": tipo_vh,
        "distancia_km": distancia_km,
        "duracion_min": duracion_min if not cancelado else None,
        "tarifa_cop": tarifa if not cancelado else None,
        "metodo_pago": metodo_pago,
        "calificacion": calificacion if not cancelado else None,
        "n_pasajeros": n_pasajeros,
        "cancelado": cancelado,
        "factor_demanda": round(factor_demanda, 2),
    }


# ── Generar ─────────────────────────────────────────────────────────────────
print(f"Generando {N_VIAJES:,} viajes...")
viajes = [generar_viaje(i) for i in range(1, N_VIAJES + 1)]
df = pd.DataFrame(viajes)

# Introducir suciedad controlada para practicar limpieza
idx_nulos = np.random.choice(df.index, size=300, replace=False)
df.loc[idx_nulos[:100], "calificacion"] = np.nan
df.loc[idx_nulos[100:200], "zona_destino"] = np.nan
df.loc[idx_nulos[200:], "metodo_pago"] = np.nan

# Algunos outliers reales
df.loc[np.random.choice(df.index, 20), "distancia_km"] = np.random.uniform(80, 200, 20)
df.loc[np.random.choice(df.index, 15), "tarifa_cop"] = np.nan

df.to_csv("viajes_urbanos_2024.csv", index=False)
print(f"✅  Dataset guardado: viajes_urbanos_2024.csv")
print(f"    Filas: {len(df):,}  |  Columnas: {len(df.columns)}")
print(df.dtypes)
