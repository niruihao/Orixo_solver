'''
Author: Ruihao Ni
EN.640.635 Software Carpentry
Lazor Project Substitute - Orixo Project
This is a solver program for the game Orixo.
It will read the input file bff and return
the solution to the level of game.
In the comment, the 'board' means the level of game
and the whole part of the picture.
The box means each of the individual part of the board,
and the grid means the single little box in the box.
'''

import copy


def read_bff(filename):
    '''
    Read the bff file and pick up all the information

    **Parameters**

        filename: *str*
            The .bff file that contains all the Lazor information

    **Return**

        list of boxes: *list*
            This is a list of list, the large list contain different
            boxes, the sublist contain information of each line of the boxes.
    '''
    fi = open(filename, 'r')
    bff = fi.read()
    line_split = bff.strip().split('\n')
    # split the input file by line

    box = []
    assert 'GRID START' in line_split, 'Please start input with GRID START'
    assert 'GRID STOP' in line_split, 'Please terminate input with GRID STOP'
    # if the input
    a = line_split.index('GRID START')
    b = line_split.index('GRID STOP')
    # get the index of start and end of the box

    for line in line_split[a + 1:b]:
        box_line = []
        for i in line:
            if i != ' ':
                if i == 'o' or i == 'x' or i == 'f':
                    box_line.append(i)
                else:
                    box_line.append(int(i))
        box.append(box_line)
    fi.close()
    # convert each line of the message to list

    nbox = 1 + box.count([])
    assert nbox <= 3, 'Don\'t input more than 3 boxes at one time'
    # nbox is the number of boxes in this board, cannot exceed 3

    if nbox == 1:
        return [box]
    else:
        seg = [i for i in range(len(box)) if box[i] == []]
        # find the empty line which segregate the boxes, then seperate
        # the boxes to multiple lists
        if nbox == 2:
            return [box[0:seg[0]], box[seg[0] + 1:]]
        elif nbox == 3:
            return [box[0:seg[0]], box[seg[0] + 1:seg[1]], box[seg[1] + 1:]]


def num_point(box):
    '''
    Read how many grid with a number in the box. Also include the
    information of the coordination of the number.

    **Parameters**

        box: *list*
            list which contain information of a single list.

    **Return**

        numlist: *list*
            A list of grid with number in the box, number + coordination

    '''
    numlist = []
    width, height = len(box[0]), len(box)
    for y in range(height):
        for x in range(width):
            if type(box[y][x]) == int:
                numlist.append([x, y])
    return numlist


class Block():
    '''
    input the coordination of the grid and name of the box,
    we can get the number on this grid, return it's coordination
    and we can read how many options of move is available for it.
    To use this class, we must specify the coordinatin of the number box
    and the box.
    '''

    def __init__(self, x, y, box):
        '''
        **Parameters**

            x: *int*
                x coordination of the number grid.
            y: *int*
                y coordination of the number grid.
            box: *list*
                specify which box we are dealing with
        '''
        self.x = x
        self.y = y
        self.box = box

    def num(self):
        '''
        **Return**
            num: *int*
                number on this grid.
        '''
        return self.box[self.y][self.x]

    def coor(self):
        '''
        **Return**
            coor: *list*
                coordination of this box.
        '''
        return [self.x, self.y]

    def option(self):
        '''
        **Return**
            option: *list*
                coordination of this box.
        Find all the moving options around the box. Count how many grids are
        available to move in each direction.

        '''
        output = []
        width, height = len(self.box[0]), len(self.box)
        x, y = self.x, self.y
        # while x >= 0 and x <= width - 1 and y >= 0 and y <= height - 1:
        # check how many box available to be filled on the left side
        nW, nE, nN, nS = 0, 0, 0, 0
        '''
        count the available moving steps, count 'o' boxes one by one,
        if it is number or filled box, skip the box and move to the next.
        If it is a 'x' or the boundary, terminate the counting.
        '''
        x0, y0 = x, y
        while x0 >= 0:
            if self.box[y0][x0] == 'x':
                break
            elif self.box[y0][x0] == 'o':
                nW += 1
            x0 -= 1
        x0, y0 = x, y
        while x0 <= width - 1:
            if self.box[y0][x0] == 'x':
                break
            elif self.box[y0][x0] == 'o':
                nE += 1
            x0 += 1
        x0, y0 = x, y
        while y0 >= 0:
            if self.box[y0][x0] == 'x':
                break
            elif self.box[y0][x0] == 'o':
                nN += 1
            y0 -= 1
        x0, y0 = x, y
        while y0 <= height - 1:
            if self.box[y0][x0] == 'x':
                break
            elif self.box[y0][x0] == 'o':
                nS += 1
            y0 += 1
        if nW != 0 and nW >= self.box[self.y][self.x]:
            output.append(['W', nW])
        if nE != 0 and nE >= self.box[self.y][self.x]:
            output.append(['E', nE])
        if nN != 0 and nN >= self.box[self.y][self.x]:
            output.append(['N', nN])
        if nS != 0 and nS >= self.box[self.y][self.x]:
            output.append(['S', nS])
        return output


