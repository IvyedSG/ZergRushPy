import pygame
import sys
from config import ANCHO, ALTO, NEGRO, BLANCO, VERDE, AZUL, ROJO, AMARILLO, FUENTE, FPS
from juego import Juego

def mostrar_pantalla(pantalla, mensaje, boton_texto):
    pantalla.fill(NEGRO)

    # Titulo grande y centrado
    texto_titulo = pygame.font.SysFont("Arial", 24).render(mensaje, True, BLANCO)
    pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, ALTO // 3 - texto_titulo.get_height() // 2))

    # Boton en color verde
    texto_boton = pygame.font.SysFont("Arial", 36).render(boton_texto, True, VERDE)
    pantalla.blit(texto_boton, (ANCHO // 2 - texto_boton.get_width() // 2, ALTO // 2))

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Pulsa Enter para continuar
                    esperando = False

def ejecutar_nivel(pantalla, reloj, dificultad, mensaje_nivel):
    juego = Juego(dificultad)
    mostrar_pantalla(pantalla, mensaje_nivel, "Presiona ENTER para comenzar")
    
    while True:
        reloj.tick(FPS)
        eventos = pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        juego.manejar_eventos(eventos)
        juego.actualizar()
        juego.dibujar(pantalla)
        pygame.display.flip()

        if len(juego.estructuras) == 0:
            return "perdido", juego.puntuacion
        if (pygame.time.get_ticks() - juego.tiempo_inicio) // 1000 >= juego.tiempo_total:
            return "ganado", juego.puntuacion

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Zerg Rush")
    reloj = pygame.time.Clock()

    # Pantalla inicial
    mostrar_pantalla(pantalla, "Zerg Rush", "Presiona ENTER para empezar")

    niveles = [
        ("Facil", "Nivel 1: Evita que destruyan tu base. ¡Haz click en ellos!"),
        ("Normal", "Nivel 2: En esta oportunidad hay más estructuras. ¡Cuídalas!"),
        ("Dificil", "Nivel 3: ¡Último desafío! Protege las estructuras a toda costa."),
    ]

    for idx, (dificultad, mensaje_nivel) in enumerate(niveles):
        resultado, puntuacion = ejecutar_nivel(pantalla, reloj, dificultad, mensaje_nivel)
        if resultado == "perdido":
            mostrar_pantalla(pantalla, f"¡Perdiste en el Nivel {idx + 1}! Puntuación: {puntuacion}", "Presiona ENTER para salir")
            pygame.quit()
            sys.exit()

        if idx < len(niveles) - 1:  # Si no es el último nivel
            mostrar_pantalla(pantalla, f"¡Ganaste el Nivel {idx + 1}!", "Presiona ENTER para continuar")

    # Pantalla de victoria
    mostrar_pantalla(pantalla, "¡Ganaste el juego!", "Presiona ENTER para salir")
    pygame.quit()

if __name__ == "__main__":
    main()