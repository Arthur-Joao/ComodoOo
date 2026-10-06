import pygame
import math

class Inimigo:
    def __init__(self, x, y, largura=80, altura=80):
        self.largura = largura
        self.altura = altura
        self.rect = pygame.Rect(x, y, largura, altura)
        self.posicao_x = float(x)
        self.posicao_y_base = float(y)
        
        self.velocidade = 2
        self.raio_deteccao = 300
        self.tempo_flutuacao = 0
        self.amplitude = 8
        self.velocidade_flutuacao = 0.05
        
        self.derrotado = False 
        self.vida = 1
        self.velocidade_queda = 0
        self.pontos = 10  # Pontuação base

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
            self.velocidade_queda += 0.5
            self.posicao_y_base += self.velocidade_queda
            self.rect.y = int(self.posicao_y_base)
            if plataformas:
                for plat in plataformas:
                    if self.rect.colliderect(plat.rect) and self.velocidade_queda > 0:
                        self.rect.bottom = plat.rect.top
                        self.posicao_y_base = float(self.rect.y)
                        self.velocidade_queda = 0
            return

        self.contador_frame += 1
        if self.contador_frame >= 15:
            self.contador_frame = 0
            self.index_frame = (self.index_frame + 1) % len(self.frames_vivo)

        distancia_x = jogador.rect.centerx - self.rect.centerx
        distancia_y = jogador.rect.centery - self.rect.centery
        distancia_total = math.hypot(distancia_x, distancia_y)

        if 0 < distancia_total < self.raio_deteccao:
            direcao_x = distancia_x / distancia_total
            direcao_y = distancia_y / distancia_total

            self.posicao_x += direcao_x * self.velocidade
            self.posicao_y_base += direcao_y * self.velocidade
            self.rect.x = int(self.posicao_x)
            self.rect.y = int(self.posicao_y_base)
        else:
            self.tempo_flutuacao += self.velocidade_flutuacao
            deslocamento = math.sin(self.tempo_flutuacao) * self.amplitude
            self.rect.y = int(self.posicao_y_base + deslocamento)

    def receber_dano(self):
        self.vida -= 1
        if self.vida <= 0:
            self.derrotado = True

    def desenhar(self, tela):
        if self.derrotado:
            rect_relogio = self.imagem_relogio.get_rect(center=self.rect.center)
            tela.blit(self.imagem_relogio, rect_relogio)
        else:
            tela.blit(self.frames_vivo[self.index_frame], self.rect)

    def resetar(self, x, y):
        self.rect.topleft = (x, y)
        self.posicao_x = float(x)
        self.posicao_y_base = float(y)
        self.derrotado = False
        self.vida = 1
        self.velocidade_queda = 0


