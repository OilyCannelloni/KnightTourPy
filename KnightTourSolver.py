"""
Knight Tour algorithm.

Firstly, a NxN chessboard is filled with Wandorf's Heuristic Algorithm until
the knight has no more moves. Then, reroutes are being calculated which may lead to
filling the missing squares. This procedure is repeated until the whole board is filled.
"""

from copy import deepcopy
from math import inf
from time import time
from dataclasses import dataclass


@dataclass
class KnightTourSolver:
    deltas = ((-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2))
    size: int

    def __post_init__(self):
        self.board = self.create_empty_board()

    def create_empty_board(self):
        return [[0] * self.size for _ in range(self.size)]

    def get_accessible_fields(self, r, c):
        """
        Calculates (r, c) coordinates of all squares the knight can potentially
        jump to from the given square
        :param r: row of the origin
        :param c: column of the origin
        :return: A generator for (r, c) tuples of accessible squares
        """
        for delta in self.deltas:
            if 0 <= r + delta[0] < self.size and 0 <= c + delta[1] < self.size:
                yield r + delta[0], c + delta[1]

    def get_possible_jumps(self, brd, r, c):
        """
        Calculates (r, c) coordinates of all EMPTY squares the knight
        can potentially access.
        :param brd: board reference
        :param r: row of the origin
        :param c: column of the origin
        :return: A generator for (r, c) tuples of EMPTY accessible squares
        """
        for field in self.get_accessible_fields(r, c):
            if brd[field[0]][field[1]] == 0:
                yield field

    def wandorf_fill(self, brd, r, c, num=1):
        """
        Fills the board using the Wandorf Heuristic until blocked.
        Can start with a non-empty board
        :param brd: board reference
        :param r: row of the starting square
        :param c: column of the starting square
        :param num: number to be written into the starting square
        :return: (r, c) coordinates of the square where the knight got blocked
        """
        while True:
            brd[r][c] = num
            num += 1

            jumps = tuple(self.get_possible_jumps(brd, r, c))
            if len(jumps) == 0:
                return r, c

            best_deg, best_jump = 9, (0, 0)
            for jump in jumps:
                deg = len(tuple(self.get_possible_jumps(brd, *jump)))
                if deg < best_deg:
                    best_deg, best_jump = deg, jump

            r, c = best_jump

    def get_next(self, brd, r, c):
        """
        Returns the coordinates of the field with number
        1 higher than the given field
        :param brd: board reference
        :param r: row of the origin
        :param c: column of the origin
        :return: (r, c) coordinates of the next field
        """
        for field in self.get_accessible_fields(r, c):
            if brd[field[0]][field[1]] == brd[r][c] + 1:
                return field
        return None

    def get_prev(self, brd, r, c):
        """
        Returns the coordinates of the field with number
        1 lower than the given field
        :param brd: board reference
        :param r: row of the origin
        :param c: column of the origin
        :return: (r, c) coordinates of the previous field
        """
        for field in self.get_accessible_fields(r, c):
            if brd[field[0]][field[1]] == brd[r][c] - 1:
                return field
        return None

    def find(self, brd, num):
        """
        Finds coordinates of field with given number
        :param brd: board reference
        :param num: field number
        :return: (r, c) coordinates of field
        """
        for r in range(self.size):
            for c in range(self.size):
                if brd[r][c] == num:
                    return r, c
        return None

    def get_max(self, brd):
        """
        Gets the coordinates of the last number on the board
        :param brd: board reference
        :return: (r, c) coordinates of the highest number
        """
        m, mr, mc = 0, 0, 0
        for r in range(self.size):
            for c in range(self.size):
                if brd[r][c] > m:
                    m, mr, mc = brd[r][c], r, c
        return mr, mc

    def verify(self, brd):
        """
        Checks if the solution is correct
        :param brd: board reference
        :return: True if correct, False otherwise
        """
        i = 2
        r, c = self.find(brd, 1)
        m = self.get_max(brd)
        while brd[r][c] < brd[m[0]][m[1]]:
            r, c = self.get_next(brd, r, c)
            if brd[r][c] != i:
                return False
            i += 1
        return True

    def shortest_path_length(self, x1, y1, x2, y2):
        """
        Gets the minimal number of jumps required to get
        from (x1, y1) to (x2, y2)
        :param x1: row of origin
        :param y1: column of origin
        :param x2: row of destination
        :param y2: column of destination
        :return: length of shortest path between origin and destination
        """
        checked = {(x1, y1)}
        d = 0
        while True:
            if (x2, y2) in checked:
                return d
            temp = set()
            for c in checked:
                for f in self.get_accessible_fields(*c):
                    temp.add(f)
            checked = temp
            d += 1

    def get_rank(self, brd, last=None):
        """
        Gets the rank of the board, defined as the minimal amount of jumps
        required to get from the last field to the nearest empty field
        :param brd: board reference
        :param last: (r, c) coordinates of field with highest number
        :return: rank of the board
        """
        if last is None:
            last = self.get_max(brd)
        empty_fields = [(r, c) for r in range(self.size) for c in range(self.size) if brd[r][c] == 0]
        min_d = inf
        for field in empty_fields:
            d = self.shortest_path_length(*last, *field)
            min_d = min(d, min_d)
        return min_d

    def reroute(self, brd, last):
        """
        Calculates all possible board layouts after a rerouting process.
        It works as follows:
        If the knight got blocked, it certainly has at least one accessible square
        that has already been filled, say N. The knight now jumps from 1 to N,
        then to the last square, and then back to N+1 tracing its last path backwards
        :param last: (r, c) coordinates of the square with highest number
        :return: A generator yielding (board, end, rank) tuples, where
        board - rerouted board
        end - last square of new board
        rank - rank of new board
        """
        possible_ends = [self.get_next(brd, *field) for field in self.get_accessible_fields(*last)]
        for end in possible_ends:
            if end == last:
                continue

            b = deepcopy(brd)
            f1, f2 = end, last
            for i in range((b[last[0]][last[1]] - b[end[0]][end[1]]) // 2 + 1):
                next_f1, next_f2 = self.get_next(b, *f1), self.get_prev(b, *f2)
                b[f1[0]][f1[1]], b[f2[0]][f2[1]] = b[f2[0]][f2[1]], b[f1[0]][f1[1]]
                f1 = next_f1
                f2 = next_f2

            yield b, end, self.get_rank(b)

    def print_board(self, brd):
        """
        Prints board to console in a nice way
        :param brd: board reference
        :return: None
        """
        s, cell_size = self.size ** 2, 1
        while s > 1:
            s //= 10
            cell_size += 1

        for row in brd:
            for field in row:
                print(f"{field:{cell_size + 1}}", end="")
            print()

    def solve(self, board, start_r, start_c, verbose=False, print_solution=False):
        solution_found = False
        t0 = time()

        # Wandorf-fill until blocked
        las = self.wandorf_fill(board, start_r, start_c)

        # If it managed to fill the whole board on the first try
        if board[las[0]][las[1]] == self.size ** 2 and self.verify(board):
            solution_found = True
            if verbose:
                print("***** FOUND SOLUTION *****")
                self.print_board(board)
            return {
                'board': board,
                'iterations': 0,
                'reroutes': 0,
                'time': time() - t0
            }

        boards = [(board, las)]  # list of rerouted trials
        reroute_count = 0
        i = 0
        while not solution_found:
            t1 = time()
            i += 1
            if verbose:
                print(f"----- ITERATION {i} -----")

            reroutes = []
            for (brd, last) in boards:
                found_deg1_board = False

                for rerouted in self.reroute(brd, last):
                    reroute_count += 1
                    if verbose:
                        self.print_board(brd)
                        print(f"Rank: {rerouted[2]} Last: {brd[last[0]][last[1]]}")

                    if rerouted[2] == 1:  # rank = 1, meaning we get to an empty square
                        deg1_brd = rerouted[0]
                        # fill it until stuck again
                        deg1_last = self.wandorf_fill(deg1_brd, *rerouted[1], deg1_brd[rerouted[1][0]][rerouted[1][1]])
                        # if the whole board is filled
                        if deg1_brd[deg1_last[0]][deg1_last[1]] == self.size ** 2:
                            if print_solution:
                                print("***** FOUND SOLUTION *****")
                                self.print_board(deg1_brd)
                            return {
                                'board': deg1_brd,
                                'reroutes': reroute_count,
                                'iterations': i,
                                'time': time() - t0
                            }

                        found_deg1_board = True
                        break

                    reroutes.append((rerouted[0], rerouted[1]))
                if found_deg1_board:
                    break

            boards = reroutes
            if verbose:
                print(f"finished iteration {i} within {round(time() - t1, 4)}s")
