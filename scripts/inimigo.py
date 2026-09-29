import pygame
import math

class Inimigo:
    def __init__(self, x, y, largura=80, altura=80):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.velocidade = 2
        self.raio_deteccao = 300
        self.posicao_y_base = float(y)
        self.tempo_flutuacao = 0
        self.amplitude = 8
        self.velocidade_flutuacao = 0.05
        
        self.derrotado = False 
        self.vida = 1
        self.velocidade_queda = 0

        # Carregamento das animações e imagens
        self.frames_vivo = []
        for i in range(7):
            try:
                img = pygame.image.load(f"assets/Fantasminha-{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (largura, altura))
            except pygame.error:
                img = pygame.Surface((largura, altura))
                img.fill((200, 200, 250))
            self.frames_vivo.append(img)

        try:
            self.imagem_relogio = pygame.image.load("assets/Relógio.png").convert_alpha()
            self.imagem_relogio = pygame.transform.scale(self.imagem_relogio, (36, 48))
        except pygame.error:
            self.imagem_relogio = pygame.Surface((36, 48))
            self.imagem_relogio.fill((139, 69, 19))

        self.index_frame = 0
        self.contador_frame = 0

    def perseguir(self, jogador, plataformas=None):
        if self.derrotado:
            # Objeto caindo e parando no chão/plataformas ao ser derrotado
            self.velocidade_queda += 0.5
            self.rect.y += self.velocidade_queda
            if plataformas:
                for plat in plataformas:
                    if self.rect.colliderect(plat.rect) and self.velocidade_queda > 0:
                        self.rect.bottom = plat.rect.top
                        self.velocidade_queda = 0
            return

        # Animação de troca de frames enquanto vivo
        self.contador_frame += 1
        if self.contador_frame >= 15:  # Troca de frame a cada 15 tiques/frames
            self.contador_frame = 0
            self.index_frame = (self.index_frame + 1) % len(self.frames_vivo)

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
            deslocamento = math.sin(self.tempo_flutuacao) * self.amplitude
            self.rect.y = self.posicao_y_base + deslocamento

    def receber_dano(self):
        self.vida -= 1
        if self.vida <= 0:
            self.derrotado = True

    def desenhar(self, tela):
        if self.derrotado:
            tela.blit(self.imagem_relogio, self.rect)
        else:
            tela.blit(self.frames_vivo[self.index_frame], self.rect)

    def resetar(self, x, y):
        self.rect.topleft = (x, y)
        self.posicao_y_base = float(y)
        self.derrotado = False
        self.vida = 1
        self.velocidade_queda = 0


class FantasmaCozinha(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.tempo_investida = 0

    def perseguir(self, jogador, plataformas=None):
        if self.derrotado:
            super().perseguir(jogador, plataformas)
            return

        self.contador_frame += 1
        if self.contador_frame >= 15:
            self.contador_frame = 0
            self.index_frame = (self.index_frame + 1) % len(self.frames_vivo)

        self.tempo_investida += 1
        vel = 7.0 if (self.tempo_investida % 100) < 25 else 1.5
        
        if self.rect.centerx < jogador.rect.centerx:
            self.rect.x += vel
        else:
            self.rect.x -= vel
        
        if self.rect.centery < jogador.rect.centery:
            self.rect.y += 1
        else:
            self.rect.y -= 1


class FantasmaBanheiro(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.direcao = 1

    def inverter_direcao(self):
        self.direcao *= -1
        self.rect.x += self.direcao * 5

    def perseguir(self, jogador, plataformas=None):
        if self.derrotado:
            super().perseguir(jogador, plataformas)
            return

        self.contador_frame += 1
        if self.contador_frame >= 15:
            self.contador_frame = 0
            self.index_frame = (self.index_frame + 1) % len(self.frames_vivo)

        self.rect.x += 5 * self.direcao
        if self.rect.right >= 1000 or self.rect.left <= 20:
            self.inverter_direcao()


class ChefeArmario(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y, largura=80, altura=120)
        self.cor = (130, 80, 40)
        self.vida = 3
        self.projeteis = []
        self.tempo_disparo = 0

    def perseguir(self, jogador, plataformas=None):
        if self.derrotado:
            super().perseguir(jogador, plataformas)
            return

        self.tempo_disparo += 1
        if self.tempo_disparo >= 60:
            self.tempo_disparo = 0
            
            dx = jogador.rect.centerx - self.rect.centerx
            dy = jogador.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist != 0:
                vel_x = (dx / dist) * 6
                vel_y = (dy / dist) * 6
            else:
                vel_x, vel_y = -6, 0

            self.projeteis.append({
                "rect": pygame.Rect(self.rect.centerx, self.rect.centery, 16, 16),
                "vx": vel_x,
                "vy": vel_y
            })

        for proj in self.projeteis[:]:
            proj["rect"].x += proj["vx"]
            proj["rect"].y += proj["vy"]
            
            if proj["rect"].x < 0 or proj["rect"].x > 1024 or proj["rect"].y < 0 or proj["rect"].y > 768:
                self.projeteis.remove(proj)

    def desenhar(self, tela):
        if self.derrotado:
            tela.blit(self.imagem_relogio, self.rect)
        else:
            pygame.draw.rect(tela, self.cor, self.rect, border_radius=6)

        for proj in self.projeteis:
            pygame.draw.rect(tela, (230, 50, 50), proj["rect"])