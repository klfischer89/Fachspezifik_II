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
def aufgabe4():
    value = sum(range(1,1001))
    print(value)

# Aufgabe 5
import datetime

class CV():
    firstname = ""
    lastname = ""
    birthday = ""
    address = ""
    knowledge = ""

    def buildCV(self, cvData):
        self.firstname = cvData.get("firstname")
        self.lastname = cvData.get("lastname")
        self.birthday = cvData.get("birthday")
        self.address = cvData.get("address")
        self.knowledge = cvData.get("knowledge")

    def writeCV(self):
        cvString = (
            f"\033[32m"
            f"My CV:\n"
            f"Firstname: {self.firstname}\n"
            f"Lastname: {self.lastname}\n"
            f"Birthday: {self.birthday}\n"
            f"Address: {self.address}\n"
            f"Knowledge: {self.knowledge}"
            f"\033[0m"
        )
        return cvString
        
def inputCV():
    cvData = {}
    cvData["firstname"] = input("Firstname: ")
    cvData["lastname"] = input("Lastname: ")
    cvData["birthday"] = datetime.datetime.strptime(input("Date of birth (in form YYYY-MM-DD): "), "%Y-%m-%d").date()
    cvData["address"] = input("Address: ")
    cvData["knowledge"] = input("Knowledge: ")
    return cvData

cv = CV()
cv.buildCV(inputCV())
print(cv.writeCV())