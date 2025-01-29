# main.py
import pygame
from logica import JuegoColgado
from interfaz import Interfaz
import os

def main():
    """Función principal para ejecutar el juego."""

    categoria = "geek"  # o "gamer", según la preferencia
    juego = JuegoColgado(categoria)
    interfaz = Interfaz(juego)
    interfaz.correr()

    # Reiniciar el juego si el jugador lo desea
    while True:
        # Esperar a que el jugador presione espacio para reiniciar
        esperando_reinicio = True
        while esperando_reinicio:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        esperando_reinicio = False

        # Reiniciar el juego
        juego = JuegoColgado(categoria)
        interfaz = Interfaz(juego)
        interfaz.correr()

if __name__ == "__main__":
    main()