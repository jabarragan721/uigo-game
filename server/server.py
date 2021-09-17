#!/usr/bin/env python
import asyncio
import json
import logging
import websockets
import maps
import threading
import time
import weapons
import ruta
import math
import os

from config import SERVER_CONF

logging.basicConfig()
users_pos={}
USERS = {}
maps.populate_tiles()
async def register_user(ws,map,nombre):
    USERS[ws] = {"mapa":map,"id":str(ws)}

async def encontrar(ws,new_map,WS):#encontrar y eliminar un persona del mapa
    results=[]
    player_target = {}
    for map in maps.world:
        for player in maps.world[map]["players"]:
            if player == ws:
                results.append(map)
                player_target = maps.world[map]["players"][player]
                break
    if results:
        maps.world[results[0]]["players"].pop(ws)
        new_map["players"][ws] = player_target
        USERS[WS]["mapa"]=new_map["map_name"]

async def stop_player(ws,map,map_name):
    if ws in map["players"]:
        map["players"][ws]["ruta"] = {}
        map["players"][ws]["action"] = "stop"
        map["players"][ws]["step"] = 1
        map["players"][ws]["moves"] = 0
        await send_update(ws,map_name)

async def update_player_position(map,dir,action,ws,step,moves):
    if ws in map["players"]:
        player = map["players"][ws]
        #TODO: Agregar una función de movimiento al player
        if dir == "up":
            player["posY"] -= player["speed"]
        elif dir == "down":
            player["posY"] += player["speed"]
        elif dir == "left":
            player["posX"] -= player["speed"]
        elif dir == "right":
            player["posX"] += player["speed"]
        player["frame"] += 1
        # action siempre es diferente de shoot, solo se envía walk para el
        # mensaje type walk
        if player["frame"] > 5 and action != "shoot":
            player["frame"] = 0
            player["action"] = action
        elif player["frame"] > 3:
            player["frame"] = 0
            player["action"] = "stop"
        player["dir"] = dir
        player["step"] = step
        player["moves"] = moves

async def player_refresh(map,map_name,posX,posY,ws,desX,desY):#Nuevo movimiento de jugador
    if ws in map["players"]:
        H = map["players"][ws]["H"]
        W = map["players"][ws]["W"]
        map["players"][ws]["posX"] = posX
        map["players"][ws]["posY"] = posY
        map["players"][ws]["ruta"] = ruta.calcular_ruta(posX,posY,W,H,desX,desY,map_name)
        map["players"][ws]["step"] = 1
        map["players"][ws]["moves"] = 0
        await send_update(ws,map_name)

async def new_attack(x1,y1,x2,y2,target,player,weapon):
    speed = weapons.clases[weapon]["speed"]
    sprite = weapons.clases[weapon]["sprite"]
    bullet = weapons.clases[weapon]["bullet"]
    width = weapons.clases[weapon]["width"]
    height = weapons.clases[weapon]["height"]
    animated = weapons.clases[weapon]["animated"]
    alcance = weapons.clases[weapon]["alcance"]
    dir = ""
    vx = x2-x1
    vy = y2-y1
    dist = math.sqrt(vx * vx + vy * vy)
    dx = vx / dist
    dy = vy / dist
    dx *= speed
    dy *= speed
    if x1 < x2 and y2 < y1:
        if abs(vx) > abs(vy):
            dir="right"
        else:
            dir="up"
    elif x1 > x2 and y2 < y1:
        if abs(vx) > abs(vy):
            dir="left"
        else:
            dir="up"
    elif x1 < x2 and y2 > y1:
        if abs(vx) > abs(vy):
            dir="right"
        else:
            dir="down"
    elif x1 > x2 and y2 > y1:
        if abs(vx) > abs(vy):
            dir="left"
        else:
            dir="down"
    elif x1 == x2 and y2 < y1:
        dir = "up"
    elif x1 == x2 and y2 > y1:
        dir = "down"
    elif x1 > x2 and y2 == y1:
        dir = "left"
    elif x1 < x2 and y2 == y1:
        dir = "right"
    for user in USERS:
        if player == USERS[user]["id"] or target == USERS[user]["id"]:
            data = {
                "type":"new_attack",
                "data":{
                    "dx":dx,
                    "dy":dy,
                    "speed":speed,
                    "sprite":sprite,
                    "bullet":bullet,
                    "width":width,
                    "height":height,
                    "animated":animated,
                    "alcance":alcance,
                    "w_dir":dir,
                    "frame":0,
                    "frame_ratio":0,
                    "x":x1,
                    "y":y1,
                    "player":player,
                    "dir":dir
                }
            }
            message = json.dumps(data)
            await user.send(message)

