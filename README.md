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
        choice = [0, 2]
        for i in range(self.n):
            temp = random.randint(0, 2)
            if i > 0 and self.chromosome_cell[i - 1] == 1 and temp == 1:
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

    # def extra_jumps(self, steps, action):
        # if action == "1":
        #     steps -= 0.5

    def get_score(self, actions):
        current_level = self.levels[self.current_level_index]
        steps, max = 0, 0
        for i in range(self.current_level_len):
            current_step = current_level[i]
            if current_step == '_':
                steps += 1
                if i > 1 and actions[i-2] == '1':
                    steps -= 0.5
            elif current_step == 'M':
                if (i > 0 and actions[i-1] != '1') or i == 0:
                    steps += 3
                if i > 1 and actions[i - 2] == "1":
                    steps -= 0.5
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
            max += 5
        if actions[len(actions)-1] == '1':
            max += 1
        return max

class Game:
    def __init__(self, heuristic, chromosome):
        self.heuristic = heuristic
        self.chromosome = chromosome
        self.chromosomes = chromosome.build_all_chromosomes()

    def score_all(self):
        population = []
        # ch = self.heuristic.get_score("2221000001021")
        # print(ch)
        for i in range (len(self.chromosomes)):
            string_chromosome = ''
            for j in range (len(self.chromosomes[i])):
                string_chromosome += str(self.chromosomes[i][j])
            population.append([string_chromosome, self.heuristic.get_score(string_chromosome)])
        print(population)
        population = self.sort(population)
        return population

    def sort(self, population):
        for i in range (len(population)):
            for j in range(len(population)-i-1):
                if population[j][1] < population[j+1][1]:
                    temp = population[j]
                    population[j] = population[j+1]
                    population[j+1] = temp
        print(population)
        return population

    def choose(self, population):
        children = []
        for i in range (int(len(population)/2)):
            children.append(population[i])
        self.crossOver(children)
        return children

    def build_children(self, population):
        self.choose(population)

    def crossOver(self, children):
        chromosome1 = random.randint(0, len(children))
        chromosome2 = random.randint(0, len(children))
        print(children[chromosome1], children[chromosome2])
        for i in range (int(len(children[0][0])/2), len(children[0][0])):
            children[chromosome1][0], children[chromosome2][0] = children[chromosome2][0] , children[chromosome1][0]
        children[0] = ''.join(children[0])
        children[0] = ''.join(children[0])
        print(chromosome1, chromosome2)
        print(children[chromosome1], children[chromosome2])

        #     temp1 = chromosome1[0]






if __name__ == '__main__':
    g = Heuristic(["_M__GG_____G_"])
    g.load_next_level()
    # print(g.get_score("0001000000100"))
    Chro = Chromosome(13)
    game = Game(g, Chro)
    population = game.score_all()
    game.build_children(population)
