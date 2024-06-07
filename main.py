from utils import face2idx, str_to_state, state_to_str, is_oscube_solved
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
depth_limit = 10
solve_num = 0
solve_states = set()
all_states = set()

def dfs():
    global current_state, solution, state2step, solve_num, depth_limit, all_states
    # print(depth_limit)
    if len(solution) > depth_limit:
        return
    # try RUF turns
    for tidx in tidxes:
        # 如果和上两次的操作相同，那么就跳过
        if len(solution) >= 2 and solution[-1] == solution[-2] == tidx:
            continue
        # 如果和上次相同，且均为逆操作，那么跳过
        if len(solution) >= 1 and solution[-1] == (tidx+3)%6:
            continue
        # 如果和上次相同，且均为逆时针操作，那么跳过
        if len(solution) >= 1 and solution[-1] == tidx and solution[-1] > 2:
            continue

        # print(len(state2step), solved)
        # print(current_state)
        tidx2func[tidx](current_state)
        state_str = state_to_str(current_state)
        solution.append(tidx)
        # print(all_states)
        all_states.add(state_str)

        # 检查是否已经解决
        if is_oscube_solved(current_state):
            solve_num += 1
            # print("Solved!")
            # print("Solution: ", "".join([tidx2str[i] for i in solution]))
            # print("state: ", state_to_str(current_state))
            # print("statue: ", current_state)
            solve_states.add(state_to_str(current_state))
        
        # 这样搜会漏掉一些非最优解
        if state_str not in state2step or len(solution) < state2step[state_str]:
        # if True:
            state2step[state_str] = len(solution)
            dfs()
        solution.pop()
        tidx2func[(tidx+3)%6](current_state)

def main():
    global current_state, solution, state2step, depth_limit, all_states

    state_str = input("Enter the initial state: ")
    # 我直接硬编码我现在的状态
    state_str = "111010111010011010000010" if state_str == "" else state_str
    # 逆时针转角一次
    # state_str = "111110110010011010000010"
    # 顺时针转角一次
    # state_str = "111011110010011010000010"

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
    # print(is_oscube_solved(state_array))
    
    # 改成迭代加深搜索
    import time
    for d in range(1, 15):
        current_state = str_to_state(state_str)
        solution = []
        state2step = dict()
        state2step[state_str] = 0
        depth_limit = d
        beg_time = time.time()
        dfs()
        print(f"Depth limit: {d}, All state: {len(all_states)}, Solve num: {solve_num}, Solve state num: {len(solve_states)}, Time: {time.time()-beg_time}s")

if __name__ == "__main__":
    # 测试运行时间
    import time
    start_time = time.time()
    main()
    print(f"Time: {time.time()-start_time}s")
    print(f"Solve num: {solve_num}")