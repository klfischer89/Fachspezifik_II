import math
import random
import matplotlib.pyplot as plt
import networkx as nx

# Import für die mathematische Validierung (Gegenüberstellung von Soll- und Ist-Werten)
from sklearn.metrics import confusion_matrix, classification_report


# --- AKTIVIERUNGSFUNKTIONEN ---

def sigmoid(x):
    """
    Die logistische Sigmoid-Funktion skaliert beliebige reelle Zahlen 
    nicht-linear in ein exaktes Intervall zwischen 0 und 1.
    Das ist ideal, um Wahrscheinlichkeiten oder Scores darzustellen.
    """
    return 1 / (1 + math.exp(-x))


def sigmoid_ableitung(output):
    """
    Die erste Ableitung der Sigmoid-Funktion bestimmt die Steigung der Kurve.
    Mathematischer Shortcut: Da 'output' bereits das Ergebnis von sigmoid(x) ist,
    berechnet sich die Ableitung extrem effizient über f(x) * (1 - f(x)).
    Wichtig für die Bestimmung des Gradienten bei der Backpropagation.
    """
    return output * (1 - output)


# --- NEURON KLASSE ---

class Neuron:
    def __init__(self, name=""):
        self.wert = 0.0        # Speichert die aktuelle Aktivierung (Ausgangssignal) des Neurons
        self.delta = 0.0       # Speichert das Fehlersignal (Delta) für den Backpropagation-Schritt
        self.eingaenge = []    # Liste aus Tupeln: [(vorheriges_neuron_objekt, gewicht_der_verbindung), ...]
        self.name = name       # Optionaler Identifikationsname für die spätere Visualisierung

    def verbinde_mit(self, vorheriges_neuron):
        """
        Erstellt eine synaptische Verbindung zu einem Neuron der vorherigen Schicht.
        Das Gewicht wird zufällig zwischen -1.0 und 1.0 initialisiert (Symmetriebrechung).
        """
        zufalls_gewicht = random.uniform(-1.0, 1.0)
        self.eingaenge.append((vorheriges_neuron, zufalls_gewicht))

    def forward(self):
        """
        Der Forward Pass (Vorwärtsschub): Berechnet die gewichtete Summe (gsum) 
        aller eingehenden Signale und jagt das Ergebnis durch die Sigmoid-Aktivierungsfunktion.
        """
        gsum = 0.0
        for ni, wi in self.eingaenge:
            gsum += wi * ni.wert  # Gewicht mal Aktivierung des vorherigen Neurons aufsummieren
        self.wert = sigmoid(gsum)  # Ergebnis aktivieren und im Neuron für die nächste Schicht speichern

    def aktualisiere_gewichte(self, lernrate):
        """
        Der Optimierungsschritt mittels Gradientenabstieg (Delta-Regel).
        Passt jedes eingehende Gewicht basierend auf dem berechneten Fehlersignal an.
        """
        for i, (ni, wi) in enumerate(self.eingaenge):
            # Formel: Neues_Gewicht = Altes_Gewicht + Lernrate * Delta * Eingangssignal
            neues_gewicht = wi + (lernrate * self.delta * ni.wert)
            # Listen Index überschreiben
            self.eingaenge[i] = (ni, neues_gewicht)


# --- NETZWERK MANAGER KLASSE ---

