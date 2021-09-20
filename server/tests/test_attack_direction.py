def new_attack(pos_player_x, pos_player_y, pos_target_x, pos_target_y):
    vx = pos_target_x - pos_player_x
    vy = pos_target_y - pos_player_y

    direction = ""
    if pos_player_x < pos_target_x and pos_target_y < pos_player_y:
        if abs(vx) > abs(vy):
            direction="right"
        else:
            direction="up"
    elif pos_player_x > pos_target_x and pos_target_y < pos_player_y:
        if abs(vx) > abs(vy):
            direction="left"
        else:
            direction="up"
    elif pos_player_x < pos_target_x and pos_target_y > pos_player_y:
        if abs(vx) > abs(vy):
            direction="right"
        else:
            direction="down"
    elif pos_player_x > pos_target_x and pos_target_y > pos_player_y:
        if abs(vx) > abs(vy):
            direction="left"
        else:
            direction="down"

    elif pos_player_x == pos_target_x and pos_target_y < pos_player_y:
        direction = "up"
    elif pos_player_x == pos_target_x and pos_target_y > pos_player_y:
        direction = "down"
    elif pos_player_x > pos_target_x and pos_target_y == pos_player_y:
        direction = "left"
    elif pos_player_x < pos_target_x and pos_target_y == pos_player_y:
        direction = "right"

    return direction

def new_attack_new(pos_player_x, pos_player_y, pos_target_x, pos_target_y):
    vx = pos_target_x - pos_player_x
    vy = pos_target_y - pos_player_y

    direction = ""
    if vx != 0 or vy != 0: # Si el player y target están en diferentes posiciones
        if abs(vx) > abs(vy):
            direction = "right" if (vx > 0) else "left"
        else:
            direction = "down" if (vy > 0) else "up"

    return direction

ppx = 5
ppy = 10
ptx = 5
pty = 10

na = new_attack(ppx, ppy, ptx, pty)
nan = new_attack_new(ppx, ppy, ptx, pty)
# Prueba están en la misma posición player y target
assert na == nan, f"Error with ppx: {ppx}, ppy: {ppy}, ptx: {ptx}, pty: {pty}, na: {na}, nan: {nan}"

ppx = 5
ppy = 10
ptx = 10
pty = 5

na = new_attack(ppx, ppy, ptx, pty)
nan = new_attack_new(ppx, ppy, ptx, pty)
assert na == nan, f"Error with ppx: {ppx}, ppy: {ppy}, ptx: {ptx}, pty: {pty}, na: {na}, nan: {nan}"

ppx = 5
ppy = 10
ptx = 5
pty = 5

na = new_attack(ppx, ppy, ptx, pty)
nan = new_attack_new(ppx, ppy, ptx, pty)
assert na == nan, f"Error with ppx: {ppx}, ppy: {ppy}, ptx: {ptx}, pty: {pty}, na: {na}, nan: {nan}"

import random
for n in range(1000):
    ppx = random.randrange(300)
    ppy = random.randrange(300)
    ptx = random.randrange(300)
    pty = random.randrange(300)
    na = new_attack(ppx, ppy, ptx, pty)
    nan = new_attack_new(ppx, ppy, ptx, pty)
    assert na == nan, f"Error with ppx: {ppx}, ppy: {ppy}, ptx: {ptx}, pty: {pty}, na: {na}, nan: {nan}"
    # print (f"Computed with ppx: {ppx}, ppy: {ppy}, ptx: {ptx}, pty: {pty}, na: {na}, nan: {nan}")

print("prueba exitosa")