def must_move(box):
    '''
    If there is only one direction for this grid to move
    and the available grids in this line equals to the number,
    we can say that we must make this move to solve the problem.

    **Parameters**

        box: *list*
            list which contain information of a single list.

    **Return**

        move_list: *list*
            All the must_move step in the current box.

    '''
    move_list = []
    pointlist = num_point(box)
    for point in pointlist:
        a = Block(point[0], point[1], box)
        if len(a.option()) == 1 and a.option()[0][1] == a.num():
            move_list.append([a.coor(), a.option()[0]])
    return move_list


def may_move(box):
    '''
    Return all the available move for the grid.

    **Parameters**

        box: *list*
            list which contain information of a single list.

    **Return**

        numlist: *list*
            All the other available move in this box.
    '''
    choice_list = []
    pointlist = num_point(box)
    for point in pointlist:
        a = Block(point[0], point[1], box)
        for choice in a.option():
            choice_list.append([a.coor(), choice])
    return choice_list


def update_box(box, move_list):
    '''
    After making the move, update the box just like swipe
    the number in the grid. The box was filled would be
    changed from 'o' to 'f'. And the number will return to
    zero.

    **Parameters**

        box: *list*
            list which contain information of a single list.

        move_list: *list*
            list of the move instrction.

    **Return**

        box1: *list*
            The updated box which move by the instruction.
    '''

    width, height = len(box[0]), len(box)
    box1 = box
    for move in move_list:
        x0, y0 = move[0][0], move[0][1]
        direction = move[1][0]
        n = Block(x0, y0, box1).num()
        box[y0][x0] = 0

        if direction == 'W':
            while x0 >= 0 and n > 0:
                if box1[y0][x0] == 'x':
                    break
                elif box1[y0][x0] == 'o':
                    box1[y0][x0] = 'f'
                    n -= 1
                x0 -= 1

        elif direction == 'E':
            while x0 <= width - 1 and n > 0:
                if box1[y0][x0] == 'x':
                    break
                elif box1[y0][x0] == 'o':
                    box1[y0][x0] = 'f'
                    n -= 1
                x0 += 1

        elif direction == 'N':
            while y0 >= 0 and n > 0:
                if box1[y0][x0] == 'x':
                    break
                elif box1[y0][x0] == 'o':
                    box1[y0][x0] = 'f'
                    n -= 1
                y0 -= 1

        elif direction == 'S':
            while y0 <= height - 1 and n > 0:
                if box1[y0][x0] == 'x':
                    break
                elif box1[y0][x0] == 'o':
                    box1[y0][x0] = 'f'
                    n -= 1
                y0 += 1
    return box1


def count_o(box):
    '''
    Count how many grids with 'o' in the box.

    **Parameters**

        box: *list*
            list which contain information of a single list.

    **Return**

        no: *int*
            the number of o boxes.
    '''
    no = 0
    for line in box:
        for element in line:
            if element == 'o':
                no += 1
    return no


