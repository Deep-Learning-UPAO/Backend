# pylint: disable=E1101

import tensorflow as tf
import numpy as np
from pathlib import Path

# Cargar el modelo una sola vez
model_path = Path(__file__).resolve().parent.parent.parent / "model.keras"
model = tf.keras.models.load_model(model_path)

def predecir(df):

    # Asegurarse de que df sea un arreglo de NumPy (si es un DataFrame de pandas)
    input_array = np.array(df).reshape(1, -1)

    # Obtener la probabilidad de clase 1
    prob_clase_1 = model.predict(input_array)[0][0]
    prob_clase_0 = 1 - prob_clase_1

    # Convertir probabilidad a float para evitar problemas de serialización
    prob_clase_1 = float(prob_clase_1)
    prob_clase_0 = float(prob_clase_0)

    # Aplicar umbral personalizado
    umbral = 0.580
    clase_predicha = int(prob_clase_1 >= umbral)

    # Convertir probabilidad a porcentaje (solo la de la clase predicha)
    probabilidad = prob_clase_1 if clase_predicha == 1 else prob_clase_0
    riesgo_autismo = round(probabilidad * 100, 2)
    # Convertir el riesgo de autismo a float también para evitar problemas
    riesgo_autismo = float(riesgo_autismo)

    return {
        "clase_predicha": clase_predicha,
        "riesgo_autismo": riesgo_autismo,
    }
