from flask import Flask, request
from model import Ciudad, CarroReactivo, CarroInteligente, Autobus, Peaton, Perro, Semaforo

app = Flask(__name__)

modelo = None

@app.route('/')
def home():
    return 'Hola mundo'


@app.route('/crear-ciudad', methods=['POST'])
def crear_ciudad():

    JSON = dict(request.get_json())
    NUM_CARROS_REACTIVOS = JSON.get('NUM_CARROS_REACTIVOS')
    NUM_CARROS_INTELIGENTES = JSON.get('NUM_CARROS_INTELIGENTES')
    NUM_AUTOBUSES = JSON.get('NUM_AUTOBUSES')
    NUM_PEATONES = JSON.get('NUM_PEATONES')
    NUM_PERROS = JSON.get('NUM_PERROS')

    if not (str(NUM_CARROS_REACTIVOS) and str(NUM_CARROS_INTELIGENTES) and str(NUM_AUTOBUSES) and str(NUM_PEATONES) and str(NUM_PERROS)):
        return ({'error': 'Bad request',
                'messsage': 'Missing requiered parameters in body',
                'details': '''Missing requiered parameter(s) in body:
                    \'NUM_CARROS_REACTIVOS\', \'NUM_AUTOBUSES\', \'NUM_PEATONES\', \'NUM_PERROS\''''},
                    400)

    global modelo
    modelo = Ciudad(int(NUM_CARROS_REACTIVOS), int(NUM_CARROS_INTELIGENTES),int(NUM_AUTOBUSES), int(NUM_PEATONES), int(NUM_PERROS))

    return {'message': 'Ciudad creada'}, 200


@app.route('/step')
def step_modelo():
    
        if not modelo:
            return ({'error': 'Bad request',
                    'messsage': 'Model not initialized',
                    'details': 'Model not initialized'},
                    400)
    

        result = {'agents' : []}
        agents = modelo.schedule.agents

        tipo_agente = ''
        estado = ''
        for agent in agents:
            if type(agent) is CarroReactivo:
                tipo_agente = 'CarroReactivo'
            elif type(agent) is CarroInteligente:
                tipo_agente = 'CarroInteligente'
            elif type(agent) is Autobus:
                tipo_agente = 'Autobus'
            elif type(agent) is Peaton:
                tipo_agente = 'Peaton'
            elif type(agent) is Perro:
                tipo_agente = 'Perro'
            elif type(agent) is Semaforo:
                tipo_agente = 'Semaforo'
                estado = agent.color
            else:
                continue
            
            result['agents'].append({
                'id': agent.unique_id,
                'tipo': tipo_agente,
                'x': agent.pos[0],
                'y': agent.pos[1],
                'estado':estado
            })

        modelo.step()
    
        return result, 200

@app.route('/semaforos')
def semaforos():
    if not modelo:
        return ({'error': 'Bad request',
                'messsage': 'Model not initialized',
                'details': 'Model not initialized'},
                400)

    result = {}
    agents = modelo.schedule.agents

    for agent in agents:
        if type(agent) is Semaforo:
            result[agent.unique_id] = {
                'id': agent.unique_id,
                'x': agent.pos[0],
                'y': agent.pos[1],
                'estado': agent.color
            }
    
    return result, 200


if __name__ == '__main__':
    app.run(debug=True)
