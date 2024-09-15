from model import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    if type(agent) is Semaforo:
        if agent.color == 'verde':
            portrayal = {"Shape": "rect",
                        "w": 1,
                        "h": 1,
                        "Filled": "true",
                        "Layer": 1,
                        "Color": "green"}
        elif agent.color == 'amarillo':
            portrayal = {"Shape": "rect",
                        "w": 1,
                        "h": 1,
                        "Filled": "true",
                        "Layer": 1,
                        "Color": "yellow"}
        elif agent.color == 'rojo':
            portrayal = {"Shape": "rect",
                        "w": 1,
                        "h": 1,
                        "Filled": "true",
                        "Layer": 1,
                        "Color": "red"}
        else:
            portrayal = {"Shape": "rect",
                        "w": 1,
                        "h": 1,
                        "Filled": "true",
                        "Layer": 1,
                        "Color": "black"}

    if type(agent) is Edificio:
        portrayal = {"Shape": "rect",
                "w": 1,
                "h": 1,
                "Filled": "true",
                "Layer": 0,
                "Color": "#4FA7FF"}

    if type(agent) is Estacionamiento:
        portrayal = {"Shape": "rect",
                "w": 1,
                "h": 1,
                "Filled": "true",
                "Layer": 0,
                "Color": "orange"}

    if type(agent) is Glorieta:
        portrayal = {"Shape": "rect",
                "w": 1,
                "h": 1,
                "Filled": "true",
                "Layer": 0,
                "Color": "brown"}

    if type(agent) is Banqueta:
        portrayal = {"Shape": "rect",
                "w": 1,
                "h": 1,
                "Filled": "true",
                "Layer": 1,
                "Color": "grey"}

    if type(agent) is Calle:
        portrayal = {"Shape": "rect",
                "w": 1,
                "h": 1,
                "Filled": "true",
                "Layer": 0,
                "Color": "#ccc"}

    if type(agent) is Parada:
        portrayal = {"Shape": "rect",
                "w": .5,
                "h": .5,
                "Filled": "true",
                "Layer": 3,
                "Color": "black"}

    if type(agent) is Cruce:
        portrayal = {"Shape": "rect",
                "w": .4,
                "h": .4,
                "Filled": "true",
                "Layer": 1,
                "Color": "white"}

    if type(agent) is CarroReactivo:
        portrayal = {"Shape": "circle",
                "r": .5,
                "Filled": "true",
                "Layer": 5,
                "Color": "#F300FF"}

    if type(agent) is CarroInteligente:
        portrayal = {"Shape": "circle",
                "r": .5,
                "Filled": "true",
                "Layer": 5,
                "Color": "#36FF00"}

    if type(agent) is Autobus:
        portrayal = {"Shape": "circle",
                "r": .5,
                "Filled": "true",
                "Layer": 5,
                "Color": "#F7FFA9"}

    if type(agent) is Peaton:
        portrayal = {"Shape": "circle",
                "r": .6,
                "Filled": "true",
                "Layer": 5,
                "Color": "#2ff7e7"}

    if type(agent) is Perro:
        portrayal = {"Shape": "circle",
                "r": .4,
                "Filled": "true",
                "Layer": 5,
                "Color": "#761F0F"}

    return portrayal


ancho = 33
alto = 33
grid = CanvasGrid(agent_portrayal, ancho, alto, 400, 400)
server = ModularServer(Ciudad,
                       [grid],
                       "City",
                       {"carrosrect": 20, "carrosint": 150, "autobuses": 0, "peatones": 200, "perros": 10})
server.port = 8521 # The default
server.launch()
