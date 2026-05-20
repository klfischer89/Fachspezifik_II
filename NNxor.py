import math
import random

# --- AKTIVIERUNGSFUNKTIONEN ---
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_ableitung(output):
    return output * (1 - output)


# --- NEURON KLASSE ---
class Neuron:
    def __init__(self):
        self.wert = 0.0       
        self.delta = 0.0      
        self.eingaenge = []   

    def verbinde_mit(self, vorheriges_neuron):
        # Zufälliges Startgewicht zwischen -1.0 und 1.0
        zufalls_gewicht = random.uniform(-1.0, 1.0)
        self.eingaenge.append((vorheriges_neuron, zufalls_gewicht))

    def forward(self):
        gsum = 0.0
        for ni, wi in self.eingaenge:
            gsum += wi * ni.wert
        self.wert = sigmoid(gsum)

    def aktualisiere_gewichte(self, lernrate):
        for i, (ni, wi) in enumerate(self.eingaenge):
            neues_gewicht = wi + (lernrate * self.delta * ni.wert)
            self.eingaenge[i] = (ni, neues_gewicht)


# --- NETZWERK MANAGER KLASSE ---
class NeuronalesNetzwerk:
    def __init__(self, anzahl_input, anzahl_hidden, anzahl_output):
        # Schichten erstellen
        self.input_layer = [Neuron() for _ in range(anzahl_input)]
        self.hidden_layer = [Neuron() for _ in range(anzahl_hidden)]
        self.output_layer = [Neuron() for _ in range(anzahl_output)]

        # Schichten vollvermaschen
        for hn in self.hidden_layer:
            for in_n in self.input_layer:
                hn.verbinde_mit(in_n)

        for on in self.output_layer:
            for hn in self.hidden_layer:
                on.verbinde_mit(hn)

    def trainiere(self, x_daten, y_daten, epochen, lernrate):
        print(f"Starte Training für {epochen} Epochen...\n")
        
        for epoche in range(1, epochen + 1):
            gesamt_fehler = 0.0
            
            # Gehe durch jeden einzelnen Trainingsdatensatz (Muster)
            for x, y_ziel in zip(x_daten, y_daten):
                
                # 1. FORWARD PASS
                # Inputs setzen
                for i, input_wert in enumerate(x):
                    self.input_layer[i].wert = input_wert
                
                # Hidden Layer berechnen
                for hn in self.hidden_layer:
                    hn.forward()
                # Output Layer berechnen
                for on in self.output_layer:
                    on.forward()

                # Fehler für die Epochen-Statistik aufaddieren (Quadratischer Fehler)
                for i, on in enumerate(self.output_layer):
                    gesamt_fehler += 0.5 * (y_ziel[i] - on.wert) ** 2

                # 2. BACKPROPAGATION
                # Schritt A: Delta für Output-Schicht
                for i, on in enumerate(self.output_layer):
                    fehler_output = y_ziel[i] - on.wert
                    on.delta = fehler_output * sigmoid_ableitung(on.wert)

                # Schritt B: Delta für Hidden-Schicht
                for hn in self.hidden_layer:
                    fehler_hidden = 0.0
                    for on in self.output_layer:
                        for ni, wi in on.eingaenge:
                            if ni == hn:
                                fehler_hidden += wi * on.delta
                    hn.delta = fehler_hidden * sigmoid_ableitung(hn.wert)

                # 3. GEWICHTE ANPASSEN
                for on in self.output_layer:
                    on.aktualisiere_gewichte(lernrate)
                for hn in self.hidden_layer:
                    hn.aktualisiere_gewichte(lernrate)

            # Alle 2000 Epochen den aktuellen Fehler ausgeben
            if epoche % 2000 == 0 | epoche == 1:
                print(f"Epoche {epoche:5d} | Netzwerk-Fehler (Loss): {gesamt_fehler:.6f}")

    def vorhersage(self, x):
        # Hilfsfunktion, um das Netz nach dem Training abzufragen
        for i, input_wert in enumerate(x):
            self.input_layer[i].wert = input_wert
        for hn in self.hidden_layer:
            hn.forward()
        for on in self.output_layer:
            on.forward()
        return [on.wert for on in self.output_layer]


# --- TRAININGSDATEN (XOR-Logik) ---
# Inputs: zwei Bits | Outputs: Das exklusive Oder (nur 1 wenn ungleich)
XOR_INPUTS = [
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0]
]

XOR_ZIALE = [
    [0.0],
    [1.0],
    [1.0],
    [0.0]
]

# --- PROGRAMM STARTEN ---

# Wir erstellen ein Netz: 2 Eingänge, 3 Hidden-Neuronen, 1 Ausgang
netz = NeuronalesNetzwerk(anzahl_input=2, anzahl_hidden=3, anzahl_output=1)

# Netz trainieren (10000 Wiederholungen aller Daten, Lernrate 0.2)
netz.trainiere(XOR_INPUTS, XOR_ZIALE, epochen=10000, lernrate=0.2)

print("\n--- ERGEBNISSE NACH DEM TRAINING ---")
for x in XOR_INPUTS:
    ergebnis = netz.vorhersage(x)
    print(f"Input: {x} -> Vorhersage: {ergebnis[0]:.4f} (Soll: {1.0 if x[0]!=x[1] else 0.0})")
