from config import *
from random import randint, shuffle
from keyboard import is_pressed
from os import get_terminal_size, chdir, system
from math import ceil
from time import sleep
from pygame import mixer
mixer.init()

chdir("D:/Python/Jogo de trabalho projeto")

TEMPO_DE_ESPERA_POR_CADA_IMAGEM = 1 / FPS
TOTAL_CARTAS = CARTAS_HORIZONTAIS * CARTAS_VERTICAIS
COORDENADAS_HORIZONTAIS_EXISTENTES = COORDENADAS_HORIZONTAIS[:CARTAS_HORIZONTAIS]
COORDENADAS_VERTICAIS_EXISTENTES = COORDENADAS_VERTICAIS[:CARTAS_VERTICAIS]

tempo_limite = 10
tempo_atual = 0
ganhou = None

cartas = []
pares = None
cartas_visiveis = [{}] * 2

sequencia = ""
pausar = False

esta_em_menu = True

def resetarJogo():
    global tempo_atual, ganhou, cartas, pares, cartas_visiveis, sequencia, pausar

    tempo_atual = 0
    ganhou = None

    cartas = []
    pares = None
    cartas_visiveis = [{}] * 2

    sequencia = ""
    pausar = False

def menu():
    global esta_em_menu

    esta_em_menu = True

    mixer.music.load("Tema.mp3")
    mixer.music.play(loops=-1)

    while True:
        tamanho_horizontal_consola = get_terminal_size().columns
        tamanho_vertical_consola = get_terminal_size().lines

        for _ in range((tamanho_vertical_consola // 2) - 3):
            print()

        print("Jogo da Memoria".center(tamanho_horizontal_consola))
        print()
        print("Pressione ENTER para começar".center(tamanho_horizontal_consola))

        if is_pressed("enter"):
            break

        sleep(TEMPO_DE_ESPERA_POR_CADA_IMAGEM)
        system("cls")

    mixer.music.stop()
    sleep(1)
    esta_em_menu = False

def fazerParesDeCartas():
    global pares
    IDs = list(range(1, TOTAL_CARTAS + 1))

    shuffle(IDs)
    pares = list(zip(IDs[::2], IDs[1::2]))

    for cartaV in cartas:
        for cartaH in cartaV:
            for par in pares:
                if cartaH["ID"] == par[0]:
                    cartaH["Par"] = par[1]
                elif cartaH["ID"] == par[1]:
                    cartaH["Par"] = par[0]
  
def escolherConteudoParaCadaPar():
    escolhidos = []

    for par in pares:
        conteudo = CONTEUDOS_POSSIVEIS[randint(0, len(CONTEUDOS_POSSIVEIS) - 1)]
        
        while escolhidos.count(conteudo) > 0:
            conteudo = CONTEUDOS_POSSIVEIS[randint(0, len(CONTEUDOS_POSSIVEIS) - 1)]
        
        escolhidos.append(conteudo)

        for cartaV in cartas:
            for cartaH in cartaV:
                if cartaH["Par"] == par[0] or cartaH["Par"] == par[1]:
                    cartaH["Conteúdo"] = conteudo

def criarCartas():
    # Esta funcao vai servir para criar as cartas
    # Todas as cartas vao tar dentro do array "cartas"
    # Esse array vai ter arrays de dicionarios -> {}
    # Cada {} ou dicionario corresponde a uma carta

    contador = 0
    for cartaV in range(CARTAS_VERTICAIS):
        cartas.append([])
        
        for _ in range(CARTAS_HORIZONTAIS):
            contador += 1
            conteudo = CONTEUDOS_POSSIVEIS[randint(0, len(CONTEUDOS_POSSIVEIS) - 1)]

            carta = {
                "Conteúdo": conteudo,  
                "Visível": False,
                "ID": contador,
                "Par": None}
            
            cartas[cartaV].append(carta)

def detetarResposta():
    global sequencia, pausar

    for posicao_horizontal in range(len(COORDENADAS_HORIZONTAIS_EXISTENTES)):
        quebrou = False
        coordenada_horizontal = COORDENADAS_HORIZONTAIS_EXISTENTES[posicao_horizontal]

        if is_pressed(coordenada_horizontal) and sequencia == "":
            sequencia = coordenada_horizontal

            for posicao_vertical in range(len(COORDENADAS_VERTICAIS_EXISTENTES)):
                coordenada_vertical = COORDENADAS_VERTICAIS_EXISTENTES[posicao_vertical]

                if is_pressed(coordenada_vertical) and sequencia[0] == coordenada_horizontal:
                    sequencia = coordenada_horizontal + coordenada_vertical

                    carta = cartas[posicao_vertical][posicao_horizontal]

                    if carta["Visível"] == False:
                        carta["Visível"] = True

                        if cartas_visiveis[0] == {}:
                            cartas_visiveis[0] = carta
                        elif cartas_visiveis[1] == {} and cartas_visiveis[0] != carta:
                            pausar = True
                            cartas_visiveis[1] = carta

                        quebrou = True
                        break
                    else:
                        sequencia = ""
        else:
            sequencia = ""

        if quebrou:
            break

def desenharJogo():
    tamanho_horizontal_consola = get_terminal_size().columns
    tamanho_vertical_consola = get_terminal_size().lines

    linhas_ocupadas_por_imagem = (5 + (CARTAS_VERTICAIS * ALTURA_CARTA) + (ESPACO_VERTICAL_ENTRE_CARTAS * (CARTAS_VERTICAIS - 1)))
    for _ in range(tamanho_vertical_consola // 2 - linhas_ocupadas_por_imagem // 2):
        print()

    print(f"Tempo restante: {ceil(tempo_limite - tempo_atual)}".center(tamanho_horizontal_consola))
    print(("-" * 25).center(tamanho_horizontal_consola))

    # Desenhar coordenadas do topo (horizontais)
    linha_coordenadas = ""
    for posicao in range(CARTAS_HORIZONTAIS):
        letra = COORDENADAS_HORIZONTAIS[posicao]     # Obtemos a letra na string "COORDENADA_HORIZONTAL" com a nossa posicao atual
        if is_pressed(letra):                        # Se essa letra tiver a ser pressionada no teclado
            letra = letra.lower()                    # Metemos essa letra em minusculas

        linha_coordenadas += letra.center(LARGURA_CARTA+2)

        # Enquanto a posicao nao for a ultima
        # adicionamos o espacamento entre as cartas
        if posicao + 1 < CARTAS_HORIZONTAIS:
            linha_coordenadas += " " * ESPACO_HORIZONTAL_ENTRE_CARTAS
        
    print(linha_coordenadas.center(tamanho_horizontal_consola))
    print(("-" * len(linha_coordenadas)).center(tamanho_horizontal_consola))

    # Desenhar cartas assim como coordenadas verticais
    for cartaV in range(1, CARTAS_VERTICAIS + 1):
        for altura in range(1, ALTURA_CARTA + 1):
            linha = "" # A linha inicialmente é uma string vazia

            if altura == ceil(ALTURA_CARTA / 2):
                linha += str(cartaV).center(LARGURA_CARTA) + "|"
            else:
                linha += (" " * LARGURA_CARTA) + "|"
            
            linha += " " * ESPACO_HORIZONTAL_ENTRE_CARTAS
            
            for cartaH in range(1, CARTAS_HORIZONTAIS + 1): # Depois neste loop vamos "calcular" como seria essa linha
                if altura == 1:
                    linha += SIMBOLO_SUPERIOR_ESQUERDO + (SIMBOLO_HORIZONTAL * LARGURA_CARTA) + SIMBOLO_SUPERIOR_DIREITO
                elif altura == ALTURA_CARTA:
                    linha += SIMBOLO_INFERIOR_ESQUERDO + (SIMBOLO_HORIZONTAL * LARGURA_CARTA) + SIMBOLO_INFERIOR_DIREITO
                elif altura == ceil(ALTURA_CARTA / 2):
                    carta_em_cartas = cartas[cartaV-1][cartaH-1]
                    conteudo_a_mostrar = ""

                    if carta_em_cartas["Visível"] == True:
                        conteudo_a_mostrar = carta_em_cartas["Conteúdo"].center(LARGURA_CARTA)
                    else:
                        conteudo_a_mostrar = " " * LARGURA_CARTA

                    linha += SIMBOLO_VERTICAL + conteudo_a_mostrar + SIMBOLO_VERTICAL
                else:
                    linha += SIMBOLO_VERTICAL + (" " * LARGURA_CARTA) + SIMBOLO_VERTICAL

                if cartaH < CARTAS_HORIZONTAIS:
                    linha += (" " * ESPACO_HORIZONTAL_ENTRE_CARTAS)
                
            espaco_ocupado_por_coordenadas_verticais = LARGURA_CARTA + 1 + ESPACO_HORIZONTAL_ENTRE_CARTAS
            linha = linha.center(tamanho_horizontal_consola)
            linha = linha[espaco_ocupado_por_coordenadas_verticais//2:]
            print(linha)


        if cartaV > 0 and cartaV <= CARTAS_VERTICAIS:
            for _ in range(ESPACO_VERTICAL_ENTRE_CARTAS):
                tamanho_todo = len(linha)
                tamanho_sem_espacos_a_direita = len(linha.lstrip())
                resultado = tamanho_todo - tamanho_sem_espacos_a_direita
                print((" " * resultado) + "|")

    # for cartaV in cartas:
    #     for cartaH in cartaV:
    #         print(cartaH)

def potencialmentePausar():
    global sequencia, pausar
    if pausar:
        sleep(1)

        if cartas_visiveis[0]["Conteúdo"] != cartas_visiveis[1]["Conteúdo"]:
            cartas_visiveis[0]["Visível"] = False
            cartas_visiveis[1]["Visível"] = False

        cartas_visiveis[0] = {}
        cartas_visiveis[1] = {}

        sequencia = ""
        pausar = False

def jogadorGanhou():
    global ganhou

    for cartaV in cartas:
        for cartaH in cartaV:
            if cartaH["Visível"] == False:
                return False
    
    ganhou = True
    return ganhou

def jogadorPerdeu():
    global ganhou

    perdeu = tempo_atual >= tempo_limite
    if perdeu:
        ganhou = False

    return perdeu

def atualizarTempo():
    global tempo_atual
    tempo_atual += TEMPO_DE_ESPERA_POR_CADA_IMAGEM

def iniciarJogo():
    resetarJogo()
    # Antes de iniciar o jogo temos que ter a certeza que nao existe nenhum erro que possa afetar o jogo
    # Informar o utilizador sobre o erro
    # Esperar 5 segundos ate que o jogo feche

    if TOTAL_CARTAS % 2 != 0:
        # Se o total de cartas for um numero impar

        print('O jogo nao pode começar, total de cartas tem que ser par.')
        sleep(5)
        exit()
    
    if (CARTAS_HORIZONTAIS > len(COORDENADAS_HORIZONTAIS)) or (CARTAS_VERTICAIS > len(COORDENADAS_VERTICAIS)):
        # Se o numero de cartas horizontais ou verticais
        # for maior que o numero disponivel de coordenadas
        
        print('O jogo nao pode comecar, numero de cartas excedem coordenadas disponiveis')
        sleep(5)
        exit()

    # Depois de ver todos os erros
    # e ver que nao ha nenhum,
    # podemos entao iniciar o jogo

    criarCartas()
    fazerParesDeCartas()
    escolherConteudoParaCadaPar()

def telaDeFimDeJogo():
    tamanho_horizontal_consola = get_terminal_size().columns
    if ganhou == True:
        mixer.music.load("Ganhar.mp3")
        mixer.music.play()
        print("Parabéns!".center(tamanho_horizontal_consola))
        sleep(1)
        print("Ganhaste o jogo!".center(tamanho_horizontal_consola))
        sleep(1)
        print("Deves ter uma memória mesmo boa!".center(tamanho_horizontal_consola))
        sleep(1)
        print()
        print("Demoraste: %d".center(tamanho_horizontal_consola) %(tempo_atual))
        sleep(2)
        print()
        print("Continuar?".center(tamanho_horizontal_consola))
        print("(Y) Sim     (M) Menu     (D) Sair".center(tamanho_horizontal_consola))
    elif ganhou == False:
        mixer.music.load("Perder.mp3")
        mixer.music.play()
        print("Perdeste".center(tamanho_horizontal_consola))
        sleep(1)
        print(":(".center(tamanho_horizontal_consola))
        sleep(2)
        print()
        print("Jogar denovo?".center(tamanho_horizontal_consola))
        print("(Y) Sim     (M) Menu     (D) Desistir".center(tamanho_horizontal_consola))
    
    while not is_pressed("Y") or not is_pressed("M") or not is_pressed("D"):
        if is_pressed("Y"):
            return "Y"
        elif is_pressed("M"):
            return "M"
        elif is_pressed("D"):
            return "D"