import pygame
import sys
from scripts.jogador import Jogador
from scripts.plataforma import Plataforma

pygame.init()

tamanhoTela = [800,600]

tela = pygame.display.set_mode((tamanhoTela))
pygame.display.set_caption("ComodoOo")

clock = pygame.time.Clock()
AZUL = (100, 180, 255)
VERDE = (80, 200, 100)
VERMELHO = (220, 60, 60)

# Jogador
jogador = Jogador(tela, 100, 450)

# Plataformas
plataformas = [
    Plataforma(0, 550, 800, 50),
    Plataforma(300, 450, 200, 30),
    Plataforma(600, 350, 150, 30),
]

while True:

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    jogador.atualizar(plataformas)

    # Desenhar fundo
    tela.fill(AZUL)

    # Desenhar plataformas
    for plataforma in plataformas:
        plataforma.desenhar(tela)

    # Desenhar jogador
    jogador.desenhar()

    clock.tick(60)
    pygame.display.flip()
