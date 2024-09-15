import mesa
from coordenadas import semaforos, edificios, estacionamientos, glorieta_coor, calle_coor, banquetas_coor, paradas, cruces, spawn_carros
import networkx as nx
from Dijkstra import nodes, edges

# ----------------------------------AGENTES----------------------------------
# Se visualiza y funciona
class Semaforo(mesa.Agent):
    def __init__(self, name, color, model):
        super().__init__(name, model)
        self.name = name
        self.color = color
        if self.color == 'verde':
            self.contador = 0
        elif self.color == 'rojo':
            self.contador = 16
            
    def step(self):
        self.colorChange()
        self.contador += 1

    def colorChange(self):
        if self.contador < 10:
            self.color = 'verde'
        elif self.contador > 10 and self.contador <= 14:
            self.color = 'amarillo'
        elif self.contador > 14 and self.contador <= 24:
            self.color = 'rojo'
        elif self.contador > 24:
            self.contador = 0

# Se visualiza
class Edificio(mesa.Agent):
    def __init__(self, name, model):
        super().__init__(name, model)
        self.name = name

    def step(self):
        ...

# Se visualiza
class Estacionamiento(mesa.Agent):
    def __init__(self, name, model):
        super().__init__(name, model)
        self.name = name

    def step(self):
        ...

# Se visualiza
class Glorieta(mesa.Agent):
    def __init__(self, name, model):
        super().__init__(name, model)
        self.name = name

    def step(self):
        ...

# Se visualiza
class Parada(mesa.Agent):
    def __init__(self, name, model):
        super().__init__(name, model)
        self.name = name

    def step(self):
        ...

# Se visualiza y funciona
class CarroReactivo(mesa.Agent):
    def __init__(self, name, model, destine):
        super().__init__(name, model)
        self.name = name
        self.destine = destine
        self.parked = True

    def step(self):
        self.move()

    def move(self):
        if self.parked:
            exits = self.model.grid.get_neighbors(
                self.pos, moore=False, include_center=False)

            for exit in exits:
                if type(exit) is Calle:
                    self.parked = False
                    self.model.grid.move_agent(self, exit.pos)
                    break
        else:
            cellmates = self.model.grid.get_cell_list_contents([self.pos])
            neighborCells = self.model.grid.get_neighborhood(
                self.pos, moore=False, include_center=False, radius=2)

            neighborVehicles = []

            for cell in neighborCells:
                for agent in self.model.grid.get_cell_list_contents(cell):
                    if type(agent) is CarroInteligente or type(agent) is CarroReactivo:
                        neighborVehicles.append(agent)
                    elif type(agent) is Autobus:
                        neighborVehicles.append(agent)
                    elif type(agent) is Perro:
                        neighborVehicles.append(agent)
                    elif type(agent) is Peaton:
                        neighborVehicles.append(agent)
                    elif type(agent) is Estacionamiento:
                        if agent.pos == self.destine:
                            self.model.grid.move_agent(self, agent.pos)
                            self.parked = True
                            self.model.schedule.remove(self)
                            break

            for agent in cellmates:
                if type(agent) is Calle:
                    desicion = self.random.choice(agent.direction)
                    if desicion == 'north':
                        next_cell = (self.pos[0], self.pos[1] + 1)
                    elif desicion == 'south':
                        next_cell = (self.pos[0], self.pos[1] - 1)
                    elif desicion == 'east':
                        next_cell = (self.pos[0] + 1, self.pos[1])
                    elif desicion == 'west':
                        next_cell = (self.pos[0] - 1, self.pos[1])
                    else:
                        next_cell = self.pos

            hayVehiculo = False
            for vehicle in neighborVehicles:
                if next_cell == vehicle.pos:
                    hayVehiculo = True

            semaforo = None
            if not hayVehiculo and not self.parked:
                if next_cell[0] < self.model.grid.width and 0 <= next_cell[1] < self.model.grid.height:
                    contentsNextCell = self.model.grid.get_cell_list_contents(
                        next_cell)
                    for agent in contentsNextCell:
                        if type(agent) is Semaforo:
                            semaforo = agent
                            break
                    if semaforo is None:
                        self.model.grid.move_agent(self, next_cell)
                    elif semaforo.color != 'rojo':
                        self.model.grid.move_agent(self, next_cell)

