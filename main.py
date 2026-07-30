import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Cargar la clave desde .env
load_dotenv()

# Crear el cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- System prompt con few-shot ---
SYSTEM_PROMPT = """
Eres un asistente de soporte al cliente para una plataforma SaaS. Tu trabajo es ayudar a los agentes de soporte a responder las preguntas de los clientes.

Por cada pregunta que recibas, responde SIEMPRE con un objeto JSON válido que contenga exactamente estos tres campos:
- "answer": la respuesta redactada para el cliente, en segunda persona, tal cual como se envió.
- "confidence": uno de estos tres valores exactos: "alta", "media" o "baja".
- "actions": una lista de 1 a 3 acciones concretas recomendadas.

Responde ÚNICAMENTE con el JSON, sin texto adicional.

Aquí tienes algunos ejemplos:

Pregunta: "No puedo pagar mi suscripción, la plataforma me da un error al meter la tarjeta."
Respuesta:
{
  "answer": "Este error suele deberse a los datos de la tarjeta o a la conexión. Verifica que los números estén bien ingresados y que tu conexión sea estable, y vuelve a intentarlo.",
  "confidence": "media",
  "actions": ["Esperar unos minutos y reintentar el pago", "Si el error persiste, contactar a un asesor"]
}

Pregunta: "¿Cómo cambio la contraseña de mi cuenta?"
Respuesta:
{
  "answer": "Para cambiar tu contraseña, ingresa a tu cuenta y ve a Configuración → Seguridad → Cambiar contraseña. Si olvidaste la actual, usa la opción '¿Olvidaste tu contraseña?' en la pantalla de inicio de sesión para recibir un enlace de recuperación por correo.",
  "confidence": "alta",
  "actions": ["Guiar al cliente al menú de Seguridad de su cuenta", "Si no recuerda su contraseña actual, enviar enlace de recuperación por correo"]
}
"""

# --- Pregunta de ejemplo (por ahora, fija en el código) ---
pregunta_cliente = "No me llegó el correo de confirmación después de registrarme. ¿Qué hago?"

# --- Llamada a OpenAI ---
response = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": pregunta_cliente}
    ],
    temperature=0.3
)

# --- Extraer y mostrar el resultado ---
resultado = json.loads(response.choices[0].message.content)

print("--- PREGUNTA DEL CLIENTE ---")
print(pregunta_cliente)
print("\n--- RESPUESTA DEL ASISTENTE (JSON) ---")
print(json.dumps(resultado, indent=2, ensure_ascii=False))