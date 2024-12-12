import pygame
import random
from enemigo import Enemigo
from estructura import Estructura
from config import ANCHO, ALTO, FONDO_IMG, BLANCO, FUENTE, DIFICULTADES

class Juego:
    def __init__(self, dificultad, nivel=1):
        self.dificultad = dificultad
        self.nivel = nivel
        self.config = DIFICULTADES[dificultad]
        self.enemigos = pygame.sprite.Group()
        self.estructuras = pygame.sprite.Group()
        self.tiempo_spawn = 0
        self.puntuacion = 0
        self.tiempo_total = 30 + (nivel - 1) * 10  # Incrementa el tiempo con el nivel
        self.tiempo_inicio = pygame.time.get_ticks()
        self.crear_estructuras()

    def crear_estructuras(self):
        num_estructuras = self.nivel  # Número de estructuras depende del nivel
        for i in range(num_estructuras):
            x = ANCHO // (num_estructuras + 1) * (i + 1)
            y = ALTO // 2
            estructura = Estructura(x, y, self.config["vida_estructura"], self.dificultad)
            self.estructuras.add(estructura)

    def generar_enemigos(self):
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_spawn > self.config["frecuencia"] * 1000 / self.nivel:  # Más enemigos en niveles altos
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
            enemigo = Enemigo(x, y, self.config["velocidad"] + self.nivel * 0.5, self.config["vida_zerg"] + self.nivel * 5, objetivo, self.dificultad)
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
            mensaje = f"¡Ganaste el Nivel {self.nivel}!"
        else:
            mensaje = "¡Perdiste!"
        texto_final = FUENTE.render(mensaje, True, (255, 0, 0))
        pantalla.blit(texto_final, (ANCHO // 2 - texto_final.get_width() // 2, ALTO // 2))
        pygame.display.flip()
        pygame.time.wait(3000)

        if len(self.estructuras) > 0 and self.nivel < 3:
            self.nivel += 1
            self.reiniciar_nivel(pantalla)
        else:
            self.mostrar_victoria_o_derrota(pantalla)

    def mostrar_victoria_o_derrota(self, pantalla):
        if len(self.estructuras) > 0:
            mensaje = "¡Ganaste el juego!"
        else:
            mensaje = "¡Perdiste!"  # Si pierdes en cualquier nivel

        texto_final = FUENTE.render(mensaje, True, (0, 255, 0) if len(self.estructuras) > 0 else (255, 0, 0))
        pantalla.fill((0, 0, 0))
        pantalla.blit(texto_final, (ANCHO // 2 - texto_final.get_width() // 2, ALTO // 2))
        pygame.display.flip()
        pygame.time.wait(5000)
        pygame.quit()
        exit()

    def reiniciar_nivel(self, pantalla):
        self.enemigos.empty()
        self.estructuras.empty()
        self.tiempo_spawn = 0
        self.tiempo_inicio = pygame.time.get_ticks()
        self.crear_estructuras()
        self.puntuacion = 0
        pantalla.fill((0, 0, 0))
        mensaje = FUENTE.render(f"Nivel {self.nivel} comienza ahora!", True, (255, 255, 0))
        pantalla.blit(mensaje, (ANCHO // 2 - mensaje.get_width() // 2, ALTO // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