# Se visualiza pero funciona sin cambio de carril
class CarroInteligente(mesa.Agent):
    def __init__(self, name, model, origin, destine):
        super().__init__(name, model)
        self.name = name
        self.origin = origin
        self.destine = destine

        G = nx.DiGraph()
        G.add_weighted_edges_from(edges)
        for key, val in nodes.items():
            if val == self.origin:
                origin = key
            if val == self.destine:
                destine = key

        shortest_path = nx.shortest_path(
            G, source=origin, target=destine, weight='weight')
        positions = []
        for i in range(len(shortest_path) - 1):
            source = nodes[shortest_path[i]]
            destiny = nodes[shortest_path[i + 1]]

            positions.append(
                [(destiny[0] - source[0]), (destiny[1] - source[1])])

        self.moves = list(positions)

    def step(self):
        self.move()

    def move(self):
        def check_sorrunding():
            neighborCells = self.model.grid.get_neighborhood(
                self.pos, moore=False, include_center=False, radius=1)
            neighborVehicles = []

            for cell in neighborCells:
                for agent in self.model.grid.get_cell_list_contents(cell):
                    if type(agent) is CarroInteligente or type(agent) is CarroReactivo:
                        neighborVehicles.append(agent)
                    elif type(agent) is Autobus:
                        neighborVehicles.append(agent)
                    elif type(agent) is Perro:
                        neighborVehicles.append(agent)
                    elif type(agent) is Peaton:
                        neighborVehicles.append(agent)
                    elif type(agent) is Estacionamiento:
                        if agent.pos == self.destine:
                            self.model.schedule.remove(self)
                            break

            return neighborVehicles

        def do_step(neighborVehicles):
            hayVehiculo = False
            for vehicle in neighborVehicles:
                if next_cell == vehicle.pos:
                    hayVehiculo = True

            semaforo = None
            if not hayVehiculo:
                if next_cell[0] < self.model.grid.width and 0 <= next_cell[1] < self.model.grid.height:
                    contentsNextCell = self.model.grid.get_cell_list_contents(
                        next_cell)
                    for agent in contentsNextCell:
                        if type(agent) is Semaforo:
                            semaforo = agent
                            break

                    if semaforo is None:
                        self.model.grid.move_agent(self, next_cell)
                    elif semaforo.color != 'rojo':
                        self.model.grid.move_agent(self, next_cell)
                    elif semaforo.color == 'rojo':
                        return "rojo"
            else:
                return "obstaculo"

        for move in self.moves:
            if move[0] == 0 and move[1] == 0:
                continue
            elif move[0] == 0:
                for _ in range(abs(move[1])):
                    if move[1] > 0:
                        next_cell = (self.pos[0], self.pos[1] + 1)
                        neighborVehicles = check_sorrunding()
                        if do_step(neighborVehicles) != "rojo" and do_step(neighborVehicles) != "obstaculo":
                            move[1] -= 1
                    elif move[1] < 0:
                        next_cell = (self.pos[0], self.pos[1] - 1)
                        neighborVehicles = check_sorrunding()
                        if do_step(neighborVehicles) != "rojo" and do_step(neighborVehicles) != "obstaculo":
                            move[1] += 1
                    break
                break
            elif move[1] == 0:
                for _ in range(abs(move[0])):
                    if move[0] > 0:
                        next_cell = (self.pos[0] + 1, self.pos[1])
                        neighborVehicles = check_sorrunding()
                        if do_step(neighborVehicles) != "rojo" and do_step(neighborVehicles) != "obstaculo":
                            move[0] -= 1
                    elif move[0] < 0:
                        next_cell = (self.pos[0] - 1, self.pos[1])
                        neighborVehicles = check_sorrunding()
                        if do_step(neighborVehicles) != "rojo" and do_step(neighborVehicles) != "obstaculo":
                            move[0] += 1
                    break
                break

# Se visualiza
class Calle(mesa.Agent):
    def __init__(self, name, model, direction):
        super().__init__(name, model)
        self.name = name
        self.direction = direction

    def step(self):
        ...

# Se visualiza
class Banqueta(mesa.Agent):
    def __init__(self, name, model):
        super().__init__(name, model)
        self.name = name

    def step(self):
        ...