class KreditNetzwerk:
    def __init__(self):
        # 1. Instanziierung der einzelnen Schichten (Eingänge, 3 Versteckte Schichten, 1 Ausgang)
        self.input_layer = [Neuron(f"In_{i}") for i in ["Einkommen", "Schufa", "Schulden"]]
        self.hidden_layer1 = [Neuron(f"H1_{i}") for i in range(4)]
        self.hidden_layer2 = [Neuron(f"H2_{i}") for i in range(4)]
        self.hidden_layer3 = [Neuron(f"H3_{i}") for i in range(4)]
        self.output_layer = [Neuron("Output")]

        # Kontrollliste, um das gesamte Netzwerk sequentiell von vorne nach hinten zu steuern
        self.alle_schichten = [
            self.input_layer, 
            self.hidden_layer1, 
            self.hidden_layer2, 
            self.hidden_layer3, 
            self.output_layer
        ]

        # 2. Vollvermaschung (Fully Connected): Jedes Neuron einer Schicht mit jedem der nächsten Schicht verbinden
        for i in range(len(self.alle_schichten) - 1):
            aktuelle_schicht = self.alle_schichten[i]
            naechste_schicht = self.alle_schichten[i+1]
            for n_naechste in naechste_schicht:
                for n_aktuell in aktuelle_schicht:
                    n_naechste.verbinde_mit(n_aktuell)

    def trainiere(self, x_daten, y_daten, epochen, lernrate):
        print(f"Starte Bank-Modell Training für {epochen} Epochen...\n")
        
        for epoche in range(1, epochen + 1):
            gesamt_fehler = 0.0  # quadratischern Fehler (Loss) in dieser Epoche
            
            # Iteration durch alle bereitgestellten Trainingsbeispiele
            for x, y_ziel in zip(x_daten, y_daten):
                
                # --- STEP 1: INPUTS SETZEN & NORMALISIEREN ---
                # Teilen durch 100 verschiebt Rohwerte (0-100) in das mathematisch stabile Intervall (0-1)
                for i, input_wert in enumerate(x):
                    self.input_layer[i].wert = input_wert / 100.0
                
                # --- STEP 2: FORWARD PASS ---
                # Signale schichtweise von vorne nach hinten durchrechnen (Input-Layer wird übersprungen)
                for schicht in self.alle_schichten[1:]:  
                    for neuron in schicht:
                        neuron.forward()

                # Quadratischen Fehler für die Epochen-Statistik aufaddieren: Loss = 0.5 * (Soll - Ist)^2
                gesamt_fehler += 0.5 * (y_ziel[0] - self.output_layer[0].wert) ** 2

                # --- STEP 3: BACKPROPAGATION (FEHLER-RÜCKFÜHRUNG) ---
                # Delta für das Ausgangsneuron berechnen
                on = self.output_layer[0]
                fehler_output = y_ziel[0] - on.wert  # Differenz: Soll-Wert minus Ist-Wert
                # Delta = Fehler * Steigung der Aktivierungsfunktion am aktuellen Punkt
                on.delta = fehler_output * sigmoid_ableitung(on.wert)

                # Deltas für die Hidden Schichten berechnen (Kettenregel rückwärts angewendet)
                # s_idx läuft rückwärts: Schicht 3 (Index 3) -> Schicht 2 (Index 2) -> Schicht 1 (Index 1)
                for s_idx in range(len(self.alle_schichten) - 2, 0, -1):
                    aktuelle_schicht = self.alle_schichten[s_idx]
                    naechste_schicht = self.alle_schichten[s_idx + 1]
                    
                    for hn in aktuelle_schicht:
                        fehler_hidden = 0.0
                        # Der Fehler eines Hidden Neurons ist die Summe der Fehler (Deltas) der Folge-Neuronen,
                        # gewichtet mit der jeweiligen Verbindungsstärke.
                        for vorwaerts_n in naechste_schicht:
                            for ni, wi in vorwaerts_n.eingaenge:
                                if ni == hn:  # Überprüfung, ob die Verbindung von diesem Hidden-Neuron stammt
                                    fehler_hidden += wi * vorwaerts_n.delta
                        # Berechnetes Hidden-Delta im Neuron hinterlegen
                        hn.delta = fehler_hidden * sigmoid_ableitung(hn.wert)

                # --- STEP 4: GEWICHTS-UPDATE ---
                # Nachdem alle Deltas feststehen, passen alle Schichten (außer Input) ihre Gewichte an
                for schicht in self.alle_schichten[1:]:
                    for neuron in schicht:
                        neuron.aktualisiere_gewichte(lernrate)

            # Zwischenbericht alle 500 Epochen ausgeben, um den Lernfortschritt (Loss-Abfall) zu tracken
            if epoche % 500 == 0 or epoche == 1:
                print(f"Epoche {epoche:5d} | Quadratischer Fehler (Loss): {gesamt_fehler:.6f}")

    def vorhersage(self, x):
        """
        Nimmt Daten eines neuen Kunden, normalisiert sie und führt einen reinen 
        Forward Pass aus, um den prognostizierten Kredit-Score zurückzugeben.
        """
        for i, input_wert in enumerate(x):
            self.input_layer[i].wert = input_wert / 100.0
        for schicht in self.alle_schichten[1:]:
            for neuron in schicht:
                neuron.forward()
        return self.output_layer[0].wert

    def visualisiere_netzwerk(self):
        """
        Transformiert die Neuronenobjekte in einen mathematischen Graphen.
        Stellt Gewichtsachsen farblich und in ihrer Dicke proportional zur Stärke dar.
        """
        G = nx.DiGraph()  # Instanziiert einen gerichteten Graphen (Directed Graph)
        pos = {}          # Dictionary für die 2D-Koordinaten der Neuronen auf der Zeichenfläche
        node_colors = []  # Farbliste für die optische Trennung der Schichten
        
        # Neuronen-Knoten positionieren und einfärben
        for s_idx, schicht in enumerate(self.alle_schichten):
            for n_idx, neuron in enumerate(schicht):
                G.add_node(neuron)
                # x-Koordinate = Schicht-Index, y-Koordinate = Zentrierung um die Null-Linie
                pos[neuron] = (s_idx, n_idx - (len(schicht) - 1) / 2.0)
                
                # Farbschema festlegen
                if s_idx == 0: node_colors.append('#3498db')       # Blau für Eingänge
                elif s_idx == 4: node_colors.append('#e74c3c')     # Rot für den Ausgang
                else: node_colors.append('#2ecc71')                # Grün für alle Hidden-Layer

        # Synaptische Kanten (Verbindungen) samt gelernten Gewichten in den Graphen packen
        for schicht in self.alle_schichten[1:]:
            for neuron in schicht:
                for ni, wi in neuron.eingaenge:
                    G.add_edge(ni, neuron, weight=wi)

        plt.figure(figsize=(12, 8))
        edges = G.edges(data=True)
        
        # (u=Knoten von, v=Knoten zu, d=Daten-Dictionary)
        weights = [abs(d['weight']) * 0.8 for u, v, d in edges]  # Liniendicke = Absolutbetrag des Gewichts
        edge_colors = ['blue' if d['weight'] > 0 else 'red' for u, v, d in edges]  # Blau = erregend, Rot = hemmend

        # Graphen-Elemente zeichnen
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700, alpha=0.9)
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=weights, arrows=True, arrowsize=15, alpha=0.6)
        
        # Beschriftungen für Eingangs- und Ausgangsneuronen zuordnen
        labels = {n: n.name for n in self.input_layer + self.output_layer}
        nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight="bold")

        plt.title("Gelerntes Kreditkarten-Netzwerk\n(Blau = Positives Gewicht, Rot = Negatives Gewicht, Dicke = Stärke)", fontsize=14)
        plt.axis('off')  # Koordinatenachsen ausblenden 
        plt.tight_layout()
        plt.show()


