import crypt
import GuessGen
import sys

def main():
    users = [] #List of users to crack
    numUsers = 1
    while(numUsers < len(sys.argv)):
        users.append(sys.argv[numUsers])
        numUsers +=1
    #List of users added

    hashed_passes = []

    for u in users:
    #Module that will search for username in command line
        with open('/etc/shadow') as f:
            line = f.read()
            print(line)
            uName_Index = line.find(u)
            if uName_Index != -1: #if username found
                passIndexFirst = len(u) + 1
                chop = line[uName_Index+(passIndexFirst):] #starting from first index where username found + add up to index of when pass starts 
                colonAfterPass = chop.find(":") #find index of first occurrence of colon
                hashed = chop[0:colonAfterPass] #excluded colon index
                print("extracted hash:",end="")
                print(hashed)
                hashed_passes.append(hashed)

    solved_passes = []
    print(hashed_passes)
    if len(hashed_passes) == 0:
        print("users not found") 
        sys.exit()
    else:
        guesser = GuessGen.GuessGen()
        for word in hashed_passes:
            result = guesser.crackCycle(word)
            print(result)
            solved_passes.append(result)

    print(solved_passes)
   



if __name__ == "__main__":
    main()