''' 
1. 搜索复原构型
2. 从当前平凹搜索可能的状态
'''

'''
1. 已经在main.py搜索了4个001和四个011角块的前提下，所有构型（指角块朝向组合）的复原构型数量，
   复原态数量分别为17 17 41，奇艺选择了其中一个17个复原状态的构型
'''

from enum import IntEnum


class Facelet(IntEnum):
    """
    The names of the facelet positions of the cube
              |********|
              |*U1**U2*|
              |********|
              |*U4**U3*|
              |********|
     |********|********|********|********|
     |*L1**L2*|*F1**F2*|*R1**R2*|*B1**B2*|
     |********|********|********|********|
     |*L4**L3*|*F4**F3*|*R4**R3*|*B4**B3*|
     |********|********|********|********|
              |********|
              |*D1**D2*|
              |********|
              |*D4**D3*|
              |********|
    Stolen from Kociemba's implementation
    The diffs is the order of the faces, here use ULFRDB with clockwise order in each face.
    """
    U1 = 0
    U2 = 1
    U3 = 2
    U4 = 3
    L1 = 4
    L2 = 5
    L3 = 6
    L4 = 7
    F1 = 8
    F2 = 9
    F3 = 10
    F4 = 11
    R1 = 12
    R2 = 13
    R3 = 14
    R4 = 15
    D1 = 16
    D2 = 17
    D3 = 18
    D4 = 19
    B1 = 20
    B2 = 21
    B3 = 22
    B4 = 23

class UpDownFacelet(IntEnum):
    """
    descript the os cube the flat or concave of surfaces
    the ULF faces' pole pairs
    with ULF and clockwise order
    """
    U1D4 = 0
    U2D3 = 1
    U3D2 = 2
    U4D1 = 3
    L1R2 = 4
    L2R1 = 5
    L3R4 = 6
    L4R3 = 7
    F1B2 = 8
    F2B1 = 9
    F3B4 = 10
    F4B3 = 11

Face2FaceMap = {
    Facelet.U1: Facelet.D4,
    Facelet.U2: Facelet.D3,
    Facelet.U3: Facelet.D2,
    Facelet.U4: Facelet.D1,
    Facelet.L1: Facelet.R2,
    Facelet.L2: Facelet.R1,
    Facelet.L3: Facelet.R4,
    Facelet.L4: Facelet.R3,
    Facelet.F1: Facelet.B2,
    Facelet.F2: Facelet.B1,
    Facelet.F3: Facelet.B4,
    Facelet.F4: Facelet.B3,
    # reverse
    Facelet.D4: Facelet.U1,
    Facelet.D3: Facelet.U2,
    Facelet.D2: Facelet.U3,
    Facelet.D1: Facelet.U4,
    Facelet.R2: Facelet.L1,
    Facelet.R1: Facelet.L2,
    Facelet.R4: Facelet.L3,
    Facelet.R3: Facelet.L4,
    Facelet.B2: Facelet.F1,
    Facelet.B1: Facelet.F2,
    Facelet.B4: Facelet.F3,
    Facelet.B3: Facelet.F4,
}

class UpDown(IntEnum):
    # may be up for high is more reasonable
    DOWN = 0
    UP = 1

class Pole(IntEnum):
    N = 0
    S = 1

class Corner(IntEnum):
    # stolen from Kociemba's implementation
    URF = 0
    UFL = 1
    ULB = 2
    UBR = 3
    DRB = 4
    DFR = 5
    DLF = 6
    DBL = 7


class Move(IntEnum):
    U1 = 0
    U2 = 1
    U3 = 2
    R1 = 3
    R2 = 4
    R3 = 5
    F1 = 6
    F2 = 7
    F3 = 8


# map cornerpositions to facelet positions
# the same corner orders with kociemba's
cornerFacelet = [
    [Facelet.U3, Facelet.R1, Facelet.F2],  # URF
    [Facelet.U4, Facelet.F1, Facelet.L2],  # UFL
    [Facelet.U1, Facelet.L1, Facelet.B2],  # ULB
    [Facelet.U2, Facelet.B1, Facelet.R2],  # UBR
    [Facelet.D3, Facelet.R3, Facelet.B4],  # DRB
    [Facelet.D2, Facelet.F3, Facelet.R4],  # DFR
    [Facelet.D1, Facelet.L3, Facelet.F4],  # DLF
    [Facelet.D4, Facelet.B3, Facelet.L4]   # DBL
]


# 使用generator yield所有可能的状态
# 1. 基于块的搜索，得到所有可能的状态（无视构型）
# 2. 基于构型的优先级排列，首先返回奇艺的构型的状态


