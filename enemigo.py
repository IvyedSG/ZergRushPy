import pygame
import math
from config import ROJO, VERDE, DIFICULTADES

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad, vida, objetivo, dificultad):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("img/enemigo.png"), (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad = velocidad
        self.vida = vida
        self.objetivo = objetivo
        self.dificultad = dificultad
        self.tiempo_ultimo_ataque = pygame.time.get_ticks()  

    def update(self):
        
        dx, dy = self.objetivo.rect.centerx - self.rect.centerx, self.objetivo.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)
        if distancia == 0:
            return  

      
        distancia_minima = 30
        if distancia > distancia_minima:
            dx, dy = dx / distancia, dy / distancia
            self.rect.x += dx * self.velocidad
            self.rect.y += dy * self.velocidad

     
        if distancia <= distancia_minima:
            ahora = pygame.time.get_ticks()
            if ahora - self.tiempo_ultimo_ataque > DIFICULTADES[self.dificultad]["velocidad_ataque"] * 1000:
                self.objetivo.recibir_dano()
                self.tiempo_ultimo_ataque = ahora

    def recibir_dano(self):
        self.vida -= 5 
        if self.vida <= 0:
            self.kill()

    def dibujar_barra_vida(self, pantalla):
        pygame.draw.rect(pantalla, ROJO, (self.rect.x, self.rect.y - 10, 40, 5))
        pygame.draw.rect(pantalla, VERDE, (self.rect.x, self.rect.y - 10, 40 * (self.vida / DIFICULTADES[self.dificultad]["vida_zerg"]), 5))
