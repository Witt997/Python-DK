import pgzrun
import random

GRID_HEIGHT = 10
GRID_WIDTH = 10
GRID_SIZE = 50
WIDTH = GRID_WIDTH * GRID_SIZE
HEIGHT = GRID_HEIGHT * GRID_SIZE
GUARD_MOVE_INTERVAL = 0.5
PLAYER_MOVE_INTERVAL = 0.1
BACKGROUND_SEED = 123456

def screen_coords(x, y):
    return (x * GRID_SIZE, y * GRID_SIZE)

def grid_coords(actor):
    return (round(actor.x / GRID_SIZE), round(actor.y / GRID_SIZE))

def setup_game(difficulty):
    global game_over, player_won, player, keys_to_collect, guards, GRID_WIDTH, GRID_HEIGHT, WIDTH, HEIGHT, MAP
    if difficulty == "normale":
        GRID_WIDTH = 16
        GRID_HEIGHT = 12
        WIDTH = GRID_WIDTH * GRID_SIZE
        HEIGHT = GRID_HEIGHT * GRID_SIZE
        MAP = ["WWWWWWWWWWWWWWWW",
               "W              W",
               "W              W",
               "W  W  KG       W",
               "W  WWWWWWWWWW  W",
               "W              W",
               "W      P       W",
               "W  WWWWWWWWWW  W",
               "W      GK   W  W",
               "W              W",
               "W              D",
               "WWWWWWWWWWWWWWWW"]
    elif difficulty == "difficile":
        GRID_WIDTH = 20
        GRID_HEIGHT = 15
        WIDTH = GRID_WIDTH * GRID_SIZE
        HEIGHT = GRID_HEIGHT * GRID_SIZE
        MAP = ["WWWWWWWWWWWWWWWWWWWW",
               "W         W        W",
               "W         W        W",
               "W   W          W   D",
               "W   W G K      W   W",
               "W   WWWWWWWWWWWW   W",
               "W                  W",
               "W                  W",
               "W   WWWWW  WWWWW   W",
               "W   W      W  KW   W",
               "W   W  P   WG  W   W",
               "W   WWWWWWW    W   W",
               "W     G            W",
               "W     K            W",
               "WWWWWWWWWWWWWWWWWWWW"]

    game_over = False
    player_won = False
    player = Actor("player", anchor=("left", "top"))
    keys_to_collect = []
    guards = []
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            square = MAP[y][x]
            if square == "P":
                player.pos = screen_coords(x, y)
            elif square == "K":
                key = Actor("key", anchor=("left", "top"), pos=screen_coords(x, y))
                keys_to_collect.append(key)
            elif square == "G":
                guard = Actor("guard", anchor=("left", "top"), pos=screen_coords(x, y))
                guards.append(guard)

def draw_scenery():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            square = MAP[y][x]
            if square == "W":
                screen.blit("wall", screen_coords(x, y))
            elif square == "D" and len(keys_to_collect) == 0:
                screen.blit("door", screen_coords(x, y))

def draw_actors():
    player.draw()
    for key in keys_to_collect:
        key.draw()
    for guard in guards:
        guard.draw()

def draw_game_over():
    screen_middle = (WIDTH / 2, HEIGHT / 2)
    screen.draw.text("GAME OVER", midbottom=screen_middle, fontsize=GRID_SIZE, color="cyan", owidth=1)
    if player_won:
        screen.draw.text("Hai vinto!", midtop=screen_middle, fontsize=GRID_SIZE, color="green", owidth=1)
    else:
        screen.draw.text("Hai perso!", midtop=screen_middle, fontsize=GRID_SIZE, color="red", owidth=1)
    screen.draw.text("Premi SPAZIO per rigiocare", midtop=(WIDTH / 2, HEIGHT / 2 + GRID_SIZE), fontsize=GRID_SIZE / 2, color="cyan", owidth=1)

def draw_background():
    random.seed(BACKGROUND_SEED)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if x % 2 == y % 2:
                screen.blit("floor1", screen_coords(x, y))
            else:
                screen.blit("floor2", screen_coords(x, y))
            n = random.randint(0, 99)
            if n < 5:
                screen.blit("crack1", screen_coords(x, y))
            elif n < 10:
                screen.blit("crack2", screen_coords(x, y))

def draw():
    draw_background()
    draw_scenery()
    draw_actors()
    if game_over:
        draw_game_over()

def on_key_up(key):
    global game_over
    if key == keys.SPACE and game_over:
        setup_game("normale")
        game_over = False

def on_key_down(key):
    if key == keys.LEFT:
        move_player(-1, 0)
    elif key == keys.UP:
        move_player(0, -1)
    elif key == keys.RIGHT:
        move_player(1, 0)
    elif key == keys.DOWN:
        move_player(0, 1)

def move_player(dx, dy):
    global game_over, player_won
    if game_over:
        return
    (x, y) = grid_coords(player)
    x += dx
    y += dy
    square = MAP[y][x]
    if square == "W":
        return
    elif square == "D":
        if len(keys_to_collect) > 0:
            return
        else:
            game_over = True
            player_won = True
    for key in keys_to_collect:
        (key_x, key_y) = grid_coords(key)
        if x == key_x and y == key_y:
            keys_to_collect.remove(key)
            break
    animate(player, pos=screen_coords(x, y), duration=PLAYER_MOVE_INTERVAL, on_finished=repeat_player_move)

def repeat_player_move():
    if keyboard.left:
        move_player(-1, 0)
    if keyboard.up:
        move_player(0, -1)
    if keyboard.right:
        move_player(1, 0)
    if keyboard.down:
        move_player(0, 1)

def move_guard(guard):
    global game_over
    if game_over:
        return
    (player_x, player_y) = grid_coords(player)
    (guard_x, guard_y) = grid_coords(guard)
    if player_x > guard_x and MAP[guard_y][guard_x + 1] != "W":
        guard_x += 1
    elif player_x < guard_x and MAP[guard_y][guard_x - 1] != "W":
        guard_x -= 1
    elif player_y > guard_y and MAP[guard_y + 1][guard_x] != "W":
        guard_y += 1
    elif player_y < guard_y and MAP[guard_y - 1][guard_x] != "W":
        guard_y -= 1
    animate(guard, pos=screen_coords(guard_x, guard_y), duration=GUARD_MOVE_INTERVAL)
    if guard_x == player_x and guard_y == player_y:
        game_over = True

def move_guards():
    for guard in guards:
        move_guard(guard)

def start_game():
    difficulty = None
    while difficulty not in ["1", "2"]:
        difficulty = input("Scelta difficoltà (1/2): ")
    if difficulty == "1":
        setup_game("normale")
    elif difficulty == "2":
        setup_game("difficile")
    draw()
    clock.schedule_interval(move_guards, GUARD_MOVE_INTERVAL)
    pgzrun.go()

start_game()
