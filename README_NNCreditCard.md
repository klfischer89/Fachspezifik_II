# Umfassende Fachdokumentation: Künstliches Neuronales Netzwerk zur Kreditkartenprüfung

Diese Dokumentation beschreibt die theoretischen Grundlagen, die mathematischen Kernmechanismen sowie die softwareseitige Implementierung eines mehrschichtigen künstlichen neuronalen Netzwerks (Multi-Layer-Perceptron, MLP). Das System wurde von Grund auf in reinem Python (ohne High-Level-Frameworks wie TensorFlow oder PyTorch) entwickelt. 

Das Ziel des Modells ist es, für ein Bankinstitut eine binäre Klassifikationsentscheidung zu treffen: Soll einem Kunden basierend auf seinen finanziellen Kennzahlen eine Kreditkarte genehmigt ($1$) oder verweigert ($0$) werden?

---

## 1. System- und Netzwerkarchitektur

Das Netzwerk basiert auf einer tiefen, vollvermaschten Vorwärtsarchitektur (Fully Connected Feedforward Network) mit insgesamt fünf Schichten.

### 1.1 Die Schichten im Detail
*   **Eingabeschicht (Input Layer - 3 Neuronen):** Nimmt die normalisierten Merkmale des Antragstellers auf.
*   **Versteckte Schichten (Hidden Layers 1 bis 3 - jeweils 4 Neuronen):** Diese Schichten sind für das Extrahieren komplexer, nicht-linearer Abhängigkeiten verantwortlich (z. B. das Verhältnis von Schulden zu Einkommen in Kombination mit der Schufa-Historie).
*   **Ausgabeschicht (Output Layer - 1 Neuron):** Liefert einen kontinuierlichen Wert im Intervall $[0, 1]$. Über einen definierten Schwellenwert (Threshold $\theta = 0.5$) wird die finale binäre Entscheidung abgeleitet.

### 1.2 Mathematische Vorverarbeitung (Featureskalierung)
Neuronale Netze, die mit der Sigmoid-Funktion arbeiten, reagieren extrem sensitiv auf große Eingangswerte. Große Zahlen führen dazu, dass die Ableitung der Aktivierungsfunktion gegen Null geht, wodurch das Netz aufhört zu lernen (Gradienten-Sättigung). 

Um dies zu verhindern, wird eine Min-Max-Skalierung auf den Wertebereich $[0, 1]$ angewendet, indem alle Rohwerte ($0$ bis $100$) durch das Maximum geteilt werden:
$$X_{\text{normalisiert}} = \frac{X_{\text{roh}}}{100.0}$$

---

## 2. Tiefgehende mathematische Analyse der Kernabschnitte

### 2.1 Nicht-lineare Aktivierung & das Sättigungsproblem
Ohne eine nicht-lineare Aktivierungsfunktion wäre das gesamte neuronale Netzwerk – unabhängig von der Anzahl der Schichten – mathematisch kollabierbar zu einer einzigen linearen Transformation (einfache Matrixmultiplikation). Die **Sigmoid-Funktion** (logistische Funktion) führt die notwendige Nicht-Linearität ein.

#### Mathematische Definition:
$$f(x) = \frac{1}{1 + e^{-x}}$$

#### Die mathematische Besonderheit der Ableitung:
Für die Backpropagation benötigen wir die erste Ableitung $f'(x)$. Die logistische Funktion besitzt die elegante mathematische Eigenschaft, dass ihre Ableitung direkt durch ihren eigenen Funktionswert ausgedrückt werden kann:
$$f'(x) = f(x) \cdot (1 - f(x))$$

Da das Neuron den Aktivierungswert nach dem Forward Pass bereits in der Variable `self.wert` speichert ($output = f(x)$), muss der zeitaufwändige Exponentialterm $e^{-x}$ im Rückwärtsdurchlauf nicht erneut berechnet werden. Das spart massiv Rechenleistung.

```python
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_ableitung(output):
    # Mathematischer Shortcut: Nutzt den bereits gespeicherten Aktivierungswert
    return output * (1 - output)
```

---

### 2.2 Der Vorwärtsschub (Forward Pass) & Vektor-Äquivalenz
Jedes Neuron in einer nachfolgenden Schicht empfängt die Aktivierungswerte aller Neuronen der vorherigen Schicht. Jede dieser Verbindungen besitzt ein individuelles, anpassbares Gewicht.

