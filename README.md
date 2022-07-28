# KnightTourPy

A heuristic algorithm for solving a knight tour problem on a square chessboard.

## Goal

The goal is to find a path of knight moves which visits every square on the chessboard exactly once.

#### Naive solution

A naive approach would be to recursively jump randomly until the knight is stuck
and use backtracking to fix the wrong jumps. This is easy to code, however a solution for
a 8x8 chessboard takes some dozens of seconds.

#### A better jumping method?

A simple improvement is to make the knight choose a square, from which there are the fewest forward moves available.
This is called the Warnsdorff's Heuristic and it speeds up the process significantly.

## Another heuristic - or not?

Warnsdorff's rule still does not solve the main issue - the finding of the last few moves. 
In most cases, the knight has to backtrack a very long way back. I came up with a solution,
which solves the "endgame" much quicker.

#### The algorithm explained with an example

Let's assume our knight got stuck on its 13th square on a 4x4 board. It appeares, that from this square it can reach the already-visited 
square 9. We take a new route as follows, taking a *shortcut* from 9 to 13 going *back* from 13 to 10:

1-...-9-13-12-11-10.

#### What's the deal?

We have not moved forward - the knight still covered only 13 squares.
However, with the new layout, new unvisited squares may become reachable from the new end of the chain - the square #10!

If not, we repeat the process, looking for a new loop in our path.
With enough repetitions, we will ultimately find the complete path.

#### Wait, but what about an infinite loop?

That's right - we could *revert* the previous reroute with a new one, ending up in an infinite loop.
But here comes the final, unbelievable trick - we can prevent this for any square (and not only) board!

Each square on the board (except for the corners) has at least three neighbours. Thus after entering it and getting stuck,
the knight has *at least 2 possible connections* to its previous path, which gives at least 2 reroutes every time!
We will have plenty of possible reroutes to choose from, and a bit of randomness should take care of the repetitions.

It does not work on 4x4 though - the two corners
