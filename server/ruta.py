import maps
import math

def calcular_ruta(hx,hy,hw,hh,dx,dy,map):
    hero_x = hx
    hero_y = hy
    hero_w = hw
    hero_h = hh
    destino_x = math.floor(dx)-(hw/2)
    destino_y = math.floor(dy)-(hh/2)
    hero_map = map
    t_size = maps.world[hero_map]["t_size"]
    map_width = maps.world[hero_map]["cols"] * t_size
    map_height = maps.world[hero_map]["rows"] * t_size
    cuadrante = ""
    actual_move = ""
    previous_move = "stop"
    step = 0
    move_x=0
    move_y=0
    ruta={"steps":{}}

    if destino_x > hero_x and destino_y < hero_y:
        cuadrante = "NE"
    elif destino_x < hero_x and destino_y < hero_y:
        cuadrante = "NO"
    elif destino_x > hero_x and destino_y > hero_y:
        cuadrante = "SE"
    elif destino_x < hero_x and destino_y > hero_y:
        cuadrante = "SO"
    elif destino_x == hero_x and destino_y < hero_y:
        cuadrante = "N"
    elif destino_x == hero_x and destino_y > hero_y:
        cuadrante = "S"
    elif destino_x < hero_x and destino_y == hero_y:
        cuadrante = "O"
    elif destino_x > hero_x and destino_y == hero_y:
        cuadrante = "E"

    def free_place(x,y):
        for tile in maps.world[hero_map]["layers"]["blocked"]:
            tilex1 = tile["x"]
            tiley1 = tile["y"]
            tilex2 = tile["x"] + t_size
            tiley2 = tile["y"] + t_size
            if x < tilex2 and x > tilex1 and y < tiley2 and y > tiley1:
                return False
        return True

    def colision(x,y,h,w):
        herox1 = x
        heroy1 = y
        herox2 = x + w
        heroy2 = y + h
        for tile in maps.world[hero_map]["layers"]["blocked"]:
            tilex1 = tile["x"] + 5
            tiley1 = tile["y"] + t_size / 2.5
            tilex2 = tile["x"] + t_size - 5
            tiley2 = tile["y"] + t_size / 2
            if herox1 < tilex2 and herox2 > tilex1 and heroy1 < tiley2 and heroy2 > tiley1:
                return False
            elif herox2 > map_width or heroy2 > map_height:
                return False
        return True

    def conection(x,y,h,w):
        herox1 = x
        heroy1 = y
        herox2 = x + w
        heroy2 = y + h
        for tile in maps.world[hero_map]["layers"]["conections"]:
            tilex1 = tile["x"]
            tiley1 = tile["y"] + t_size / 2.5
            tilex2 = tile["x"] + t_size
            tiley2 = tile["y"] + t_size / 2
            if herox1 < tilex2 and herox2 > tilex1 and heroy1 < tiley2 and heroy2 > tiley1:
                return [True,tile["conect"],tile["conect_x"],tile["conect_y"]]
        return [False]

    if free_place(dx,dy):
        while hero_x != destino_x or hero_y != destino_y:
            if cuadrante == "NE":
                moves = [
                    colision(hero_x+2,hero_y,hero_h,hero_w),
                    colision(hero_x,hero_y-2,hero_h,hero_w),
                    colision(hero_x-2,hero_y,hero_h,hero_w),
                    colision(hero_x,hero_y+2,hero_h,hero_w)
                ]
                if moves[0] and moves[1] and hero_x < destino_x:
                    actual_move = "right"
                    if actual_move != previous_move:
                        move_x = 0
                        hero_x += 1
                        move_x += 1
                        step += 1
                        ruta["steps"][step]={"x":move_x}
                        previous_move = "right"
                    else:
                        hero_x += 1
                        move_x += 1
                        ruta["steps"][step]={"x":move_x}
                if not moves[0] and moves[1] and hero_x < destino_x:
                    actual_move = "up"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y -= 1
                        move_y -= 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "up"
                    else:
                        hero_y -= 1
                        move_y -= 1
                        ruta["steps"][step]={"y":move_y}
                if moves[1] and hero_x == destino_x and hero_y < destino_y:
                    actual_move = "down"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y += 1
                        move_y += 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "down"
                    else:
                        hero_y += 1
                        move_y += 1
                        ruta["steps"][step]={"y":move_y}
                if moves[1] and hero_x == destino_x and hero_y > destino_y:
                    actual_move = "up"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y -= 1
                        move_y -= 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "up"
                    else:
                        hero_y -= 1
                        move_y -= 1
                        ruta["steps"][step]={"y":move_y}
                if moves[0] and not moves[1] or not moves[0] and not moves[1]:
                    break
                Conection = conection(hero_x,hero_y,hero_h,hero_w)
                if Conection[0]:
                    actual_move = "stop"
                    if actual_move != previous_move:
                        step += 1
                        new_map = Conection[1]
                        c_x = Conection[2]
                        c_y = Conection[3]
                        ruta["steps"][step]={"c":{"map":new_map,"conect_x":c_x,"conect_y":c_y}}
                        previous_move = "stop"
                        break
            elif cuadrante == "NO":
                moves = [
                    colision(hero_x-2,hero_y,hero_h,hero_w),
                    colision(hero_x,hero_y-2,hero_h,hero_w),
                    colision(hero_x+2,hero_y,hero_h,hero_w),
                    colision(hero_x,hero_y+2,hero_h,hero_w)
                ]
                if moves[0] and moves[1] and hero_x > destino_x:
                    actual_move = "left"
                    if actual_move != previous_move:
                        move_x = 0
                        hero_x -= 1
                        move_x -= 1
                        step += 1
                        ruta["steps"][step]={"x":move_x}
                        previous_move = "left"
                    else:
                        hero_x -= 1
                        move_x -= 1
                        ruta["steps"][step]={"x":move_x}
                if not moves[0] and moves[1] and hero_x > destino_x:
                    actual_move = "up"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y -= 1
                        move_y -= 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "up"
                    else:
                        hero_y -= 1
                        move_y -= 1
                        ruta["steps"][step]={"y":move_y}
                if moves[1] and hero_x == destino_x and hero_y < destino_y:
                    actual_move = "down"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y += 1
                        move_y += 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "down"
                    else:
                        hero_y += 1
                        move_y += 1
                        ruta["steps"][step]={"y":move_y}
                if moves[1] and hero_x == destino_x and hero_y > destino_y:
                    actual_move = "up"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y -= 1
                        move_y -= 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "up"
                    else:
                        hero_y -= 1
                        move_y -= 1
                        ruta["steps"][step]={"y":move_y}
                if moves[0] and not moves[1] or not moves[0] and not moves[1]:
                    break
                Conection = conection(hero_x,hero_y,hero_h,hero_w)
                if Conection[0]:
                    actual_move = "stop"
                    if actual_move != previous_move:
                        step += 1
                        new_map = Conection[1]
                        c_x = Conection[2]
                        c_y = Conection[3]
                        ruta["steps"][step]={"c":{"map":new_map,"conect_x":c_x,"conect_y":c_y}}
                        previous_move = "stop"
                        break
            elif cuadrante == "SE":
                moves = [
                    colision(hero_x+2,hero_y,hero_h,hero_w),
                    colision(hero_x,hero_y+2,hero_h,hero_w),
                ]
                #print("x:"+str(hero_x)+" y:"+str(hero_y)+" R:"+str(moves[0])+" D:"+str(moves[1]))
                if moves[0] and moves[1] and hero_x < destino_x:
                    actual_move = "right"
                    if actual_move != previous_move:
                        move_x = 0
                        hero_x += 1
                        move_x += 1
                        step += 1
                        ruta["steps"][step]={"x":move_x}
                        previous_move = "right"
                    else:
                        hero_x += 1
                        move_x += 1
                        ruta["steps"][step]={"x":move_x}
                if not moves[0] and moves[1] and hero_x < destino_x:
                    actual_move = "down"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y += 1
                        move_y += 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "down"
                    else:
                        hero_y += 1
                        move_y += 1
                        ruta["steps"][step]={"y":move_y}
                if moves[1] and hero_x == destino_x and hero_y < destino_y:
                    actual_move = "down"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y += 1
                        move_y += 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "down"
                    else:
                        hero_y += 1
                        move_y += 1
                        ruta["steps"][step]={"y":move_y}
                if moves[1] and hero_x == destino_x and hero_y > destino_y:
                    actual_move = "up"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y -= 1
                        move_y -= 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "up"
                    else:
                        hero_y -= 1
                        move_y -= 1
                        ruta["steps"][step]={"y":move_y}
                if moves[0] and not moves[1] or not moves[0] and not moves[1]:
                    break
                Conection = conection(hero_x,hero_y,hero_h,hero_w)
                if Conection[0]:
                    actual_move = "stop"
                    if actual_move != previous_move:
                        step += 1
                        new_map = Conection[1]
                        c_x = Conection[2]
                        c_y = Conection[3]
                        ruta["steps"][step]={"c":{"map":new_map,"conect_x":c_x,"conect_y":c_y}}
                        previous_move = "stop"
                        break
            elif cuadrante == "SO":
                moves = [
                    colision(hero_x-2,hero_y,hero_h,hero_w),
                    colision(hero_x,hero_y+2,hero_h,hero_w),
                    colision(hero_x+2,hero_y,hero_h,hero_w),
                    colision(hero_x,hero_y-2,hero_h,hero_w)
                ]
                if moves[0] and moves[1] and hero_x > destino_x:
                    actual_move = "left"
                    if actual_move != previous_move:
                        move_x = 0
                        hero_x -= 1
                        move_x -= 1
                        step += 1
                        ruta["steps"][step]={"x":move_x}
                        previous_move = "left"
                    else:
                        hero_x -= 1
                        move_x -= 1
                        ruta["steps"][step]={"x":move_x}
                if not moves[0] and moves[1] and hero_x > destino_x:
                    actual_move = "down"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y += 1
                        move_y += 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "down"
                    else:
                        hero_y += 1
                        move_y += 1
                        ruta["steps"][step]={"y":move_y}
                if moves[1] and hero_x == destino_x and hero_y < destino_y:
                    actual_move = "down"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y += 1
                        move_y += 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "down"
                    else:
                        hero_y += 1
                        move_y += 1
                        ruta["steps"][step]={"y":move_y}
                if moves[1] and hero_x == destino_x and hero_y > destino_y:
                    actual_move = "up"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y -= 1
                        move_y -= 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "up"
                    else:
                        hero_y -= 1
                        move_y -= 1
                        ruta["steps"][step]={"y":move_y}
                if moves[0] and not moves[1] or not moves[0] and not moves[1]:
                    break
                Conection = conection(hero_x,hero_y,hero_h,hero_w)
                if Conection[0]:
                    actual_move = "stop"
                    if actual_move != previous_move:
                        step += 1
                        new_map = Conection[1]
                        c_x = Conection[2]
                        c_y = Conection[3]
                        ruta["steps"][step]={"c":{"map":new_map,"conect_x":c_x,"conect_y":c_y}}
                        previous_move = "stop"
                        break
            elif cuadrante == "N":
                moves = [
                    colision(hero_x,hero_y-2,hero_h,hero_w),
                    colision(hero_x,hero_y-2,hero_h,hero_w),
                    colision(hero_x-2,hero_y,hero_h,hero_w),
                    colision(hero_x,hero_y+2,hero_h,hero_w)
                ]
                if moves[0] and hero_y > destino_y:
                    actual_move = "up"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y -= 1
                        move_y -= 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "up"
                    else:
                        hero_y -= 1
                        move_y -= 1
                        ruta["steps"][step]={"y":move_y}
                else:
                    break
                Conection = conection(hero_x,hero_y,hero_h,hero_w)
                if Conection[0]:
                    actual_move = "stop"
                    if actual_move != previous_move:
                        step += 1
                        new_map = Conection[1]
                        c_x = Conection[2]
                        c_y = Conection[3]
                        ruta["steps"][step]={"c":{"map":new_map,"conect_x":c_x,"conect_y":c_y}}
                        previous_move = "stop"
                        break
            elif cuadrante == "S":
                moves = [
                    colision(hero_x,hero_y+2,hero_h,hero_w),
                    colision(hero_x,hero_y-2,hero_h,hero_w),
                    colision(hero_x-2,hero_y,hero_h,hero_w),
                    colision(hero_x,hero_y+2,hero_h,hero_w)
                ]
                if moves[0] and hero_y < destino_y:
                    actual_move = "down"
                    if actual_move != previous_move:
                        move_y = 0
                        hero_y += 1
                        move_y += 1
                        step += 1
                        ruta["steps"][step]={"y":move_y}
                        previous_move = "down"
                    else:
                        hero_y += 1
                        move_y += 1
                        ruta["steps"][step]={"y":move_y}
                else:
                    break
                Conection = conection(hero_x,hero_y,hero_h,hero_w)
                if Conection[0]:
                    actual_move = "stop"
                    if actual_move != previous_move:
                        step += 1
                        new_map = Conection[1]
                        c_x = Conection[2]
                        c_y = Conection[3]
                        ruta["steps"][step]={"c":{"map":new_map,"conect_x":c_x,"conect_y":c_y}}
                        previous_move = "stop"
                        break
            elif cuadrante == "E":
                moves = [
                    colision(hero_x+2,hero_y,hero_h,hero_w),
                    colision(hero_x,hero_y-2,hero_h,hero_w),
                    colision(hero_x-2,hero_y,hero_h,hero_w),
                    colision(hero_x,hero_y+2,hero_h,hero_w)
                ]
                if moves[0] and hero_x < destino_x:
                    actual_move = "right"
                    if actual_move != previous_move:
                        move_x = 0
                        hero_x += 1
                        move_x += 1
                        step += 1
                        ruta["steps"][step]={"x":move_x}
                        previous_move = "right"
                    else:
                        hero_x += 1
                        move_x += 1
                        ruta["steps"][step]={"x":move_x}
                else:
                    break
                Conection = conection(hero_x,hero_y,hero_h,hero_w)
                if Conection[0]:
                    actual_move = "stop"
                    if actual_move != previous_move:
                        step += 1
                        new_map = Conection[1]
                        c_x = Conection[2]
                        c_y = Conection[3]
                        ruta["steps"][step]={"c":{"map":new_map,"conect_x":c_x,"conect_y":c_y}}
                        previous_move = "stop"
                        break
            elif cuadrante == "O":
                moves = [
                    colision(hero_x-2,hero_y,hero_h,hero_w),
                    colision(hero_x,hero_y-2,hero_h,hero_w),
                    colision(hero_x-2,hero_y,hero_h,hero_w),
                    colision(hero_x,hero_y+2,hero_h,hero_w)
                ]
                if moves[0] and hero_x > destino_x:
                    actual_move = "left"
                    if actual_move != previous_move:
                        move_x = 0
                        hero_x -= 1
                        move_x -= 1
                        step += 1
                        ruta["steps"][step]={"x":move_x}
                        previous_move = "left"
                    else:
                        hero_x -= 1
                        move_x -= 1
                        ruta["steps"][step]={"x":move_x}
                else:
                    break
                Conection = conection(hero_x,hero_y,hero_h,hero_w)
                if Conection[0]:
                    actual_move = "stop"
                    if actual_move != previous_move:
                        step += 1
                        new_map = Conection[1]
                        c_x = Conection[2]
                        c_y = Conection[3]
                        ruta["steps"][step]={"c":{"map":new_map,"conect_x":c_x,"conect_y":c_y}}
                        previous_move = "stop"
                        break
    return ruta["steps"]
    #print(ruta["steps"])
