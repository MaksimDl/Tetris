import tkinter as tk
from tkinter import Label
from tkinter import *
from PIL import ImageTk, Image
import copy
import keyboard

sizeM = 1000  # size of window
sizeN = 1000  # size of window
field_size_m = 20  # num of cells
field_size_n = 10  # num of cells
path_empty = "20.png"  # empty cell
path_filled = "20f.png"  # busy cell
x = 0  # position of begin cell of figure
y = 0

window = tk.Tk()
window.title("Tetris Test")
screen_resolution = str(sizeM) + 'x' + str(sizeN)
window.geometry(screen_resolution)
window.configure(background='grey')
window.resizable(False, False)
image_empty = ImageTk.PhotoImage(Image.open(path_empty))
image_filled = ImageTk.PhotoImage(Image.open(path_filled))


def figure_calibrate():
    global figure
    print_fig_over_field(1)
    print("before calibrate: ", figure, x, y)

    for times in range(0, 3):  # need to calibrate 3 times (remove 1 zero rows or cols at a time)
        i = 0
        while i < 3:
            sum_row = 0
            for j in range(0, 4):
                sum_row += figure[i][j]
            if sum_row == 0:
                for j in range(0, 4):
                    figure[i][j] = figure[i + 1][j]
                    figure[i + 1][j] = 0
            i += 1

        j = 0
        while j < 3:
            sum_col = 0
            for i in range(0, 4):
                sum_col += figure[i][j]
            if sum_col == 0:
                for i in range(0, 4):
                    figure[i][j] = figure[i][j + 1]
                    figure[i][j + 1] = 0
            j += 1

    print("after calibrate cols", figure)
    print_fig_over_field(0)


def go_rotate():
    global x
    global Y
    # check what will happen if figure will start not from [0][0] (fig[0][0] = 0)
    # rewrite position (x, y)
    print("Let's rotate!")
    global figure
    temp = copy.deepcopy(figure)
    print("cur_figure_before_rotate", figure)
    print_fig_over_field(1)  # erase current figure from screen

    # print(figure)

    for i in range(0, 4):
        for j in range(0, 4):
            print(figure[i][j], end=" ")
            figure[i][j] = temp[3 - j][i]
        print()
    print()
    print()

    if check_out_of_border() == 1 or check_for_crash_fig() == 1:  # rotate didn't succeed
        # can't rotate because will go out of field or out of main_array, or stack previously cells
        # get rotate back
        figure = copy.deepcopy(temp)
        print("rotate back")
        print_fig_over_field(0)  # print figure back to it's position
    else:  # rotate succeed
        print_fig_over_field(0)  # print rotated figure to screen

    del (temp)
    figure_calibrate()

    for i1 in range(0, 4):
        for j1 in range(0, 4):
            print(figure[i1][j1], end=" ")
        print()


def go_down():
    global x
    global y
    print_fig_over_field(1)  # remove figure in previous position before mooving
    x += 1
    if check_out_of_border() == 1 or check_for_crash_fig() == 1:
        # reach the bottom. stack the figure
        # or reach already stacked figure
        x -= 1
        stack_the_figure()
        print("got to the finish")
        print_fig_over_field(0)  # remove it after stack
    else:
        print_fig_over_field(0)


def go_up():  # for testing puprposes only -  wil not go in future. not checking!
    # check if can add!
    global x
    global y
    print_fig_over_field(1)  # remove figure in previous position before mooving
    x -= 1
    if check_out_of_border() == 0:
        print_fig_over_field(0)
    else:
        x += 1  # go to prev x, where fig didn't crash and finish
        print_fig_over_field(0)
        # stack_the_figure And reWrite the field! (our figure is already erased)
        print("got to the topline!")


def go_right():
    # check if can add!
    global x
    global y
    print_fig_over_field(1)  # remove figure in previous position before mooving
    y += 1
    if check_out_of_border() == 0 and check_for_crash_fig() == 0:
        print_fig_over_field(0)
    else:
        y -= 1  # go to prev x, where fig didn't crash and finish
        print_fig_over_field(0)
        # stack_the_figure And reWrite the field! (our figure is already erased)
        print("got to the right line!")


