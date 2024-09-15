import networkx as nx

nodes = {'C1': (1,31),
         'C2': (8,31),
         'C3': (16,31),
         'C4': (20,31),
         'C5': (25,31),
         'C6': (31,31),
         'C7': (1,24),
         'C8': (8,24),
         'C9': (16,24),
         'C10': (1, 16),
         'C11': (16, 16),
         'C12': (20, 16),
         'C13': (25, 16),
         'C14': (31, 16),
         'C15': (1, 12),
         'C16': (8, 12),
         'C17': (16, 12),
         'C18': (20, 12),
         'C19': (25,12),
         'C20': (31, 12),
         'C21': (1, 7),
         'C22': (8, 7),
         'C23': (20, 7),
         'C24': (25, 7),
         'C25': (31, 7),
         'C26': (1, 1),
         'C27': (8, 1),
         'C28': (16, 1),
         'C29': (20, 1),
         'C30': (25, 1),
         'C31': (31, 1),
         'E1.2': (11, 31),
         'E1.1': (11, 29),
         'E2.2': (25, 28),
         'E2.1': (23, 28),
         'E3.2': (8, 27),
         'E3.1': (5, 27),
         'E4.2': (16, 27),
         'E4.1': (14, 27),
         'E5.2': (25, 27),
         'E5.1': (28, 27),
         'E6.2': (12, 24),
         'E6.1': (12, 21),
         'E7.2': (1, 20),
         'E7.1': (3, 20),
         'E8.2': (31, 20),
         'E8.1': (29, 20),
         'E9.2': (16, 19),
         'E9.1': (14, 19),
         'E10.2': (20, 19),
         'E10.1': (22, 19),
         'E11.2': (8, 16),
         'E11.1': (8, 18),
         'E12.2.1': (1, 9),
         'E12.1': (3, 9),
         'E12.2.2': (3, 7),
         'E13.1': (23, 9),
         'E13.2.1': (25, 9),
         'E13.2.2': (23, 7),
         'E14.1': (14, 6),
         'E14.2': (16, 6),
         'E15.2.1': (6, 7),
         'E15.1': (6, 4),
         'E15.2.2': (8, 4),
         'E16.1': (11, 4),
         'E17.2.1': (25, 3),
         'E17.1': (28, 3),
         'E17.2.2': (28, 1),
         'P1': (13, 31),
         'P2': (22, 31),
         'P3': (1, 29),
         'P4': (31, 24),
         'P5': (20, 21),
         'P6': (10, 16),
         'P7': (16, 9),
         'P8': (20, 9),
         'P9': (31, 4),
         'P10': (4, 1)
         }

