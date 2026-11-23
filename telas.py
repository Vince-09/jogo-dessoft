"""Telas que não são o jogo em si: início, instruções e fim de jogo."""
import pygame
from config import (FPS, LARGURA, ALTURA, BRANCO, AMARELO, PRETO,
                    SAIR, INICIO, INSTRUCOES, JOGANDO, ARQUIVO_RECORDE, ARQUIVO_TEMPOS)
from game_screen import formatar_tempo

def escrever(janela, fonte, texto, cor, centro):
    """Desenha um texto centralizado no ponto `centro`."""
    imagem = fonte.render(texto, True, cor)
    retangulo = imagem.get_rect()
    retangulo.center = centro
    janela.blit(imagem, retangulo)


def desenhar_fundo(janela, assets):
    """Desenha o céu e os prédios atrás das telas."""
    janela.blit(assets['fundo'], (0, 0))
    janela.blit(assets['predios'], (0, 0))


def esperar_tecla(janela, assets, desenhar, tecla_avancar, proximo_estado):
    """Desenha a tela até o jogador apertar uma tecla.
    ENTER/ESPAÇO -> devolve proximo_estado; ESC ou fechar -> SAIR."""
    relogio = pygame.time.Clock()
    while True:
        relogio.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return SAIR
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return SAIR
                if evento.key in tecla_avancar:
                    return proximo_estado
        desenhar_fundo(janela, assets)
        desenhar(janela)
        pygame.display.update()


def tela_inicio(janela, assets):
    """Tela com o nome do jogo."""
    def desenhar(janela):
        escrever(janela, assets['fonte_grande'], 'Raposa da Faquinha', PRETO, (LARGURA // 2 + 3, 133))
        escrever(janela, assets['fonte_grande'], 'Raposa da Faquinha', AMARELO, (LARGURA // 2, 130))
        imagem = pygame.transform.scale(assets['raposa']['parado'][0], (132, 128))
        janela.blit(imagem, imagem.get_rect(center=(LARGURA // 2, 260)))
        escrever(janela, assets['fonte_media'], 'Aperte ENTER para começar', BRANCO, (LARGURA // 2, 380))
        escrever(janela, assets['fonte_pequena'], f'Recorde: {ler_recorde()}', BRANCO, (LARGURA // 2, 430))

    return esperar_tecla(janela, assets, desenhar, [pygame.K_RETURN, pygame.K_SPACE], INSTRUCOES)


def tela_instrucoes(janela, assets):
    """Explica os controles."""
    linhas = [
        'Setas (ou A/D): andar',
        'Seta para cima (ou W): pular  ->  espinhos',
        'Seta para baixo (ou S): agachar  ->  galhos de palmeira',
        'X ou J: cortar com a faquinha  ->  pilhas de provas e jacarés',
        'Pule em cima dos jacarés para derrotá-los!',
        'P: pausar      ESC: sair',
    ]

    def desenhar(janela):
        escrever(janela, assets['fonte_grande'], 'Como jogar', AMARELO, (LARGURA // 2, 70))
        for i in range(len(linhas)):
            escrever(janela, assets['fonte_pequena'], linhas[i], PRETO, (LARGURA // 2, 150 + i * 40))
        escrever(janela, assets['fonte_media'], 'ENTER para jogar', BRANCO, (LARGURA // 2, 420))

    return esperar_tecla(janela, assets, desenhar, [pygame.K_RETURN, pygame.K_SPACE], JOGANDO)


def tela_fim(janela, assets, venceu, pontos, tempo_ms):
    """Tela de vitória ou de game over. Salva o recorde e, na vitória, o ranking de tempos."""
    recorde = ler_recorde()
    novo_recorde = pontos > recorde
    if novo_recorde:
        salvar_recorde(pontos)

    if venceu:
        titulo = 'Você venceu!'
        melhores, posicao = registrar_tempo(tempo_ms)
        assets['som_vitoria'].play()     # liga na Etapa 10
    else:
        titulo = 'Game Over'
        melhores, posicao = [], -1
        assets['som_game_over'].play()   # liga na Etapa 10

    def desenhar(janela):
        escrever(janela, assets['fonte_grande'], titulo, AMARELO, (LARGURA // 2, 80))
        info = f'Pontos: {pontos}    Tempo: {formatar_tempo(tempo_ms)}'
        escrever(janela, assets['fonte_media'], info, BRANCO, (LARGURA // 2, 150))
        if novo_recorde:
            escrever(janela, assets['fonte_pequena'], 'NOVO RECORDE DE PONTOS!', AMARELO, (LARGURA // 2, 192))
        if venceu:
            escrever(janela, assets['fonte_media'], 'Melhores tempos', PRETO, (LARGURA // 2, 250))
            for i in range(len(melhores)):
                texto = f'{i + 1}º   {formatar_tempo(melhores[i])}'
                cor = BRANCO
                if i == posicao:
                    texto = texto + '   <- você!'
                    cor = AMARELO
                escrever(janela, assets['fonte_media'], texto, cor, (LARGURA // 2, 295 + i * 40))
        escrever(janela, assets['fonte_pequena'], 'ENTER: voltar ao início    ESC: sair', BRANCO, (LARGURA // 2, ALTURA - 40))

    return esperar_tecla(janela, assets, desenhar, [pygame.K_RETURN], INICIO)


def ler_tempos():
    """Lê os melhores tempos do arquivo (um por linha, em ms). Sem arquivo: lista vazia."""
    try:
        with open(ARQUIVO_TEMPOS, 'r') as arquivo:
            linhas = arquivo.read().split()
        tempos = []
        for linha in linhas:
            tempos.append(int(linha))
        return tempos
    except (FileNotFoundError, ValueError):
        return []


def salvar_tempos(tempos):
    """Grava os melhores tempos no arquivo, um por linha."""
    with open(ARQUIVO_TEMPOS, 'w') as arquivo:
        for tempo in tempos:
            arquivo.write(f'{tempo}\n')


def registrar_tempo(tempo_ms):
    """Coloca o tempo novo no ranking e guarda só os 3 menores.

    Devolve (lista_dos_3_melhores, posição_do_tempo_novo). A posição é -1
    se o tempo novo não entrou no ranking.
    """
    tempos = ler_tempos()
    tempos.append(tempo_ms)
    tempos.sort()             # do menor (melhor) para o maior
    melhores = tempos[:3]     # fatiamento: só os 3 primeiros
    salvar_tempos(melhores)
    if tempo_ms in melhores:
        posicao = melhores.index(tempo_ms)
    else:
        posicao = -1
    return melhores, posicao


def ler_recorde():
    """Lê o recorde do arquivo. Se o arquivo não existir ainda, é 0."""
    try:
        with open(ARQUIVO_RECORDE, 'r') as arquivo:
            return int(arquivo.read())
    except (FileNotFoundError, ValueError):
        return 0


def salvar_recorde(pontos):
    """Grava o novo recorde no arquivo."""
    with open(ARQUIVO_RECORDE, 'w') as arquivo:
        arquivo.write(str(pontos))