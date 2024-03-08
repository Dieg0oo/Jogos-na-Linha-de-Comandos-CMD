from os import system
from getpass import getpass
from time import sleep, time

whiteList = "qwertyuiopasdfghjklçzxcvbnm "

def desenharForca():
    top = ""
    middle1 = ""
    middle2 = ""
    bottom = ""

    if tentativa >= 1:
        top = "O"
    
    if tentativa >= 2:
        middle1 = " |"
        middle2 = "|"

    if tentativa >= 3:
        middle1 = " |\\"

    if tentativa >= 4:
        middle1 = "/|\\"

    if tentativa >= 5:
        bottom = "  \\"

    if tentativa == 6:
        bottom = "/ \\"

    print("\t----------")
    sleep(0.1)
    print("\t|/       |")
    sleep(0.1)
    print("\t|        " + top)
    sleep(0.1)
    print("\t|       " + middle1)
    sleep(0.1)
    print("\t|        " + middle2)
    sleep(0.1)
    print("\t|       " + bottom)
    sleep(0.1)
    print("\t|")
    sleep(0.1)
    print("--------------------")

def displayStats():
    sleep(0.25)
    desenharForca()
    sleep(0.25)
    print(adivinha.center(20))
    sleep(0.25)
    #print("Tentivas restantes: " + str(maxTentivas - tentativa))
    #time.sleep(0.25)
    print(str(erradas))

def ocultarPalavra(string,ignorar):
    ocultada = ""
    for letra in string:
        broke = False

        for ign in ignorar:
            if letra == ign:
                broke = True
                break
        if not letra == " ":
            if broke:
                ocultada += letra
            else:
                ocultada += "_"
        else:
            ocultada += " "

    return ocultada

resposta = "s"
while resposta == "s":
    palavra = getpass("Escolha a palavra: ").lower()
    palavra2 = ""
    for letra in palavra:
        if letra in whiteList:
            palavra2 += letra
    palavra = palavra2

    adivinhas = []
    certas = []
    erradas = []
    adivinha = ocultarPalavra(palavra,adivinhas)
    tentativa = 0
    maxTentivas = 6

    displayStats()
    comecou = time()
    while adivinha != palavra:
        sleep(0.5)
        letra = str(input("\nEscolha uma letra: ")).lower()
        letra = letra[0]
        if letra in adivinhas:
            print("Ja escolheste essa letra!")
            continue

        if not letra in palavra:
            tentativa += 1
            if tentativa >= maxTentivas:
                break
            erradas.append(letra)
        else:
            certas.append(letra)

        adivinhas.append(letra)
        adivinha = ocultarPalavra(palavra,adivinhas)

        system('cls')
        displayStats()

    if adivinha != palavra or tentativa >= maxTentivas:
        system('cls')
        displayStats()
        print("\n")
        print("Não conseguiste, a palavra era: " + palavra)
    else:
        print("\n")
        demorou = time() - comecou
        print("Parabéns! conseguiste acertar na " + str(tentativa) + "º tentativa!")
        print("Demoraste %.1f segundos" %(demorou))

    resposta = input("\n's' para jogar outra vez ").lower()
    system("cls")