edges = [('C2', 'C1', 7),
         ('E1.2', 'C2', 3),
         ('P1', 'E1.2', 2),
         ('C3', 'P1', 3),
         ('C4', 'C3', 4),
         ('P2', 'C4',2),
         ('C5', 'P2',3),
         ('C6','C5',6),
         ('C1','P3',2),
         ('P3','C7',5),
         ('C7','E7.2',4),
         ('E7.2','C10',4),
         ('C10','C15',4),
         ('C15','E12.2.1',3),
         ('E12.2.1','C21',2),
         ('C21','C26',6),
         ('C26','P10',3),
         ('P10','C27',4),
         ('C27','C28',8),
         ('C28','C29',4),
         ('C29','C30',5),
         ('C30', 'E17.2.2',3),
         ('E17.2.2','C31',3),
         ('C31', 'P9',3),
         ('P9', 'C25', 3),
         ('C25', 'C20', 5),
         ('C20', 'C14', 4),
         ('C14', 'E8.2', 4),
         ('E8.2', 'P4', 4),
         ('P4', 'C6', 7),
         ('C8','E3.2',3),
         ('E3.2', 'C2', 4),
         ('E3.2', 'E3.1', 3),
         ('C8', 'C7', 7),
         ('E6.2','C8',4),
         ('C9', 'E6.2',4),
         ('E1.2','E1.1',2),
         ('E1.1','E1.2',2),
         ('E3.1','E3.2',3),
         ('C3','E4.2',4),
         ('E4.2','E4.1',2),
         ('E4.1','E4.2',2),
         ('E4.2','C9',3),
         ('E6.2','E6.1',3),
         ('E6.1', 'E6.2',3),
         ('C9','E9.2',5),
         ('E9.2', 'E9.1',2),
         ('E9.1', 'E9.2', 2),
         ('E9.2', 'C11', 3),
         ('C11' , 'C17', 4),
         ('C17' , 'P7', 3),
         ('P7','E14.2', 3),
         ('E14.2', 'E14.1', 2),
         ('E14.1', 'E14.2', 2),
         ('E14.2', 'C28', 4),
         ('E7.2','E7.1',2),
         ('E7.1', 'E7.2',2),
         ('C11', 'P6', 6),
         ('P6', 'E11.2', 2),
         ('E11.2', 'C10', 7),
         ('E11.1', 'E11.2', 2),
         ('E11.2', 'E11.1', 2),
         ('C15', 'C16', 7),
         ('C16', 'C17',8),
         ('C16','C22',4),
         ('C22', 'E15.2.2', 3),
         ('E15.2.2', 'C27', 3),
         ('C22', 'E15.2.1', 2),
         ('E15.2.1', 'E12.2.2',2),
         ('E12.2.2', 'C21', 2),
         ('E12.2.1','E12.1',2),
         ('E12.1','E12.2.1',2),
         ('E12.2.2','E12.1',2),
         ('E12.1','E12.2.2',2),
         ('E15.1', 'E15.2.1',3),
         ('E15.2.1', 'E15.1', 3),
         ('E15.1', 'E15.2.2',3),
         ('E15.2.2', 'E15.1', 3),
         ('E15.2.2','E16.1', 3),
         ('E16.1', 'E15.2.2',3),
         ('C14', 'C13', 6),
         ('C13', 'C12', 5),
         ('C12', 'C11', 4),
         ('C17','C18', 4),
         ('C18', 'C19', 5),
         ('C19', 'C20', 6),
         ('C29', 'C23', 6),
         ('C23','P8',2),
         ('P8', 'C18', 3),
         ('C18', 'C12', 4),
         ('C12','E10.2', 3),
         ('E10.2', 'E10.1',2),
         ('E10.1', 'E10.2', 2),
         ('E10.2', 'P5', 2),
         ('P5', 'C4', 10),
         ('C5','E2.2',3),
         ('E2.2', 'E2.1', 2),
         ('E2.1', 'E2.2', 2),
         ('E2.2','E5.2', 1),
         ('E5.2', 'E5.1',3),
         ('E5.1', 'E5.2', 3),
         ('E5.2', 'C13', 11),
         ('E8.2','E8.1',2),
         ('E8.1', 'E8.2', 2),
         ('C25', 'C24', 6),
         ('C24', 'E13.2.2',2),
         ('E13.2.2', 'E13.1',2),
         ('E13.1', 'E13.2.2', 2),
         ('E13.2.2', 'C23', 3),
         ('C19', 'E13.2.1', 3),
         ('E13.2.1', 'E13.1', 2),
         ('E13.1', 'E13.2.1', 2),
         ('E13.2.1', 'C24', 2),
         ('C30', 'E17.2.1', 2),
         ('E17.2.1', 'C24',4),
         ('E17.2.1', 'E17.1', 3),
         ('E17.1', 'E17.2.1', 3),
         ('E17.2.2', 'E17.1', 2),
         ('E17.1', 'E17.2.2', 2)
        ]


if __name__ == "__main__":
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges)
    shortest_path = nx.shortest_path(G, source='E1.1', target='E2.1', weight='weight')
    length = nx.shortest_path_length(G, source='E1.1', target='E2.1', weight='weight')
    # print(shortest_path)
    # print(length)
    positions = []
    for i in range (len(shortest_path) - 1):
        source = nodes[shortest_path[i]]
        destiny = nodes[shortest_path[i + 1]]
        positions.append([(destiny[0] - source[0]),(destiny[1] - source[1])])

    # print(list(reversed(positions)))
    print(list(positions))
    print(nx.complement(G))

    for key, val in nodes.items():
        if val == (11, 29):
            origin = key
        if val == (23, 28):
            destin = key
    # print(origin)
    # print(destin)

    # [[0, 2], [-3, 0], [-7, 0], [0, -2], [0, -5], [0, -4], [0, -4], [0, -4], [7, 0], [8, 0], [4, 0], [5, 0], [6, 0], [0, 4], [0, 4], [0, 4], [0, 7], [-6, 0], [0, -3], [-2, 0]]
