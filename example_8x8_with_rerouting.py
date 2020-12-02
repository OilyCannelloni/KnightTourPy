from KnightTourSolver import KnightTourSolver


SIZE = 8
origin_row, origin_column = 3, 2

# initialize solver
Solver = KnightTourSolver(SIZE)

# create 8x8 board filled with 0's
board = Solver.create_empty_board()

# search for solution. Starting from (3, 2) is interesting because
# the algorithm doesn't guess correctly on the first try, thus
# needing to reroute the path several times.
solution = Solver.solve(board, origin_row, origin_column, verbose=True, print_solution=True)

# print the results
print(f"N = {SIZE}, Origin = ({origin_row}, {origin_column})",
      f"Time: {round(solution['time'], 5)}s",
      f"Iterations: {solution['iterations']}",
      f"Total boards created: {solution['reroutes']}",
      sep="\n")