async def start_player(map,map_name,player_name,body,hair,outfit,ws,fase):# Parametros iniciales al conectarse
    #TODO Usar un constructor de un player
    map["players"][ws] = {
        "name": player_name,
        "body": body,
        "hair": hair,
        "outfit": outfit,
        "frame": 0,
        "dir": "down",
        "action": "stop",
        "chat": "",
        "posX": 544,
        "posY": 800,
        "H": 48,
        "W": 32,
        "Socket": ws,
        "max_health": 50,
        "health": 50,
        "speed": 3,
        "ruta": {},
        "step": 1,
        "moves": 0,
        "weapons": { #TODO Usar un constructor de weapons, probablemente dentro
                    #del constructor del player
            weapons.clases["normal_gun"]["name"]: weapons.clases["normal_gun"],
            weapons.clases["normal_bomerang"]["name"]: weapons.clases["normal_bomerang"]
        }
    }
    await send_start_message(ws,map_name,fase)

async def new_map_player(map,dir,posX,posY,ws):
    map["players"][ws]["dir"] = dir
    map["players"][ws]["action"] = "stop"
    map["players"][ws]["posX"] = posX
    map["players"][ws]["posY"] = posY
    map["players"][ws]["ruta"] = {}
    map["players"][ws]["step"] = 1
    map["players"][ws]["moves"] = 0

async def send_update(user_id,map_name):
    if USERS:
        for user in USERS:
            if map_name == USERS[user]["mapa"]:
                data = {
                    "data":maps.world[USERS[user]["mapa"]]["players"][user_id],
                    "type":"new_move"
                }
                message = json.dumps(data)
                await user.send(message)

async def send_msj(user_id,player_name,map_name,chat):
    if USERS:
        for user in USERS:
            translation_table = dict.fromkeys(map(ord, '<>/$@'), None)
            chat = chat.translate(translation_table)
            if map_name == USERS[user]["mapa"]:
                data = {
                    "data":chat,
                    "player":user_id,
                    "type":"new_msj",
                    "player_name":player_name
                }
                message = json.dumps(data)
                await user.send(message)

async def player_attacked(map,target,player,weapon,wx,wy):
    target_1_x = map["players"][target]["posX"]
    target_2_x = map["players"][target]["posX"] + map["players"][target]["W"]
    target_1_y = map["players"][target]["posY"]
    target_2_y = map["players"][target]["posY"] + map["players"][target]["H"]
    if wx>target_1_x and wx<target_2_x and wy>target_1_y and wy<target_2_y:
        dammage = weapons.clases[weapon]["dammage"]
        health = map["players"][target]["health"] - dammage
        if health<1:
            health = 0
        map["players"][target]["health"]-=dammage
        for user in USERS:
            if player == USERS[user]["id"] or target == USERS[user]["id"]:
                data = {
                    "type":"player_dammaged",
                    "data":{
                        "player":target,
                        "health": health,
                    }
                }
                message = json.dumps(data)
                await user.send(message)
'''
Envía un mensaje a todos los usuarios
Si el usuario es el mismo que se conectó, le envía el mensaje start
De lo contrario, valida que esté en el mismo mapa que el usuario que ingresó
    para notificarle que un usuario nuevo ingresó
'''
async def send_start_message(user_id,map_name,fase):
    if USERS:
        for user in USERS:
            if user_id == USERS[user]["id"]:
                message = json.dumps({
                "type":"start",
                "data":maps.world[USERS[user]["mapa"]],
                "id":user_id,
                "fase":fase})
                await user.send(message)
            elif map_name == USERS[user]["mapa"]:
                data = {
                    "data":maps.world[map_name]["players"][user_id],
                    "items":{},
                    "type":"new_player"
                }
                message = json.dumps(data)
                await user.send(message)

