import pygame 
from config import TAM_BLOCO
from sprites import Bloco
FASE_1 = [ '..............................................................',
 # ... (12 linhas no total; vejam o arquivo do exemplo) 
 '.J...........P.......C....A.....M...I...P.....A...C..M..I...F.',
 'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG..GGGGGGGGGGGGGGGGGGGGGGGGGG',
   'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT..TTTTTTTTTTTTTTTTTTTTTTTTTT', ] 
FASE_2 = [ ... ]
FASES = [FASE_1, FASE_2]
def construir_fase(mapa, assets): 
    """Percorre o mapa e cria um sprite para cada caractere.""" 
    grupos = { 'blocos': pygame.sprite.Group(),   # chão e plataformas (sólidos)
               'todos': pygame.sprite.Group(),  # usado para atualizar e desenhar 
               } 
    inicio = (0, 0)
    for linha in range(len(mapa)):
        for coluna in range(len(mapa[linha])): 
            letra = mapa[linha][coluna]          
            x = coluna * TAM_BLOCO           
            y = linha * TAM_BLOCO           
            chao_do_bloco = y + TAM_BLOCO   # base do quadradinho
            if letra == 'G':       
                novo = Bloco(assets['grama'], x, y)              
                grupos['blocos'].add(novo)               
                grupos['todos'].add(novo)           
            elif letra == 'T':               
                novo = Bloco(assets['terra'], x, y)               
                grupos['blocos'].add(novo)                  
                grupos['todos'].add(novo)            
            elif letra == 'B':                
                novo = Bloco(assets['bloco'], x, y)              
                grupos['blocos'].add(novo)                
                grupos['todos'].add(novo)            
            elif letra == 'J':                
                inicio = (x + TAM_BLOCO // 2, chao_do_bloco)
        largura_fase = len(mapa[0]) * TAM_BLOCO   
        return grupos, inicio, largura_fase
    
            