class UpDownCube:
    """descript the os cube the up or down of surfaces"""
    def __init__(self) -> None:
        self.state = []
        # just a solved state, where there are other 16 solutions
        self.from_string('000000000000')
    def __str__(self) -> str:
        return self.to_string()
    
    def from_string(self, state_str: str):
        if len(state_str) != 12:
            return 'error state string length, should be 12'
        self.state = []
        for p in state_str:
            self.state.append(UpDown(int(p)))
    def to_string(self):
        return ''.join([str(p.value) for p in self.state])
    
    # reconstruct the possible pole cube
    def recon_polecube(self):
        for i in range(2**12):
            pole_pairs = []
            for j in range(12):
                pole_pairs.append((i >> j) & 1)
            # fullfill the pole cube from pole pairs
            full_poles = pole_pairs[:] + [-1]*12
            for j in range(12):
                full_poles[Face2FaceMap[j]] = pole_pairs[j] if self.state[j] == UpDown.UP else 1 - pole_pairs[j]
            yield PoleCube(''.join([str(p) for p in full_poles]))

            
class PoleCube:
    """represent the pole of the corner, similar to the kociemba's FaceCube"""
    def __init__(self, state_str) -> None:
        self.state = []
        self.from_string(state_str)    
    def __str__(self) -> str:
        return self.to_string()
    
    def from_string(self, state_str: str):
        if len(state_str) != 24:
            return 'error state string length, should be 24'
        self.state = []

        for p in state_str:
            self.state.append(Pole(int(p)))
    def to_string(self):
        return ''.join([str(p.value) for p in self.state])

    def from_oldstyle_state(self, state):
        self.state = []
        for i in state:
            for j in i:
                self.state.append(Pole(j))

    def to_oldstyle_state(self):
        return [[j.value for j in self.state[i:i+4]] for i in range(0, 24, 4)]

    def check_corner_valid(self):
        """
        check the corner with 4x001 and 4x011 corners exist
        """
        corner_exist = [0]*2
        for i in Corner:
            face_idxs = cornerFacelet[i]
            for j in range(3):
                if self.state[face_idxs[j]] != self.state[face_idxs[(j+1)%3]] \
                and self.state[face_idxs[j]] != self.state[face_idxs[(j+2)%3]]:
                    corner_exist[self.state[face_idxs[j]]] += 1
        if corner_exist[0] == 4 and corner_exist[1] == 4:
            return True
        return False

    def check_orientation(self):
        """
        it's not needed to write the koceimba's cubiecube class for cp and co
        just check the orientation of the corner is enough
        奇艺构型的 sum(co) % 3 == 2
        """
        corner_ori = [0]*8
        for i in Corner:
            face_idxs = cornerFacelet[i]
            for ori in range(3):
                if self.state[face_idxs[ori]] != self.state[face_idxs[(ori+1)%3]] \
                and self.state[face_idxs[ori]] != self.state[face_idxs[(ori+2)%3]]:
                    corner_ori[i] = ori
                    break
        return sum(corner_ori) % 3

from oscube_utils import face2idx, str_to_state, state_to_str, is_solved, state_to_viz_str
from oscube_utils import turn_R, turn_U, turn_F, turn_R_rev, turn_U_rev, turn_F_rev
from main import tidx2func, tidxes, tidx2str
from copy import deepcopy
from IPython import embed

def apply_pre_turns(current_state, pre_turns):
    for turn in pre_turns:
        tidx2func[turn](current_state)


def iddfs_solve(oldstyle_state, pre_turns):
    """ 
    just move the old implement iddfs in main.py to here
    """
    current_state = deepcopy(oldstyle_state)

    # turn the pre_turns
    apply_pre_turns(current_state, pre_turns)
    ori_current_state = deepcopy(current_state)

    state2step = dict()
    solution = []
    depth_limit = 10 # 8 is enough actually
    final_solution = []
    state2step[state_to_str(current_state)] = 0

    def iddfs():
        nonlocal final_solution
        if len(solution) > depth_limit:
            return
        for tidx in tidx2func:
            if len(solution) >= 2 and solution[-1] == solution[-2] == tidx:
                continue
            if len(solution) >= 1 and solution[-1] == (tidx+3)%6:
                continue
            if len(solution) >= 1 and solution[-1] == tidx and solution[-1] > 2:
                continue

            tidx2func[tidx](current_state)
            state_str = state_to_str(current_state)
            solution.append(tidx)
            if is_solved(current_state):
                final_solution = solution[:]
                return True

            if state_str not in state2step or len(solution) < state2step[state_str]:
                state2step[state_str] = len(solution)
                ret = iddfs()
                if ret:
                    return True
        
            solution.pop()
            tidx2func[(tidx+3)%6](current_state)
        return False
    for d in range(1, 9):
        # 傻逼了，这个需要的是pre_turns之后的状态，而不是传入的原始状态
        # current_state = deepcopy(oldstyle_state)
        current_state = deepcopy(ori_current_state)
        solution = []
        state2step = dict()
        state2step[state_to_str(current_state)] = 0
        depth_limit = d
        if iddfs():
            return final_solution, "".join([tidx2str[i] for i in final_solution])


    # if iddfs():
    #     return final_solution, "".join([tidx2str[i] for i in final_solution])
    print("No solution found")
    return None, None

