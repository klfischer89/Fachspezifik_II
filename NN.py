class Neuron:
    #x= Eingabneuron
    #y= Ausgabeneuron
    #Sensor liefert einen Wert zw. 0 und 100
    #Kritischer Wert ab 85
    #Das Netz soll entscheiden:  0=nicht kritisch,  oder 1=kritisch

    #Konstruktor
    def __init__(self,schwelle=None, eingaenge=[]):
        self.wert=None              #Wert des Neurons, Standard = None für Eingangsneuronen
        self.schwelle= schwelle     #Schwelle des Neurons, Standard = None für Eingangsneuronen
        self.eingaenge = eingaenge  #Eingaenge des Neurons (Enthält Tupel von Werten: Vorgänger Neuron und Gewicht)

    # wert normalisieren, liefert Werte zwischen 0 und 1
    def setWert(self,wert):
        self.wert= wert/100

    def denke(self):
        #gewichtete Summe bilden
        gsum = 0

        for ni, wi in self.eingaenge:   #ni Eingangsneuron, wi Gewicht
            gsum += wi * ni.wert        #Summe = Gewichti * Wert des Neuronsi

        # wenn Summe >= Schwelle -> kritisch = 1, ansonsten nicht kritisch = 0
        if gsum>= self.schwelle:
            return 1
        else:
            return 0

    def lerne(self, fehler, lernrate):
        #Alle Gewichte anpassen
        for i in range (len(self.eingaenge)):
            #Aktuelle werte holen
            ni, wi = self.eingaenge[i]

            #Neue Gewichtung berechnen
            #neues Gewicht = altes Gewicht+lernrate*fehler*eingaenge
            neues_gewicht = wi + lernrate *fehler * ni.wert

            self.eingaenge[i] = (ni, neues_gewicht) # Eingangsneuron bleibt gleich, Gewicht wird angepasst

        self.schwelle -= lernrate * fehler #Anpassung der Schwelle an lernrate und fehler


#Ohne Lernen
x = Neuron()
x.setWert(90)
y = Neuron( 0.85, [(x,1)])            #Schwelle = 0.85, Eingang kommt von Neuron x, Gewicht = 1

#Ausgabe ob kritisch oder nicht
print("Ausgabe: ", y.denke())
#Ausgabe des Gewichts, kommend vom Vorgängerneuron
print("Gewicht: ", y.eingaenge[0][1])
#Ausgabe der Schwelle, Initial 0.85
print("Schwelle: ", y.schwelle)

#Mit Lernen, Einfluss auf das Modell hat die Berechnung der Fehler (Gradienten), Gewichte und Schwelle (Übergangs- und Aktivierungsfunktion)
#Wenn fehler = 0 alles Korrekt, wenn fehler = 1 dann fehlerhaft
#fehler = 0-y.denke() #Ändert die Schwelle, in diesem Fall nicht sinnvoll, da Modell bereits richtig arbeitet
#angepasste Fehlerfunktion
fehler = 1-y.denke()        #Fehler = Soll(selbst festgelegt) - Ist (liefert das Modell)

#Lernrate festlegen (stärke der Anpassung), fixer Wert, sollte niedrig gewählt werden (langsames lernen), bei großen Werten -> schnelles lernen aber instabil
lernrate = 0.1
#Anpassung der Übergangs- und Aktivierungsfunktion
y.lerne(fehler, lernrate)

#Ausgabe nach dem lernen
print("Ausgabe nach dem Lernen", y.denke())
print("Neues Gewicht:", y.eingaenge[0][1])
print("Neue Schwelle: ", y.schwelle)

#Aktivierungsfunktionen und Backpropagtion

#Relu
def relu(x):
    return max(0, x)

def relu_ableitung(x):
    return 1 if x > 0 else 0

#sigmoid
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_ableitung(output):
    # 'output' ist das bereits berechnete Ergebnis von sigmoid(x)
    return output * (1 - output)

#def backpropagation():
    # 1. FORWARD PASS (Dein Code erweitert)
    gsum = 0
    for ni, wi in self.eingaenge:
        gsum += wi * ni.wert

    # Aktivierung berechnen und im Neuron speichern
    self.wert = sigmoid(gsum)

    # 2. BACKPROPAGATION (Fehlerkorrektur für dieses Neuron)
    # Angenommen, 'ziel_wert' ist das gewünschte Ergebnis (nur am Ausgangsneuron)
    # Oder 'fehler_von_vorne' kommt von den nachfolgenden Schichten
    fehler = ziel_wert - self.wert 

    # Delta (Fehlersignal) berechnen: Fehler * Steigung der Aktivierungsfunktion
    delta = fehler * sigmoid_ableitung(self.wert)

    # 3. GEWICHTE ANPASSEN (Lernschritt)
    lernrate = 0.1

    for i, (ni, wi) in enumerate(self.eingaenge):
        # Neues Gewicht = Altes Gewicht + Lernrate * Fehlersignal * Eingangswert
        neues_gewicht = wi + lernrate * delta * ni.wert
        
        # Aktualisiere das Gewicht in deiner Liste
        self.eingaenge[i] = (ni, neues_gewicht)