# Se visualiza y funciona
class Autobus(mesa.Agent):
    def __init__(self, name, model, origin, destine):
        super().__init__(name, model)
        self.name = name
        self.origin = origin
        self.destine = destine

        G = nx.DiGraph()
        G.add_weighted_edges_from(edges)
        for key, val in nodes.items():
            if val == self.origin:
                origin = key
            if val == self.destine:
                destine = key

        shortest_path = nx.shortest_path(
            G, source=origin, target=destine, weight='weight')
        positions = []
        for i in range(len(shortest_path) - 1):
            source = nodes[shortest_path[i]]
            destiny = nodes[shortest_path[i + 1]]

            positions.append(
                [(destiny[0] - source[0]), (destiny[1] - source[1])])

        self.moves = list(positions)

        reverse_path = nx.shortest_path(
            G, source=destine, target=origin, weight='weight')
        reverse_positions = []
        for i in range(len(reverse_path) - 1):
            source = nodes[reverse_path[i]]
            destiny = nodes[reverse_path[i + 1]]

            reverse_positions.append(
                [(destiny[0] - source[0]), (destiny[1] - source[1])])

        self.reverse = list(reverse_positions)

        for i in self.reverse:
            self.moves.append(i)

        self.lista = []


    def grafo(self):
            ruta = []

            G = nx.DiGraph()
            G.add_weighted_edges_from(edges)
            for key, val in nodes.items():
                if val == self.origin:
                    self.origin = key
                if val == self.destine:
                    self.destine = key

            shortest_path = nx.shortest_path(
                G, source=self.origin, target=self.destine, weight='weight')
            positions = []
            for i in range(len(shortest_path) - 1):
                source = nodes[shortest_path[i]]
                destiny = nodes[shortest_path[i + 1]]

                positions.append(
                    [(destiny[0] - source[0]), (destiny[1] - source[1])])

            ruta = list(positions)

            reverse_path = nx.shortest_path(
                G, source=self.destine, target=self.origin, weight='weight')
            reverse_positions = []
            for i in range(len(reverse_path) - 1):
                source = nodes[reverse_path[i]]
                destiny = nodes[reverse_path[i + 1]]

                reverse_positions.append(
                    [(destiny[0] - source[0]), (destiny[1] - source[1])])

            regreso = list(reverse_positions)

            for i in regreso:
                ruta.append(i)

            return ruta


    def step(self):
        ruta = self.grafo()
        self.move(ruta)


    def move(self, ruta):
        def check_sorrunding():
            neighborCells = self.model.grid.get_neighborhood(
                self.pos, moore=False, include_center=False, radius=1)

            neighborVehicles = []

            for cell in neighborCells:
                for agent in self.model.grid.get_cell_list_contents(cell):
                    if type(agent) is CarroInteligente or type(agent) is CarroReactivo:
                        neighborVehicles.append(agent)
                    elif type(agent) is Autobus:
                        neighborVehicles.append(agent)
                    elif type(agent) is Perro:
                        neighborVehicles.append(agent)
                    elif type(agent) is Peaton:
                        neighborVehicles.append(agent)

            return neighborVehicles


        def do_step(neighborVehicles):
            hayVehiculo = False
            for vehicle in neighborVehicles:
                if next_cell == vehicle.pos:
                    hayVehiculo = True

            semaforo = None
            if not hayVehiculo:
                if next_cell[0] < self.model.grid.width and 0 <= next_cell[1] < self.model.grid.height:
                    contentsNextCell = self.model.grid.get_cell_list_contents(
                        next_cell)
                    for agent in contentsNextCell:
                        if type(agent) is Semaforo:
                            semaforo = agent
                            break

                    if semaforo is None:
                        self.model.grid.move_agent(self, next_cell)
                    elif semaforo.color != 'rojo':
                        self.model.grid.move_agent(self, next_cell)
                    elif semaforo.color == 'rojo':
                        return "rojo"
            else:
                return "obstaculo"

        def cycle():
            if len(self.lista) == len(ruta):
                self.lista = []
            for _ in self.lista:
                ruta.pop(0)
            self.lista.append(self.moves.pop(0))
            self.moves.append(ruta[0])


        for move in self.moves:
            if move[0] == 0 and move[1] == 0:
                cycle()
                break
            elif move[0] == 0:
                for _ in range(abs(move[1])):
                    if move[1] > 0:
                        next_cell = (self.pos[0], self.pos[1] + 1)
                        neighborVehicles = check_sorrunding()
                        if do_step(neighborVehicles) != "rojo" and do_step(neighborVehicles) != "obstaculo":
                            move[1] -= 1
                    elif move[1] < 0:
                        next_cell = (self.pos[0], self.pos[1] - 1)
                        neighborVehicles = check_sorrunding()
                        if do_step(neighborVehicles) != "rojo" and do_step(neighborVehicles) != "obstaculo":
                            move[1] += 1
                    break
                break
            elif move[1] == 0:
                for _ in range(abs(move[0])):
                    if move[0] > 0:
                        next_cell = (self.pos[0] + 1, self.pos[1])
                        neighborVehicles = check_sorrunding()
                        if do_step(neighborVehicles) != "rojo" and do_step(neighborVehicles) != "obstaculo":
                            move[0] -= 1
                    elif move[0] < 0:
                        next_cell = (self.pos[0] - 1, self.pos[1])
                        neighborVehicles = check_sorrunding()
                        if do_step(neighborVehicles) != "rojo" and do_step(neighborVehicles) != "obstaculo":
                            move[0] += 1
                    break
                break

