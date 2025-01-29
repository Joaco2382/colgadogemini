# config.py

PALABRAS_GEEK = [
    "python", "javascript", "codigo", "bug", "hacker",
    "servidor", "internet", "linux", "consola", "framework"
]

PALABRAS_GAMER = [
    "minecraft", "fortnite", "gamer", "joystick", "streaming",
    "esports", "level", "pokemon", "nintendo", "playstation"
]

RUTA_IMAGENES = "recursos/imagenes/"
RUTA_SONIDOS = "recursos/sonidos/"  # No se usaran sonidos

class Configuracion:
    def __init__(self):
        # Configuracion de Pygame
        self.ANCHO = 800
        self.ALTO = 600
        self.FPS = 60

        # Colores
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.ROJO = (255, 0, 0)
        self.VERDE = (0, 255, 0)
        self.AZUL = (0, 0, 255)

        # API Key de Pixabay (reemplaza con tu clave)
        self.API_KEY_PIXABAY = "48525779-33ad97c292bfad17a526907ea"

