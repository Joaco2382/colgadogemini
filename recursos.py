# recursos.py
import os
import requests
from config import RUTA_IMAGENES, API_KEY_PIXABAY

def descargar_imagen_de_pixabay(palabra):
    """Descarga una imagen relacionada con la palabra desde Pixabay."""
    try:
        url = f"https://pixabay.com/api/?key={API_KEY_PIXABAY}&q={palabra}&image_type=photo"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data["totalHits"] > 0:
            img_url = data["hits"][0]["webformatURL"]
            img_data = requests.get(img_url).content
            ruta_guardado = os.path.join(RUTA_IMAGENES, f"{palabra}.jpg")
            with open(ruta_guardado, "wb") as f:
                f.write(img_data)
            return ruta_guardado
        else:
            print(f"No se encontraron imágenes para '{palabra}' en Pixabay.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen para '{palabra}' desde Pixabay: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al descargar la imagen para '{palabra}' desde Pixabay: {e}")
        return None

def obtener_ruta_imagen(palabra):
    """
    Obtiene la ruta de la imagen para una palabra.

    Primero busca una imagen generada previamente en la carpeta de imágenes.
    Si no la encuentra, intenta descargar una de Pixabay.
    """
    ruta_local = os.path.join(RUTA_IMAGENES, f"{palabra}.jpg")
    if os.path.exists(ruta_local):
        return ruta_local
    else:
        print(f"No se encontró una imagen generada para '{palabra}'. Intentando descargar de Pixabay...")
        return descargar_imagen_de_pixabay(palabra)

# Asegurarse de que el directorio de imágenes exista
os.makedirs(RUTA_IMAGENES, exist_ok=True)