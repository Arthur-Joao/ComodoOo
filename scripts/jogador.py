import pygame


class Jogador:

    def __init__(self, tela, x, y):

        # Tela
        self.tela = tela

        # Posição e tamanho
        self.posicao = [x, y]
        self.tamanho = [60,114]

        # Retângulo de colisão
        self.rect = pygame.Rect(self.posicao, self.tamanho)

        # Física
        self.velocidade = 5
        self.velocidade_y = 0

        self.gravidade = 0.5
        self.forca_pulo = -12

        self.no_chao = False

        # Animação
        self.contador = 0
        self.imagemAtual = 0
        self.listaImagens = []

        for i in range(2):
            imagem = pygame.image.load(
                f"assets/jogador{i}.png"
            ).convert_alpha()

            imagem = pygame.transform.scale(
                imagem,
                self.tamanho
            )

            self.listaImagens.append(imagem)

    def movimentar(self):

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            self.posicao[0] -= self.velocidade

        if teclas[pygame.K_RIGHT]:
            self.posicao[0] += self.velocidade

    def pular(self):

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_SPACE] and self.no_chao:
            self.velocidade_y = self.forca_pulo
            self.no_chao = False

    def aplicar_gravidade(self):

        self.velocidade_y += self.gravidade

        self.posicao[1] += self.velocidade_y

    def verificar_colisoes(self, plataformas):

        self.no_chao = False

        # Atualiza o rect antes de verificar
        self.rect = pygame.Rect(
            self.posicao,
            self.tamanho
        )

        for plataforma in plataformas:

            if (
                self.rect.colliderect(plataforma.rect)
                and self.velocidade_y >= 0
            ):

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

        self.tela.blit(
            self.listaImagens[self.imagemAtual],
            self.posicao
        )