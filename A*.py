from collections import deque
from itertools import chain, tee
from math import sqrt
from random import choice


class Puzzle:
    HOLE = 0

    """
    A class representing an '8-puzzle'.
    - 'board' should be a square list of lists with integer entries 0...width^2 - 1
       e.g. [[1,2,3],[4,0,6],[7,5,8]]
    """

    def __init__(self, board, hole_location=None, width=None):
        # Use a flattened representation of the board (if it isn't already)
        self.board = list(chain.from_iterable(board)) if hasattr(board[0], '__iter__') else board
        self.hole = hole_location if hole_location is not None else self.board.index(Puzzle.HOLE)
        self.width = width or int(sqrt(len(self.board)))

    @property
    def solved(self):
        """
        The puzzle is solved if the flattened board's numbers are in
        increasing order from left to right and the '0' tile is in the
        last position on the board
        """
        return self.board == list(range(1, self.width * self.width)) + [Puzzle.HOLE]

    @property
    def possible_moves(self):
        """
        A generator for the possible moves for the hole, where the
        board is linearized in row-major order.  Possibilities are
        -1 (left), +1 (right), -width (up), or +width (down).
        """
        # Up, down
        for dest in (self.hole - self.width, self.hole + self.width):
            if 0 <= dest < len(self.board):
                yield dest
        # Left, right
        for dest in (self.hole - 1, self.hole + 1):
            if dest // self.width == self.hole // self.width:
                yield dest

    def move(self, destination):
        """
        Move the hole to the specified index.
        """
        board = self.board[:]
        board[self.hole], board[destination] = board[destination], board[self.hole]
        return Puzzle(board, destination, self.width)

    def shuffle(self, moves=1000):
        """
        Return a new puzzle that has been shuffled with random moves
        """
        p = self
        for _ in range(moves):
            p = p.move(choice(list(p.possible_moves)))
        return p

    @staticmethod
    def direction(a, b):
        """
        The direction of the movement of the hole (L, R, U, or D) from a to b.
        """
        if a is None:
            return None
        return {
            -a.width: 'Up',
            -1: 'Left', 0: None, +1: 'Right',
            +a.width: 'Down',
        }[b.hole - a.hole]

    def __str__(self):
        return "\n".join(str(self.board[start: start + self.width])
                         for start in range(0, len(self.board), self.width))

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        h = 0
        for value, i in enumerate(self.board):
            h ^= value << i
        return h


class MoveSequence:
    """
    Represents the successive states of a puzzle taken to reach an end state.
    """

    def __init__(self, last, prev_holes=None):
        self.last = last
        self.prev_holes = prev_holes or []

    def branch(self, destination):
        """
        Makes a MoveSequence with the same history followed by a move of
        the hole to the specified destination index.
        """
        return MoveSequence(self.last.move(destination),
                            self.prev_holes + [self.last.hole])

    def __iter__(self):
        """
        Generator of puzzle states, starting with the initial configuration
        """
        states = [self.last]
        for hole in reversed(self.prev_holes):
            states.append(states[-1].move(hole))
        yield from reversed(states)


class Solver:
    """
    An '8-puzzle' solver
    - 'start' is a Puzzle instance
    """

    def __init__(self, start):
        self.start = start

    def solve(self):
        """
        Perform breadth-first search and return a MoveSequence of the solution,
        if it exists
        """
        queue = deque([MoveSequence(self.start)])
        seen = {self.start}
        if self.start.solved:
            return queue.pop()

        for seq in iter(queue.pop, None):
            for destination in seq.last.possible_moves:
                attempt = seq.branch(destination)
                if attempt.last not in seen:
                    seen.add(attempt.last)
                    queue.appendleft(attempt)
                    if attempt.last.solved:
                        return attempt


# https://docs.python.org/3/library/itertools.html#itertools-recipes
def pairwise(iterable):
    """
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


if __name__ == '__main__':
    board = [[1, 2, 3],
             [5, 8, 4],
             [6, 0, 7]]

    puzzle = Puzzle(board)
    print(puzzle)

    import time

    start_time = time.time()
    move_seq = iter(Solver(puzzle).solve())
    end_time = time.time()

    counter = 1
    for from_state, to_state in pairwise(move_seq):
        counter += 1
        print()
        print(Puzzle.direction(from_state, to_state))
        print(to_state)

    print()
    print("--- %s seconds ---" % (end_time - start_time))
    print("Cost : ", counter)