def solve(box):
    '''
    This function can solve a single box.

    **Parameters**

        box: *list*
            list of box to be solved.

    **Return**

        record3: *list*
            Record the list of move(solution).

    '''
    record1 = []
    box1 = box
    # first move the 'must move'
    while must_move(box1):
        motion = must_move(box1)
        box1 = update_box(box1, motion)
        record1 += motion

    if count_o(box1) == 0:
        return record1

    box2 = box1
    record2 = record1
    # then move the 'may move'
    maychoice = may_move(box2)
    for choice in maychoice:
        box3 = copy.deepcopy(box2)
        record3 = copy.deepcopy(record2)
        box4 = update_box(box3, [choice])
        record3.append(choice)
        # the operate another 'must_move'
        while must_move(box4):
            motion = must_move(box4)
            box3 = update_box(box4, motion)
            record3 += motion

        if count_o(box4) == 0:
            return record3


def solve_problem(filename):
    '''

    **Parameters**

        filename: *str*
            name of the file.

    **Return**

        None
    '''
    def write_solu(solu):
        '''
        Write the each step of solution in the file
        the format is: coordination + direction.

        **Parameters**

            solu: *list*
                list which contain information of a single list.

        **Return**

            None
        '''
        for i in solu:
            f.write(str(i[0]) + ',' + str(i[1][0]) + '\n')

    filename1 = filename[:-4] + '_solution.txt'
    # create the filename of the output file
    f = open(filename1, 'w')
    f.write('**********************\nsolution:')
    boxlist = read_bff(filename)
    # read the bff and convert them to lists

    # solve the boxes and write all the steps in a text file.
    if len(boxlist) == 1:
        f.write('\nbox1:\n')
        write_solu(solve(boxlist[0]))

    elif len(boxlist) == 2:

        f.write('\nbox1:\n')
        write_solu(solve(boxlist[0]))

        f.write('\nbox2:\n')
        write_solu(solve(boxlist[1]))

    elif len(boxlist) == 3:

        f.write('\nbox1:\n')
        write_solu(solve(boxlist[0]))

        f.write('\nbox2:\n')
        write_solu(solve(boxlist[1]))

        f.write('\nbox3:\n')
        write_solu(solve(boxlist[2]))

    # add the output explanation
    f.write('\n**********************')
    f.write('\nhow to read the output:' + '\n' + '[x, y], direction\n\n')
    f.write('direction:\nN: move up\nS: move down\nW: move left\n')
    f.write('E: move right\n\ncoordination [x, y]\n x 0  1  2  3\n')
    f.write('y __ __ __ __\n0|__|__|__|__|\n1|__|__|__|__|\n')
    f.write('2|__|__|__|__|\n3|__|__|__|__|')
    f.write('\n**********************\n')

    f.close()


def Unittest():
    '''
    A Unit test function to test whether the functions are working.

    **Parameters**

        None

    **Return**

        None
    '''
    # Read the box
    boxlist = read_bff('board_1_13.bff')
    box = boxlist[0]

    # test read_bff function
    assert box[0][2] == 2, 'read_bff failed'
    assert box[1][4] == 1, 'read_bff failed'
    # test the numpoint function
    # numpoint:
    # [[1, 0], [2, 0], [3, 0], [1, 1], [4, 1], [4, 2], [0, 3]]
    assert num_point(box)[0] == [1, 0], 'num_point failed'
    # test count_o function, there are 12 o for original box
    assert count_o(box) == 12, 'count_o failed'

    a = Block(1, 1, box)
    # number for [1,1] is 1
    assert a.num() == 1
    # coordination is [1, 1]
    assert a.coor() == [1, 1]
    # option is [['E', 2], ['S', 2]]
    assert a.option()[0] == ['E', 2]
    b = Block(0, 3, box)
    # number for [0,3] is 2
    assert b.num() == 2
    # coordination is [0, 3]
    assert b.coor() == [0, 3]
    # option is [['E', 5]]
    assert b.option() == [['E', 5]]

    solved = (update_box(box, solve(box)))
    for y in range(len(solved)):
        for x in range(len(solved[0])):
            assert solved[y][x] == 'x' or solved[y][x] == 'f' \
                or solved[y][x] == 0
    print('11 unit tests are finished')


if __name__ == '__main__':
    # Unittest()

    solve_problem('board_1_02.bff')
    solve_problem('board_1_03.bff')
    solve_problem('board_1_13.bff')
    solve_problem('board_1_14.bff')
    solve_problem('board_1_50.bff')
    solve_problem('board_2_02.bff')
    solve_problem('board_2_16.bff')
    solve_problem('board_3_14.bff')
    solve_problem('board_4_26.bff')
