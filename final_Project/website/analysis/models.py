from django.db import models

class Itemset:
    def __init__(self, rank, name, frequency, min_support):
        self.rank = rank
        self.name = name
        self.frequency = frequency
        self.min_support = min_support