def go_left():
    # check if can add!
    global x
    global y
    print_fig_over_field(1)  # remove figure in previous position before mooving
    y -= 1
    if check_out_of_border() == 0 and check_for_crash_fig() == 0:
        print_fig_over_field(0)
    else:
        y += 1  # go to prev x, where fig didn't crash and finish
        print_fig_over_field(0)
        # stack_the_figure And reWrite the field! (our figure is already erased)
        print("got to the left  line!")


def com(event):
    # print("нажата клваиша",event.keysym)
    if event.keysym == "Down":
        print("down!")
        go_down()
    if event.keysym == "Up":
        print("up!")
        go_up()
    if event.keysym == "Left":
        print("Left!")
        go_left()
    if event.keysym == "Right":
        print("Right!")
        go_right()
    if event.keysym == "space":
        print("Space!")
        go_rotate()
    # left right down and up!


def get_figure():  # here will be random generated several figures. for right now - one
    # fig = [[1, 1, 1], [0, 0, 1]]
    global figure
    for i in range(0, 4):
        for j in range(0, 4):
            figure[i][j] = 0
    """"
    figure[0][0] = 1
    figure[0][1] = 1
    figure[0][2] = 1
    figure[0][3] = 1
    figure[1][3] = 1
    """
    figure[1][0] = 0
    figure[2][1] = 1
    figure[2][2] = 1
    figure[2][3] = 1
    figure[3][3] = 1
    global x
    x = 0
    global y
    y = 0

    figure_calibrate()

    # if appear already on busy field - game finishes!
    for i in range(x, x + 4):
        for j in range(y, y + 4):
            if figure[i - x][j - y] == 1 and main_field[i][j] == 1:
                end_game()
    return 1


def check_out_of_border():
    print("check border", x, y)
    if x < 0 or y < 0:
        return 1
    for i in range(0, 4):
        for j in range(0, 4):
            if figure[i][j] == 1:
                if x + i >= field_size_m or y + j >= field_size_n:
                    #  out of border (right or down)
                    return 1

    return 0


def check_for_crash_fig():
    print("check crash (x,y)", x, y)
    for i in range(x, x + 4):
        for j in range(y, y + 4):
            if figure[i - x][j - y] == 1 and main_field[i][j] == 1:
                return 1  # figure gets on any busy cell of field
    return 0  # everything OK


def print_array_debug(in_array):
    for i1 in range(0, field_size_m):
        for j1 in range(0, field_size_n):
            print(in_array[i1][j1], end=' ')
        print()


def print_main_field_to_window():
    # print_array_debug(main_field)

    for i in range(0, field_size_m):
        for j in range(0, field_size_n):
            if main_field[i][j] == 0:
                label = Label()
                label['image'] = image_empty
                label.grid(row=i, column=j, ipadx=0, ipady=0, padx=0, pady=0)
            elif main_field[i][j] == 1:

                label = Label()
                label['image'] = image_filled
                label.grid(row=i, column=j, ipadx=0, ipady=0, padx=0, pady=0)


def print_fig_over_field(clear):
    if clear == 0:
        for i in range(x, x + 4):
            for j in range(y, y + 4):
                if figure[i - x][j - y] == 1:
                    label = Label()
                    label['image'] = image_filled
                    label.grid(row=x + (i - x), column=y + (j - y), ipadx=0, ipady=0, padx=0, pady=0)
    elif clear == 1:
        for i in range(x, x + 4):
            for j in range(y, y + 4):
                if figure[i - x][j - y] == 1:
                    label = Label()
                    label['image'] = image_empty
                    label.grid(row=x + (i - x), column=y + (j - y), ipadx=0, ipady=0, padx=0, pady=0)


def stack_the_figure():
    global main_field
    for i in range(x, x + 4):
        for j in range(y, y + 4):
            if figure[i - x][j - y] == 1:
                main_field[i][j] = 1
    print_main_field_to_window()
    get_figure()


def end_game():
    print("yoo loose!")
    # print big picture! LOOSE


# init main field where empty and stacked cells will be stored. MxN size
main_field = [0] * field_size_m
for i in range(0, field_size_m):
    main_field[i] = [0] * field_size_n

# generate array for current figure(empty now). Supposed to be 4x4
figure = [0] * 4
for i in range(0, 4):
    figure[i] = [0] * 4

# for i in range(0, 4):
#    for j in range(0, 4):
#        print(figure[i][j], end=' ')
#    print()

# main_field[1][2] = 1

print_main_field_to_window()

get_figure()

print_fig_over_field(0)

window.bind("<Key>", com)

window.mainloop()
