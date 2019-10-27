import random
import copy

class Pumpkin_random:
    def __init__(self, GameData):
        self.GameData = GameData

    def getName(self):
        pass
    
    def initialize(self):
        pass
    
    def update(self):
        pass
    
    def dayStart(self):
        pass
    
    def talk(self):
        return "Over"

    def whisper(self):
        return "Over"

    def vote(self):
        return self.select_random()


    def attack(self):
        return self.select_random()
    
    def divine(self):
        return self.select_random()

    def guard(self):
        return self.select_random()

    def finish(self):
        pass

    def select_random(self):
        aliveAgent = copy.deepcopy(self.GameData.aliveAgent)
        myAgentIdx = self.GameData.myAgentIdx
        aliveAgent.remove(myAgentIdx)
        return random.choice(aliveAgent)