

def transferLegalStates():

    oldCode = open("TTT.py","r").read()
    newCode = open("TTT2.py","w")

    newCode.write(oldCode)
    newCode.write("\n")

    for i in range(0,9):
        distTxt = open("Distance"+str(i),"r")
        newCode.write("Distance"+str(i)+" = [[")
        giantString = distTxt.read().strip().replace("\n","],[")
        newCode.write(giantString + "]]\n")
    
    newCode.write("Distance9 = []")


if __name__ == '__main__':

    transferLegalStates()
