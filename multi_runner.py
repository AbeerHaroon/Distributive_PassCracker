import os
import GuessGen_rough as gR
import multiprocessing as mp

test_data = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n"]

#s = len(os.sched_getaffinity(0))

#print(s)

#m = gR.GuessGen_rough()

#x = m.getCores()

#print("GuessGen's getCores(): ", x)

def printList(x, tName):
    for l in x:
        print("Thread ", tName, ": ", l)

if __name__ == "__main__": 

    g = gR.GuessGen_rough("")

    #p1 = mp.Process(target=printList(test_data, "1"))
    #p2 = mp.Process(target=printList(test_data, "2"))

    #p1.start()
    #p2.start()
    #p1.join() #join() ensures child process is complete before main process offs
    #p2.join()

    g.mp_tick("xyu","$y$j9T$dunb35YUgYH54yaI9qCRk/$UouOdfBIbg2POJqh1zwZyJvg563o.1MWvO5RkV3Ljb/")

    #x = g.tick(g="12")
    #print(x)