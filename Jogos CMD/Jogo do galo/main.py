from os import system

winConditions = [
    # Horizontais
    ["A1","B1","C1"],
    ["A2","B2","C2"],
    ["A3","B3","C3"],

    # Verticais
    ["A1","A2","A3"],
    ["B1","B2","B3"],
    ["C1","C2","C3"],
    
    # Diagonais
    ["A1","B2","C3"],
    ["C1","B2","A3"]
]

def resetGame():
    global player,currentPlays
    player = "X"
    currentPlays = {
    "1": {"A": " ","B": " ","C": " "},
    "2": {"A": " ","B": " ","C": " "},
    "3": {"A": " ","B": " ","C": " "}
}
    
resetGame()

def drawGrid():
    system("cls")
    print("   A   B   C")
    for index,row in enumerate(currentPlays):
        index += 1
        row = currentPlays[str(row)]
        print(str(index) + "  " + row["A"] + " " + "|" + " " + row["B"] + " " + "|" + " " + row["C"])
        if index < 3:
            print("  ---|---|---")

def checkIfCellExists():
    try:
        currentPlays[cell[1]][cell[0]]
    except(KeyError):
        return False
    
    return True

def checkIfCellIsUnoccupied():
    if checkIfCellExists():
        return currentPlays[cell[1]][cell[0]] == " "

    return False

def checkWin():
    check = "X"
    for i in range(2):
        for i,_ in enumerate(winConditions):
            count = 0
            for play in winConditions[i]:
                if currentPlays[play[1]][play[0]] == check:
                    count += 1

            if count == 3:
                return check
            
        check = "O"
    
    return False

def checkTie():
    for _,line in currentPlays.items():
        for _,play in line.items():
            if play == " ":
                return False
            
    return True
            
resp = "s"
while resp == "s":
    drawGrid()
    cell = "Z9"

    while not checkIfCellExists() and not checkIfCellIsUnoccupied():
        cell = str(input("\nVez do "+player+": ")).upper()[:2]

    if checkIfCellIsUnoccupied():
        currentPlays[cell[1]][cell[0]] = player
        player = player == "O" and "X" or player == "X" and "O"
    else:
        print("A celula " + cell + " está ocupada!")

    win = checkWin()
    if win:
        drawGrid()
        print("\n" + win + " ganhou!")
    elif checkTie():
        drawGrid()
        print("\nEmpate!")
    else:
        continue

    resp = str(input("\n's' para jogar denovo: "))
    resetGame()

input("Obrigado por jogar! prima qualquer tecla para terminar...")