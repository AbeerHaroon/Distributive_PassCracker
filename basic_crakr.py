#! /usr/bin/python3.10

import crypt
import GuessGen

p = b'checkThisPass123'
s = b'12893'

#print(xs.decode("utf-16"))

actual = "$y$j9T$dunb35YUgYH54yaI9qCRk/$UouOdfBIbg2POJqh1zwZyJvg563o.1MWvO5RkV3Ljb/"

t1 = "guess1"
t1_b = "gues222"
t1_c = "gue1251"
actual_pw = "djfido"

t2 = "$y$j9T$obLg9uEA6.f1CUcBkAKvt0$YpePzCYaxtYovGfPkXXJK5addsPPDF66ceQbxjFg/25"
another = crypt.crypt(word=t1,salt=actual)
print(another)
if(another == actual) :
    print("pass match")
else :
    print("no")

another = crypt.crypt(word=t1_b,salt=actual)
if(another == actual) :
    print("pass match")
else :
    print("no")
another = crypt.crypt(word=t1_c,salt=actual)
if(another == actual) :
    print("pass match")
else :
    print("no")
another = crypt.crypt(word=actual_pw,salt=actual)
if(another == actual) :
    print("pass match")
else :
    print("no")

print("crypt: ",end="")
print(another)


h = hashlib.new("sha256")
h.update(b"Check This hash")
print(h.hexdigest())
print(hashlib.algorithms_available)

i = 0b1001
x = bin(i)
print("printing variable i:",end=" ")
print(bin(i)[2:3])

string_test = "hello"
print(string_test[0:2])

g = GuessGen.GuessGen()
