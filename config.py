"""Constantes do jogo: janela, cores, física, tempos e estados."""
# ----- Janela ----
LARGURA = 800
ALTURA = 480
FPS = 60 
TITULO = 'Raposa da Faquinha' 
TAM_BLOCO = 40    # cada quadradinho do mapa tem 40x40 pixels
# ----- Cores (R, G, B) ----
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AMARELO = (255, 220, 0)
VERMELHO = (220, 40, 40)
AZUL_CEU = (120, 190, 255)
# ----- Física do jogador ----
GRAVIDADE = 0.8         # quanto a velocidade vertical aumenta a cada frame
VEL_MAX_QUEDA = 15
VEL_PULO = -17          # negativo = para cima (o eixo y cresce para baixo)
VEL_ANDAR = 5
VEL_AGACHADO = 2
# ----- Regras ----
VIDAS_INICIAIS = 3
PONTOS_MOEDA = 10
PONTOS_INIMIGO = 50
PONTOS_CIPO = 30
# ----- Tempos (milissegundos) ----
TEMPO_INVENCIVEL = 1500
DURACAO_CORTE = 200
INTERVALO_CORTE = 400
TEMPO_FRAME = 100
# ----- Estados (qual tela está ativa) ----
SAIR = 0
INICIO = 1
INSTRUCOES = 2
JOGANDO = 3
GAME_OVER = 4
VITORIA = 5
ARQUIVO_RECORDE = 'recorde.txt'