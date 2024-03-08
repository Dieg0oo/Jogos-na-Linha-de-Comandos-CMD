from time import sleep
from os import system
from config import *
from funcoes import *

resposta = None

if esta_em_menu:
    menu()

def rodarJogo():
    global resposta

    iniciarJogo()
    while True:
        while True:
            detetarResposta()
            desenharJogo()
            potencialmentePausar()

            if jogadorGanhou() or jogadorPerdeu():
                system("cls")
                break
            
            sleep(TEMPO_DE_ESPERA_POR_CADA_IMAGEM)
            atualizarTempo()
            system("cls")

        resposta = telaDeFimDeJogo()

        if resposta == "Y":
            rodarJogo()
        elif resposta == "M":
            menu()
            rodarJogo()
        elif resposta == "D":
            print("A sair...")
            sleep(1)
            print("Obrigado por jogar!")
            sleep(2)
            exit()

rodarJogo()