async def update_players(new_map,actual_map,user_id):
    if USERS:
        for user in USERS:
            if actual_map == USERS[user]["mapa"] and user_id != USERS[user]["id"]:
                data = {
                    "data":user_id,
                    "items":{},
                    "type":"player_out"
                }
                message = json.dumps(data)
                await user.send(message)
            elif new_map == USERS[user]["mapa"] and user_id != USERS[user]["id"]:
                data = {
                    "data":maps.world[USERS[user]["mapa"]]["players"][user_id],
                    "items":{},
                    "type":"new_player"
                }
                message = json.dumps(data)
                await user.send(message)
            elif new_map == USERS[user]["mapa"] and user_id == USERS[user]["id"]:
                message = json.dumps({"type":"new_map","data":maps.world[USERS[user]["mapa"]]})
                await user.send(message)

async def unregister_user(ws):
    USERS.pop(ws, None)
    for map in maps.world:
        for player in maps.world[map]["players"]:
            if player == str(ws):
                maps.world[map]["players"].pop(player)
                for user in USERS:
                    if map == USERS[user]["mapa"]:
                        data = {
                            "data":str(ws),
                            "type":"player_out"
                        }
                        message = json.dumps(data)
                        await user.send(message)
                break

async def action(websocket, path): #Escuchar acciones del cliente
    try:
         async for message in websocket:
            data = json.loads(message)
            if data['type']=='new_state':
                map=maps.world[data['map']]
                map_name=data['map']
                posX=data['posX']
                posY=data['posY']
                desX = data['desX']
                desY = data['desY']
                await player_refresh(map,map_name,posX,posY,str(websocket),desX,desY)
            elif data['type']=='new_position':
                map=maps.world[data['map']]
                dir=data['dir']
                step=data['step']
                moves=data['moves']
                action=data['action']
                await update_player_position(map,dir,action,str(websocket),step,moves)
            elif data['type']=='new_map':
                new_map=maps.world[data['new_map']]
                posX=data['posX']
                posY=data['posY']
                await encontrar(str(websocket),new_map,websocket)
                await new_map_player(new_map,dir,posX,posY,str(websocket))
                await update_players(data['new_map'],data['actual_map'],str(websocket))
            elif data['type']=='start':
                await register_user(websocket,data['map'],data['player_name'])
                map=maps.world[data['map']]
                map_name=data['map']
                fase = data['fase']
                player_name=data['player_name']
                body=data['body']
                hair=data['hair']
                outfit=data['outfit']
                await start_player(map,map_name,player_name,body,hair,outfit,str(websocket),fase)
            elif data['type']=='attack':
                map=maps.world[data['map']]
                target=data['ws']
                player=str(websocket)
                weapon=data['weapon']
                wx=data['Wx']
                wy=data['Wy']
                await player_attacked(map,target,player,weapon,wx,wy)
            elif data['type']=='dead_player':
                await unregister_user(websocket)
            elif data['type']=='stop':
                map_name=data['map']
                map=maps.world[data['map']]
                await stop_player(str(websocket),map,map_name)
            elif data['type']=='chat':
                map_name=data['map']
                player_name=data['player_name']
                chat=data['chat']
                await send_msj(str(websocket),player_name,map_name,chat)
            elif data['type']=='attack_action':
                target=data['target_id']
                player=str(websocket)
                px=data['px']
                py=data['py']
                tx=data['tx']
                ty=data['ty']
                weapon=data['weapon']
                await new_attack(px,py,tx,ty,target,player,weapon)
            else:
                logging.error(f'unsupported event: {data}')
    finally:
        await unregister_user(websocket)


#Desabilita la advertencia pylint, que se activa porque websockets hace un lazy load de las propiedades
#pylint: disable = no-member
start_server = websockets.serve(action, SERVER_CONF.IP, int(SERVER_CONF.PORT))
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
