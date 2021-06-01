import random
from matplotlib import pyplot

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
        # print(self.chromosomes)
        return self.chromosomes


class Heuristic:
    def __init__(self, levels):
        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0

    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])

    def get_score(self, actions):
        current_level = self.levels[self.current_level_index]
        steps, max = 0, 0
        win = True
        for i in range(self.current_level_len):
            current_step = current_level[i]
            if current_step == '_':
                steps += 1
                if i > 1 and actions[i - 2] == '1':
                    steps -= 0.5
            elif current_step == 'M':
                if (i > 0 and actions[i - 1] != '1') or i == 0:
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
                win = False
            if max < steps:
                max = steps
        if steps == self.current_level_len:
            max += 5
        if actions[len(actions) - 1] == '1':
            max += 1
        return max, win


class Game:
    def __init__(self, heuristic, chromosome):
        self.heuristic = heuristic
        self.chromosome = chromosome
        self.chromosomes = chromosome.build_all_chromosomes()
        self.average = 0
        self.avg_plot = []

    def score_all(self):
        population = []
        # ch = self.heuristic.get_score("2221000001021")
        # print(ch)
        for i in range(len(self.chromosomes)):
            string_chromosome = ''
            for j in range(len(self.chromosomes[i])):
                string_chromosome += str(self.chromosomes[i][j])
            population.append([string_chromosome, self.heuristic.get_score(string_chromosome)])
        population = self.sort(population)
        return population

    def sort(self, population):
        for i in range(len(population)):
            for j in range(len(population) - i - 1):
                if population[j][1] < population[j + 1][1]:
                    temp = population[j]
                    population[j] = population[j + 1]
                    population[j + 1] = temp
        return population

    def choose(self, children):
        grandchildren = []
        for i in range(int(len(children) / 2)):
            child1, child2 = self.cross_over(children)
            grandchildren.append(child1)
            grandchildren.append(child2)
        children = self.next_generation(children, grandchildren)
        children = self.mutation(children)
        self.game_over(children)
        return children

    def build_children(self, population, children):
        for i in range(int(len(population) / 2)):
            children.append(population[i])
        self.choose(children)

    def cross_over(self, children):
        random1 = random.randint(0, len(children) - 1)
        random2 = random.randint(0, len(children) - 1)
        chromosome1 = list(children[random1][0])
        chromosome2 = list(children[random2][0])
        for i in range(int(len(children[0][0]) / 2), len(children[0][0])):
            chromosome1[i], chromosome2[i] = chromosome2[i], chromosome1[i]
        chromosome1 = ''.join(chromosome1)
        chromosome2 = ''.join(chromosome2)
        return [chromosome1, h.get_score(chromosome1)], [chromosome2, h.get_score(chromosome2)]

    def next_generation(self, children, grandchildren):
        for i in range(len(children)):
            grandchildren.append(children[i])
        grandchildren = self.sort(grandchildren)
        children = []
        for i in range(int(len(grandchildren) / 2)):
            children.append(grandchildren[i])
        return children

    def game_over(self, children):
        check = 0
        average = self.heuristic_avg(children)
        if average - self.average < 0.000001:
            for i in range(len(children)):
                if children[i][1][1] == True:
                    print('YOU WIN WITH', children[i][1][0], 'SCORE :)')
                    print(children[i][0])
                    check = 1
                    # pyplot.plot(len(self.avg_plot), self.avg_plot)
                    break
            if check == 0:
                print('YOU LOSE WITH', children[0][1][0], 'SCORE :(')
                print(children[0][0])
                check = 1
        self.average = average
        if check == 0:
            self.choose(children)
        # print(len(children), "yup")
        # max_score = 0
        # for i in range(len(h.levels[0])):
        #     if h.levels[0][i] == '_' or h.levels[0][i] == 'L':
        #         max_score += 1
        #     elif h.levels[0][i] == 'G':
        #         if i > 0 and h.levels[0][i - 1] != 'G':
        #             max_score += 3
        #         else:
        #             max_score += 1
        #     elif h.levels[0][i] == 'M':
        #         max_score += 3
        # max_score += 1
        # print("maxxxxxx", max_score)

        # print(children[0][1][0])
        # if children[0][1][0] == max_score and children[0][1][1] == True:
        #     print('YOU WIN WITH', max_score, 'SCORE :)')
        #     print(children[0][0])
        # else:
        #     self.choose(children)
        # self.average = average

    def mutation(self, grandchildren):
        # print(grandchildren)
        k = random.randint(0, len(grandchildren[0][0]))  # change how many cells
        for j in range(len(grandchildren)):
            for i in range(k):
                yes_no = random.choices([0, 1], weights=(80, 20), k=1)  # yes or no
                if yes_no == 1:
                    change = random.randint(0, len(grandchildren[0][0]))
                    grandchildren[j][0][change] = 0  # reset to zero
        # print(grandchildren, "changedddd")
        return grandchildren

    def heuristic_avg(self, grandchildren):
        sum_value = 0
        for i in range(len(grandchildren)):
            sum_value += grandchildren[i][1][0]
        average = sum_value / len(grandchildren)
        print(average)
        self.avg_plot.append(average)
        return average


if __name__ == '__main__':
    num = 1
    for i in range(10):
        file_name = "level" + str(num) + ".txt"
        f = open(file_name, "r")
        content = f.read()
        print(content)
        h = Heuristic([content])
        # h = Heuristic(["_M__GG_____G_"])
        h.load_next_level()
        print(len(content))
        Chro = Chromosome(len(content))
        game = Game(h, Chro)
        population = game.score_all()
        game.build_children(population, [])
        num += 1
