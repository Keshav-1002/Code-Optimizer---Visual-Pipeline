# Construct AST manually
# Expression: b + (c * d)

tree = Node('+',
            Node('b'),
            Node('*', Node('c'), Node('d'))
           )

# Generate TAC
result = generate_TAC(tree)

# Assignment
tac.append(f"a = {result}")

# Generate Quadruples
generate_quadruples()

# Output
print("Three Address Code (TAC):")
for line in tac:
    print(line)

print("\nQuadruples:")
for quad in quadruples:
    print(quad)
