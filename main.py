# Aufgabe 1
def aufgabe1():
    restultString = ""

    testSet = {1,2,3,4,5}
    value = int(input("Type a Number to check if it is part oft the set: "))

    if value in testSet:
        restultString = f"{value} is part of the set!"
    else:
        restultString = f"{value} is NOT part of the set!"

    return restultString

#Aufgabe 2


