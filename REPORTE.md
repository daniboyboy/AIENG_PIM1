# Reporte Técnico — Asistente de Soporte al Cliente con IA

## 1. Arquitectura

El proyecto sigue una estructura modular con responsabilidades separadas:

- **main.py** — orquesta el flujo completo: recibe la pregunta, invoca al asistente, mide la latencia, extrae la respuesta y las métricas, y las guarda.
- **asistente.py** — contiene la lógica de conexión con la API de OpenAI y el system prompt con la técnica de few-shot.
- **metricas.py** — funciones para calcular el costo estimado y guardar las métricas en un archivo CSV.
- **test_asistente.py** — test automatizado que verifica que la salida respeta el contrato definido.

El flujo de una ejecución es: pregunta → llamada al modelo (con system prompt few-shot) → respuesta JSON estructurada → cálculo de métricas → registro en `metrics.csv`.

## 2. Contrato de salida

Se definió un contrato estable antes de implementar la lógica. Cada respuesta es un objeto JSON con tres campos:

- **answer**: respuesta redactada para el cliente.
- **confidence**: nivel de confianza del modelo (`alta`, `media` o `baja`).
- **actions**: lista de 1 a 3 acciones recomendadas.

El formato JSON se eligió porque la salida está pensada para ser consumida por sistemas posteriores (downstream), que requieren datos estructurados en lugar de texto libre.

## 3. Técnica de prompt engineering: Few-shot

Se eligió **few-shot learning**: el system prompt incluye dos ejemplos resueltos (pregunta → JSON esperado) que sirven de molde al modelo.

**Justificación:** la prioridad del asistente es que la salida tenga un formato consistente y bien estructurado, ya que alimenta sistemas downstream. Few-shot destaca en tareas sensibles al formato, porque el modelo aprende el patrón por imitación de los ejemplos. Se verificó que, ante preguntas no incluidas en los ejemplos, el modelo mantiene el formato y la escala de confianza correctamente.

Se descartaron las alternativas: **Chain-of-Thought** es más útil cuando lo crítico es el razonamiento multi-paso, no el formato; **Self-consistency** implica múltiples llamadas y mayor costo, sin aportar al objetivo de consistencia de formato.

## 4. Métricas

Por cada ejecución se registran en `metrics.csv`: marca de tiempo, latencia (segundos), tokens de entrada/salida/total y costo estimado en USD.

Valores de ejemplo observados:
- Latencia: ~2.5 a 3.9 segundos por consulta.
- Tokens: ~385 de entrada (el system prompt con ejemplos es fijo) y ~110-125 de salida.
- Costo estimado: ~0.00013 USD por consulta (modelo gpt-4o-mini).

El costo de entrada es fijo porque el system prompt no cambia; el de salida varía según la respuesta.

## 5. Trade-offs y decisiones

- **Confidence como palabras (alta/media/baja) en vez de número:** se priorizó la legibilidad humana. Como contrapartida, se pierde la precisión que daría un número de 0 a 1 para filtrar por umbrales automáticamente.
- **Temperature baja (0.3):** se busca consistencia y precisión sobre creatividad, apropiado para un contexto de soporte.
- **Test con llamada real a la API:** prueba el sistema completo de punta a punta, pero consume tokens y depende de conexión. Un test sin llamada (mock) sería más rápido y gratuito, pero probaría solo la lógica aislada.
- **metrics.csv incluido en el repositorio:** permite al evaluador ver métricas de ejemplo sin ejecutar el código.

## 6. Posibles mejoras

- Recibir la pregunta de forma dinámica (por entrada de teclado o argumento) en lugar de fija en el código.
- Añadir un módulo de seguridad para manejar entradas adversariales (bonus opcional).
- Migrar el system prompt específico a un archivo de configuración para facilitar ajustes.