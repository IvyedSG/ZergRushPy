ANCHO, ALTO = 800, 600
FPS = 60

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)

import pygame
pygame.init()
FUENTE = pygame.font.SysFont("Arial", 24)

FONDO_IMG = pygame.image.load("img/map1.png")

DIFICULTADES = {
    "Facil": {
        "vida_estructura": 100,
        "vida_zerg": 10,  
        "velocidad": 1,
        "frecuencia": 2,
        "velocidad_ataque": 1, 
        "dano_zerg": 2 
    },
    "Normal": {
        "vida_estructura": 150,
        "vida_zerg": 15,  
        "velocidad": 1.5,
        "frecuencia": 1.5,
        "velocidad_ataque": 0.8,
        "dano_zerg": 3
    },
    "Dificil": {
        "vida_estructura": 200,
        "vida_zerg": 20, 
        "velocidad": 2,
        "frecuencia": 1,
        "velocidad_ataque": 0.5,
        "dano_zerg": 5
    },
    "Extremo": {
        "vida_estructura": 250,
        "vida_zerg": 25, 
        "velocidad": 2.5,
        "frecuencia": 0.8,
        "velocidad_ataque": 0.3,
        "dano_zerg": 7
    },
    "Imposible": {
        "vida_estructura": 300,
        "vida_zerg": 30, 
        "velocidad": 3,
        "frecuencia": 0.5,
        "velocidad_ataque": 0.2,
        "dano_zerg": 10
    }
}
