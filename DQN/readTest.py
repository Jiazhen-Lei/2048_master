from DQN2048 import *
import pickle
test = DQN()
with open(".\storage\DQNClass-score1604.pkl",'rb') as file:
    test = pickle.loads(file.read())

print(test.choose_action([16]*16))
