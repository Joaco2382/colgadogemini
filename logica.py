# logica.py
import random
from config import PALABRAS_GEEK, PALABRAS_GAMER
from recursos import obtener_ruta_imagen

class JuegoColgado:
    def __init__(self, categoria):
        self.palabra = self.elegir_palabra(categoria).upper()
        self.categoria = categoria  # Agregar la categoría
        self.letras_adivinadas = set()
        self.intentos_restantes = 6
        self.imagen_actual = ""
        self.terminado = False
        self.ganado = False

    def elegir_palabra(self, categoria):
        """Elige una palabra aleatoria según la categoría."""
        if categoria == "geek":
            return random.choice(PALABRAS_GEEK)
        elif categoria == "gamer":
            return random.choice(PALABRAS_GAMER)
        else:
            raise ValueError("Categoría no válida")

    def adivinar_letra(self, letra):
        """Adivina una letra y actualiza el estado del juego."""
        letra = letra.upper()
        if letra in self.letras_adivinadas or self.terminado:
            return

        self.letras_adivinadas.add(letra)
        if letra not in self.palabra:
            self.intentos_restantes -= 1

        self.verificar_estado()

    def verificar_estado(self):
        """Verifica si el juego ha terminado (ganado o perdido)."""
        if self.intentos_restantes <= 0:
            self.terminado = True
            self.ganado = False
        elif all(letra in self.letras_adivinadas for letra in self.palabra):
            self.terminado = True
            self.ganado = True

    def obtener_palabra_oculta(self):
        """Devuelve la palabra oculta con guiones bajos para las letras no adivinadas."""
        palabra_oculta = ""
        for letra in self.palabra:
            if letra in self.letras_adivinadas:
                palabra_oculta += letra + " "
            else:
                palabra_oculta += "_ "
        return palabra_oculta.strip()

    def obtener_imagen_ahorcado(self):
        """Devuelve la ruta de la imagen del ahorcado actual."""
        return f"recursos/ahorcado/ahorcado_{6 - self.intentos_restantes}.png"

    def agregar_palabra(self, palabra):
        """Agrega una nueva palabra a la lista de palabras de la categoría actual."""
        palabra = palabra.lower()  # Convertir a minúsculas para consistencia
        if self.categoria == "geek":
            if palabra not in PALABRAS_GEEK:
                PALABRAS_GEEK.append(palabra)
        elif self.categoria == "gamer":
            if palabra not in PALABRAS_GAMER:
                PALABRAS_GAMER.append(palabra)