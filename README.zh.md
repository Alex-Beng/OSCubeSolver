# 使用暴力搜索解决OS Cube（弹块魔方）问题

## 简介

[English](README.md) | 中文

这个项目用于解决OS Cube问题。使用的算法是最简单的暴力深度优先搜索（DFS），限制搜索深度为14。
我们都知道2x2x2魔方的神数是11，所以这对我们解决OS Cube问题已经足够了。

## 使用`recov.py` 来求解

这个脚本只需要获取ULF面的平凹状态，并尝试多个解决方案，这将是交互式的。

1. 获取ULF面的平凹状态。0表示向下，1表示向上。
2. 运行程序并输入平凹状态
3. 按照指示操作，并尝试解决魔方


## 使用`main.py` 来求解

这个脚本需要获取魔方的完整状态，并找到**近似最优**（由于iddfs，它不是最优）但足够短的（低于8步）解决方案。

1. 手动获取魔方状态
2. 将魔方状态输入到程序中
3. 运行程序并获取解决方案
4. 按照任何一个解决方案，解决问题！

**唯一需要注意的事情**是如何获取魔方状态。

### 魔方状态

OS Cube在2x2x2魔方上工作，24个磁铁位于24个接触面上。
如果两个接触面有相同的极性，它们会互相排斥，使表面“弹出”。
我们定义解决状态为没有表面“弹出”。

所以我们可以用0/1定义具有不同接触极性的表面。
由于二进制极性，有可能翻转极性，这不会改变解决方案。

因此，定义序列顺序与Speffz符号法相同，
以ULFRDB为顺序，每个面按顺时针顺序。

一个示例状态看起来像 001101110111010000110100

## 其他实验的文档

查看[extra](extra.md)以获取更多实验的文档