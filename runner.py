import GuessGen
import crypt

g = GuessGen.GuessGen()

try_this = "!       "
try_this_en = "$y$j9T$NDOCNWBa5FhkwCNbkIvZi0$b8ZXvQ5DWEyI.QDMTOxFXI3Q.wWnJmJyonUYPdxlBG3" #hash of pass: "~!      "
try_en = crypt.crypt(word=try_this,salt="$y$j9T$odFxZKQR3fIkMpvojHI9n0$TDIoYgYI5y4iPf.V.yfnMi3JIjKM4wi42.imXzGxkkC")

h = "$y$j9T$dunb35YUgYH54yaI9qCRk/$UouOdfBIbg2POJqh1zwZyJvg563o.1MWvO5RkV3Ljb/"
x = "$y$j9T$BVkCZB63mOffrdHGUb3Kn0$eo.YQx2MUW1M8Nrn4wsteELcN.IgMsN58LO8.XdIa92"
x1="$y$j9T$fJ7MENHcxNjWS.2gfA72f0$vMKKTSvHh/JfoKjdjfQaUikc3bDjSpHFZ7KZZJHpT35"
o = g.crackCycle(try_this_en)

print("password is: ")
print(o)

#g.tick("~ dddd")
