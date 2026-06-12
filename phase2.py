temp_count = 0

def new_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"


tac = []  # stores three address code

def generate_TAC(node):
    # If leaf node (operand)
    if node.left is None and node.right is None:
        return node.value
    
    # Recursively process left and right
    left = generate_TAC(node.left)
    right = generate_TAC(node.right)
    
    temp = new_temp()
    tac.append(f"{temp} = {left} {node.value} {right}")
    
    return temp
