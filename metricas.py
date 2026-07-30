import os
import csv
from datetime import datetime


def calcular_costo(tokens_entrada, tokens_salida):
    """Calcula el costo estimado en USD según los tokens usados."""
    precio_entrada = 0.15 / 1_000_000
    precio_salida = 0.60 / 1_000_000
    return (tokens_entrada * precio_entrada) + (tokens_salida * precio_salida)


def guardar_metricas(latencia, tokens_entrada, tokens_salida, tokens_total, costo, archivo="metrics.csv"):
    """Guarda una fila de métricas en el archivo CSV, creando el encabezado si no existe."""
    existe = os.path.exists(archivo)
    with open(archivo, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["timestamp", "latencia_seg", "tokens_entrada", "tokens_salida", "tokens_total", "costo_usd"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            f"{latencia:.2f}",
            tokens_entrada,
            tokens_salida,
            tokens_total,
            f"{costo:.6f}"
        ])