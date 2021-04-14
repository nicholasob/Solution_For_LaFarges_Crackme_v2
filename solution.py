# Nicholas Sjöqvist Obucina

# Max length of the serial key is 25 characters

# 89h ; ‰
# 0C4h ; Ä
# 0FEh ; þ

firstEncryptionArray = [int(x, 16) for x in ["AA", "89", "0C4", "0FE", "46"]]
secondEncryptionArray = [int(x, 16) for x in ["78", "0F0", "0D0", "3", "0E7"]]

thirdEncryptionArray = [int(x, 16) for x in ["0F7", "FD", "F4", "E7", "0B9"]]
fourthEncryptionArray = [int(x, 16) for x in ["0B5", "1B", "C9", "50", "73"]]


def firstencryptThisArray(nameToArray=[], encryptArray=[]):
    returnArray = [nameToArray[0]]
    nameToArray.append(0)
    countVariable = 0
    for x in range(1, len(nameToArray)):
        val = (nameToArray[x] ^ encryptArray[countVariable])
        returnArray.append(val)
        encryptArray[countVariable] = nameToArray[x]

        if(countVariable == 4):
            countVariable = 0
        else:
            countVariable = countVariable + 1

    return returnArray


def secondencryptThisArray(nameToArray=[], encryptArray=[]):
    returnArray = []
    countVariable = 0
    for x in range(len(nameToArray) - 1, 0, -1):
        val = (encryptArray[countVariable] ^ nameToArray[x])
        returnArray.insert(0, val)
        encryptArray[countVariable] = nameToArray[x]

        if(countVariable == 4):
            countVariable = 0
        else:
            countVariable = countVariable + 1

    returnArray.insert(0, nameToArray[0])
    return returnArray


def createIntRepresentationOfStringFromDecimalValues(array=[]):
    #    EAX = int(("".join([hex(x).lstrip("0x") for x in arrayToReturn])), 16)
    temporaryReturnArray = []
    for eachElement in array:
        returnValue = hex(eachElement).lstrip("0x")
        if(len(returnValue) < 2):
            returnValue = "0" + returnValue
        temporaryReturnArray.append(returnValue)
    return int(("".join(temporaryReturnArray)), 16)


Username = input("Type your username: ")

if(len(Username) < 4):
    print("Your username is to short")
else:
    ArrayOfName = []
    for x in Username:
        ArrayOfName.append(ord(x))

    firstEcryptionOfUserName = firstencryptThisArray(
        ArrayOfName, firstEncryptionArray)

    secondEncryptionOfUserName = secondencryptThisArray(
        firstEcryptionOfUserName, secondEncryptionArray)

    thirdEncryptionOfUserName = firstencryptThisArray(
        secondEncryptionOfUserName, thirdEncryptionArray)[:-1]

    finalEncryptionOfUserName = secondencryptThisArray(
        thirdEncryptionOfUserName, fourthEncryptionArray)

    arrayToReturn = [0, 0, 0, 0]
    for eachIteration in range(0, len(finalEncryptionOfUserName) - 1):
        firstArray = finalEncryptionOfUserName.copy()
        firstArray.insert(0, 0)

        ECX = bin(eachIteration & 3)

        bl = arrayToReturn[3 - (eachIteration - (int(eachIteration / 4) * 4))]
        cl = finalEncryptionOfUserName[eachIteration + 1]

        bl = bl + cl

        if(bl > 256):
            bl = bl - (int(bl/256) * 256)

        arrayToReturn[3 - (eachIteration - (int(eachIteration / 4) * 4))] = bl

    userNameStringRepresentation = []
    EAX = createIntRepresentationOfStringFromDecimalValues(arrayToReturn)
    i = 0
    while(EAX != 0):
        EDX = EAX % int("0xA", 16)
        EAX = int(EAX / int("0xA", 16))
        userNameStringRepresentation.append(EDX + 30)
        i = i + 1

    # The serial key is the username's representation but in reverse.
    serialKeyStringRepresentation = userNameStringRepresentation.copy()[::-1]

    #####################
    # Final REVERSING STEPS
    #####################
    stringArray = "".join([str(thefinals - 30)
                           for thefinals in serialKeyStringRepresentation])
    print("Your reg.code: " + stringArray)
    input("Press any key to exit")