# Se visualiza y funciona
class Peaton(mesa.Agent):
    def __init__(self, name, model):
        super().__init__(name, model)
        self.name = name
        self.prev_steps = []
        self.prev_cruces = []

    def step(self):
        self.move()

    def move(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=False, include_center=False)

        if self.pos not in self.prev_steps:
            self.prev_steps.append(self.pos)

        if len(self.prev_steps) > 10:
            self.prev_steps.pop(0)

        if len(self.prev_cruces) > 10:
            self.prev_cruces.pop(0)

        semaforo = None

        banqsCrux = []
        for vecino in neighbors:
            banqsCrux.append(vecino)

        def normal(semaforo):
            for partner in neighbors:
                if type(partner) is Cruce:
                    for content in self.model.grid.get_cell_list_contents(partner.pos):
                        if type(content) is Semaforo:
                            semaforo = content
                    if semaforo is None:
                        if partner.pos not in self.prev_steps:
                            if partner.pos not in self.prev_cruces:
                                self.prev_cruces.append(partner.pos)
                                self.model.grid.move_agent(self, partner.pos)
                                break
                    elif semaforo.color == 'rojo':
                        if partner.pos not in self.prev_steps:
                            if partner.pos not in self.prev_cruces:
                                self.prev_cruces.append(partner.pos)
                                self.model.grid.move_agent(self, partner.pos)
                            break
                if type(partner) is Semaforo:
                    if partner.color == 'rojo':
                        for content in self.model.grid.get_cell_list_contents(partner.pos):
                            if type(content) is Cruce:
                                if content.pos not in self.prev_steps:
                                    if content.pos not in self.prev_cruces:
                                        self.prev_cruces.append(content.pos)
                                        self.model.grid.move_agent(self, content.pos)
                                        break
                elif type(partner) is Banqueta:
                    if partner.pos not in self.prev_steps:
                        self.model.grid.move_agent(self, partner.pos)
                        break

        def find_cruce():
            sem = None
            opciones = []
            for elem in banqsCrux:
                if type(elem) is Cruce:
                    for content in self.model.grid.get_cell_list_contents(elem.pos):
                        if type(content) is Semaforo:
                            sem = content
                    if sem is None:
                        opciones.append(elem)
                    elif sem.color == 'rojo':
                        opciones.append(elem)
            if opciones:
                return (opciones, True)
            else:
                return (None, False)

        amigo = find_cruce()
        if amigo[1]:
            seleccion = self.random.choice(amigo[0])
            if seleccion.pos not in self.prev_steps:
                if seleccion.pos not in self.prev_cruces:
                    self.prev_cruces.append(seleccion.pos)
                    self.model.grid.move_agent(self, seleccion.pos)
                else:
                    normal(semaforo)
            else:
                normal(semaforo)
        else:
            normal(semaforo)

# Se visualiza
class Cruce(mesa.Agent):
    def __init__(self, name, model):
        super().__init__(name, model)
        self.name = name

    def step(self):
        ...

# Se visualiza y funciona
class Perro(mesa.Agent):
    def __init__(self, name, model):
        super().__init__(name, model)
        self.name = name

    def step(self):
        self.move()

    def move(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos, moore=False, include_center=False)
        surroundings = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=False)

        neighborVehicles = []

        for cell in surroundings:
            for agent in self.model.grid.get_cell_list_contents(cell):
                if type(agent) is CarroInteligente or type(agent) is CarroReactivo:
                    neighborVehicles.append(agent)
                elif type(agent) is Autobus:
                    neighborVehicles.append(agent)

        move = self.random.choice(surroundings)

        hayVehiculo = False
        for vehicle in neighborVehicles:
            if move == vehicle.pos:
                hayVehiculo = True

        if not hayVehiculo:
            while move in edificios or move in estacionamientos:
                move = self.random.choice(surroundings)

            for partner in neighbors:
                if partner == type(Edificio):
                    move = self.random.choice(surroundings)
                    self.model.grid.move_agent(self, move)
                    break
                else:
                    self.model.grid.move_agent(self, move)


