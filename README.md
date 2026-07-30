# Asistente de Soporte al Cliente con IA

Prototipo de un asistente que responde preguntas de soporte al cliente usando la API de OpenAI, devolviendo una respuesta estructurada en JSON y registrando métricas de cada ejecución.

## ¿Qué hace?

Recibe la pregunta de un cliente y devuelve un objeto JSON con:
- **answer**: la respuesta redactada para el cliente.
- **confidence**: nivel de confianza del modelo (alta, media o baja).
- **actions**: lista de acciones recomendadas.

Además, por cada ejecución registra métricas (latencia, tokens y costo estimado) en `metrics.csv`.

## Requisitos

- Python 3.10 o superior
- Una clave de API de OpenAI

## Instalación

1. Clonar el repositorio:

       git clone https://github.com/daniboyboy/AIENG_PIM1.git
       cd AIENG_PIM1

2. Crear y activar un entorno virtual:

       py -m venv venv
       .\venv\Scripts\Activate.ps1

3. Instalar las dependencias:

       pip install -r requirements.txt

4. Configurar la clave de API. Copiar `.env.example` a un archivo `.env` y añadir tu clave real:

       OPENAI_API_KEY=tu_clave_aqui

## Uso

Ejecutar el asistente:

       python main.py

Ejecutar el test:

       python test_asistente.py

## Estructura del proyecto

- `main.py` — orquesta el flujo: recibe la pregunta, llama al asistente, muestra el resultado y guarda las métricas.
- `asistente.py` — lógica de conexión con OpenAI y el system prompt (few-shot).
- `metricas.py` — cálculo del costo y guardado de métricas en CSV.
- `test_asistente.py` — test automatizado que verifica el contrato de salida.