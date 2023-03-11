import tkinter as tk
from tkinter import Label
from tkinter import *
from PIL import ImageTk, Image
import copy
from random import randint
import time
import keyboard

sizeM = 1000  # size of window
sizeN = 1000  # size of window
field_size_m = 30  # num of cells
field_size_n = 15  # num of cells
path_empty = "20.png"  # empty cell
path_filled = "20f.png"  # busy cell
x = 0  # position of begin cell of figure
y = 0
score = 0

window = tk.Tk()
window.title("Tetris Test")
screen_resolution = str(sizeM) + 'x' + str(sizeN)
window.geometry(screen_resolution)
window.configure(background='grey')
window.resizable(False, False)
image_empty = ImageTk.PhotoImage(Image.open(path_empty))
image_filled = ImageTk.PhotoImage(Image.open(path_filled))


def figure_calibrate(flag_check=0):
    # flag check = 1 if we are not sure will it fit (when we are calibrating only for test)
    global figure
    start = time.time()
    if flag_check != 1:
        print_fig_over_field(1)
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
    if flag_check != 1:
        print_fig_over_field(0)
    end = time.time()
    print("calibrate method takes :", (end - start) * 10 ** 3, "ms")


def go_rotate():
    global x
    global y
    start = time.time()
    global figure
    temp = copy.deepcopy(figure)
    print_fig_over_field(1)  # erase current figure from screen

    # print(figure)
    for i in range(0, 4):
        for j in range(0, 4):
            figure[i][j] = temp[3 - j][i]

    figure_calibrate(1)
    if check_out_of_border() == 1 or check_for_crash_fig() == 1:  # rotate didn't succeed
        # can't rotate because will go out of field or out of main_array, or stack previously cells
        # get rotate back
        figure = copy.deepcopy(temp)
        print_fig_over_field(0)  # print figure back to it's position
    else:  # rotate succeed
        print_fig_over_field(0)  # print rotated figure to screen
    del temp
    end = time.time()
    print("rotate method takes :", (end - start) * 10 ** 3, "ms")


def go_down():
    global x
    global y
    start = time.time()
    print_fig_over_field(1)  # remove figure in previous position before mooving
    x += 1
    if check_out_of_border() == 1 or check_for_crash_fig() == 1:
        # reach the bottom. stack the figure
        # or reach already stacked figure
        x -= 1
        stack_the_figure()
    else:
        print_fig_over_field(0)
    end = time.time()
    print("go down method takes :", (end - start) * 10 ** 3, "ms")


def go_up():  # for testing puprposes only -  wil not go in future. not checking!
    # check if can add!
    global x
    global y
    start = time.time()
    print_fig_over_field(1)  # remove figure in previous position before mooving
    x -= 1
    if check_out_of_border() == 0:
        print_fig_over_field(0)
    else:
        x += 1  # go to prev x, where fig didn't crash and finish
        print_fig_over_field(0)
        # stack_the_figure And reWrite the field! (our figure is already erased)
    end = time.time()
    print("go up method takes :", (end - start) * 10 ** 3, "ms")


def go_right():
    # check if can add!
    global x
    global y
    start = time.time()
    print_fig_over_field(1)  # remove figure in previous position before mooving
    y += 1
    if check_out_of_border() == 0 and check_for_crash_fig() == 0:
        print_fig_over_field(0)
    else:
        y -= 1  # go to prev x, where fig didn't crash and finish
        print_fig_over_field(0)
        # stack_the_figure And reWrite the field! (our figure is already erased)
    end = time.time()
    print("go right method takes :", (end - start) * 10 ** 3, "ms")


def go_left():
    # check if can add!
    global x
    global y
    start = time.time()
    print_fig_over_field(1)  # remove figure in previous position before mooving
    y -= 1
    if check_out_of_border() == 0 and check_for_crash_fig() == 0:
        print_fig_over_field(0)
    else:
        y += 1  # go to prev x, where fig didn't crash and finish
        print_fig_over_field(0)
        # stack_the_figure And reWrite the field! (our figure is already erased)
    end = time.time()
    print("go left method takes :", (end - start) * 10 ** 3, "ms")


