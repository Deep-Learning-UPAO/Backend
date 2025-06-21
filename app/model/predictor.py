import tensorflow as tf
import numpy as np
from pathlib import Path

# Cargar el modelo una sola vez
model_path = Path(__file__).resolve().parent.parent.parent / "model.keras"
model = tf.keras.models.load_model(model_path)

def predecir(df):
    input_array = np.array(df).reshape(1, -1)

    # Obtener probabilidad de clase 1
    prob_clase_1 = model.predict(input_array)[0][0]
    prob_clase_0 = 1 - prob_clase_1

    # Aplicar umbral personalizado
    umbral = 0.605
    clase_predicha = int(prob_clase_1 >= umbral)

    # Obtener probabilidad de la clase predicha (como hacía scikit-learn)
    probabilidad = prob_clase_1 if clase_predicha == 1 else prob_clase_0
    riesgo_autismo = round(probabilidad * 100, 2)

    return {
        "clase_predicha": clase_predicha,
        "riesgo_autismo": riesgo_autismo,
    }
