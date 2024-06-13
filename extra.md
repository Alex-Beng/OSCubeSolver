定义： 001 和 011 为两种不同的角块，其按顺时针的磁极为 0, 0, 1 和 0, 1, 1。

# 搜索四个 001 和四个 011 角块的可复原构型和复原状态

定义**构型**为：拼装时的角块orientation和permutation的组合。对于弹块/二阶魔方而言，仅取决于某一个角块的orientation状态。
故对弹块魔方而言，构型数为3。

定义**复原状态**为：所有接触面上的磁铁对的磁极都是相反的，即表面都是平的。

## 结论

三种构型均有复原状态，均可复原。且复原态均不相同。
 
## 各个构型的复原状态

| 构型 | 复原状态 |
| --- | --- |
|当前奇艺构型| 17个|
|奇艺构型+一个角块逆时针旋转|17个|
|奇艺构型+一个角块顺时针旋转|41个|

# 从平凹状态恢复状态

由上一节可知，实际上可能是一个平凹状态对应多个状态。

## 搜索不确定性的来源

1. DBL块的不确定，有6种可能
2. 不同状态对应同样的平凹状态


定义一个角块的主方向（类似于二阶魔方中R/D的方向）为，该面的颜色与其他两面不同。

# 通过恢复的状态尝试复原

尽管不能一次搜索就复原，但是可以通过交互式的方法，让用户遍历所有的可能解法。

即：
```
possible_states = SEARCH()
prev_solution = []
for possible_state in possible_states:
    possible_state.apply(prev_solution)
    possible_solution = SOLVE(possible_state)
    prev_solution.append(possible_solution)
    
    solved = input("Is it solved? (y/n, default n)")
    if solved == "y":
        break
```

possible_states为通过平凹状态搜索得到的所有可能状态。

