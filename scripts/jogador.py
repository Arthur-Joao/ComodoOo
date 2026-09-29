import pygame

class Jogador:
    def __init__(self, tela, x, y, largura_tela=1024):
        self.tela = tela
        self.posicao = [x, y]
        self.tamanho = [60, 114]
        self.rect = pygame.Rect(self.posicao, self.tamanho)
        self.largura_tela = largura_tela

        self.velocidade = 5
        self.velocidade_y = 0
        self.gravidade = 0.5
        self.forca_pulo = -12
        self.no_chao = False

        self.tem_lanterna = False
        self.raio_lanterna = 90

        self.contador = 0
        self.imagemAtual = 0
        self.listaImagens = []

        for i in range(2):
            try:
                imagem = pygame.image.load(f"assets/jogador{i}.png").convert_alpha()
                imagem = pygame.transform.scale(imagem, self.tamanho)
            except pygame.error:
                imagem = pygame.Surface(self.tamanho)
                imagem.fill((100, 180, 255))
            self.listaImagens.append(imagem)

    def movimentar(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.posicao[0] -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.posicao[0] += self.velocidade
        
        # 5. Impede que o jogador saia da tela
        if self.posicao[0] < 0:
            self.posicao[0] = 0
        elif self.posicao[0] > self.largura_tela - self.tamanho[0]:
            self.posicao[0] = self.largura_tela - self.tamanho[0]

        self.rect.x = self.posicao[0]

    def pular(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE] and self.no_chao:
            self.velocidade_y = self.forca_pulo
            self.no_chao = False

    def aplicar_gravidade(self):
        self.velocidade_y += self.gravidade
        self.posicao[1] += self.velocidade_y
        self.rect.y = self.posicao[1]

    def verificar_colisoes(self, plataformas):
        self.no_chao = False
        # 3. Física de plataforma onde o jogador passa por baixo sem ser teleportado
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                # Só colide se estiver caindo e a base do jogador estava acima/no topo da plataforma
                if self.velocidade_y >= 0 and (self.rect.bottom - self.velocidade_y) <= plataforma.rect.top + 10:
                    self.rect.bottom = plataforma.rect.top
                    self.posicao[1] = self.rect.y
                    self.velocidade_y = 0
                    self.no_chao = True

    def animar(self):
        self.contador += 1
        if self.contador > 19:
            self.contador = 0
            self.imagemAtual = (self.imagemAtual + 1) % len(self.listaImagens)

    def atualizar(self, plataformas):
        self.movimentar()
        self.pular()
        self.aplicar_gravidade()
        self.verificar_colisoes(plataformas)
        self.animar()

    def desenhar(self):
        self.tela.blit(self.listaImagens[self.imagemAtual], self.posicao)
        
        if self.tem_lanterna:
            centro = self.rect.center
            superficie_luz = pygame.Surface((self.raio_lanterna * 2, self.raio_lanterna * 2), pygame.SRCALPHA)
            pygame.draw.circle(superficie_luz, (255, 255, 180, 120), (self.raio_lanterna, self.raio_lanterna), self.raio_lanterna)
            pygame.draw.circle(superficie_luz, (255, 255, 220, 255), (self.raio_lanterna, self.raio_lanterna), self.raio_lanterna, 3)
            self.tela.blit(superficie_luz, (centro[0] - self.raio_lanterna, centro[1] - self.raio_lanterna))

    def resetar(self, x, y):
        self.posicao = [x, y]
        self.velocidade_y = 0
        self.no_chao = False
        self.tem_lanterna = False
        self.rect.topleft = (x, y)