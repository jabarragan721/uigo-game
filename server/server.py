#!/usr/bin/env python
import websockets
import asyncio
import math
import json
import logging
logging.basicConfig()

import maps
import weapons
from player import Player

from config import SERVER_CONF

users_pos={}
USERS = {}
maps.populate_tiles()

def register_user(ws, map_name, newPlayer):
    USERS[ws] = {
        "mapa" : map_name,
        "player" : newPlayer
    }

def move_to_new_map(ws, new_map_name):
    for map in maps.world.values():
        #Easier to ask for forgiveness than permission
        #https://docs.python.org/3/glossary.html#term-eafp
        try:
            player = map['players'].pop(ws)
            maps.world[new_map_name]['players'][ws] = player
            break
        except KeyError:
            pass

async def stop_player(ws, map_name):
    #Easier to ask for forgiveness than permission
    #https://docs.python.org/3/glossary.html#term-eafp
    try:
        player = maps.world[map_name]['players'][ws]
        player.stop()
        # No es necesario esperar a enviar el mensaje

        await send_update(ws, map_name)
    except KeyError:
        pass


def update_player_position(map_name, direction, ws, step, moves):
    #Easier to ask for forgiveness than permission
    #https://docs.python.org/3/glossary.html#term-eafp
    try:
        player = maps.world[map_name]['players'][ws]
        player.move(direction, step, moves)
    except KeyError:
        pass


async def player_refresh(map_name, posX, posY, ws, desX, desY):
    #Easier to ask for forgiveness than permission
    #https://docs.python.org/3/glossary.html#term-eafp
    try:
        player = maps.world[map_name]['players'][ws]
        player.refresh(posX, posY, desX, desY, map_name)
        await send_update(ws, map_name)
    except KeyError:
        pass

async def new_attack(pos_player_x, pos_player_y, pos_target_x, pos_target_y, target, player, weapon):
    player_weapon = weapons.clases[weapon]

    #TODO: Mover a weapon
    speed = player_weapon["speed"]
    sprite = player_weapon["sprite"]
    bullet = player_weapon["bullet"]
    width = player_weapon["width"]
    height = player_weapon["height"]
    animated = player_weapon["animated"]
    alcance = player_weapon["alcance"]# TODO: Cambiar a range

    vx = pos_target_x - pos_player_x
    vy = pos_target_y - pos_player_y
    dist = math.sqrt(vx * vx + vy * vy)

    dx = (vx / dist) * speed
    dy = (vy / dist) * speed

    direction = ""
    if vx != 0 or vy != 0: # Si el player y target están en diferentes posiciones
        if abs(vx) > abs(vy):
            direction = "right" if (vx > 0) else "left"
        else:
            direction = "down" if (vy > 0) else "up"


    for user in USERS:
        #TODO: Mover método de envíar información a player
        #User es igual a id y no hay que recorrer todo el array
        #TODO: Quitar el for sobra
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
                    "alcance":alcance, # Cambiar a range
                    "w_dir":direction,
                    "frame":0,
                    "frame_ratio":0,
                    "x":pos_player_x,
                    "y":pos_player_y,
                    "player":player,
                    "dir":direction
                }
            }
            message = json.dumps(data)
            await user.send(message)

async def start_player(map_name, player_name, body, hair, outfit, ws, fase):# Parametros iniciales al conectarse
    newPlayer = Player(player_name, body, hair, outfit, ws)
    register_user(ws, map_name, newPlayer)
    maps.world[map_name]['players'][ws] = newPlayer

    await send_start_message(ws,map_name,fase)

async def new_map_player(map,dir,posX,posY, ws):
    map["players"][ws]["dir"] = dir
    map["players"][ws]["posX"] = posX
    map["players"][ws]["posY"] = posY
    map["players"][ws]["ruta"] = {}
    map["players"][ws]["step"] = 1
    map["players"][ws]["moves"] = 0

