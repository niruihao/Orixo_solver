'''
Author: Ruihao Ni
EN.640.635 Software Carpentry
Lazor Project Substitute - Orixo Project
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

    '''
    fi = open(filename, 'r')
    bff = fi.read()
    line_split = bff.strip().split('\n')

    box = []
    a = line_split.index('GRID START')
    b = line_split.index('GRID STOP')

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

    nbox = 1 + box.count([])
    if nbox == 1:
        return [box]
    else:
        seg = [i for i in range(len(box)) if box[i] == []]
        if nbox == 2:
            return [box[0:seg[0]], box[seg[0] + 1:]]
        elif nbox == 3:
            return [box[0:seg[0]], box[seg[0] + 1:seg[1]], box[seg[1] + 1:]]


def num_point(box):
    numlist = []
    width, height = len(box[0]), len(box)
    for y in range(height):
        for x in range(width):
            if type(box[y][x]) == int:
                numlist.append([x, y])
    return numlist


class Block():

    def __init__(self, x, y, box):
        self.x = x
        self.y = y
        self.box = box

    def num(self):
        return self.box[self.y][self.x]

    def coor(self):
        return [self.x, self.y]

    def option(self):
        output = []
        width, height = len(self.box[0]), len(self.box)
        x, y = self.x, self.y
        # while x >= 0 and x <= width - 1 and y >= 0 and y <= height - 1:
        # check how many box available to be filled on the left side
        nW, nE, nN, nS = 0, 0, 0, 0
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
    move_list = []
    pointlist = num_point(box)
    for point in pointlist:
        a = Block(point[0], point[1], box)
        if len(a.option()) == 1 and a.option()[0][1] == a.num():
            move_list.append([a.coor(), a.option()[0]])
    return move_list


def may_move(box):
    choice_list = []
    pointlist = num_point(box)
    for point in pointlist:
        a = Block(point[0], point[1], box)
        for choice in a.option():
            choice_list.append([a.coor(), choice])
    return choice_list


def update_box(box, move_list):

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
    no = 0
    for line in box:
        for element in line:
            if element == 'o':
                no += 1
    return no


def solve(box):
    record1 = []
    box1 = box
    while must_move(box1):
        motion = must_move(box1)
        box1 = update_box(box1, motion)
        record1 += motion

    if count_o(box1) == 0:
        return record1

    box2 = box1
    record2 = record1

    maychoice = may_move(box2)
    for choice in maychoice:
        box3 = copy.deepcopy(box2)
        record3 = copy.deepcopy(record2)
        box4 = update_box(box3, [choice])
        record3.append(choice)

        while must_move(box4):
            motion = must_move(box4)
            box3 = update_box(box4, motion)
            record3 += motion

        if count_o(box4) == 0:
            return record3


def solve_problem(filename):
    filename1 = filename[:-4] + '_solution.txt'
    f = open(filename1, 'w')

    boxlist = read_bff(filename)
    if len(boxlist) == 1:
        solu1 = solve(boxlist[0])
        f.write('box1:' + '\n')
        for i in solu1:
            f.write(str(i[0]) + ',' + str(i[1][0]) + '\n')

    elif len(boxlist) == 2:
        solu1 = solve(boxlist[0])
        f.write('box1:' + '\n')
        for i in solu1:
            f.write(str(i[0]) + ',' + str(i[1][0]) + '\n')
        solu2 = solve(boxlist[1])
        f.write('\n' + 'box2:' + '\n')
        for i in solu2:
            f.write(str(i[0]) + ',' + str(i[1][0]) + '\n')

    elif len(boxlist) == 3:
        solu1 = solve(boxlist[0])
        f.write('box1:' + '\n')
        for i in solu1:
            f.write(str(i[0]) + ',' + str(i[1][0]) + '\n')
        solu2 = solve(boxlist[1])
        f.write('\n' + 'box2:' + '\n')
        for i in solu2:
            f.write(str(i[0]) + ',' + str(i[1][0]) + '\n')
        solu3 = solve(boxlist[2])
        f.write('\n' + 'box3:' + '\n')
        for i in solu3:
            f.write(str(i[0]) + ',' + str(i[1][0]) + '\n')
    f.close()


if __name__ == '__main__':
    solve_problem('board_1_02.bff')
    solve_problem('board_1_03.bff')
    solve_problem('board_1_13.bff')
    solve_problem('board_1_14.bff')
    solve_problem('board_1_50.bff')
    solve_problem('board_2_02.bff')
    solve_problem('board_2_16.bff')
    solve_problem('board_3_14.bff')
    solve_problem('board_4_26.bff')
