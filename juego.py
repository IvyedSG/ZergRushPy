import pygame
import random
from enemigo import Enemigo
from estructura import Estructura
from config import ANCHO, ALTO, FONDO_IMG, BLANCO, FUENTE, DIFICULTADES

class Juego:
    def __init__(self, dificultad):
        self.dificultad = dificultad
        self.config = DIFICULTADES[dificultad]
        self.enemigos = pygame.sprite.Group()
        self.estructuras = pygame.sprite.Group()
        self.tiempo_spawn = 0
        self.puntuacion = 0
        self.tiempo_total = 30
        self.tiempo_inicio = pygame.time.get_ticks()
        self.crear_estructuras()

    def crear_estructuras(self):
        for i in range(3):
            x = ANCHO // 4 * (i + 1)
            y = ALTO // 2
            estructura = Estructura(x, y, self.config["vida_estructura"], self.dificultad)
            self.estructuras.add(estructura)

    def generar_enemigos(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_spawn > self.config["frecuencia"] * 1000:
            while True:
                lado = random.choice(["izquierda", "derecha", "arriba", "abajo"])
                enemigo_ancho, enemigo_alto = 40, 40 
                if lado == "izquierda":
                    x, y = -enemigo_ancho, random.randint(0, ALTO - enemigo_alto)
                elif lado == "derecha":
                    x, y = ANCHO - 1, random.randint(0, ALTO - enemigo_alto)
                elif lado == "arriba":
                    x, y = random.randint(0, ANCHO - enemigo_ancho), -enemigo_alto
                elif lado == "abajo":
                    x, y = random.randint(0, ANCHO - enemigo_ancho), ALTO - 1

                if not any(estructura.rect.collidepoint(x, y) for estructura in self.estructuras):
                    break

            objetivo = random.choice(self.estructuras.sprites())
            enemigo = Enemigo(x, y, self.config["velocidad"], self.config["vida_zerg"], objetivo, self.dificultad)
            self.enemigos.add(enemigo)
            self.tiempo_spawn = ahora

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                clic_pos = pygame.mouse.get_pos()
                for enemigo in self.enemigos:
                    if enemigo.rect.collidepoint(clic_pos):
                        enemigo.recibir_dano()
                        if enemigo.vida <= 0:
                            self.puntuacion += 10

    def actualizar(self):
        self.enemigos.update()
        self.generar_enemigos()

    def dibujar(self, pantalla):
        pantalla.blit(FONDO_IMG, (0, 0))
        self.estructuras.draw(pantalla)
        self.enemigos.draw(pantalla)

        for enemigo in self.enemigos:
            enemigo.dibujar_barra_vida(pantalla)
        for estructura in self.estructuras:
            estructura.dibujar_barra_vida(pantalla)

        tiempo_restante = self.tiempo_total - (pygame.time.get_ticks() - self.tiempo_inicio) // 1000
        texto_puntuacion = FUENTE.render(f"Puntuación: {self.puntuacion}", True, BLANCO)
        texto_tiempo = FUENTE.render(f"Tiempo: {tiempo_restante}s", True, BLANCO)
        pantalla.blit(texto_puntuacion, (10, 10))
        pantalla.blit(texto_tiempo, (10, 40))

        if tiempo_restante <= 0 or len(self.estructuras) == 0:
            self.mostrar_fin_juego(pantalla)

    def mostrar_fin_juego(self, pantalla):
        if len(self.estructuras) > 0:
            mensaje = "¡Ganaste!"
        else:
            mensaje = "¡Perdiste!"
        texto_final = FUENTE.render(f"{mensaje} Puntuación: {self.puntuacion}", True, (255, 0, 0))
        pantalla.blit(texto_final, (ANCHO // 2 - texto_final.get_width() // 2, ALTO // 2))
        pygame.display.flip()
        pygame.time.wait(5000)
        pygame.quit()
        exit()
