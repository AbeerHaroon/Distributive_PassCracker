import os
import GuessGen

s = len(os.sched_getaffinity(0))

print(s)

m = GuessGen.GuessGen()

x = m.getCores()

print("GuessGen's getCores(): ", x)