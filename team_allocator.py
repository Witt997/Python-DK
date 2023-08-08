import random
players = []
print("Benvenuto su Team Allocator!")
number_of_players = int(input("Quanti sono i giocatori? "))
for i in range(1, number_of_players +1):
    players.append(i)
while True:
    random.shuffle(players)
    response = input("È uno sport di squadra o individuale? \
                     Digita squadra o individuale: ")
    if response == "squadra":
        team1 = players[:len(players)//2]
        print("Capitano Team 1: " + str(random.choice(team1)))
        print("Team 1:")
        for player in team1:
            print(player)
        team2 = players[len(players)//2:]
        print("Capitano Team 2: " + str(random.choice(team2)))
        print("Team 2:")
        for player in team2:
            print(player)
    else:
        for i in range (0, 20, 2):
            print(str(players[i]) + " vs " + str(players[i+1]))
            start = random.randrange(i, i+2)
            print("Comincia " + str(players[start]))
    response = input("Riselezionare le squadre? Digita s o n: ")
    if response == "n":
        break



