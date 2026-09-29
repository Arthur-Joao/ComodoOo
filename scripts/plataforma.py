import pygame

class Plataforma:
    def __init__(self, x, y, largura, altura, cor=(80, 200, 100)):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = cor

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, self.rect)


class Lanterna:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.coletada = False

    def desenhar(self, tela):
        if not self.coletada:
            pygame.draw.rect(tela, (255, 230, 0), self.rect, border_radius=4)


class Porta:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 80)
        self.desbloqueada = False

    def desenhar(self, tela):
        cor = (50, 205, 50) if self.desbloqueada else (120, 60, 30)
        pygame.draw.rect(tela, cor, self.rect, border_radius=6)