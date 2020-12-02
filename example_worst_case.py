from KnightTourSolver import KnightTourSolver


for SIZE in range(6, 60, 2):
    Solver = KnightTourSolver(SIZE)
    worst_time = worst_iter = worst_reroutes = 0
    worst_origin = tuple()
    worst_board = []
    for i in range(SIZE):
        for j in range(SIZE):
            # print(f"*** start = ({i}, {j}) ***")
            board = Solver.create_empty_board()
            solution = Solver.solve(board, i, j, verbose=False)
            # Solver.print_board(solution['board'])
            if solution['time'] > worst_time:
                worst_time = solution['time']
                worst_iter = solution['iterations']
                worst_origin = (i, j)
                worst_board = solution['board']
                worst_reroutes = solution['reroutes']

            # print(f"Reroutes: {solution['reroutes']}")
            # print(f"Iterations: {solution['iterations']}")
            # print(f"Time: {round(solution['time'], 4)}s")

    Solver.print_board(worst_board)
    print(f"Worst case for N={SIZE}:\n\tOrigin: {worst_origin}\n\tTime: {round(worst_time, 4)}s"
          f"\n\tIterations: {worst_iter}\n\tReroutes: {worst_reroutes}")
