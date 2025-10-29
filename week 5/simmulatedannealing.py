import random
import math

def display(board):
    n = len(board)
    for i in range(n):
        print(" ".join("Q" if board[i] == j else "." for j in range(n)))
    print()

def cost(board):
    n = len(board)
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                c += 1
    return c

def neighbor(board):
    n = len(board)
    b = list(board)
    r = random.randint(0, n - 1)
    c = random.randint(0, n - 1)
    b[r] = c
    return b

def simulated_annealing(n, t0=100, cool=0.95, t_min=1):
    state = [random.randint(0, n - 1) for _ in range(n)]
    energy = cost(state)
    temp = t0
    step = 1
    print("Initial Board:")
    display(state)
    print(f"Initial Cost: {energy}\n")
    while temp > t_min and energy > 0:
        nxt = neighbor(state)
        nxt_cost = cost(nxt)
        d = nxt_cost - energy
        if d < 0 or random.random() < math.exp(-d / temp):
            state = nxt
            energy = nxt_cost
        print(f"Step {step}: Temp={temp:.3f}, Cost={energy}")
        step += 1
        temp *= cool
    print("\nFinal Board:")
    display(state)
    print(f"Final Cost: {energy}")
    if energy == 0:
        print("Goal State Reached!")
    else:
        print("Terminated before reaching goal.")

simulated_annealing(8)
