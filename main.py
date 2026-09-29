import pygame
import sys
import random
from scripts.jogador import Jogador
from scripts.plataforma import Plataforma, Lanterna, Porta
from scripts.inimigo import Inimigo, FantasmaCozinha, FantasmaBanheiro, ChefeArmario

pygame.init()

# 6. Tamanho da tela maior (1024x768)
LARGURA, ALTURA = 1024, 768
tamanhoTela = [LARGURA, ALTURA]
tela = pygame.display.set_mode(tamanhoTela)
pygame.display.set_caption("ComodoOo")

clock = pygame.time.Clock()

AZUL = (100, 180, 255)
VERDE = (80, 200, 100)
VERDE_HOVER = (100, 230, 120)
BRANCO = (255, 255, 255)

fonte_titulo = pygame.font.SysFont("arial", 56, bold=True)
fonte_botao = pygame.font.SysFont("arial", 32, bold=True)

estado_jogo = "MENU"
fase_atual = 0  # 0: Floresta, 1: Corredor, 2: Sala, 3: Cozinha, 4: Banheiro, 5: Quarto

# Gotas de chuva adaptadas para o tamanho maior da tela
gotas_chuva = [[random.randint(0, LARGURA), random.randint(0, ALTURA)] for _ in range(100)]

# Botões
rect_botao = pygame.Rect(LARGURA // 2 - 120, 330, 240, 70)
rect_botao_reiniciar = pygame.Rect(LARGURA // 2 - 120, 430, 240, 60)

jogador = Jogador(tela, 100, 500, largura_tela=LARGURA)

fantasmas = []
lanternas = []
plataformas = []
porta = Porta(LARGURA - 100, 580)

def carregar_fase(fase):
    global fantasmas, lanternas, plataformas, porta
    fantasmas.clear()
    lanternas.clear()
    plataformas.clear()

    # Chão principal
    plataformas.append(Plataforma(0, 660, LARGURA, 108, (60, 60, 60)))
    porta = Porta(LARGURA - 100, 580)

    if fase == 0:  # Floresta
        porta.desbloqueada = True
    elif fase == 1:  # Corredor
        lanternas.append(Lanterna(400, 630))
        fantasmas.append(Inimigo(700, 560))
    elif fase == 2:  # Sala de Estar
        plataformas.append(Plataforma(300, 520, 200, 20, (140, 80, 40)))
        plataformas.append(Plataforma(650, 400, 200, 20, (140, 80, 40)))
        lanternas.extend([Lanterna(340, 490), Lanterna(690, 370)])
        fantasmas.extend([Inimigo(580, 600), Inimigo(720, 340)])
    elif fase == 3:  # Cozinha
        lanternas.extend([Lanterna(250, 630), Lanterna(320, 630)])
        fantasmas.extend([FantasmaCozinha(400, 400), FantasmaCozinha(850, 400)])
    elif fase == 4:  # Banheiro
        lanternas.extend([Lanterna(300, 630), Lanterna(550, 630)])
        fantasmas.extend([FantasmaBanheiro(450, 620), FantasmaBanheiro(750, 620)])
    elif fase == 5:  # Quarto (Chefe)
        # 2. Várias plataformas/prateleiras envolta do armário
        plataformas.append(Plataforma(150, 520, 180, 20, (140, 80, 40)))
        plataformas.append(Plataforma(700, 520, 180, 20, (140, 80, 40)))
        plataformas.append(Plataforma(250, 380, 180, 20, (140, 80, 40)))
        plataformas.append(Plataforma(600, 380, 180, 20, (140, 80, 40)))

        lanternas.extend([Lanterna(200, 490), Lanterna(750, 490), Lanterna(300, 350)])
        # 2. Armário (Boss) posicionado no centro
        fantasmas.append(ChefeArmario(LARGURA // 2 - 40, 540))

carregar_fase(fase_atual)

while True:
    pos_mouse = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado_jogo == "MENU" and rect_botao.collidepoint(pos_mouse):
                estado_jogo = "JOGO"
                fase_atual = 0
                carregar_fase(fase_atual)
                jogador.resetar(100, 500)

            elif estado_jogo == "GAME_OVER" and rect_botao_reiniciar.collidepoint(pos_mouse):
                estado_jogo = "JOGO"
                fase_atual = 0
                carregar_fase(fase_atual)
                jogador.resetar(100, 500)

        if evento.type == pygame.KEYDOWN and estado_jogo == "JOGO":
            if evento.key == pygame.K_c:
                if jogador.rect.colliderect(porta.rect) and porta.desbloqueada:
                    if fase_atual < 5:
                        fase_atual += 1
                        carregar_fase(fase_atual)
                        jogador.resetar(50, 500)

    if estado_jogo == "MENU":
        tela.fill(AZUL)
        texto_titulo = fonte_titulo.render("ComodoOo", True, BRANCO)
        tela.blit(texto_titulo, texto_titulo.get_rect(center=(LARGURA // 2, 200)))

        cor_atual_botao = VERDE_HOVER if rect_botao.collidepoint(pos_mouse) else VERDE
        pygame.draw.rect(tela, cor_atual_botao, rect_botao, border_radius=12)
        pygame.draw.rect(tela, BRANCO, rect_botao, width=3, border_radius=12)

        texto_jogar = fonte_botao.render("JOGAR", True, BRANCO)
        tela.blit(texto_jogar, texto_jogar.get_rect(center=rect_botao.center))

    elif estado_jogo == "JOGO":
        jogador.atualizar(plataformas)

        fantasmas_vivos = [f for f in fantasmas if not f.derrotado]
        if len(fantasmas_vivos) == 0:
            porta.desbloqueada = True

        for lant in lanternas:
            if not lant.coletada and not jogador.tem_lanterna:
                if jogador.rect.colliderect(lant.rect):
                    lant.coletada = True
                    jogador.tem_lanterna = True

        if jogador.tem_lanterna:
            circulo_lanterna = pygame.Rect(
                jogador.rect.centerx - jogador.raio_lanterna,
                jogador.rect.centery - jogador.raio_lanterna,
                jogador.raio_lanterna * 2,
                jogador.raio_lanterna * 2
            )

            for fantasma in fantasmas_vivos:
                if circulo_lanterna.colliderect(fantasma.rect):
                    fantasma.receber_dano()
                    jogador.tem_lanterna = False
                    break

        # 4. Checagem de colisão entre fantasmas do banheiro
        fantasmas_banheiro = [f for f in fantasmas if isinstance(f, FantasmaBanheiro) and not f.derrotado]
        for i in range(len(fantasmas_banheiro)):
            for j in range(i + 1, len(fantasmas_banheiro)):
                f1 = fantasmas_banheiro[i]
                f2 = fantasmas_banheiro[j]
                if f1.rect.colliderect(f2.rect):
                    f1.inverter_direcao()
                    f2.inverter_direcao()

        for fantasma in fantasmas:
            # 1. Passa as plataformas para que o fantasma derrotado pare no chão
            fantasma.perseguir(jogador, plataformas)

            if not fantasma.derrotado and jogador.rect.colliderect(fantasma.rect):
                estado_jogo = "GAME_OVER"

            if isinstance(fantasma, ChefeArmario):
                for proj in fantasma.projeteis:
                    if jogador.rect.colliderect(proj["rect"]):
                        estado_jogo = "GAME_OVER"

        # --- Desenho da Tela ---
        if fase_atual == 0:
            tela.fill((20, 35, 25))
            for gota in gotas_chuva:
                pygame.draw.line(tela, (150, 180, 220), gota, (gota[0], gota[1] + 6), 1)
                gota[1] += 10
                if gota[1] > ALTURA:
                    gota[1] = 0
                    gota[0] = random.randint(0, LARGURA)
        else:
            tela.fill((35, 25, 45))

        for plat in plataformas:
            plat.desenhar(tela)

        porta.desenhar(tela)

        for lant in lanternas:
            lant.desenhar(tela)

        for fantasma in fantasmas:
            fantasma.desenhar(tela)

        jogador.desenhar()

        if jogador.rect.colliderect(porta.rect) and porta.desbloqueada:
            texto_p = fonte_botao.render("Aperte C para entrar", True, BRANCO)
            tela.blit(texto_p, (LARGURA // 2 - 140, 50))

    elif estado_jogo == "GAME_OVER":
        tela.fill((30, 30, 30))
        texto_go = fonte_titulo.render("GAME OVER", True, (220, 60, 60))
        tela.blit(texto_go, texto_go.get_rect(center=(LARGURA // 2, 280)))

        pygame.draw.rect(tela, VERDE, rect_botao_reiniciar, border_radius=8)
        texto_retry = fonte_botao.render("REINICIAR", True, BRANCO)
        tela.blit(texto_retry, texto_retry.get_rect(center=rect_botao_reiniciar.center))

    clock.tick(60)
    pygame.display.flip()