import hashlib
from functools import reduce

# One-way permutation function using SHA256
# Already Implemented.
def OWP(x):
    h = hashlib.sha256()
    h.update(x)
    return h.digest()


# A PRG construction that generates one random bit at a time
# Using the Goldreich-Levin hardcore bit construction that we studied in the class
class PRG:

    def __init__(self, seed):
        self.r = seed[32:]

        self.x = seed[:32]

        self.f = OWP

    # TODO: Return the inner product between self.r and self.x, and update self.x using self.f
    # HINT: Convert the byte strings to int objects and then use Python's math operators.
    def getbit(self ):

        int_r=int.from_bytes(self.r,"little")
        int_x = int.from_bytes(self.x, "little")

        multiply = int_r & int_x

        count = 0
        while multiply:
            multiply &= (multiply - 1)
            count += 1

        self.x=self.f(self.x)

        return (count % 2)

    def confirm(self):

        r= int.from_bytes(self.r, "little")
        x = int.from_bytes(self.x, "little")

        x=bin(x)[2:]
        r=bin(r)[2:]

        diff= abs(len(x)-len(r))
        begin=""
        if(len(x)>len(r)):
            for a in range(0, diff):
                begin=begin+"0"
            r=begin+r

        elif (len(x)<len(r)) :
            for a in range(0, diff):
                begin=begin+"0"
            x = begin + x

        list=[]

        for i in range(0,len(x)):
            #print(i)
            val=(int(x[i])*int(r[i]))
            list.append(val)

        dummy=list[0]^list[1]

        for i in range(2, len(list)):
            dummy=(dummy ^ list[i])

        self.x=self.f(self.x)
        return dummy

    def alternate(self):

        r = int.from_bytes(self.r, "little")
        x = int.from_bytes(self.x, "little")


        multiply = r & x

        s=bin(multiply)[2:]
        list=[]
        for i in range(0, len(s)):
            list.append(int(s[i]))
        dummy=sum(list) % 2
        self.x = self.f(self.x)
        return dummy


# A Length-doubling PRG construction that extends 512-bit seed to 1024-bit output
# TODO: Using the PRG class, generate 128 bytes from a 64 bytes seed
def double_length(seed):
    flag = 0
    PRG_obj = PRG(seed)
    #int_r = int.from_bytes(PRG_obj.r, "little")

    list = []
    while (flag != 1024):

        computedbit = PRG_obj.getbit()
        list.append(str(computedbit))
        flag = flag + 1

    finallist = ''.join([(elem) for elem in list])
    result = int(finallist, 2)

    finallyans = result.to_bytes(128, byteorder='little')

    return finallyans


if __name__ == '__main__':
    with open("64bytes", "rb") as fp:

    with open("128bytes", "rb") as fp:
        result = fp.read()

    assert double_length(seed) == result
