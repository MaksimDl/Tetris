import tkinter as tk
from tkinter import Label
from tkinter import *
from PIL import ImageTk, Image
import keyboard

sizeM = 1000
sizeN = 1000
field_size_m = 20
field_size_n = 20
path_empty = "20.png"
path_filled = "20f.png"
x = 0
y = 0

window = tk.Tk()
window.title("Tetris Test")
screen_resolution = str(sizeM) + 'x' + str(sizeN)
window.geometry(screen_resolution)
window.configure(background='grey')
window.resizable(False, False)
image_empty = ImageTk.PhotoImage(Image.open(path_empty))
image_filled = ImageTk.PhotoImage(Image.open(path_filled))


def go_down():
    # check if can add!
    global x
    print_fig_over_field(1)
    x += 1
    print_fig_over_field(0)


def com(event):
    # print("нажата клваиша",event.keysym)
    if event.keysym == "Down":
        print("!!!!!!!")
        go_down()


def get_figure():
    # fig = [[1, 1, 1], [0, 0, 1]]
    global figure
    figure[0][0] = 1
    figure[0][1] = 1
    figure[0][2] = 1
    figure[0][3] = 1
    figure[1][3] = 1
    global x
    x = 0
    global y
    y = 0


def print_array_debug(in_array):
    for i1 in range(0, field_size_m):
        for j1 in range(0, field_size_n):
            print(in_array[i1][j1], end=' ')
        print()


def print_array_to_window(in_array, empty, filled):
    # print_array_debug(main_field)

    for i in range(0, field_size_m):
        for j in range(0, field_size_n):
            if in_array[i][j] == 0:
                label = Label()
                label['image'] = image_empty
                label.grid(row=i, column=j, ipadx=0, ipady=0, padx=0, pady=0)
            elif in_array[i][j] == 1:

                label = Label()
                label['image'] = filled
                label.grid(row=i, column=j, ipadx=0, ipady=0, padx=0, pady=0)


def print_fig_over_field(clear):
    if clear == 0:
        label = Label()
        label['image'] = image_filled
        label.grid(row=x, column=y, ipadx=0, ipady=0, padx=0, pady=0)
    elif clear == 1:
        label = Label()
        label['image'] = image_empty
        label.grid(row=x, column=y, ipadx=0, ipady=0, padx=0, pady=0)


# add main field where wi will store  everything
main_field = [0] * field_size_m
for i in range(0, field_size_n):
    main_field[i] = [0] * field_size_n

figure = [0] * 4
for i in range(0, 4):
    figure[i] = [0] * 4

# for i in range(0, 4):
#    for j in range(0, 4):
#        print(figure[i][j], end=' ')
#    print()

# main_field[1][2] = 1

# image_empty = ImageTk.PhotoImage(Image.open(path_empty))
# image_filled = ImageTk.PhotoImage(Image.open(path_filled))

print_array_to_window(main_field, image_empty, image_filled)
x = 100
y = 100

# print("x, y = ", x, y)
get_figure()

print_fig_over_field(0)

window.bind("<Key>", com)

window.mainloop()
