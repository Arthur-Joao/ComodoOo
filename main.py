import pygame
import sys
from scripts.jogador import Jogador
from scripts.plataforma import Plataforma
from scripts.inimigo import Inimigo

pygame.init()

tamanhoTela = [800,600]

tela = pygame.display.set_mode((tamanhoTela))
pygame.display.set_caption("ComodoOo")

clock = pygame.time.Clock()
AZUL = (100, 180, 255)
VERDE = (80, 200, 100)
VERMELHO = (220, 60, 60)
VERDE_HOVER = (100, 230, 120)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Fonte
fonte_titulo = pygame.font.SysFont("arial", 48, bold=True)
fonte_botao = pygame.font.SysFont("arial", 32, bold=True)

#Estado inicial do jogo
estado_jogo = "MENU"

# Configuração do Botão Jogar
largura_botao, altura_botao = 200, 60
pos_x_botao = (tamanhoTela[0] // 2) - (largura_botao // 2)
pos_y_botao = (tamanhoTela[1] // 2) - (altura_botao // 2)
rect_botao = pygame.Rect(pos_x_botao, pos_y_botao, largura_botao, altura_botao)

# Jogador
jogador = Jogador(tela, 100, 450)

#Inimigo
inimigo = Inimigo(500, 510)

#Configuração do Botão Reiniciar
rect_botao_reiniciar = pygame.Rect(300, 350, 200, 50)

# Plataformas
plataformas = [
    Plataforma(0, 550, 800, 50),
    Plataforma(300, 450, 200, 30),
    Plataforma(600, 350, 150, 30),
]

while True:
    pos_mouse = pygame.mouse.get_pos()

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if estado_jogo == "MENU" and rect_botao.collidepoint(pos_mouse):
                    estado_jogo = "JOGO"
        
        elif estado_jogo == "GAME_OVER" and rect_botao_reiniciar.collidepoint(pos_mouse):
            jogador.resetar(100, 450)
            inimigo.resetar(500, 510) # Restaura a posição inicial
            estado_jogo = "JOGO"

    #Lógica do Desenho
    if estado_jogo == "MENU":
        tela.fill(AZUL)

        #Título
        texto_titulo = fonte_titulo.render("ComodoOo", True, BRANCO)
        rect_titulo = texto_titulo.get_rect(center=(tamanhoTela[0] // 2, 150))
        tela.blit(texto_titulo, rect_titulo)

        #Efeito ao passar o mouse
        cor_atual_botao = VERDE_HOVER if rect_botao.collidepoint(pos_mouse) else VERDE
        pygame.draw.rect(tela,cor_atual_botao, rect_botao, border_radius=12)
        pygame.draw.rect(tela,BRANCO, rect_botao, width=3, border_radius=12)

        texto_jogar = fonte_botao.render("JOGAR", True, BRANCO)
        rect_texto_jogar = texto_jogar.get_rect(center=rect_botao.center)
        tela.blit(texto_jogar, rect_texto_jogar)

    elif estado_jogo == "JOGO":
        jogador.atualizar(plataformas)

        inimigo.perseguir(jogador)

        if jogador.rect.colliderect(inimigo.rect):
            estado_jogo = "GAME_OVER"
        
        tela.fill(AZUL)
        for plataforma in plataformas:
            plataforma.desenhar(tela)

        inimigo.desenhar(tela)
        jogador.desenhar()

    elif estado_jogo == "GAME_OVER":
        tela.fill((30, 30, 30)) # Fundo escuro/cinza

        # Texto de Game Over
        texto_go = fonte_titulo.render("GAME OVER", True, (220, 60, 60))
        rect_go = texto_go.get_rect(center=(400, 200))
        tela.blit(texto_go, rect_go)

        # Botão Tentar Novamente
        pygame.draw.rect(tela, VERDE, rect_botao_reiniciar, border_radius=8)
        texto_retry = fonte_botao.render("REINICIAR", True, BRANCO)
        rect_retry = texto_retry.get_rect(center=rect_botao_reiniciar.center)
        tela.blit(texto_retry, rect_retry)

    clock.tick(60)
    pygame.display.flip()
