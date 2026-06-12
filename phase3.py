quadruples = []

def generate_quadruples():
    for line in tac:
        parts = line.split()
        result = parts[0]
        arg1 = parts[2]
        op = parts[3]
        arg2 = parts[4]
        
        quadruples.append((op, arg1, arg2, result))
        
