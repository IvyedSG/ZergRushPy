import pygame
from config import ROJO, VERDE, DIFICULTADES

class Estructura(pygame.sprite.Sprite):
    def __init__(self, x, y, vida, dificultad):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("img/estructura.png"), (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vida = vida
        self.dificultad = dificultad

    def recibir_dano(self):
        dano_por_ataque = DIFICULTADES[self.dificultad]["dano_zerg"]
        self.vida -= dano_por_ataque
        if self.vida <= 0:
            self.kill()

    def dibujar_barra_vida(self, pantalla):
        pygame.draw.rect(pantalla, ROJO, (self.rect.x, self.rect.y - 10, 60, 5))
        pygame.draw.rect(pantalla, VERDE, (self.rect.x, self.rect.y - 10, 60 * (self.vida / DIFICULTADES[self.dificultad]["vida_estructura"]), 5))
