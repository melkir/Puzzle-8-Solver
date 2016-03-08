def id_dfs(puzzle, goal, get_moves):
    import itertools

    def dfs(route, depth):
        if depth == 0:
            return
        if route[-1] == goal:
            return route
        for move in get_moves(route[-1]):
            if move not in route:
                next_route = dfs(route + [move], depth - 1)
                if next_route:
                    return next_route

    for depth in itertools.count():
        route = dfs([puzzle], depth)
        if route:
            return route


def num_moves(rows, cols):
    def get_moves(subject):
        moves = []

        zrow, zcol = next((r, c)
                          for r, l in enumerate(subject)
                          for c, v in enumerate(l) if v == 0)

        def swap(row, col):
            import copy
            s = copy.deepcopy(subject)
            s[zrow][zcol], s[row][col] = s[row][col], s[zrow][zcol]
            return s

        # north
        if zrow > 0:
            moves.append(swap(zrow - 1, zcol))
        # east
        if zcol < cols - 1:
            moves.append(swap(zrow, zcol + 1))
        # south
        if zrow < rows - 1:
            moves.append(swap(zrow + 1, zcol))
        # west
        if zcol > 0:
            moves.append(swap(zrow, zcol - 1))
        return moves

    return get_moves


def print_puzzle(matrix):
    for line in matrix:
        print('[' + str(line[0]), end="")
        for i in range(1, len(line)):
            print("," + str(line[i]), end="")
        print(']')


def print_solution(solution):
    for matrix in solution:
        print_puzzle(matrix)
        print("")


if __name__ == '__main__':
    puzzle = [[1, 2, 3],
              [5, 8, 4],
              [6, 0, 7]]

    goal = [[1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]]

    import time

    start_time = time.time()
    solution = id_dfs(puzzle, goal, num_moves(3, 3))
    end_time = time.time()

    print_solution(solution)
    print("Cost : ", len(solution))
    print("--- %s seconds ---" % (end_time - start_time))
