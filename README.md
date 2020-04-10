# Orixo_solver
This is a game solver for the Orixo puzzle game.
The solver will not work for the

Input
start with 'GRID START', and end with 'GRID STOP'.
Symbol:
'x': Not a grid, nothing.
'o': Empty grid to be filled.
'integer number': the number grid
split the box by space.

example:
GRID START
x  o  x  4  x  x
x  4  o  o  o  o
x  o  x  o  x  x
3  o  o  o  o  o
x  o  x  o  x  x
x  o  o  o  o  3
x  4  x  x  x  x
GRID STOP


Output:

Must move the steps in the output by order of they appear.

format: [x, y], direction

direction:
N: move up
S: move down
W: move left
E: move right

coordination [x, y]

 x 0  1  2  3  4  5
y __ __ __ __ __ __
0|__|__|__|__|__|__|
1|__|__|__|__|__|__|
2|__|__|__|__|__|__|
3|__|__|__|__|__|__|
4|__|__|__|__|__|__|
5|__|__|__|__|__|__|
