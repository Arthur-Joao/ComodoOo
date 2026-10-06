import pygame
import sys
import random

# Tenta importar do módulo scripts ou do diretório atual
from scripts.jogador import Jogador
from scripts.plataforma import Plataforma, Lanterna, Porta
from scripts.inimigo import Inimigo, FantasmaCozinha, FantasmaBanheiro, ChefeArmario
from scripts.banco import inicializar_banco, salvar_pontuacao, obter_top_scores

pygame.init()
inicializar_banco()

LARGURA, ALTURA = 1024, 768
tamanhoTela = [LARGURA, ALTURA]
tela = pygame.display.set_mode(tamanhoTela)
pygame.display.set_caption("ComodoOo")

clock = pygame.time.Clock()

AZUL = (100, 180, 255)
VERDE = (80, 200, 100)
VERDE_HOVER = (100, 230, 120)
BRANCO = (255, 255, 255)
AMARELO = (255, 215, 0)

fonte_titulo = pygame.font.SysFont("arial", 56, bold=True)
fonte_botao = pygame.font.SysFont("arial", 32, bold=True)
fonte_pequena = pygame.font.SysFont("arial", 22)

estado_jogo = "MENU"
fase_atual = 0  # 0 a 5
pontuacao = 0

# Entrada de Nome do Jogador
nome_jogador = ""
pontuacao_salva = False
rect_caixa_texto = pygame.Rect(LARGURA // 2 - 120, 360, 240, 45)

gotas_chuva = [[random.randint(0, LARGURA), random.randint(0, ALTURA)] for _ in range(100)]

rect_botao = pygame.Rect(LARGURA // 2 - 120, 330, 240, 70)
rect_botao_reiniciar = pygame.Rect(LARGURA // 2 - 120, 520, 240, 50)
rect_botao_salvar = pygame.Rect(LARGURA // 2 - 120, 420, 240, 45)

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

    plataformas.append(Plataforma(0, 660, LARGURA, 108, (60, 60, 60)))
    porta = Porta(LARGURA - 100, 580)

    if fase == 0:
        porta.desbloqueada = True
    elif fase == 1:
        lanternas.append(Lanterna(400, 630))
        fantasmas.append(Inimigo(700, 560))
    elif fase == 2:
        plataformas.append(Plataforma(300, 280, 200, 20, (140, 80, 40)))
        plataformas.append(Plataforma(300, 520, 200, 20, (140, 80, 40)))
        plataformas.append(Plataforma(650, 400, 200, 20, (140, 80, 40)))
        lanternas.extend([Lanterna(340, 490), Lanterna(690, 370)])
        fantasmas.extend([Inimigo(580, 600), Inimigo(720, 340)])
    elif fase == 3:
        plataformas.append(Plataforma(300, 280, 200, 20, (140, 80, 40)))
        plataformas.append(Plataforma(300, 520, 200, 20, (140, 80, 40)))
        plataformas.append(Plataforma(650, 400, 200, 20, (140, 80, 40)))
        lanternas.extend([Lanterna(340, 490), Lanterna(690, 370), Lanterna(340, 250)])
        fantasmas.extend([FantasmaCozinha(400, 200), FantasmaCozinha(850, 200), FantasmaCozinha(600, 200)])
    elif fase == 4:
        lanternas.extend([Lanterna(300, 630), Lanterna(550, 630)])
        fantasmas.extend([FantasmaBanheiro(450, 620), FantasmaBanheiro(750, 620)])
    elif fase == 5:
        plataformas.append(Plataforma(150, 520, 180, 20, (140, 80, 40)))
        plataformas.append(Plataforma(700, 520, 180, 20, (140, 80, 40)))
        plataformas.append(Plataforma(250, 380, 180, 20, (140, 80, 40)))
        plataformas.append(Plataforma(600, 380, 180, 20, (140, 80, 40)))
        lanternas.extend([Lanterna(200, 490), Lanterna(750, 490), Lanterna(300, 350)])
        fantasmas.append(ChefeArmario(LARGURA // 2 - 40, 540))

carregar_fase(fase_atual)

def reiniciar_jogo():
    global fase_atual, pontuacao, nome_jogador, pontuacao_salva, estado_jogo
    estado_jogo = "JOGO"
    fase_atual = 0
    pontuacao = 0
    nome_jogador = ""
    pontuacao_salva = False
    carregar_fase(fase_atual)
    jogador.resetar(100, 500)

while True:
    pos_mouse = pygame.mouse.get_pos()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if estado_jogo == "MENU" and rect_botao.collidepoint(pos_mouse):
                reiniciar_jogo()

            elif estado_jogo in ["GAME_OVER", "VITORIA"]:
                if rect_botao_salvar.collidepoint(pos_mouse) and not pontuacao_salva:
                    salvar_pontuacao(nome_jogador, pontuacao)
                    pontuacao_salva = True
                elif rect_botao_reiniciar.collidepoint(pos_mouse):
                    reiniciar_jogo()

        if evento.type == pygame.KEYDOWN:
            if estado_jogo == "JOGO":
                if evento.key == pygame.K_c and jogador.rect.colliderect(porta.rect) and porta.desbloqueada:
                    if fase_atual < 5:
                        fase_atual += 1
                        carregar_fase(fase_atual)
                        jogador.resetar(50, 500)
                    elif fase_atual == 5:
                        estado_jogo = "VITORIA"


        elif estado_jogo in ["GAME_OVER", "VITORIA"]:
                tela.fill((30, 30, 30))
                titulo = "VOCÊ VENCEU!" if estado_jogo == "VITORIA" else "GAME OVER"
                cor_titulo = (100, 230, 120) if estado_jogo == "VITORIA" else (220, 60, 60)
                
                # Título principal
                texto_st = fonte_titulo.render(titulo, True, cor_titulo)
                tela.blit(texto_st, texto_st.get_rect(center=(LARGURA // 2, 80)))

                # Exibição da Pontuação Atual
                txt_p_final = fonte_botao.render(f"Sua Pontuação Final: {pontuacao}", True, AMARELO)
                tela.blit(txt_p_final, txt_p_final.get_rect(center=(LARGURA // 2, 140)))

                # Entrada de Nome e Botão Salvar
                if not pontuacao_salva:
                    txt_inst = fonte_pequena.render("Digite seu nome e pressione ENTER para Salvar:", True, BRANCO)
                    tela.blit(txt_inst, txt_inst.get_rect(center=(LARGURA // 2, 190)))

                    pygame.draw.rect(tela, BRANCO, rect_caixa_texto, width=2, border_radius=6)
                    txt_nome = fonte_pequena.render(nome_jogador, True, BRANCO)
                    tela.blit(txt_nome, txt_nome.get_rect(center=rect_caixa_texto.center))

                    pygame.draw.rect(tela, VERDE, rect_botao_salvar, border_radius=8)
                    txt_btn_salvar = fonte_pequena.render("SALVAR PONTOS", True, BRANCO)
                    tela.blit(txt_btn_salvar, txt_btn_salvar.get_rect(center=rect_botao_salvar.center))
                else:
                    txt_confirm = fonte_pequena.render("Pontuação Salva com Sucesso!", True, (100, 230, 120))
                    tela.blit(txt_confirm, txt_confirm.get_rect(center=(LARGURA // 2, 230)))

                # --- RANKING DE JOGADORES (TOP 5) NA TELA FINAL ---
                top_scores = obter_top_scores()
                txt_rank_titulo = fonte_botao.render("RANKING - TOP 5", True, AMARELO)
                tela.blit(txt_rank_titulo, txt_rank_titulo.get_rect(center=(LARGURA // 2, 310)))

                y_offset = 350
                for idx, (nome, pts) in enumerate(top_scores, start=1):
                    # Destaca com a cor verde se for o nome atual recém-salvo
                    cor_texto = (100, 230, 120) if (pontuacao_salva and nome == nome_jogador and pts == pontuacao) else BRANCO
                    txt_item = fonte_pequena.render(f"{idx}. {nome} - {pts} pts", True, cor_texto)
                    tela.blit(txt_item, txt_item.get_rect(center=(LARGURA // 2, y_offset)))
                    y_offset += 28

                # Botão Reiniciar na parte inferior
                pygame.draw.rect(tela, VERDE, rect_botao_reiniciar, border_radius=8)
                texto_retry = fonte_botao.render("REINICIAR", True, BRANCO)
                tela.blit(texto_retry, texto_retry.get_rect(center=rect_botao_reiniciar.center))

    if estado_jogo == "MENU":
        tela.fill(AZUL)
        texto_titulo = fonte_titulo.render("ComodoOo", True, BRANCO)
        tela.blit(texto_titulo, texto_titulo.get_rect(center=(LARGURA // 2, 120)))

        cor_atual_botao = VERDE_HOVER if rect_botao.collidepoint(pos_mouse) else VERDE
        pygame.draw.rect(tela, cor_atual_botao, rect_botao, border_radius=12)
        pygame.draw.rect(tela, BRANCO, rect_botao, width=3, border_radius=12)
        texto_jogar = fonte_botao.render("JOGAR", True, BRANCO)
        tela.blit(texto_jogar, texto_jogar.get_rect(center=rect_botao.center))

        # Desenhar Ranking (Top 5)
        top_scores = obter_top_scores()
        txt_rank_titulo = fonte_botao.render("TOP 5 RANKING", True, AMARELO)
        tela.blit(txt_rank_titulo, txt_rank_titulo.get_rect(center=(LARGURA // 2, 440)))

        y_offset = 480
        for idx, (nome, pts) in enumerate(top_scores, start=1):
            txt_item = fonte_pequena.render(f"{idx}. {nome} - {pts} pts", True, BRANCO)
            tela.blit(txt_item, txt_item.get_rect(center=(LARGURA // 2, y_offset)))
            y_offset += 30

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
                    if fantasma.derrotado:
                        pontuacao += fantasma.pontos  # Contabiliza os pontos de acordo com o inimigo
                    jogador.tem_lanterna = False
                    break

        fantasmas_banheiro = [f for f in fantasmas if isinstance(f, FantasmaBanheiro) and not f.derrotado]
        for i in range(len(fantasmas_banheiro)):
            for j in range(i + 1, len(fantasmas_banheiro)):
                f1 = fantasmas_banheiro[i]
                f2 = fantasmas_banheiro[j]
                if f1.rect.colliderect(f2.rect):
                    f1.inverter_direcao()
                    f2.inverter_direcao()

        for fantasma in fantasmas:
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

        # Exibe a pontuação no topo da tela durante o jogo
        txt_pontos = fonte_pequena.render(f"Pontos: {pontuacao}", True, AMARELO)
        tela.blit(txt_pontos, (20, 20))

        if jogador.rect.colliderect(porta.rect) and porta.desbloqueada:
            texto_p = fonte_botao.render("Aperte C para entrar", True, BRANCO)
            tela.blit(texto_p, (LARGURA // 2 - 140, 50))

    elif estado_jogo in ["GAME_OVER", "VITORIA"]:
        tela.fill((30, 30, 30))
        titulo = "VOCÊ VENCEU!" if estado_jogo == "VITORIA" else "GAME OVER"
        cor_titulo = (100, 230, 120) if estado_jogo == "VITORIA" else (220, 60, 60)
        
        texto_st = fonte_titulo.render(titulo, True, cor_titulo)
        tela.blit(texto_st, texto_st.get_rect(center=(LARGURA // 2, 200)))

        txt_p_final = fonte_botao.render(f"Pontuação Final: {pontuacao}", True, AMARELO)
        tela.blit(txt_p_final, txt_p_final.get_rect(center=(LARGURA // 2, 280)))

        if not pontuacao_salva:
            txt_inst = fonte_pequena.render("Digite seu nome e pressione ENTER para Salvar:", True, BRANCO)
            tela.blit(txt_inst, txt_inst.get_rect(center=(LARGURA // 2, 330)))

            pygame.draw.rect(tela, BRANCO, rect_caixa_texto, width=2, border_radius=6)
            txt_nome = fonte_pequena.render(nome_jogador, True, BRANCO)
            tela.blit(txt_nome, txt_nome.get_rect(center=rect_caixa_texto.center))

            pygame.draw.rect(tela, VERDE, rect_botao_salvar, border_radius=8)
            txt_btn_salvar = fonte_pequena.render("SALVAR PONTOS", True, BRANCO)
            tela.blit(txt_btn_salvar, txt_btn_salvar.get_rect(center=rect_botao_salvar.center))
        else:
            txt_confirm = fonte_pequena.render("Pontuação Salva com Sucesso!", True, (100, 230, 120))
            tela.blit(txt_confirm, txt_confirm.get_rect(center=(LARGURA // 2, 380)))

        pygame.draw.rect(tela, VERDE, rect_botao_reiniciar, border_radius=8)
        texto_retry = fonte_botao.render("REINICIAR", True, BRANCO)
        tela.blit(texto_retry, texto_retry.get_rect(center=rect_botao_reiniciar.center))

    clock.tick(60)
    pygame.display.flip()