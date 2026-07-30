import json
import time
from asistente import consultar_asistente
from metricas import calcular_costo, guardar_metricas

# --- Pregunta de ejemplo ---
pregunta_cliente = "No me llegó el correo de confirmación después de registrarme. ¿Qué hago?"

# --- Llamada al asistente (con cronómetro para la latencia) ---
inicio = time.time()
response = consultar_asistente(pregunta_cliente)
fin = time.time()
latencia = fin - inicio

# --- Extraer respuesta y tokens ---
resultado = json.loads(response.choices[0].message.content)
tokens_entrada = response.usage.prompt_tokens
tokens_salida = response.usage.completion_tokens
tokens_total = response.usage.total_tokens

# --- Calcular costo ---
costo = calcular_costo(tokens_entrada, tokens_salida)

# --- Mostrar resultados ---
print("--- PREGUNTA DEL CLIENTE ---")
print(pregunta_cliente)
print("\n--- RESPUESTA DEL ASISTENTE (JSON) ---")
print(json.dumps(resultado, indent=2, ensure_ascii=False))

print("\n--- MÉTRICAS ---")
print(f"Latencia: {latencia:.2f} segundos")
print(f"Tokens (entrada/salida/total): {tokens_entrada} / {tokens_salida} / {tokens_total}")
print(f"Costo estimado: ${costo:.6f} USD")

# --- Guardar métricas ---
guardar_metricas(latencia, tokens_entrada, tokens_salida, tokens_total, costo)
print("\nMétricas guardadas en metrics.csv")