# ----------------------------------MODELO----------------------------------
class Ciudad(mesa.Model):
    def __init__(self, carrosrect, carrosint, autobuses, peatones, perros):
        super().__init__()
        self.num_carrosrect = carrosrect
        self.num_carrosint = carrosint
        self.num_autobuses = autobuses
        self.num_peaton = peatones
        self.num_perros = perros
        self.schedule = mesa.time.SimultaneousActivation(self)
        self.grid = mesa.space.MultiGrid(33, 33, False)

        id = 0

        for i in range(len(semaforos)):
            s = Semaforo(id, semaforos[i][2], self)
            self.schedule.add(s)
            x, y = semaforos[i][0], semaforos[i][1]
            self.grid.place_agent(s, (x, y))
            id += 1

        for i in range(len(edificios)):
            e = Edificio(id, self)
            self.schedule.add(e)
            x, y = edificios[i][0], edificios[i][1]
            self.grid.place_agent(e, (x, y))
            id += 1

        for i in range(len(estacionamientos)):
            e = Estacionamiento(id, self)
            self.schedule.add(e)
            x, y = estacionamientos[i][0], estacionamientos[i][1]
            self.grid.place_agent(e, (x, y))
            id += 1

        for i in range(len(glorieta_coor)):
            g = Glorieta(id, self)
            self.schedule.add(g)
            x, y = glorieta_coor[i][0], glorieta_coor[i][1]
            self.grid.place_agent(g, (x, y))
            id += 1

        for i in range(len(banquetas_coor)):
            b = Banqueta(id, self)
            self.schedule.add(b)
            x, y = banquetas_coor[i][0], banquetas_coor[i][1]
            self.grid.place_agent(b, (x, y))
            id += 1

        for i in range(len(calle_coor)):
            c = Calle(id, self, calle_coor[i][2])
            self.schedule.add(c)
            x, y = calle_coor[i][0], calle_coor[i][1]
            self.grid.place_agent(c, (x, y))
            id += 1

        for i in range(len(paradas)):
            p = Parada(id, self)
            self.schedule.add(p)
            x, y = paradas[i][0], paradas[i][1]
            self.grid.place_agent(p, (x, y))
            id += 1

        for i in range(len(cruces)):
            cr = Cruce(id, self)
            self.schedule.add(cr)
            x, y = cruces[i][0], cruces[i][1]
            self.grid.place_agent(cr, (x, y))
            id += 1

        for i in range(self.num_carrosrect):
            est_org = self.random.choice(estacionamientos)
            est_dest = self.random.choice(estacionamientos)
            # est_org = (11, 29)
            # est_dest = (23, 28)
            if est_dest == est_org:
                est_dest = self.random.choice(estacionamientos)

            c = CarroReactivo(id, self, est_dest)
            self.schedule.add(c)

            x = est_org[0]
            y = est_org[1]
            self.grid.place_agent(c, (x, y))
            id += 1

        for i in range(self.num_autobuses):
            origin = self.random.choice(paradas)
            destine = self.random.choice(paradas)
            if destine == origin:
                destine = self.random.choice(paradas)

            stops = self.grid.get_neighbors(origin, moore=False, include_center=False)
            for stop in stops:
                if type(stop) is Calle:
                    origen = stop.pos

            destin_stops = self.grid.get_neighbors(destine, moore=False, include_center=False)
            for stop in destin_stops:
                if type(stop) is Calle:
                    destino = stop.pos

            a = Autobus(id, self, origen, destino)
            self.schedule.add(a)

            self.grid.place_agent(a, origen)
            id += 1

        for i in range(self.num_peaton):
            p = Peaton(id, self)
            self.schedule.add(p)
            x, y = self.random.choice(banquetas_coor)
            self.grid.place_agent(p, (x, y))
            id += 1

        for i in range(self.num_perros):
            p = Perro(id, self)
            self.schedule.add(p)
            x, y = self.random.choice(banquetas_coor)
            self.grid.place_agent(p, (x, y))
            id += 1

        for i in range(self.num_carrosint):
            est_org = self.random.choice(spawn_carros)
            est_dest = self.random.choice(estacionamientos)
            # est_org = (11, 29)
            # est_dest = (23, 28)
            if est_dest == est_org:
                est_dest = self.random.choice(estacionamientos)

            c = CarroInteligente(id, self, est_org, est_dest)
            self.schedule.add(c)

            x = est_org[0]
            y = est_org[1]
            self.grid.place_agent(c, (x, y))
            id += 1

    def step(self):
        self.schedule.step()
