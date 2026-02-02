# search the 222 cube
# just for fun
# from twobytwo_utils import face2idx, str_to_state, state_to_str, is_solved
# from twobytwo_utils import turn_R, turn_U, turn_F, turn_R_rev, turn_U_rev, turn_F_rev

from oscube_utils import face2idx, str_to_state, state_to_str, is_solved
from oscube_utils import turn_R, turn_U, turn_F, turn_R_rev, turn_U_rev, turn_F_rev

# 维护一个 state -> RUF 步数的map
state2step = dict()
# 维护一个当前的steps
steps = []
# 当前的状态
current_state = []
depth_limit = 10
all_states = set()


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


# still iddfs
# 状态不是最优解就是了，，
def dfs():
    global current_state, steps, state2step
    if len(steps) > depth_limit:
        return
    for tidx in range(6):
        # 使用与os相同的剪枝
        if len(steps) >= 2 and steps[-1] == steps[-2] == tidx:
            continue
        if len(steps) >= 1 and steps[-1] == (tidx+3)%6:
            continue
        if len(steps) >= 1 and steps[-1] == tidx and steps[-1] > 2:
            continue
        tidx2func[tidx](current_state)
        state_str = state_to_str(current_state)
        steps.append(tidx)
        all_states.add(state_str)
        
        if state_str not in state2step or len(steps) < state2step[state_str]:
            state2step[state_str] = len(steps)
            all_states.add(state_str)
            dfs()
        steps.pop()
        tidx2func[(tidx+3)%6](current_state)

# 切成bfs看看
def bfs():
    global state2step
    import time
    beg_time = time.time()
    cur_depth = 0

    state_str = state_to_str(current_state)
    state2step[state_str] = 0
    queue = [state_str]
    
    # last_iter_time = time.time()
    while len(queue):
        # print(f"\rQueue: {len(queue)}", end="")
        # last_iter_time = time.time()

        cur_state_str = queue.pop(0)
        cur_state = str_to_state(cur_state_str)
        cur_step = state2step[cur_state_str]
        all_states.add(cur_state_str)

        if state2step[cur_state_str] > cur_depth:
            cur_depth = state2step[cur_state_str]
            print(f"Depth: {cur_depth}, Time: {time.time()-beg_time}, All state: {len(all_states)}")
            beg_time = time.time()

        for tidx in range(6):
            tidx2func[tidx](cur_state)
            new_state_str = state_to_str(cur_state)
            if new_state_str not in state2step or cur_step + 1 < state2step[new_state_str]:
                state2step[new_state_str] = cur_step + 1
                queue.append(new_state_str)
            tidx2func[(tidx+3)%6](cur_state)
    

def main():
    global current_state, steps, state2step, all_states, depth_limit

    state_str = "111010111010011010000010"
    import time
    for d in range(1, 15):
        # print(f"Depth: {d}")
        current_state = str_to_state(state_str)
        steps = []
        state2step = dict()
        state2step[state_str] = 0
        all_states = set()
        depth_limit = d
        beg_time = time.time()
        dfs()
        print(f"Depth: {d}, All state: {len(all_states)}, Time: {time.time()-beg_time}")

def bfs_main():
    global current_state, steps, state2step, all_states, depth_limit

    state_str = "000011112222333344445555"
    state_str = "111011110010011010000010"
    import time

    current_state = str_to_state(state_str)
    steps = []
    state2step = dict()
    state2step[state_str] = 0
    all_states = set()
    # depth_limit = d
    beg_time = time.time()
    bfs()
    # for d in range(1, 15):
    print(f"All state: {len(all_states)}, Time: {time.time()-beg_time}")

if __name__ == "__main__":
    # main()
    bfs_main()

'''
Depth: 1, All state: 33, Time: 0.000997304916381836
Depth: 2, All state: 153, Time: 0.000997781753540039
Depth: 3, All state: 687, Time: 0.0069806575775146484
Depth: 4, All state: 2943, Time: 0.03191566467285156
Depth: 5, All state: 11912, Time: 0.13463997840881348
Depth: 6, All state: 44970, Time: 0.4846835136413574
Depth: 7, All state: 159119, Time: 1.9148905277252197
Depth: 8, All state: 519627, Time: 7.04910135269165
Depth: 9, All state: 1450216, Time: 23.587539196014404
Depth: 10, All state: 2801068, Time: 66.45322751998901
Depth: 11, All state: 3583604, Time: 138.06610870361328
Depth: 12, All state: 3673884, Time: 214.8760039806366
Depth: 13, All state: 3674160, Time: 287.8271441459656
Depth: 14, All state: 3674160, Time: 359.45083022117615


'''