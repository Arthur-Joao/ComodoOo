import pygame
import math

class Inimigo:
    def __init__(self, x, y, largura=40, altura=40):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = (220, 60, 60)
        self.velocidade = 2
        self.raio_deteccao = 250
        self.posicao = [x, y]

    def perseguir(self, jogador):
        distancia_x = jogador.rect.centerx - self.rect.centerx
        distancia_y = jogador.rect.centery - self.rect.centery

        distanci_total = math.hypot(distancia_x, distancia_y)

        if distanci_total < self.raio_deteccao and distanci_total != 0:
            if distancia_x > 0:
                self.rect.x += self.velocidade
            elif distancia_x < 0:
                self.rect.x -= self.velocidade

    def desenhar(self,tela):
        pygame.draw.rect(tela, self.cor, self.rect) 

    def resetar(self, x, y):
        self.posicao = [x, y]
        self.velocidade_y = 0
        self.no_chao = False
        self.rect.topleft = (x, y)