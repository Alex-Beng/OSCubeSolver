# The brute force search for solving OS Cube(弹块魔方)

## Introduction

English | [中文](README.zh.md)

This project works for solving OS Cube. The alg is simplest brute force DFS, which limited the search depth to 14.
We all know the god number of 222 cube is 11, so it's enough for us to solve the OS Cube.

## Usage

1. get the cube state manually
2. input the cube state to the program
3. run the program and get the solution
4. follow any one of the solution, and solve!

The **only carefull thing** is how to get the cube state.

## Cube State

OS Cube work in 222 cube with 24 magnets on the 24 contect faces.
if twe contacted faces have the same pole, the repell each other, make the surface "pop".
we define the solved state as no surface "pop".


So we can define the surface with 0/1 with different contact pole.
Due to the binary pole, it's possible to flip the pole, which won't change the solution.


So, define the sequence order as the same as Speffz notation, 
with ULFRDB as the order, each face with clockwise order.

an example state looks like 001101110111010000110100

## Other experiment

see [extra](extra.md) for more experiment