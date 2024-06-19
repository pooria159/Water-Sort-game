import copy
import heapq


class GameSolution:
    """
        A class for solving the Water Sort game and finding solutions(normal, optimal).

        Attributes:
            ws_game (Game): An instance of the Water Sort game which implemented in game.py file.
            moves (List[Tuple[int, int]]): A list of tuples representing moves between source and destination tubes.
            solution_found (bool): True if a solution is found, False otherwise.

        Methods:
            solve(self, current_state):
                Find a solution to the Water Sort game from the current state.
                After finding solution, please set (self.solution_found) to True and fill (self.moves) list.

            optimal_solve(self, current_state):
                Find an optimal solution to the Water Sort game from the current state.
                After finding solution, please set (self.solution_found) to True and fill (self.moves) list.
    """
    def __init__(self, game):
        """
            Initialize a GameSolution instance.
            Args:
                game (Game): An instance of the Water Sort game.
        """
        self.ws_game = game  # An instance of the Water Sort game.
        self.moves = []  # A list of tuples representing moves between source and destination tubes.
        self.tube_numbers = game.NEmptyTubes + game.NColor  # Number of tubes in the game.
        self.solution_found = False  # True if a solution is found, False otherwise.
        self.visited_tubes = set()  # A set of visited tubes.

    def solve(self, current_state):
        """
            Find a solution to the Water Sort game from the current state.

            Args:
                current_state (List[List[int]]): A list of lists representing the colors in each tube.

            This method attempts to find a solution to the Water Sort game by iteratively exploring
            different moves and configurations starting from the current state.
        """
        for limit in range(10000, 10001):
            self.visited_tubes.clear()
            if not self.solution_found:
                state = copy.deepcopy(current_state)
                self.DFS(state, 0, limit)
            else: 
                break

    def DFS(self, tubes, depth, limit, stack : list = []):
        self.visited_tubes.add(GameSolution.Hash(sorted(tubes)))
        if self.IsSolved(tubes):
            self.solution_found = True
            self.moves = copy.deepcopy(stack)
            return
        for neigh in self.DFSNeighbors(tubes):
            tmp = self.Next(tubes, neigh)
            if GameSolution.Hash(sorted(tubes)) not in self.visited_tubes and depth < limit:
                stack.append(neigh)
                self.DFS(tubes, depth+1, limit, stack)
                stack.pop()
            self.Prev(tubes, neigh, tmp)
            if self.solution_found:
                return
        
        
    def optimal_solve(self, current_state):
        """
            Find an optimal solution to the Water Sort game from the current state.

            Args:
                current_state (List[List[int]]): A list of lists representing the colors in each tube.

            This method attempts to find an optimal solution to the Water Sort game by minimizing
            the number of moves required to complete the game, starting from the current state.
        """
        q = []
        cost = {}
        par = {}
        ops = {}
        q.append((self.res(current_state), copy.deepcopy(current_state)))
        par[self.Hash(current_state)] = -1
        cost[self.Hash(current_state)] = 0
        index = -1
        while len(q) != 0:
            f, top = heapq.heappop(q)
            if f != cost[self.Hash(top)] + self.res(top):
                continue
            
            if self.IsSolved(top):
                self.solution_found = True
                index = self.Hash(top)
                break

            for neigh, op in self.Neighbors(top):
                if self.Hash(neigh) not in cost.keys() \
                        or cost[self.Hash(neigh)] > cost[self.Hash(top)] + 1:
                    cost[self.Hash(neigh)] = cost[self.Hash(top)] + 1
                    heapq.heappush(q, (cost[self.Hash(neigh)] + self.res(neigh), neigh))
                    par[self.Hash(neigh)] = self.Hash(top)
                    ops[self.Hash(neigh)] = op

        if self.solution_found:
            while par[index] != -1:
                self.moves.append(ops[index])
                index = par[index]
        
        self.moves = self.moves[::-1]

    @staticmethod
    def Hash(state):
        x1 = 7
        x2 = 293
        mod = 999999937
        hash = 0
        for i in state:
            _this_hash = 0
            for j in i:
                _this_hash = _this_hash * x1 + j + 1
            hash = hash * x2 + _this_hash
        return hash % mod

    def IsSolved(self, state):
        won = True
        for i in range(len(state)):
            if len(state[i]) > 0:
                if len(state[i]) != self.ws_game.NColorInTube:
                    won = False
                else:
                    main_color = state[i][-1]
                    for j in range(len(state[i])):
                        if state[i][j] != main_color:
                            won = False
        return won
    
    def Neighbors(self, state):
        neighs = []
        for i in range(self.tube_numbers):
            for j in range(self.tube_numbers):
                if i == j:
                    continue
                if len(state[i]) == 0:
                    continue
                if len(state[j]) == 0 or state[j][-1] == state[i][-1]:
                    neig = copy.deepcopy(state)
                    while len(neig[i]) != 0 and (len(neig[j]) == 0 or neig[i][-1] == neig[j][-1]) and len(neig[j]) < self.ws_game.NColorInTube:
                        neig[j].append(neig[i].pop(-1))
                    if sorted(neig) != sorted(state):
                        neighs.append((neig, (i, j)))
        return neighs

    def DFSNeighbors(self, state):
        neighs = []
        for i in range(self.tube_numbers):
            for j in range(self.tube_numbers):
                if i == j:
                    continue
                if len(state[i]) == 0:
                    continue
                neighs.append((i, j))
        return neighs
    
    def Next(self, state:list, neigh: tuple):
        tmp = 0
        i = neigh[0]
        j = neigh[1]
        while len(state[i]) != 0 and (len(state[j]) == 0 or state[i][-1] == state[j][-1]) \
                and len(state[j]) < self.ws_game.NColorInTube:
            state[j].append(state[i].pop())
            tmp += 1
        return tmp

    def Prev(self, state, neigh, tmp):
        i = neigh[0]
        j = neigh[1]
        while tmp:
            tmp -=1
            state[i].append(state[j].pop())

    def res(self, state):
        tmp = 0
        for i in range(self.tube_numbers):
            for j in range(1, len(state[i])):
                if state[i][j] == state[i][j-1]:
                    tmp += 1
        return self.ws_game.NColorInTube * self.ws_game.NColor - tmp