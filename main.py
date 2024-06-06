from utils import face2idx, str_to_state, state_to_str, is_solved
from utils import turn_R, turn_U, turn_F, turn_R_rev, turn_U_rev, turn_F_rev


tidx2func = {
    0: turn_R,
    1: turn_U,
    2: turn_F,
    3: turn_R_rev,
    4: turn_U_rev,
    5: turn_F_rev,
}
tidxes = tidx2func.keys()
tidx2str = ["R", "U", "F", "R'", "U'", "F'"]

# 维护一个 state -> RUF 步数的map
state2step = dict()
# 维护一个当前的解法
solution = []
# 当前的状态
current_state = []

def dfs():
    global current_state, solution, state2step, depth
    if len(solution) > 14:
        return
    # 检查是否已经解决
    solved = is_solved(current_state)
    if solved:
        print("Solved!")
        print("Solution: ", "".join([tidx2str[i] for i in solution]))
        print("state: ", state_to_str(current_state))
        return
    # try RUF turns
    for tidx in tidxes:
        # print(len(state2step), solved)
        # print(current_state)
        tidx2func[tidx](current_state)
        state_str = state_to_str(current_state)
        solution.append(tidx)
        # 仅有未出现过的状态才继续dfs
        if state_str not in state2step:
            state2step[state_str] = len(solution)
            dfs()
        solution.pop()
        tidx2func[(tidx+3)%6](current_state)

def main():
    global current_state, solution, state2step

    state_str = input("Enter the initial state: ")
    # 我直接硬编码我现在的状态
    state_str = "111010111010011010000010" if state_str == "" else state_str

    current_state = str_to_state(state_str)
    solution = []
    state2step = dict()
    state2step[state_str] = 0

    # 整点测试
    # print(current_state)
    # turn_R_rev(current_state)
    # turn_R(current_state)
    # turn_U_rev(current_state)
    # turn_U(current_state)
    # turn_F_rev(current_state)
    # turn_F(current_state)
    # print(current_state)

    # RRRRURRFFU

    # 测试是否solved
    # state_str = "111111111111000000000000"
    # state_array = str_to_state(state_str)
    # print(is_solved(state_array))

    dfs()

if __name__ == "__main__":
    # 测试运行时间
    import time
    start_time = time.time()
    main()
    print(f"Time: {time.time()-start_time}s")