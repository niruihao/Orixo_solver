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

GRID STOP


Output:

Must move the steps in the output by order of they appear.

format: [x, y], direction

coordination [x, y]

direction:
N: move up
S: move down
W: move left
E: move right

https://github.com/niruihao/Orixo_solver/blob/master/fig1.png

