from random import randint
from chromosome import Chromosome


class Population(object):

    def __init__(self):
        self.populationList = [Chromosome()] * 8065
        for index in range(0,8065):
            self.populationList[index] = Chromosome()
            self.populationList[index].initializeChromosome()
        self.initializePopulation()

    def initializePopulation(self):
        for parents in range(0,8065):
            for index in range(8):
                self.populationList[parents].combination[index] = randint(0, 7)

    def showPopulation(self):
        for index in range(0,8065):
            print(self.populationList[index].combination)
            print('fitness: ' + str(self.populationList[index].fitness))