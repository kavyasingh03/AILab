from collections import deque
import copy

target_config = [[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 0]]  


directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def locate_blank(board):

    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                return row, col

def generate_next_states(board):

    next_states = []
    row, col = locate_blank(board)
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            temp_board = copy.deepcopy(board)
            temp_board[row][col], temp_board[new_row][new_col] = temp_board[new_row][new_col], temp_board[row][col]
            next_states.append(temp_board)
    return next_states

def reached_goal(board):

    return board == target_config

def display_board(board):

    for row in board:
        print(row)
    print()

def depth_first_search(initial_board, max_depth=50):

    stack = [(initial_board, [])]
    explored = set()

    while stack:
        current_board, moves_so_far = stack.pop()
        board_key = tuple(tuple(r) for r in current_board)

        if board_key in explored:
            continue
        explored.add(board_key)

        if reached_goal(current_board):
            return moves_so_far + [current_board]

        if len(moves_so_far) >= max_depth:
            continue

        for new_board in generate_next_states(current_board):
            stack.append((new_board, moves_so_far + [current_board]))
    return None

def depth_limited_search(board, depth, path_trace, seen):

    if reached_goal(board):
        return path_trace + [board]
    if depth == 0:
        return None

    board_signature = tuple(tuple(r) for r in board)
    seen.add(board_signature)

    for successor in generate_next_states(board):
        successor_key = tuple(tuple(r) for r in successor)
        if successor_key not in seen:
            outcome = depth_limited_search(successor, depth - 1, path_trace + [board], seen)
            if outcome:
                return outcome
    return None

def iterative_deepening_search(start_board, depth_limit=50):

    for depth in range(depth_limit):
        visited_nodes = set()
        result_path = depth_limited_search(start_board, depth, [], visited_nodes)
        if result_path:
            return result_path
    return None

if __name__ == "__main__":
    puzzle_start = [[1, 2, 3],
                    [4, 0, 6],
                    [7, 5, 8]]

    print("DFS Result:")
    dfs_result = depth_first_search(puzzle_start, max_depth=20)
    if dfs_result:
        for state in dfs_result:
            display_board(state)
    else:
        print("No solution found using DFS.")

    print("\nIDS Result:")
    ids_result = iterative_deepening_search(puzzle_start, depth_limit=20)
    if ids_result:
        for state in ids_result:
            display_board(state)
    else:
        print("No solution found using IDS.")
