# einzeiliger Kommentar
"""
mehrzeiliger Kommentar
"""
"""
#Variable
x=1
print(x)
x=3.14
print(x)
x = 5+3j        #komplexe Zahlen
print(x)
text = "Hallo"      #String
print(text)
status = True           #Boolean
print(status)

a = "Hallo"
b = a

a = 0b1010      #Binäre Zahlen
a = =xAFF       #Hexadezimale Zahlen
a = 0o10        #Oktalsystem
print(0b1101011+0xFB)   #Mischoperation mit Zahlensystemen





#Datentypen von der Art Listen, Sequenzen, Mengen


z = [1,2,3,4]           #List, Liste (mutable(änderbar), Sammlung von Objekten
print(z)
print(z[0])             #Zugriff auf einzelne Elemente einer Liste mit Index

y= (1,2,3,4)            #Tupel: unveränderliche (immutable) sammlung von Objekten, geordnet, Duplikate erlaubt
print(y)

daten = {1:"Meier", 2: "Schmidt"}           #Wertepaar, Dictionary, Dict
daten1 = {"Name":"Lisa","Alter": 25}
print(daten1)

"""
"""
Typ         geordnet            änderbar        Duplikate           Syntax
List        ja                  ja              ja                  []
Tuple       ja                  nein            ja                  ()
Set         nein                ja              nein                {}
Frozenset   nein                nein            nein                frozentset()
Dict        ja/nein             ja              schlüssel:nein      {key:value}

"""
"""
a = [1,2,3]
b = a
b.append(4)
print(a)

#Mutable udn immutable, Beispiel
a = [1,2,3]
b = a           #Das ist keine

#Bei immutable Objekten, sieht es zunächst genauseo aus
a = "Hallo"
b= a            #Auch ein referenz
a+= " Klaus"
print(a)
print(b)

#range
#(range(start, stop, step)
#on demand Zahlen, werden nicht gespeichert
for i in range(5):
    print(i)
for i in range (10,0,-2):
    print(i)

print(list(range(3,10,2)))      #Beispiel zur Speicherung von range-Ausgaben


#Verzweigung
x=1
if x== 1:
    print(x)
elif x== 2:
    print(2)
else: print(3)

#Schleifen
for i in range(5):                      #Zählergesteuerte Schleifen
        print("Durchlauf Nummer ", i)

obstkorb = ["Apfel","Mango","Banane"]
for obst in obstkorb:
    print(obst)


for buchstabe in "Python":
    print(buchstabe)

x= 1
while x<=3:
    print(x)                            #Kopfgesteuerte Schleife
    x=x+1

while True:                             #Fußgesteuerte Schleifen

    if x==3:
        break


x = input ("Name:   ")
print(x)
"""
Sprachen = ['Python','Java','C#']
print(Sprachen[0])
Sprachen.append('Modula2')          #Hinzufügen eines neuen Elements zu der Liste
print(Sprachen)
Sprachen[2] = 'Lisp'                #Ein Listenelement ersetzen
print(Sprachen)
Sprachen.remove("Python")           #Entfernen eines Eklementes aus der Liste
print(Sprachen)

Laender_Hauptstadt = {"Deutschland":"Berlin","Holland":"Amsterdam","Österreich":"Wien"}
print(Laender_Hauptstadt)
print(Laender_Hauptstadt["Deutschland"])
del (Laender_Hauptstadt["Deutschland"])
print(Laender_Hauptstadt)
Laender_Hauptstadt.clear()

meineset1 = {1, 'Hallo', 4, 5}
meineset2 = {1, 'Hallo',6,7}
"""meineset1.add(5)            #Hinzufügen eines Elements zu der Menge
print(meineset1)
meineset1.discard('Hallo')  #Element aus der Menge Löschen
print(meineset1)"""

meineset3 = meineset1 | meineset2       #Vereinigung von Mengen
print(meineset3)
print(meineset2-meineset1)              #Differenzmenge
print(meineset1-meineset2)
print(meineset2 & meineset1)            #gemeinsame Schnittmenge
print(meineset2 ^ meineset1)            #Symmetrische Differenzmenge


def ausgabe (name):
    print("Hallo ich bin eine Funktion"+name)
    meinstring = f"{name}, 'das ist mein Name ' "
    print(meinstring)
    #return                 Einen Wert zurückliefern



ausgabe("..schön")
print(int(-3.14))           #float umwandeln auf integer
print(float(3))             #integer umwandeln auf float


import random
print(random.randrange(10,20))


def future_function():
    pass



class Bike:
    name=""
    gear=0

class Auto:
    _name=""
    __gear=0

class Room:
    length = 0.0
    breadth = 0.0

    def calculate_area(self):
        print("Area of Room = ",self.length*self.breadth)


class Tier:
    name=""
    def essen(self):
        print("yam yam")

class Hund(Tier):
    def zeigemich(self):
        print("mein Name ist ", self.name)


if __name__ == "__main__":
    print("Test")
    vorname = "Eduardo"
    nachname ="Janin"
    alter=26
    print(f"ich heiße  {vorname}, : {nachname}, und ich bin {alter} Jahre alt.")
    meinfahrrad = Bike()
    meinfahrrad.name = "Mountain Bike"
    meinfahrrad.gear = 21
    print(f"Name : {meinfahrrad.name}, und hat {meinfahrrad.gear}  Gänge")

    study_room = Room()         #Objekt instanzieren
    study_room.length = 7.3
    study_room.breadth = 5.0
    study_room.calculate_area()

    retriever = Hund()
    retriever.name = "Fluffy"
    retriever.essen()
    retriever.zeigemich()

    meineliste = ["Programmieren ", "Lesen ", "Party machen "]
    f = open('test.txt','w+')
    for meintxt in meineliste:
        f.write(f' {meintxt}')
        f.write('%s\n'%meintxt)
    #f.close()

    f.seek(0)
    print(f.read())

    f.close()

    with open("test.txt", "r") as f:
        print(f.read())
        for x in f.readlines():
            print(x, end='')


import requests

url = "https://httpbin.org/image/png"
response = requests.get(url)            #Objekt response beinhaltet Daten und Metadaten
if response.status_code == 200:         #Return code 200; No Error
    with open ('download.png', 'wb') as f:
        f.write(response.content)
        print("erfolgreich gespeichert")

else: print("Fehler  ", response.status_code)       #Error Code überprüfen


import json
import xml.etree.ElementTree as ET
root = ET.getroot()

payload = {'username': 'Daniel', 'password':'1234'}
url = "https://httpbin.org/post"
response = requests.get(url, params=payload)            #Befehl GET mit parameterübergabe
r = requests.post (url, payload)                #Befehl POST
print(r.json())