class FantasmaCozinha(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.pontos = 15
        self.estado = "ESPERANDO"  # "ESPERANDO" ou "AVANCANDO"
        self.tempo_espera = 0
        self.limite_espera = 90    # ~1.5 segundos a 60 FPS

        # Direção e velocidade do avanço
        self.dir_x = 0
        self.dir_y = 0
        self.vel_investida = 10.0

        # Carregamento dos sprites específicos da cozinha
        self.frames_espera = []
        for nome_img in ["Fantascozinha0.png", "Fantascozinha1.png"]:
            try:
                img = pygame.image.load(f"assets/{nome_img}").convert_alpha()
                img = pygame.transform.scale(img, (93,72))
            except pygame.error:
                img = pygame.Surface((93,72))
                img.fill((0, 200, 250))
            self.frames_espera.append(img)

        try:
            self.img_ataque = pygame.image.load("assets/Fantascozinhataq.png").convert_alpha()
            self.img_ataque = pygame.transform.scale(self.img_ataque, (111, 39))
        except pygame.error:
            self.img_ataque = pygame.Surface((111, 39))
            self.img_ataque.fill((250, 50, 50))

        self.idx_frame_espera = 0
        self.timer_animacao = 0

    def perseguir(self, jogador, plataformas=None):
        if self.derrotado:
            super().perseguir(jogador, plataformas)
            return

        if self.estado == "ESPERANDO":
            # 1. Animação de flutuação vertical (subir e descer)
            self.tempo_flutuacao += self.velocidade_flutuacao
            deslocamento = math.sin(self.tempo_flutuacao) * self.amplitude
            self.rect.y = int(self.posicao_y_base + deslocamento)

            # 2. Alternância de sprites entre Fantascozinha0 e Fantascozinha1
            self.timer_animacao += 1
            if self.timer_animacao >= 12:  # Troca de frame a cada 12 ticks
                self.timer_animacao = 0
                self.idx_frame_espera = (self.idx_frame_espera + 1) % len(self.frames_espera)

            # 3. Contagem regressiva para iniciar o avanço
            self.tempo_espera += 1
            if self.tempo_espera >= self.limite_espera:
                self.tempo_espera = 0

                # Calcula a direção em relação ao jogador no momento do disparo
                dx = jogador.rect.centerx - self.rect.centerx
                dy = jogador.rect.centery - self.rect.centery
                distancia = math.hypot(dx, dy)

                if distancia != 0:
                    self.dir_x = dx / distancia
                    self.dir_y = dy / distancia
                else:
                    self.dir_x, self.dir_y = -1, 0

                self.estado = "AVANCANDO"

        elif self.estado == "AVANCANDO":
            # Movimento retilíneo rápido atravessando cenários
            self.posicao_x += self.dir_x * self.vel_investida
            self.posicao_y_base += self.dir_y * self.vel_investida

            self.rect.x = int(self.posicao_x)
            self.rect.y = int(self.posicao_y_base)

            # Para o avanço ao encostar nas extremidades da tela
            if self.rect.left <= 0 or self.rect.right >= 1024 or self.rect.top <= 0 or self.rect.bottom >= 768:
                self.rect.clamp_ip(pygame.Rect(0, 0, 1024, 768))
                self.posicao_x = float(self.rect.x)
                self.posicao_y_base = float(self.rect.y)

                # Volta ao modo de espera e flutuação
                self.estado = "ESPERANDO"

    def desenhar(self, tela):
        if self.derrotado:
            super().desenhar(tela)
        else:
            if self.estado == "ESPERANDO":
                # Desenha o sprite alternado da espera
                tela.blit(self.frames_espera[self.idx_frame_espera], self.rect)
            elif self.estado == "AVANCANDO":
                # Desenha o sprite de ataque (inverte horizontalmente se avançar para a direita)
                if self.dir_x > 0:
                    img_flip = pygame.transform.flip(self.img_ataque, True, False)
                    tela.blit(img_flip, self.rect)
                else:
                    tela.blit(self.img_ataque, self.rect)

    def resetar(self, x, y):
        super().resetar(x, y)
        self.estado = "ESPERANDO"
        self.tempo_espera = 0


class FantasmaBanheiro(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.direcao = 1
        self.pontos = 20  # Pontuação do Fantasma de Banheiro

    def inverter_direcao(self):
        self.direcao *= -1
        self.posicao_x += self.direcao * 5
        self.rect.x = int(self.posicao_x)

    def perseguir(self, jogador, plataformas=None):
        if self.derrotado:
            super().perseguir(jogador, plataformas)
            return

        self.contador_frame += 1
        if self.contador_frame >= 15:
            self.contador_frame = 0
            self.index_frame = (self.index_frame + 1) % len(self.frames_vivo)

        self.posicao_x += 5 * self.direcao
        self.rect.x = int(self.posicao_x)

        if self.rect.right >= 1000 or self.rect.left <= 20:
            self.inverter_direcao()


class ChefeArmario(Inimigo):
    def __init__(self, x, y):
        super().__init__(x, y, largura=80, altura=120)
        self.cor = (130, 80, 40)
        self.vida = 3
        self.projeteis = []
        self.tempo_disparo = 0
        self.pontos = 100  # Pontuação do Chefe

    def perseguir(self, jogador, plataformas=None):
        # Atualiza projéteis
        for proj in self.projeteis[:]:
            proj["rect"].x += proj["vx"]
            proj["rect"].y += proj["vy"]
            if proj["rect"].x < 0 or proj["rect"].x > 1024 or proj["rect"].y < 0 or proj["rect"].y > 768:
                self.projeteis.remove(proj)

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

    def desenhar(self, tela):
        if self.derrotado:
            super().desenhar(tela)
        else:
            pygame.draw.rect(tela, self.cor, self.rect, border_radius=6)
            
        for proj in self.projeteis:
            pygame.draw.rect(tela, (230, 50, 50), proj["rect"])

    def resetar(self, x, y):
        super().resetar(x, y)
        self.vida = 3
        self.projeteis.clear()
        self.tempo_disparo = 0