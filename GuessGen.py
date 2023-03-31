#!/usr/bin/python3
import crypt
from os import sched_getaffinity
#The Guesser Machine
#Takes guess string as parameter then works on it
#has a list of 1s and 0s (no error checking) that indicate if incrementing or decrementing flow
class GuessGen: 

    MAXIMUM = 126
    MINIMUM = 32

    guess = "default" 
    
    #singleton indicator. 
        #List of number, either one/zero
        #One indicating incrementing ASCII value
        #Zero means decrementing ASCII value 
        #Upon construction. Flow, indicators are all set to 1, 
            # according to number of characters in guess
    flow_signs = [] 

    def __init__(self):
        self.guess = "~}" #8 whitespaces
        for letter in  self.guess :
            self.flow_signs.append(1)
        
        print("initial guess: ", self.guess, end="\n")
        print("flow of initial guess: ", self.flow_signs) #set the flow indicators. 1 by default

    #runs the crypt method and if the attempt_param is the correct guess
    #returns true
    #else, retrns false
    def checkHash(self,attempt_param, hashed_pw):
        attempt_hash = crypt.crypt(word=attempt_param,salt=hashed_pw)
        #print(attempt_hash)
        if(attempt_hash == hashed_pw):
            return True
        else:
            return False

    #function that will try every combo from 8 - 20 character length
    #if any match, will return the string
    #param target_hash - the hashed string which we will try to crack
    def crackCycle(self, target_hash):
        length = len(self.guess) #number of characters we start with
        attempt = self.guess 
        result = ""
        found = 0 #turns to 1 if found
        count = 0
        while (length < 21): #20 character guesses
            while (found == 0) : #if found or 96^(length) times tried
                #precursor = crypt.crypt(word=attempt, salt=target_hash)
                b = self.checkHash(attempt,target_hash) #the attempt
                #print("hash attempt:", end=" ")
                #print(b)
                if b is True:
                    found = 1
                    result = attempt
                    return result
                else:
                    count += 1
                    #if (attempt == "~"): #if attempt is last character of charset when length is 1
                    #    length +=1 #increase character
                    #    attempt += " " #add ASCII 32 (Space)
                    #    self.flow_signs.append(1)
                    a = self.tick(attempt)
                    attempt = a
        return "NO_PW_FOUND"
    #the motion to tick the combination one move forward
    #the first letter keeps going up and down
    #other letters are dependent on the letter before.
    #when prior character hits an edge character, 
        # depeneding on flow of character it questions, it will increment/decrement
    #param (string) g - the guess that has already been tried and we will now iterate
    #return - new, iterated string which is the guess. 
    #Note: There is no increment when at ASCII 126
    #      There is no decrement when at ASCII 32 
    def tick(self,g):
        print("before tick:", end=" ")
        print(g)
        original_str = list(str(g)) #the guess, turned to a List, so we could access each chars
        #if the flow changes, we'll reflect it on this copy then assign to instance variable
        #Doing this because not sure how Python behaves when passing Lists
        flow_copy = [] 
        flow_self = self.flow_signs
        flow_copy = flow_self.copy()
        iterated_str = str(g) #new string which we will return
        i = 0 #this helps to check the flow in each character

        while (i != len(iterated_str)): #while i is less than length of guess string
            if i == 0: #if first letter
                if flow_copy[i] == 0: #if decrementing flow
                    if ord(original_str[i]) == 32: 
                        if(len(original_str) == 1): #if 1 letter in guess
                            flow_copy[i] = 1 #changed flow of current bit 
                            new_char = chr(32) 
                            original_str[i] = new_char #ASCII 32 in first letter.
                            #
                            original_str.append(" ") #added ASCII 32 to guess List form
                            flow_copy.append(1) #adjusted flow
                        else: #length of guess is not 1    
                            flow_copy[i] = 1 #changed flow to increment now 
                    else :
                        current = ord(original_str[i]) #take ascii value
                        new_char = current - 1 #decrement
                        original_str[i] = chr(new_char) #convert to char, then into string
                elif flow_copy[i] == 1: #if incrementing flow
                    if(ord(original_str[i])) == 126:
                        #new_char = chr(125) #decremented. changed flow
                        #g[i:(i+1)] = new_char
                        flow_copy[i] = 0 #changed to decrementing flow
                    else :
                        current = ord(original_str[i])
                        new_char = current + 1
                        original_str[i] = chr(new_char)
            elif i == (len(original_str) - 1): #if last letter
                if flow_copy[i] == 0: #if current letter in decrementing flow
                    #if letter prior is on MIN OR MAX AND flow has changed, then we move
                    if ((ord(original_str[(i-1)]) == 32) or (ord(original_str[(i-1)]) == 126)):
                        if ( (flow_self[(i-1)]) - (flow_copy[(i-1)]) ) != 0: 
                            if ord(original_str[i]) == 32: #if current letter is ASCII 32
                                new_char = chr(33) #incremented instead of decrementing 
                                original_str[i] = new_char #new char added to guess
                                flow_copy[i] = 1 #changed flow
                            else : #if current letter not MIN
                                current = ord(original_str[i])
                                new_char = current - 1
                                original_str[i] = chr(new_char)
                elif flow_copy[i] == 1: #if incrementing flow
                    #if letter prior is on MIN OR MAX AND flow has changed, then we move
                    if ((ord(original_str[(i-1)]) == 32) or (ord(original_str[(i-1)]) == 126)):
                        if ( (flow_self[(i-1)]) - (flow_copy[(i-1)]) ) != 0: 
                            if ord(original_str[i]) == 126: #if current letter ASCII 126
                                new_char = chr(126) #decremented 
                                original_str[i] = new_char
                                flow_copy[i] = 0 #changed flow
                                
                                original_str.append(" ") #increase string length. 
                                flow_copy.append(1) #added incrementing flow
                            else: #current letter is not MAX
                                current = ord(original_str[i])
                                new_char = current + 1
                                original_str[i] = chr(new_char)
            else : #other letters. depend on letter prior
                if flow_copy[i] == 0: #if current letter in decrementing flow
                    #if letter prior is on MIN OR MAX AND flow has changed, then we move
                    if ((ord(original_str[(i-1)]) == 32) or (ord(original_str[(i-1)]) == 126)) :
                        if ( (flow_self[(i-1)]) - (flow_copy[(i-1)]) ) != 0: 
                            if ord(original_str[i]) == 32: #if current letter is ASCII 32
                                #new_char = chr(33) #incremented instead of decrementing 
                                #g[i:(i+1)] = new_char
                                flow_copy[i] = 1 #changed flow
                            else : #if current letter not MIN
                                current = ord(original_str[i])
                                new_char = current - 1
                                original_str[i] = chr(new_char)
                elif flow_copy[i] == 1: #if incrementing flow
                    #if letter prior is on MIN OR MAX AND flow has changed, then we move
                    if ((ord(original_str[(i-1)]) == 32) or (ord(original_str[(i-1)]) == 126)) :
                        if ( (flow_self[(i-1)]) - (flow_copy[(i-1)]) ) != 0: 
                            if ord(original_str[i]) == 126: #if current letter ASCII 126
                            #new_char = chr(125) #decremented 
                            #g[i:(i+1)] = new_char
                                flow_copy[i] = 0 #changed flow
                            else: #current letter is not MAX
                                current = ord(original_str[i])
                                new_char = current + 1
                                original_str[i] = chr(new_char)
            
            i += 1 #increment index of guess string (g)
            self.flow_signs = flow_copy #adjust new flow (if any changes)   
            #end of while loop

        iterated_str = str(original_str)
        z = ""
        index = 0
        while index != len(original_str):
            z=z+original_str[index]
            index += 1

        print("After iteration:",end=" ")    
        print(z)
        print("length: ", end=" ")
        print(list(z))
        self.guess = z #change instance variable to the guess we just ticked to
        #done iterating through guess      
        return z



    def recalibrateFlowIndex(s) :
        i = 0
        while i != len(s):
            self.flow_signs[i] = 1
            i += 1
        #end of while
    
    def refillFlowIndex(self,s) :
        new_indices = []
        i = 0
        while i != s:
            new_indices.append(1)
            i += 1
        #end of while
        self.flow_signs = new_indices

    def getCores(self):
        p = len(sched_getaffinity(0))
        return p