import pygame
import math

class Inimigo:
    def __init__(self, x, y, largura=40, altura=40):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = (220, 60, 60)
        self.velocidade = 2
        self.raio_deteccao = 300
        self.posicao = [x, y]
        self.posicao_y_base = float(y) # Posição Y original sem o efeito
        self.tempo_flutuacao = 0        # Contador de tempo para o seno
        self.amplitude = 8               # Quantidade de pixels que sobe/desce
        self.velocidade_flutuacao = 0.05

    def perseguir(self, jogador):
        distancia_x = jogador.rect.centerx - self.rect.centerx
        distancia_y = jogador.rect.centery - self.rect.centery

        distancia_total = math.hypot(distancia_x, distancia_y)

        if 0 < distancia_total < self.raio_deteccao:
            direcao_x = distancia_x / distancia_total
            direcao_y = distancia_y / distancia_total

            self.rect.x += direcao_x * self.velocidade
            self.posicao_y_base += direcao_y * self.velocidade
            self.rect.y = self.posicao_y_base
        
        else:
            self.tempo_flutuacao += self.velocidade_flutuacao
            
            # math.sin varia de -1 a 1 -> multiplica pela amplitude
            deslocamento = math.sin(self.tempo_flutuacao) * self.amplitude
            
            # Aplica o movimento em relação à posição base
            self.rect.y = self.posicao_y_base + deslocamento

        

    def desenhar(self,tela):
        pygame.draw.rect(tela, self.cor, self.rect) 

    def resetar(self, x, y):
        self.posicao = [x, y]
        self.velocidade_y = 0
        self.no_chao = False
        self.rect.topleft = (x, y)