# --- (20 Beispieldatensätze der Bank) ---
# Struktur pro Kunde: [Monatliches Einkommen, Schufa-Score, Aktuelle Schulden] (Wertebereich jeweils 0 bis 100)
KUNDEN_DATEN = [
    [85, 90, 10], [20, 30, 85], [70, 80, 15], [30, 40, 70], [95, 85, 5],
    [15, 20, 90], [80, 75, 20], [45, 50, 60], [65, 85, 25], [25, 35, 80],
    [90, 95, 10], [40, 30, 50], [75, 70, 30], [80, 60, 10], [60, 80, 20],
    [35, 45, 65], [70, 90, 5],  [85, 65, 15], [20, 55, 75], [50, 40, 55]
]

# Binäre Zielvorgabe: [1] = Kreditkarte genehmigen, [0] = Kreditkarte ablehnen
ENTSCHEIDUNG = [
    [1], [0], [1], [0], [1],
    [0], [1], [0], [1], [0],
    [1], [0], [1], [1], [1],
    [0], [1], [1], [0], [0]
]

# --- PIPELINE STARTEN ---

# 1. Netzwerk-Instanz erzeugen
bank_netz = KreditNetzwerk()

# 2. Netz trainieren (3000 Durchläufe über alle Datensätze mit einer Lernrate von 0.4)
bank_netz.trainiere(KUNDEN_DATEN, ENTSCHEIDUNG, epochen=3000, lernrate=0.4)


# --- EVALUATION (CONFUSION MATRIX & CLASSIFICATION REPORT) ---

# Reale Zielwerte in eine Liste für scikit-learn überführen
y_true = [ziel[0] for ziel in ENTSCHEIDUNG]
y_pred = []

# Alle Trainingsdaten erneut abfragen, um die finale Performance zu testen
for kunde in KUNDEN_DATEN:
    score = bank_netz.vorhersage(kunde)
    # Schwellenwert-Entscheidung (Klassifikation): Alles ab 0.5 wird auf Klasse 1 gerundet
    binaere_entscheidung = 1 if score >= 0.5 else 0
    y_pred.append(binaere_entscheidung)

# Berechnung der statistischen Gütekriterien
cm = confusion_matrix(y_true, y_pred)
report = classification_report(y_true, y_pred, target_names=["Abgelehnt (0)", "Genehmigt (1)"])

# Strukturierte Ausgabe des Evaluationsberichts in der Konsole
print("\n" + "="*50)
print("             EVALUATIONS-BERICHT")
print("="*50)
print("\n[1] CONFUSION MATRIX (Wahrheit vs. Vorhersage):")
print(f"                       Vorhergesagt (0)   Vorhergesagt (1)")
print(f"Tatsächlich Abgelehnt (0):      {cm[0][0]:2d}                 {cm[0][1]:2d}")
print(f"Tatsächlich Genehmigt (1):      {cm[1][0]:2d}                 {cm[1][1]:2d}")

print("\n[2] CLASSIFICATION REPORT:")
print(report)
print("="*50)

# 3. Grafische Netzwerktopologie öffnen und rendern
bank_netz.visualisiere_netzwerk()
