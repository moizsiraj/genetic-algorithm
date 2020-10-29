from chromosome import Chromosome
from population import Population
from random import randint
from random import shuffle
import traceback


class geneticAlgo(object):

    def __int__(self, population):
        self.population = population

    def initializeAlgo(self):
        self.population = Population()
        for index in range(0, 8065):
            self.fitnessFunction(self.population.populationList[index])
            self.setFMeasure(self.population.populationList[index])

    def fitnessFunction(self, chromosome):
        combination = chromosome.combination
        count = 0
        for places in range(0, 8):
            count = count + self.check1(combination, places, combination[places])
            count = count + self.check2(combination, places, combination[places])
            count = count + self.check3(combination, places, combination[places])
            count = count + self.check4(combination, places, combination[places])
            count = count + self.check5(combination, places, combination[places])
        chromosome.fitness = count
        return count

    def setFMeasure(self, chromosome):
        if chromosome.fitness != 0:
            chromosome.fMeasure = int((1 / chromosome.fitness) * 100)

    def check1(self, combination, place, location):  # rowCheck
        attackedBy = 0
        for index in range(0, 8):
            if index != place:
                if combination[index] == location:
                    attackedBy = attackedBy + 1
        return attackedBy

    def check2(self, combination, place, location):  # rightDown
        attackedBy = 0
        startIndex = place + 1
        startLocation = location + 1
        while startLocation <= 7 and startIndex <= 7:
            if combination[startIndex] == startLocation:
                attackedBy = attackedBy + 1
            startIndex = startIndex + 1
            startLocation = startLocation + 1
        return attackedBy

    def check3(self, combination, place, location):  # leftUp
        attackedBy = 0
        startIndex = place - 1
        startLocation = location - 1
        while startLocation >= 0 and startIndex >= 0:
            if combination[startIndex] == startLocation:
                attackedBy = attackedBy + 1
            startIndex = startIndex - 1
            startLocation = startLocation - 1
        return attackedBy

    def check4(self, combination, place, location):  # leftDown
        attackedBy = 0
        startIndex = place - 1
        startLocation = location + 1
        while startLocation <= 7 and startIndex >= 0:
            if combination[startIndex] == startLocation:
                attackedBy = attackedBy + 1
            startIndex = startIndex - 1
            startLocation = startLocation + 1
        return attackedBy

    def check5(self, combination, place, location):  # RightUp
        attackedBy = 0
        startIndex = place + 1
        startLocation = location - 1
        while startLocation >= 0 and startIndex <= 7:
            if combination[startIndex] == startLocation:
                attackedBy = attackedBy + 1
            startIndex = startIndex + 1
            startLocation = startLocation - 1
        return attackedBy

    def crossover(self, parent1, parent2):
        child = Chromosome()
        child.initializeChromosome()
        try:
            for index in range(0, 5):
                child.combination[index] = parent1.combination[index]
            for index in range(5, 8):
                child.combination[index] = parent2.combination[index]
        except AttributeError:
            traceback.print_exc()
        return child

    def mutation(self, chromosome):
        index = randint(0, 7)
        number = chromosome.combination[index]
        binNumber = bin(number).replace("0b", "")
        listBin = list(binNumber)
        if len(listBin) == 1:
            listBin.insert(0, 0)
            listBin.insert(1, 0)
        elif len(listBin) == 2:
            listBin.insert(0, 0)
        indexBin = randint(0, 2)
        if listBin[indexBin] == '1':
            listBin[indexBin] = '0'
        else:
            listBin[indexBin] = '1'
        s = [str(i) for i in listBin]
        listToStr = "".join(s)
        number = int(listToStr, 2)
        chromosome.combination[index] = number
        return chromosome

    def replaceWeakest(self, chromosome):
        self.population.populationList.sort(key=lambda x: x.fitness, reverse=True)
        if chromosome.fitness < self.population.populationList[0].fitness:
            self.population.populationList[0] = chromosome

    def calculateTotalFMeasure(self):
        sum = 0
        for index in range(0, 8065):
            sum = sum + self.population.populationList[index].fMeasure
        return sum

    def fillWheel(self):
        wheel = [Chromosome()] * self.calculateTotalFMeasure()
        startIndex = 0
        for index in range(0, 8065):
            chromosome = self.population.populationList[index]
            counter = 1
            while counter <= chromosome.fMeasure:
                wheel[startIndex] = chromosome
                counter = counter + 1
                startIndex = startIndex + 1
        return wheel

    def shuffleWheel(self, wheel):
        shuffle(wheel)
        return wheel

    def selectChromosome(self, wheel):
        index = int(self.calculateTotalFMeasure() / 2)
        chromosome = wheel[index]
        return chromosome

    def RWS(self):
        wheel = self.fillWheel()
        wheel = self.shuffleWheel(wheel)
        chromosome = self.selectChromosome(wheel)
        return chromosome

    def runGA(self):
        self.initializeAlgo()
        fitness = 100
        iteration = 0
        print('initial total fitness: ' + str(self.calculateTotalFMeasure()))
        while fitness != 0:
            iteration = iteration + 1
            parent1 = self.RWS()
            parent2 = self.RWS()
            newChromosome = self.crossover(parent1, parent2)
            newChromosome = self.mutation(newChromosome)
            self.fitnessFunction(newChromosome)
            self.setFMeasure(newChromosome)
            self.replaceWeakest(newChromosome)
            if newChromosome.fitness == 0:
                print("found")
                fitness = newChromosome.fitness
                print(newChromosome.combination)
                print(fitness)
                print(newChromosome.fMeasure)
                print('iteration: ' + str(iteration))
                print('final total fitness: ' + str(self.calculateTotalFMeasure()))
                exit(0)
            else:
                fitness = newChromosome.fitness
                print(newChromosome.combination)
                print(fitness)
                print(newChromosome.fMeasure)
                print('iteration: ' + str(iteration))
