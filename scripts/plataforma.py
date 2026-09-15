import pygame


class Plataforma:

    def __init__(self, x, y, largura, altura):
        self.rect = pygame.Rect(x, y, largura, altura)

    def desenhar(self, tela):
        pygame.draw.rect(tela, (80, 200, 100), self.rect)