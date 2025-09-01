import numpy as np


def parse_obj(file_path):
    vertices = []
    faces = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            
            if not parts:
                continue
            
            if parts[0] == 'v':
                vertex = list(map(float, parts[1:]))
                vertices.append(vertex)
            
            elif parts[0] == 'f':
                face = [vertices[int(idx.split('/')[0]) - 1] for idx in parts[1:]]
                faces.extend(face)
                
    #return np.array(vertices), np.array(faces)
    print(faces)
    print("\n")
    print(vertices)
    return np.array(faces)