#### Mathematische Definition der Netzeingabe (gsum):
Für ein einzelnes Neuron $j$ berechnet sich die Netzeingabe $z_j$ als das Skalarprodukt aus dem Vektor der eingehenden Aktivierungen $\vec{a}$ und dem Gewichtsvektor $\vec{w}$:
$$z_j = \sum_{i=1}^{n} (w_{ji} \cdot a_i)$$
Die finale Aktivierung des Neurons ist dann $s_j = f(z_j)$.

#### Code-Kapselung und Dynamik:
Die Implementierung löst dies elegant, indem Schichten als Listen von `Neuron`-Objekten definiert sind. Das Netz wandert dynamisch durch die Architektur. Es ist dadurch vollkommen flexibel und könnte ohne Code-Änderung auf 10 oder mehr Hidden Layers erweitert werden.

```python
# Auszug aus der Neuron-Klasse:
def forward(self):
    gsum = 0.0
    for ni, wi in self.eingaenge:
        gsum += wi * ni.wert  # ni.wert entspricht der Aktivierung a_i des vorherigen Neurons
    self.wert = sigmoid(gsum)

# Auszug aus der Netzwerk-Klasse:
# Der Forward Pass triggert die Schichten strikt sequentiell von vorne nach hinten
for schicht in self.alle_schichten[1:]:  
    for neuron in schicht:
        neuron.forward()
```

---

### 2.3 Deep Backpropagation (Fehler-Rückführung über mehrere Schichten)
Die Backpropagation ist das Herzstück des Lernalgorithmus. Sie basiert auf der mathematischen **Kettenregel der Differentialrechnung**. Das Ziel ist es, herauszufinden, wie stark sich das Gesamtergebnis verändert, wenn wir ein einzelnes Gewicht in einer tiefen Schicht minimal verändern ($\frac{\partial E}{\partial w}$).

#### 1. Die Ausgangsschicht (Output Layer)
Der Fehler (Loss) wird über die quadratische Fehlerfunktion (Mean Squared Error für ein Muster) definiert: $E = \frac{1}{2}(y_{\text{ziel}} - y_{\text{ist}})^2$. Die Ableitung nach der Netzeingabe ergibt das Fehlersignal $\delta$ (Delta):
$$\delta_{\text{output}} = \frac{\partial E}{\partial z} = (y_{\text{ziel}} - y_{\text{ist}}) \cdot f'(y_{\text{ist}})$$

#### 2. Die versteckten Schichten (Hidden Layers) – Der mathematische Kern
Ein verstecktes Neuron hat keinen direkten "Soll-Wert". Seine Schuld am Gesamtfehler lässt sich nur dadurch ermitteln, dass man die Fehlersignale ($\delta$) aller Neuronen der *nächsten* Schicht nimmt, sie mit den jeweiligen Verbindungsgewichten multipliziert und aufsummiert.

Mathematisch ausgedrückt für ein Hidden-Neuron $j$:
$$\delta_j = \left( \sum_{k} w_{kj} \cdot \delta_k \right) \cdot f'(a_j)$$
*wobei $k$ über alle Neuronen der nachfolgenden Schicht läuft.*

#### Die Rückwärtsschleife im Code:
Um diesen Prozess über 3 Hidden Layers hinweg fehlerfrei zu berechnen, nutzt der Code eine rückwärtslaufende Index-Schleife (`range` mit negativem Schritt). Sie garantiert, dass die Deltas der Schicht $s+1$ bereits fertig berechnet sind, bevor das Netz die Schicht $s$ evaluiert.

```python
# s_idx startet bei der letzten Hidden Schicht (Index 3) und läuft rückwärts bis Index 1
for s_idx in range(len(self.alle_schichten) - 2, 0, -1):
    aktuelle_schicht = self.alle_schichten[s_idx]
    naechste_schicht = self.alle_schichten[s_idx + 1]
    
    for hn in aktuelle_schicht:
        fehler_hidden = 0.0
        # Fehler-Akkumulation: Gewicht zum Folge-Neuron * Delta des Folge-Neurons
        for vorwaerts_n in naechste_schicht:
            for ni, wi in vorwaerts_n.eingaenge:
                if ni == hn:  # Wenn die Verbindung vom aktuellen Hidden-Neuron ausgeht
                    fehler_hidden += wi * vorwaerts_n.delta
                    
        # Multiplikation mit der Steigung an der aktuellen Aktivierungsposition
        hn.delta = fehler_hidden * sigmoid_ableitung(hn.wert)
```

---

### 2.4 Der Optimierungsschritt (Stochastischer Gradientenabstieg)
Sobald alle Fehlersignale ($\delta$) in allen Neuronen berechnet wurden, werden die Gewichte angepasst. Die Anpassung erfolgt entgegen der Richtung des steilsten Fehleranstiegs (Gradientenabstieg).

