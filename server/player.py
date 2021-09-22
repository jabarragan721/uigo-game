###
# attr info https://towardsdatascience.com/probably-the-best-practice-of-object-oriented-python-attr-d8c26c0e8a4
# attr página oficial https://www.attrs.org/
###
import attr

#TODO: Tiene muchos atributos, tal vez se pueda agrupar algunos en caracteristicas
@attr.s
class Player:
    name = attr.ib()
    body = attr.ib()
    hair = attr.ib()
    outfit = attr.ib()
    frame = attr.ib(init=False,default=0)
    dir = attr.ib(init=False,default='down')
    action = attr.ib(init=False,default='stop') # Esta action sobra.
    # no se elimina aún porque el front depende de este campo
    #TODO: Eliminar del front, al menos para que se use internamente
    chat = attr.ib(init=False,default='')
    #TODO: Revisar si se puede agrupar en posición
    posX = attr.ib(init=False,default=544)
    posY = attr.ib(init=False,default=800)
    H = attr.ib(init=False,default=48)
    W = attr.ib(init=False,default=32)
    Socket = attr.ib()
    max_health = attr.ib(init=False,default=50) #TODO: tal vez esto va en propiedades del juego?
    health = attr.ib(init=False,default=50)
    speed = attr.ib(init=False,default=3) #TODO: tal vez esto va en propiedades del juego?
    ruta = attr.ib(init=False,factory=dict)
    step = attr.ib(init=False,default=1)
    moves = attr.ib(init=False,default=0)
    weapons = attr.ib()
