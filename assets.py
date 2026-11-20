"""Carregamento de imagens, sons e fontes (os "assets" do jogo)."""
import os
import pygame

PASTA_IMG = os.path.join('assets', 'img')
PASTA_SND = os.path.join('assets', 'snd')

# Tamanho final de cada imagem no jogo (os sprites são redimensionados)
TAMANHO_RAPOSA = (66, 64)
TAMANHO_INIMIGO = (50, 64)
TAMANHO_MOEDA = (24, 24)


def carregar_imagem(nome, tamanho=None):
    """Carrega uma imagem de assets/img e, se pedido, muda o tamanho."""
    imagem = pygame.image.load(os.path.join(PASTA_IMG, nome)).convert_alpha()
    if tamanho is not None:
        imagem = pygame.transform.scale(imagem, tamanho)
    return imagem


def carregar_animacao(pasta, tamanho):
    """Carrega todas as .png de uma pasta, em ordem alfabética.
    Cada imagem é um quadro (frame) da animação."""
    caminho = os.path.join(PASTA_IMG, pasta)
    nomes = sorted(os.listdir(caminho))
    quadros = []
    for nome in nomes:
        if nome.endswith('.png'):
            quadros.append(carregar_imagem(os.path.join(pasta, nome), tamanho))
    return quadros


def carregar_som(nome, volume=0.5):
    som = pygame.mixer.Sound(os.path.join(PASTA_SND, nome))
    som.set_volume(volume)
    return som


def load_assets():
    """Carrega todos os assets e devolve um dicionário com eles."""
    assets = {}

    # Animações da raposa: dicionário {nome: lista de quadros}
    assets['raposa'] = {}
    for animacao in ['parado', 'andando', 'pulando', 'agachado', 'dano']:
        assets['raposa'][animacao] = carregar_animacao(os.path.join('raposa', animacao), TAMANHO_RAPOSA)

    assets['inimigo'] = carregar_animacao('inimigo', TAMANHO_INIMIGO)
    assets['moeda'] = carregar_animacao('moeda', TAMANHO_MOEDA)

    assets['grama'] = carregar_imagem('grama.png', (40, 40))
    assets['terra'] = carregar_imagem('terra.png', (40, 40))
    assets['bloco'] = carregar_imagem('bloco.png', (40, 40))
    assets['espinhos'] = carregar_imagem('espinhos.png', (40, 30))
    assets['provas'] = carregar_imagem('provas.png', (40, 400))
    assets['galho'] = carregar_imagem('galho.png', (40, 360))
    assets['bandeira'] = carregar_imagem('bandeira.png', (40, 120))
    assets['corte'] = carregar_imagem('corte.png', (50, 50))
    assets['coracao'] = carregar_imagem('coracao.png', (24, 22))
    assets['fundo'] = carregar_imagem('fundo.png', (800, 480))
    assets['predios'] = carregar_imagem('predios.png', (800, 480))

    # Os sons entram na Etapa 10. As fontes, já:
    assets['fonte_grande'] = pygame.font.Font(None, 72)
    assets['fonte_media'] = pygame.font.Font(None, 40)
    assets['fonte_pequena'] = pygame.font.Font(None, 28)
    return assets