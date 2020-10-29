from typing import Any


class Chromosome:

    def __int__(self, fitness, combination, fMeasure):
        self.fitness = fitness
        self.combination = combination
        self.fMeasure = fMeasure

    def initializeChromosome(self):
        self.fitness = 0
        self.combination = [0,0,0,0,0,0,0,0]
        self.fMeasure = 0