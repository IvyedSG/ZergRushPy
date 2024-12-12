import pygame
import sys
from config import ANCHO, ALTO, NEGRO, BLANCO, VERDE, AZUL, ROJO, AMARILLO, FUENTE, FPS
from juego import Juego


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Zerg Rush")
    reloj = pygame.time.Clock()
    menu_activo = True

    while menu_activo:
        pantalla.fill(NEGRO)
        texto_titulo = FUENTE.render("Selecciona Dificultad", True, BLANCO)
        texto_facil = FUENTE.render("1. Facil", True, VERDE)
        texto_normal = FUENTE.render("2. Normal", True, AZUL)
        texto_dificil = FUENTE.render("3. Dificil", True, ROJO)
        texto_extremo = FUENTE.render("4. Extremo", True, AMARILLO)
        texto_imposible = FUENTE.render("5. Imposible", True, ROJO)

        pantalla.blit(texto_titulo, (ANCHO // 2 - texto_titulo.get_width() // 2, 50))
        pantalla.blit(texto_facil, (ANCHO // 2 - texto_facil.get_width() // 2, 150))
        pantalla.blit(texto_normal, (ANCHO // 2 - texto_normal.get_width() // 2, 200))
        pantalla.blit(texto_dificil, (ANCHO // 2 - texto_dificil.get_width() // 2, 250))
        pantalla.blit(texto_extremo, (ANCHO // 2 - texto_extremo.get_width() // 2, 300))
        pantalla.blit(texto_imposible, (ANCHO // 2 - texto_imposible.get_width() // 2, 350))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    dificultad = "Facil"
                elif evento.key == pygame.K_2:
                    dificultad = "Normal"
                elif evento.key == pygame.K_3:
                    dificultad = "Dificil"
                elif evento.key == pygame.K_4:
                    dificultad = "Extremo"
                elif evento.key == pygame.K_5:
                    dificultad = "Imposible"
                else:
                    continue

                juego = Juego(dificultad)
                while True:
                    reloj.tick(FPS)
                    eventos = pygame.event.get()
                    juego.manejar_eventos(eventos)
                    juego.actualizar()
                    juego.dibujar(pantalla)
                    pygame.display.flip()

if __name__ == "__main__":
    main()