def print_help():
    help_str = (
        "Input the up/down(0/1) of OSCube, and try the solutions one by one until solve\n"
        "Usage:\n"
        "   input the up/down of the OSCube, 0 for down, 1 for up\n"
        "   the ULF state, which is 12 0 or 1, is needed to input, eachface clockwise with ULF order\n"
        "   example: 111100001111 meaning the U and F faces are all up\n"
    )
    print(help_str)

def main():
    """
    the main function from up/down cube state to solve the cube with interaction
    """
    print_help()
    udc = UpDownCube()
    while True:
        prev_moves = []
        updown_state = input(">>>")        
        ret = udc.from_string(updown_state)
        if ret is not None:
            print(ret)
            continue
        # collect all the possible pole cube
        # search order: 2 0
        ori2pcs = {
            0: [],
            1: [],
            2: []
        }
        for pc in udc.recon_polecube():
            if not pc.check_corner_valid():
                continue
            ori2pcs[pc.check_orientation()].append(pc)
        # sort the pcs with the shortest solution
        # for i in [2, 0, 1]:
        #     ori2pcs[i].sort(key=lambda x: len(iddfs_solve(x.to_oldstyle_state(), prev_moves)[0]))

        # find the ori == 2
        structure_names = ['QiYi+1CW', 'QiYi+1CCW', 'QiYi']
        is_solved = False
        for i in [2, 0, 1]:
            print(f"-----------the {structure_names[i]} structure has {len(ori2pcs[i])} solutions")
            print(f"-----------Try the solutions line by line until solve:")
            rej_pcs = set()
            for (j, pc) in enumerate(ori2pcs[i]):
                if pc in rej_pcs: continue
                moves, moves_str = iddfs_solve(pc.to_oldstyle_state(), prev_moves)
                print(f'{j}: {moves_str}')
                raw_input = input("Is solved? input (y/n/curr state) default n: ")
                is_solved = True if raw_input == 'y' else False
                if is_solved:
                    break
                prev_moves += moves
                viz_state = raw_input if set(raw_input) == {'0', '1'} else ''
                if viz_state: # reject incorrect pcs
                    for _pc in ori2pcs[i]:
                        if _pc in rej_pcs: continue
                        _state = _pc.to_oldstyle_state()
                        apply_pre_turns(_state, prev_moves)

                        _viz_state = state_to_viz_str(_state)

                        if _viz_state[:len(viz_state)] != viz_state:
                            rej_pcs.add(_pc)
                    print(f"rej : {len(rej_pcs)}")
            if is_solved:
                break

    # test the iddfs_solve
    # cs = [[1, 1, 1, 0], [1, 0, 1, 1], [1, 0, 1, 0], [0, 1, 1, 0], [1, 0, 0, 0], [0, 0, 1, 0]]
    
    # ret, ret_s = iddfs_solve(cs, [])
    # print(ret_s, ret)

def updowncube_test():
    print("---------updowncube test")
    udc = UpDownCube()
    print(udc.to_string())
    udc.from_string('101000011000')
    udc.from_string('000000000000')
    # udc.from_string('111111111111')
    print(udc.to_string())
    it = udc.recon_polecube()
    pc = next(it)
    print(pc.to_string(), pc.check_corner_valid(), pc.check_orientation())

    cnts = [0]*3
    for pc in it:
        # print(pc.to_string())
        if pc.check_corner_valid():
            print(pc.to_string(), pc.check_orientation())
            cnts[pc.check_orientation()] += 1
            print(pc.to_oldstyle_state())
    print(cnts)

    print("------------------------")

def polecube_test():
    print("---------polecube test")
    pc = PoleCube('101100110010110000101110')
    print(pc.to_string())
    print(pc.check_corner_valid())
    print(pc.check_orientation())
    pc.from_string('110101110100010001000111')
    print(pc.to_string())
    print(pc.check_corner_valid())
    print(pc.check_orientation())
    print("------------------------")

def iddfs_test():
    print("---------iddfs test")
    known_state = [[1, 1, 1, 0], [1, 0, 1, 1], [1, 0, 1, 0], [0, 1, 1, 0], [1, 0, 0, 0], [0, 0, 1, 0]]
    # tidx2func[0](known_state)
    moves, moves_str = iddfs_solve(known_state, [0, 1, 2, ])
    print(moves_str, moves)
    print("------------------------")

if __name__ == "__main__":
    # the unit tests
    # updowncube_test()
    # exit()
    # polecube_test()
    # iddfs_test()
    # iddfs_test()
    main()