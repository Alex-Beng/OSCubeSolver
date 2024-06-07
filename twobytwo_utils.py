face2idx = {
    'U': 0,
    'L': 1,
    'F': 2,
    'R': 3,
    'D': 4,
    'B': 5,
}

def str_to_state(state_str: str):
    state_str = state_str.strip()
    state_str_chars = set(state_str)
    assert len(state_str) == 24
    assert state_str_chars == {'0', '1', '2', '3', '4', '5'}
    state_array = [list(map(int, state_str[i:i+4])) for i in range(0, 24, 4)]
    return state_array

def state_to_str(state_array: list):
    state_str = [0]*24
    for i in range(6):
        for j in range(4):
            state_str[i*4+j] = state_array[i][j]
    state_str = ''.join([str(i) for i in state_str])
    return state_str

def is_solved(state_array: list):
    # 只要检查每个面是不是一个颜色即可
    for f in state_array:
        if len(set(f)) != 1:
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