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

# Aufgabe 2
def aufgabe2():
    testListe = ["Eindeutig","Eindeutig","Eindeutig"]
    print(testListe)
    testSet = set(testListe)
    print(testSet)

# Aufgabe 3
def aufgabe3():
    testListe = [99, 53, 42, 1, 5, 16, 27]
    testListe.sort()
    print(testListe[-3])

# Aufgabe 4

