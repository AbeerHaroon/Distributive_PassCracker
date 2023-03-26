import string

import GuessGen
import crypt
from sepehr_cracker import Cracker

# SEPEHR Cracker test


# TODO: Insert full hashed shadow line  here
hashed_password = 'sepehrman:$y$j9T$.Ciip2iHePTF7RvA1q3rX0$OeW1icDofEhPQhV4jPStlhsxPOmqmNcZlgaEfaXezE0:19381:0:99999:7:::'
cracker = Cracker(hashed_password)

all_letters = string.ascii_letters

letters_length = 1
while cracker.cracked_password is None:
    cracker.crack_hash(list(string.ascii_letters), letters_length)
    letters_length += 1

print(cracker)

# g = GuessGen.GuessGen()
#
# try_this = "!       "
# try_this_en = "$y$j9T$NDOCNWBa5FhkwCNbkIvZi0$b8ZXvQ5DWEyI.QDMTOxFXI3Q.wWnJmJyonUYPdxlBG3" #hash of pass: "~!      "
#
# try_en = crypt.crypt(word=try_this,salt="$y$j9T$odFxZKQR3fIkMpvojHI9n0$TDIoYgYI5y4iPf.V.yfnMi3JIjKM4wi42.imXzGxkkC")
#
# h = "$y$j9T$dunb35YUgYH54yaI9qCRk/$UouOdfBIbg2POJqh1zwZyJvg563o.1MWvO5RkV3Ljb/"
# x = "$y$j9T$BVkCZB63mOffrdHGUb3Kn0$eo.YQx2MUW1M8Nrn4wsteELcN.IgMsN58LO8.XdIa92"
# x1="$y$j9T$fJ7MENHcxNjWS.2gfA72f0$vMKKTSvHh/JfoKjdjfQaUikc3bDjSpHFZ7KZZJHpT35"
# nnn = "$y$j9T$Fsafila8HwR3oQZV4Siuu/$FIfdg5jBjjHzp37n2Uylrm2FXCRaaESLrcWoLdqIfN3" #hash for "dog     "
#
# o = g.crackCycle(nnn)
#
# print("password is: ")
# print(o)

# g.tick("~ dddd")
