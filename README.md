# The brute force search for solving OS Cube(弹块魔方)

## Introduction

English | [中文](README.zh.md)

This project works for solving OS Cube. The alg is simplest brute force DFS, which limited the search depth to 14.
We all know the god number of 222 cube is 11, so it's enough for us to solve the OS Cube.


## Use `recov.py` to solve

This script only neet to get the up/down states of ULF faces, and may try multiple solutions, which will be interactive.

1. get the ULF faces' up/down string. 0 for down, 1 for up.
2. run the program and input the up/down string, the program will output the possible solutions one by one.
3. try the solution, type new up/down string will speed up(~3 algs)


## Use `main.py` to solve

This script need to get the full pole state of the cube, and find the **nearly optimal**(dut to the iddfs, it's not optimal) but short enough(8 HTM at most) solution.

1. get the cube state manually
2. input the cube state to the program
3. run the program and get the solution
4. follow any one of the solution, and solve!

The **only carefull thing** is how to get the cube state.

### Cube State

OS Cube work in 222 cube with 24 magnets on the 24 contect faces.
if twe contacted faces have the same pole, the repell each other, make the surface "pop".
we define the solved state as no surface "pop".


So we can define the surface with 0/1 with different contact pole.
Due to the binary pole, it's possible to flip the pole, which won't change the solution.


So, define the sequence order as the same as Speffz notation, 
with ULFRDB as the order, each face with clockwise order.

an example state looks like 001101110111010000110100


## Other experiment document

see [extra](extra.md) for more experiment