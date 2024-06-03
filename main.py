# 这个有概率会翻转 0/1，先限定 0/1 字符
def str_to_state_first(state_str: str):
    # state str 只允许出现两种字符且数量相等
    # 顺序为ULFRBD，speffz编码的顺序
    # 同时，与speffz一致，均为顺时针开始编码
    
    # 按同样位置返回 0/1 数组
    state_str = state_str.strip()
    state_str_chars = list(set(state_str))
    assert len(state_str) == 24
    assert len(state_str_chars) == 2
    
    code_0 = state_str_chars[0]
    
    state_raw_array = [0 if c == code_0 else 1 for c in state_str]
    state_array = [state_raw_array[i:i+4] for i in range(0, 24, 4)]

    return state_array

def str_to_state(state_str: str):
    state_str = state_str.strip()
    state_str_chars = set(state_str)
    assert len(state_str) == 24
    assert state_str_chars == {'0', '1'}
    state_array = [list(map(int, state_str[i:i+4])) for i in range(0, 24, 4)]
    return state_array

def state_to_str(state_array: list):
    state_str = [0]*24
    for i in range(6):
        for j in range(4):
            state_str[i*4+j] = state_array[i][j]
    state_str = ''.join([str(i) for i in state_str])
    return state_str

face2idx = {
    'U': 0,
    'L': 1,
    'F': 2,
    'R': 3,
    'D': 4,
    'B': 5,
}

def is_solved(state_array: list):
    check_map = {
        'U': [3, 2, 1, 0],
        'L': [1, 0, 3, 2],
        'F': [1, 0, 3, 2],
    }
    face_map = {
        'U' : 'D',
        'L' : 'R',
        'F' : 'B',
    }
    
    # 检查 U L F 三个面的对面是不是 不一样的
    for f in ['U', 'L', 'F']:
        face_state = state_array[face2idx[f]]
        face_state_opposite = state_array[face2idx[face_map[f]]]
        for i in range(4):
            if face_state[i] == face_state_opposite[check_map[f][i]]:
                return False
    return True

def turn_R_rev(state_array: list):
    face_R = state_array[face2idx['R']]
    R_c0 = face_R[0]
    face_R[:3] = face_R[1:]
    face_R[3] = R_c0
    
    face_U = state_array[face2idx['U']]
    face_F = state_array[face2idx['F']]
    face_D = state_array[face2idx['D']]
    face_B = state_array[face2idx['B']]

    U_c1, U_c2 = face_U[1], face_U[2]
    face_U[1], face_U[2] = face_B[3], face_B[0]
    face_B[3], face_B[0] = face_D[1], face_D[2]
    face_D[1], face_D[2] = face_F[1], face_F[2]
    face_F[1], face_F[2] = U_c1, U_c2

def turn_R(state_array: list):
    for _ in range(3):
        turn_R_rev(state_array)

def turn_U_rev(state_array: list):
    face_U = state_array[face2idx['U']]
    U_c0 = face_U[0]
    face_U[:3] = face_U[1:]
    face_U[3] = U_c0

    face_F = state_array[face2idx['F']]
    face_R = state_array[face2idx['R']]
    face_B = state_array[face2idx['B']]
    face_L = state_array[face2idx['L']]

    F_c0, F_c1 = face_F[0], face_F[1]
    face_F[0], face_F[1] = face_L[0], face_L[1]
    face_L[0], face_L[1] = face_B[0], face_B[1]
    face_B[0], face_B[1] = face_R[0], face_R[1]
    face_R[0], face_R[1] = F_c0, F_c1

def turn_U(state_array: list):
    for _ in range(3):
        turn_U_rev(state_array)

def turn_F_rev(state_array: list):
    face_F = state_array[face2idx['F']]
    F_c0 = face_F[0]
    face_F[:3] = face_F[1:]
    face_F[3] = F_c0

    face_U = state_array[face2idx['U']]
    face_R = state_array[face2idx['R']]
    face_D = state_array[face2idx['D']]
    face_L = state_array[face2idx['L']]

    U_c2, U_c3 = face_U[2], face_U[3]
    face_U[2], face_U[3] = face_R[3], face_R[0]
    face_R[3], face_R[0] = face_D[0], face_D[1]
    face_D[0], face_D[1] = face_L[1], face_L[2]
    face_L[1], face_L[2] = U_c2, U_c3

def turn_F(state_array: list):
    for _ in range(3):
        turn_F_rev(state_array)

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