async def send_update(ws, map_name):
    #Easier to ask for forgiveness than permission
    #https://docs.python.org/3/glossary.html#term-eafp
    try:
        players_map = maps.world[map_name]['players']
        player_updated = players_map[ws]
        data = {
            "type": "new_move",
            "data": player_updated.get_data()
        }

        for player in players_map.values():
            # No es necesario esperar a enviar un mensaje a un jugador para
            # envíar el otro
            # TODO: Revisar si se puede eliminar el await
            await player.sendData(data)
    except KeyError:
        pass

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

async def player_attacked(map_name, target, player, weapon, wx, wy):
    map_target = maps.world[map_name]['players'][target]
    target_1_x = map_target["posX"]
    target_2_x = map_target["posX"] + map_target["W"]
    target_1_y = map_target["posY"]
    target_2_y = map_target["posY"] + map_target["H"]
    if (wx > target_1_x
        and wx < target_2_x
        and wy > target_1_y
        and wy < target_2_y):
        dammage = weapons.clases[weapon]["dammage"]
        health = map_target["health"] - dammage
        if health<1:
            health = 0
        map_target["health"]-=dammage
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
async def send_start_message(user_id, map_name, fase):
    try:
        player_map = maps.world[map_name]
        players_in_map = player_map['players']
        player_started = players_in_map[user_id]

        data_player = {
            "type": "start",
            #TODO: Probablemente no toda la información sea necearia aqui
            # Dictionay Comprehension para quitar players de la info envíada
            # https://stackoverflow.com/a/17665928/1647238
            # players no se puede serializar
            "data": {key:player_map[key] for key in player_map if key != 'players'},
            "id": user_id,
            "fase": fase
        }

        data_everybody_else = {
            "type": "new_player",
            #TODO: Probablemente no toda la información sea necearia aqui
            "data": player_started.get_full_data(),
            "items": {}
        }

        for ws, player in players_in_map.items():
            # No es necesario esperar a enviar un mensaje a un jugador para
            # envíar el otro
            # TODO: Revisar si se puede eliminar el await
            data = data_player if (ws == user_id) else data_everybody_else
            await player.sendData(data)
    except KeyError:
        pass

async def update_players(new_map,actual_map,user_id):
    if USERS:
        #TODO: Mover a un método de player
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
                    "type":"new_player",
                    "data":maps.world[USERS[user]["mapa"]]["players"][user_id],
                    "items":{}
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
                map_name=data['map']
                posX=data['posX']
                posY=data['posY']
                desX = data['desX']
                desY = data['desY']
                await player_refresh(map_name,posX,posY,websocket,desX,desY)
            elif data['type']=='new_position':
                map_name=data['map']
                dir=data['dir']
                step=data['step']
                moves=data['moves']
                update_player_position(map_name,dir,websocket,step,moves)
            elif data['type'] == 'new_map':
                new_map_name = data['new_map']
                new_map = maps.world[new_map_name]
                posX = data['posX']
                posY = data['posY']
                await move_to_new_map(websocket, new_map_name)
                await new_map_player(new_map,dir,posX,posY,str(websocket))
                await update_players(data['new_map'],data['actual_map'],str(websocket))
            elif data['type']=='start':
                map_name=data['map']
                fase = data['fase']
                player_name=data['player_name']
                body=data['body']
                hair=data['hair']
                outfit=data['outfit']
                await start_player(map_name, player_name, body, hair, outfit, websocket, fase)
            elif data['type']=='attack':
                map_name=data['map']
                target=data['ws']
                player=str(websocket)
                weapon=data['weapon']
                wx=data['Wx']
                wy=data['Wy']
                await player_attacked(map_name,target,player,weapon,wx,wy)
            elif data['type']=='dead_player':
                await unregister_user(websocket)
            elif data['type']=='stop':
                map_name=data['map']
                await stop_player(websocket, map_name)
            elif data['type']=='chat':
                map_name=data['map']
                player_name=data['player_name']
                chat=data['chat']
                await send_msj(str(websocket),player_name,map_name,chat)
            # Se envía un ataque
            elif data['type']=='attack_action':
                target=data['target_id']
                player=str(websocket)
                #posición player
                px=data['px']
                py=data['py']
                #posición target
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
