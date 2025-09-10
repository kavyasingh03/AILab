import heapq

target = [[1,2,3],
          [8,0,4],
          [7,6,5]]

directions = [(1,0), (-1,0), (0,1), (0,-1)]

def board_to_tuple(board):
    return tuple(tuple(row) for row in board)

def locate(board, val):
    for r in range(3):
        for c in range(3):
            if board[r][c] == val:
                return (r, c)

def misplaced_tiles_heuristic(board):
    misplaced = 0
    for r in range(3):
        for c in range(3):
            if board[r][c] != 0 and board[r][c] != target[r][c]:
                misplaced += 1
    return misplaced

def manhattan_heuristic(board):
    total_dist = 0
    for r in range(3):
        for c in range(3):
            val = board[r][c]
            if val != 0:
                goal_r, goal_c = locate(target, val)
                total_dist += abs(r - goal_r) + abs(c - goal_c)
    return total_dist

def generate_neighbors(board):
    neighbors = []
    zero_r, zero_c = locate(board, 0)
    for dr, dc in directions:
        new_r, new_c = zero_r + dr, zero_c + dc
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            new_board = [list(row) for row in board]
            new_board[zero_r][zero_c], new_board[new_r][new_c] = new_board[new_r][new_c], new_board[zero_r][zero_c]
            neighbors.append(new_board)
    return neighbors

def display_board(board):
    for row in board:
        print(' '.join(str(num) for num in row))
    print()

def a_star_search(start, heuristic_func):
    open_set = []
    g_cost = 0
    f_cost = g_cost + heuristic_func(start)
    heapq.heappush(open_set, (f_cost, g_cost, start, []))
    explored = set()

    while open_set:
        f_cost, g_cost, current_board, path_so_far = heapq.heappop(open_set)
        if current_board == target:
            return path_so_far + [current_board]

        explored.add(board_to_tuple(current_board))

        for neighbor in generate_neighbors(current_board):
            neighbor_tup = board_to_tuple(neighbor)
            if neighbor_tup not in explored:
                new_g = g_cost + 1
                new_f = new_g + heuristic_func(neighbor)
                heapq.heappush(open_set, (new_f, new_g, neighbor, path_so_far + [current_board]))

    return None

initial_state = [
    [2, 8, 3],
    [1, 6, 4],
    [7, 0, 5]
]

print("Using Misplaced Tiles Heuristic:")
solution_path = a_star_search(initial_state, misplaced_tiles_heuristic)
print("Steps:", len(solution_path) - 1)
for step_num, state in enumerate(solution_path):
    print(f"Step {step_num}:")
    display_board(state)

print("Using Manhattan Distance Heuristic:")
solution_path = a_star_search(initial_state, manhattan_heuristic)
print("Steps:", len(solution_path) - 1)
for step_num, state in enumerate(solution_path):
    print(f"Step {step_num}:")
    display_board(state)