#### Mathematische Definition der Delta-Regel:
$$\Delta w_{ji} = \eta \cdot \delta_j \cdot a_i$$
$$w_{ji}^{\text{neu}} = w_{ji}^{\text{alt}} + \Delta w_{ji}$$
*wobei $\eta$ (Eta) die Lernrate ist und $a_i$ der Aktivierungswert des sendenden Neurons.*

#### Softwarearchitektonische Besonderheit: Unpacking & In-Place Modification
In Python sind Tupel `(Objekt, Wert)` unveränderlich (*immutable*). Da die Verbindungen (`self.eingaenge`) jedoch als Liste von Tupeln vorliegen, löst der Code dies über ein explizites Entpacken und anschließendes Überschreiben des Listen-Index mittels `enumerate()`. Das schont den Arbeitsspeicher, da keine neuen Listen-Objekte erzeugt werden müssen.

```python
def aktualisiere_gewichte(self, lernrate):
    for i, (ni, wi) in enumerate(self.eingaenge):
        # ni.wert ist das Eingangssignal; self.delta ist das Fehlersignal des empfangenden Neurons
        neues_gewicht = wi + (lernrate * self.delta * ni.wert)
        self.eingaenge[i] = (ni, neues_gewicht)  # In-Place Ersetzung des Speicher-Tupels
```

---

### 2.5 Die Graphentransformation für die Visualisierung
Um den gelernten Zustand des Netzes sichtbar zu machen, wird die Objektstruktur des Netzwerks zur Laufzeit in einen gerichteten mathematischen Graphen (`networkx.DiGraph`) transformiert.

#### Das NetworkX Datentypproblem:
Die Bibliothek `networkx` gibt Kanteninformationen bei `G.edges(data=True)` als strukturierte Tripletts zurück: `(Startknoten, Zielknoten, Attribut-Dictionary)`. Ein direkter Dictionary-Zugriff auf die Kante wirft einen Typ-Fehler auf. Die Lösung ist ein sauberes semantisches *Tuple-Unpacking* in der List-Comprehension:

```python
edges = G.edges(data=True)

# Mathematische Skalierung für die Visualisierung:
# Die Kantenstärke (width) wird aus dem Absolutbetrag des gelernten Gewichts berechnet.
weights = [abs(d['weight']) * 0.8 for u, v, d in edges]

# Farbliche Signalisierung der gelernten Synapsen-Funktion:
# Positive Gewichte wirken erregend (Blau), negative Gewichte wirken hemmend (Rot).
edge_colors = ['blue' if d['weight'] > 0 else 'red' for u, v, d in edges]

nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=weights, arrows=True)
```

---

## 3. Evaluation und statistische Validierung

Nach Abschluss aller Trainings-Epochen reicht eine reine Reduzierung des mathematischen Fehlers (Loss) nicht aus, um die Qualität des Bankmodells zu beurteilen. Das System berechnet daher eine statistische Qualitätsmatrix über `scikit-learn`:

### 3.1 Die Konfusionsmatrix (Confusion Matrix)
Sie ist eine quadratische Matrix, die die realen Klassen mit den prognostizierten Klassen des Modells kreuzt:


| | Vorhergesagt: Abgelehnt (0) | Vorhergesagt: Genehmigt (1) |
|---|---|---|
| **Tatsächlich Abgelehnt (0)** | **True Negatives (TN)** <br> *(Kredit korrekt verweigert)* | **False Positives (FP)** <br> *(Risiko! Kredit fälschlich gewährt)* |
| **Tatsächlich Genehmigt (1)** | **False Negatives (FN)** <br> *(Umsatzverlust! Kunde fälschlich abgelehnt)* | **True Positives (TP)** <br> *(Kredit korrekt gewährt)* |

### 3.2 Die mathematischen Gütekriterien (Classification Report)
*   **Precision (Genauigkeit):** $\frac{TP}{TP + FP}$
    *   *Bedeutung für die Bank:* Wenn das Modell eine Kreditkarte freigibt, wie hoch ist die Wahrscheinlichkeit, dass der Kunde wirklich liquide ist? Eine niedrige Precision erhöht das Kreditausfallrisiko.
*   **Recall (Trefferquote):** $\frac{TP}{TP + FN}$
    *   *Bedeutung für die Bank:* Wie viel Prozent aller guten und liquiden Kunden hat das Modell erfolgreich herausgefiltert? Ein niedriger Recall bedeutet, dass die Bank profitable Kunden an die Konkurrenz verliert.