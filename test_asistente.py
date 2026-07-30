import json
from asistente import consultar_asistente


def test_contrato_json():
    """Verifica que la respuesta del asistente respeta el contrato de salida."""
    # Enviamos una pregunta de prueba
    pregunta = "¿Cómo actualizo mi método de pago?"
    response = consultar_asistente(pregunta)
    resultado = json.loads(response.choices[0].message.content)

    # Afirmamos que existen los tres campos del contrato
    assert "answer" in resultado, "Falta el campo 'answer'"
    assert "confidence" in resultado, "Falta el campo 'confidence'"
    assert "actions" in resultado, "Falta el campo 'actions'"

    # Afirmamos que confidence es uno de los tres valores permitidos
    assert resultado["confidence"] in ["alta", "media", "baja"], "confidence tiene un valor no permitido"

    # Afirmamos que actions es una lista
    assert isinstance(resultado["actions"], list), "'actions' debería ser una lista"

    print("✅ Test superado: el JSON respeta el contrato.")


# Ejecutar el test al correr el archivo
if __name__ == "__main__":
    test_contrato_json()