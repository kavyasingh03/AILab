import math

tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['L1', 'L2'],
    'E': ['L3', 'L4'],
    'F': ['L5', 'L6'],
    'G': ['L7', 'L8'],
    'L1': 10,
    'L2': 9,
    'L3': 14,
    'L4': 18,
    'L5': 5,
    'L6': 4,
    'L7': 50,
    'L8': 3
}


def show_tree():
    print("\nGame Tree Structure:\n")
    print("                A (MAX)")
    print("              /        \\")
    print("           B (MIN)       C (MIN)")
    print("          /     \\        /     \\")
    print("       D (MAX)  E (MAX)  F (MAX)  G (MAX)")
    print("      /   \\     /   \\     /   \\     /   \\")
    print("    10    9   14   18   5    4   50    3")
    print("\n--------------------------------------------\n")


def alpha_beta(node, depth, alpha, beta, is_max):
    pad = "  " * depth 


    if isinstance(tree[node], int):
        print(f"{pad}Reached leaf {node} with value {tree[node]}")
        return tree[node]

    if is_max:
        print(f"{pad}Exploring MAX node {node} (depth={depth}), α={alpha}, β={beta}")
        value = -math.inf
        for child in tree[node]:
            print(f"{pad}--> Exploring child {child} of {node}")
            score = alpha_beta(child, depth + 1, alpha, beta, False)
            value = max(value, score)
            alpha = max(alpha, score)
            print(f"{pad}Updated MAX node {node}: value={value}, α={alpha}, β={beta}")
            if beta <= alpha:
                print(f"{pad}!!! Pruning at MAX node {node} (β={beta} ≤ α={alpha})")
                break
        return value

    else:
        print(f"{pad}Exploring MIN node {node} (depth={depth}), α={alpha}, β={beta}")
        value = math.inf
        for child in tree[node]:
            print(f"{pad}--> Exploring child {child} of {node}")
            score = alpha_beta(child, depth + 1, alpha, beta, True)
            value = min(value, score)
            beta = min(beta, score)
            print(f"{pad}Updated MIN node {node}: value={value}, α={alpha}, β={beta}")
            if beta <= alpha:
                print(f"{pad}!!! Pruning at MIN node {node} (β={beta} ≤ α={alpha})")
                break
        return value


show_tree()
print("Starting Alpha-Beta Pruning...\n")

result = alpha_beta('A', 0, -math.inf, math.inf, True)

print("\n--------------------------------------------")
print(f"✅ Best achievable value at root (A): {result}")
print("--------------------------------------------")
