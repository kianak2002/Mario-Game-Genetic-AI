import random
import copy


class Chromosome:
    def __init__(self, length):
        self.chromosome_cell = []
        self.chromosomes = []
        self.n = length

    '''
    build each chromosome randomly
    '''
    def build_chromosome(self):
        self.chromosome_cell = []
        choice = [0,2]
        for i in range(self.n):
            temp = random.randint(0, 2)
            if i>0 and self.chromosome_cell[i-1] == 1 and temp == 1:
                temp = random.choice(choice)
            self.chromosome_cell.append(temp)
        return self.chromosome_cell
    '''
    build 200 chromosomes for population and save it
    '''
    def build_all_chromosomes(self):
        for i in range(200):
            each_chromosome = self.build_chromosome()
            self.chromosomes.append(each_chromosome)
        print(self.chromosomes)
        return self.chromosomes


class Heuristic:
    def __init__(self, levels):
        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0

    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])

    def extra_jumps(self, steps, action):
        if action == "1":
            steps -= 0.5

    def get_score(self, actions):
        current_level = self.levels[self.current_level_index]
        steps, max = 0, 0
        for i in range(self.current_level_len):
            current_step = current_level[i]
            if current_step == '_':
                steps += 1
                self.extra_jumps(steps, actions[i-1])
            elif current_step == 'M':
                steps += 2
                self.extra_jumps(steps, actions[i-1])
            elif current_step == 'G' and actions[i - 2] == '1' and i > 1:
                steps += 3
            elif current_step == 'G' and actions[i - 1] == '1':
                steps += 1
            elif current_step == 'L' and actions[i - 1] == '2':
                steps += 1
            else:
                steps = 0
            if max < steps:
                max = steps
        if steps == self.current_level_len:
            max+= 5
        return steps == self.current_level_len, max

    


g = Heuristic(["M___GG_____G_"])
g.load_next_level()

# This outputs (False, 4)
# print(g.get_score("000100200100"))
print(g.get_score("0001000000100"))

# Chro = Chromosome(8)
# Chro.build_all_chromosomes()
