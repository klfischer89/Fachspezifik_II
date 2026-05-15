# Aufgabe 1: check for a value in a set
def aufgabe1():
    # provide String fot the result
    restultString = ""
    # proide a test set and get user input (number)
    testSet = {1,2,3,4,5}
    value = int(input("Type a Number to check if it is part oft the set: "))

    # check if the input ist part of the set
    if value in testSet:
        restultString = f"{value} is part of the set!"
    else:
        restultString = f"{value} is NOT part of the set!"

    print(restultString)

# Aufgabe 2: remove duplicates
def aufgabe2():
    # provide a list with duplicates
    testListe = ["Eindeutig","Eindeutig","Eindeutig"]
    print(testListe)
    # convert the list to a set, to eliminate dublicates
    testSet = set(testListe)
    print(testSet)

# Aufgabe 3: output third highest number in a list
def aufgabe3():
    # sort a list with numbers and print the third highest entry
    testListe = [99, 53, 42, 1, 5, 16, 27]
    testListe.sort()
    print(testListe[-3])

# Aufgabe 4: sum all numbers from 1 to 1000
def aufgabe4():
    # sum numbers from 1 to 1000 and print it
    value = sum(range(1,1001))
    print(value)

# Aufgabe 5: create a CV
import datetime
def aufgabe5():
    #define a class CV with the needed attributes
    class CV():
        firstname = ""
        lastname = ""
        birthday = ""
        address = ""
        knowledge = ""

        # set the attributes of an instance of the class CV using a dictionary
        def buildCV(self, cvData):
            self.firstname = cvData.get("firstname")
            self.lastname = cvData.get("lastname")
            self.birthday = cvData.get("birthday")
            self.address = cvData.get("address")
            self.knowledge = cvData.get("knowledge")

        # write the CV in a file using a formated string based on the instances attributes
        def writeCV(self):
            # build the string using the CVs attributes
            cvString = (
                f"My CV:\n"
                f"Firstname: {self.firstname}\n"
                f"Lastname: {self.lastname}\n"
                f"Birthday: {self.birthday}\n"
                f"Address: {self.address}\n"
                f"Knowledge: {self.knowledge}"
            )
            # write the String an a file cv.txt
            with open("cv.txt", "w", encoding="utf-8") as f:
                f.write(cvString)
            print("\033[32mCV created!\033[0m")

    # get user input for the attributes of the CV        
    def inputCV():
        cvData = {}
        cvData["firstname"] = input("Firstname: ")
        cvData["lastname"] = input("Lastname: ")
        # convert the user input for birthday in a date format, only containing year, month and day
        cvData["birthday"] = datetime.datetime.strptime(input("Date of birth (in form YYYY-MM-DD): "), "%Y-%m-%d").date()
        cvData["address"] = input("Address: ")
        cvData["knowledge"] = input("Knowledge: ")
        return cvData
    
    # create an instance of a CV and call the functions to build and write a CV
    cv = CV()
    cv.buildCV(inputCV())
    cv.writeCV()

# main line
if __name__ == "__main__":
    # aufgabe1()
    # aufgabe2()
    # aufgabe3()
    # aufgabe4()
    # aufgabe5()
    pass