def com(event):
    # print("нажата клавиша",event.keysym)
    start = time.time()
    if event.keysym == "Down":
        go_down()
    if event.keysym == "Up":
        go_up()
    if event.keysym == "Left":
        go_left()
    if event.keysym == "Right":
        go_right()
    if event.keysym == "space":
        go_rotate()
    # left right down and up!
    end = time.time()
    print("com method takes :", (end - start) * 10 ** 3, "ms")


def get_figure():  # here will be random generated several figures. for right now - one
    global figure
    global x
    x = 0
    global y
    y = 0
    start = time.time()
    # clear previous
    for i in range(0, 4):
        for j in range(0, 4):
            figure[i][j] = 0
    choose = randint(0, 4)
    if choose == 0:
        figure = [[1, 1, 1, 1], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    if choose == 1:
        figure = [[1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    if choose == 2:
        figure = [[1, 1, 0, 0], [1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]]
    if choose == 3:
        figure = [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    if choose == 4:
        figure = [[1, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]]
    figure_calibrate()
    # if appear already on busy field - game finishes!
    for i in range(x, x + 4):
        for j in range(y, y + 4):
            if figure[i - x][j - y] == 1 and main_field[i][j] == 1:
                end_game()
    end = time.time()

    print("get figure method takes :", (end - start) * 10 ** 3, "ms")
    return 1


def check_out_of_border():
    start = time.time()
    if x < 0 or y < 0:
        return 1
    for i in range(0, 4):
        for j in range(0, 4):
            if figure[i][j] == 1:
                if x + i >= field_size_m or y + j >= field_size_n:
                    #  out of border (right or down)
                    end = time.time()
                    print("check out of border(return 1) method takes :", (end - start) * 10 ** 3, "ms")
                    return 1
    end = time.time()
    print("check out of border(return 0) method takes :", (end - start) * 10 ** 3, "ms")
    return 0


def check_for_crash_fig():
    start = time.time()
    for i in range(x, x + 4):
        for j in range(y, y + 4):
            if figure[i - x][j - y] == 1 and main_field[i][j] == 1:
                end = time.time()
                print("check for crash (return 1) method takes :", (end - start) * 10 ** 3, "ms")
                return 1  # figure gets on any busy cell of field
    end = time.time()
    print("check for crash (return 0) method takes :", (end - start) * 10 ** 3, "ms")
    return 0  # everything OK


def print_main_field_to_window():
    start = time.time()
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
    label = Label()
    label['text'] = "score"
    label.grid(row=field_size_m + 3, column=0, columnspan=2)

    label = Label()
    label['text'] = score
    label.grid(row=field_size_m + 3, column=2, columnspan=2)
    end = time.time()
    print("print_main_field method takes :", (end - start) * 10 ** 3, "ms")


def print_fig_over_field(clear):
    start = time.time()
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
    end = time.time()
    print("fig_over_field method takes :", (end - start) * 10 ** 3, "ms")


def stack_the_figure():
    global main_field
    start = time.time()
    for i in range(x, x + 4):
        for j in range(y, y + 4):
            if figure[i - x][j - y] == 1:
                main_field[i][j] = 1
    clear_full_lines()
    get_figure()
    end = time.time()
    print("stack figure (after 2 other methods) method takes :", (end - start) * 10 ** 3, "ms")


def clear_full_lines():
    global score
    start = time.time()
    i = field_size_m - 1  # begin from end
    count = 0  # because our fig is not more than 4 squares - not more than 4 lines will be cleared
    while count < 4 or i > 0:
        sum_cols = 0
        if count > 0:
            count += 1
        for j in range(0, field_size_n):
            sum_cols += main_field[i][j]
        if sum_cols == 0:
            count = 4  # if  we meet line wit all 0 - no need to check father - make condition to exit
            i = 1
        elif sum_cols == field_size_n:
            if count == 0:  # if we weem line to erase for first time - start count 4 times. here if no to count twice
                count += 1
            score += sum_cols
            # now start clearing the field (clear zero line, shift others)
            i1 = i
            while i1 > 0:
                for j1 in range(0, field_size_n):
                    main_field[i1][j1] = main_field[i1 - 1][j1]  # take values from line above
                i1 -= 1
            for j1 in range(0, field_size_n):
                main_field[0][j1] = 0
            if i + 1 <= field_size_m - 1:
                i += 1
        i -= 1
    end = time.time()
    print("clear_full_lines method takes :", (end - start) * 10 ** 3, "ms")
    print_main_field_to_window()


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
