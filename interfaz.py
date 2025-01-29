# interfaz.py
import pygame
from config import ANCHO, ALTO, FPS, BLANCO, NEGRO, ROJO, VERDE, AZUL
from recursos import obtener_ruta_imagen

class Interfaz:
    def __init__(self, juego):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Juego del Colgado")
        self.reloj = pygame.time.Clock()
        self.juego = juego
        self.fuente = pygame.font.Font(None, 48)
        self.imagenes_ahorcado = self.cargar_imagenes_ahorcado()
        self.imagen_resultado = None
        self.input_activo = False  # Para agregar palabras nuevas
        self.input_texto = ""
        self.mostrar_intro()

    def cargar_imagenes_ahorcado(self):
        """Carga las imágenes del ahorcado."""
        imagenes = []
        for i in range(7):
            try:
                imagen = pygame.image.load(f"recursos/ahorcado/ahorcado_{i}.png")
                imagenes.append(imagen)
            except pygame.error:
                print(f"No se pudo cargar la imagen ahorcado_{i}.png")
        return imagenes

    def mostrar_intro(self):
        """Muestra una pantalla de inicio antes de comenzar el juego."""
        self.pantalla.fill(BLANCO)
        titulo = self.fuente.render("El Juego del Colgado", True, NEGRO)
        instrucciones = self.fuente.render("Presiona ESPACIO para jugar", True, NEGRO)
        titulo_rect = titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        instrucciones_rect = instrucciones.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))
        self.pantalla.blit(titulo, titulo_rect)
        self.pantalla.blit(instrucciones, instrucciones_rect)
        pygame.display.flip()

        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        esperando = False

    def manejar_eventos(self):
        """Maneja los eventos del usuario (teclado, mouse)."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.juego.terminado = True
            elif evento.type == pygame.KEYDOWN:
                if self.input_activo:
                    if evento.key == pygame.K_RETURN:
                        self.juego.agregar_palabra(self.input_texto)
                        print(f"Palabra agregada: {self.input_texto}")
                        self.input_texto = ""
                        self.input_activo = False
                    elif evento.key == pygame.K_BACKSPACE:
                        self.input_texto = self.input_texto[:-1]
                    else:
                        self.input_texto += evento.unicode
                elif evento.unicode.isalpha() and not self.juego.terminado:
                    self.juego.adivinar_letra(evento.unicode)

                    if self.juego.terminado:
                        # Cargar imagen
                        ruta_imagen = obtener_ruta_imagen(self.juego.palabra)
                        if ruta_imagen:
                            try:
                                self.imagen_resultado = pygame.image.load(ruta_imagen)
                            except pygame.error:
                                print(f"No se pudo cargar la imagen {ruta_imagen}")
                                self.imagen_resultado = None
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                # Comprobar si se hizo clic en el botón "Agregar palabra"
                if ANCHO // 2 - 100 <= evento.pos[0] <= ANCHO // 2 + 100 and \
                   ALTO - 160 <= evento.pos[1] <= ALTO - 120:
                    self.input_activo = True

    def actualizar(self):
        """Actualiza la lógica del juego."""
        pass

    def dibujar_boton(self, texto, x, y, ancho, alto, color_activo, color_inactivo, accion=None):
        """Dibuja un botón en la pantalla."""
        mouse = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()

        if x + ancho > mouse[0] > x and y + alto > mouse[1] > y:
            pygame.draw.rect(self.pantalla, color_activo, (x, y, ancho, alto))
            if clic[0] == 1 and accion is not None:
                accion()
        else:
            pygame.draw.rect(self.pantalla, color_inactivo, (x, y, ancho, alto))

        texto_boton = self.fuente.render(texto, True, NEGRO)
        texto_rect = texto_boton.get_rect(center=(x + ancho // 2, y + alto // 2))
        self.pantalla.blit(texto_boton, texto_rect)

    def dibujar(self):
        """Dibuja los elementos en la pantalla."""
        self.pantalla.fill(BLANCO)

        # Dibujar la palabra oculta
        texto_palabra = self.fuente.render(self.juego.obtener_palabra_oculta(), True, NEGRO)
        palabra_rect = texto_palabra.get_rect(center=(ANCHO // 2, ALTO - 100))
        self.pantalla.blit(texto_palabra, palabra_rect)

        # Dibujar la imagen del ahorcado
        if not self.juego.terminado:
          # Si el juego no ha terminado, dibujar la imagen del ahorcado actual
          if self.juego.intentos_restantes < len(self.imagenes_ahorcado):
              imagen_ahorcado = self.imagenes_ahorcado[6 - self.juego.intentos_restantes]
              imagen_ahorcado = pygame.transform.scale(imagen_ahorcado, (300, 300))
              self.pantalla.blit(imagen_ahorcado, (ANCHO // 2 - 150, 50))
        else:
          # Si el juego ha terminado, mostrar la imagen relacionada a la palabra
          if self.imagen_resultado:
            imagen_escalada = pygame.transform.scale(self.imagen_resultado, (200, 200))
            imagen_rect = imagen_escalada.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
            self.pantalla.blit(imagen_escalada, imagen_rect)

        # Dibujar el estado del juego (ganado o perdido)
        if self.juego.terminado:
            if self.juego.ganado:
                texto_resultado = self.fuente.render("¡Ganaste!", True, VERDE)
            else:
                texto_resultado = self.fuente.render(f"Perdiste. La palabra era: {self.juego.palabra}", True, ROJO)
            resultado_rect = texto_resultado.get_rect(center=(ANCHO // 2, ALTO // 2 + 100))
            self.pantalla.blit(texto_resultado, resultado_rect)

            # Texto para jugar de nuevo
            texto_reinicio = self.fuente.render("Presiona ESPACIO para jugar de nuevo", True, AZUL)
            reinicio_rect = texto_reinicio.get_rect(center=(ANCHO // 2, ALTO - 50))
            self.pantalla.blit(texto_reinicio, reinicio_rect)
        else:
            # Botón para agregar palabra
            self.dibujar_boton("Agregar Palabra", ANCHO // 2 - 100, ALTO - 160, 200, 40, AZUL, (0, 0, 180), accion=None)

            # Input para agregar palabra
            if self.input_activo:
                input_rect = pygame.Rect(ANCHO // 2 - 150, ALTO - 220, 300, 40)
                pygame.draw.rect(self.pantalla, AZUL, input_rect, 2)
                texto_input = self.fuente.render(self.input_texto, True, NEGRO)
                self.pantalla.blit(texto_input, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.flip()

    def correr(self):
        """Bucle principal del juego."""
        while not self.juego.terminado:
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()
            self.reloj.tick(FPS)

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

        pygame.quit()