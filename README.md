# Orixo_solver
This is a game solver for the Orixo puzzle game.
The solver can handle the board with up to 3 independent boxes.
(If there is need to solve more than 3, please just split them to two parts and ran the solver for another time)

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

![image](https://github.com/niruihao/Orixo_solver/blob/master/fig1.png)

