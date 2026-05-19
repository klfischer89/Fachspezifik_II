import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree  # Entscheidungsbaum Klassifizierung, grafische Darstellung
from sklearn.preprocessing import OneHotEncoder             # Umwandlung von qualitativen Daten zu quantitativen Daten (Binär)
import matplotlib.pyplot as plt                             # Visualisierung

daten = {}

df = pd.DataFrame(daten)                                    # Erstellung eines Dataframe aus Dict (Schlüssel-Wertpaare)
X = df[["Wetter", "Temperatur", "Luftfeuchtigkeit", "Wind"]]# Eingabevariablen (Features)
y = df["Golfplatz_oeffnen"]                                 # Zielvariable (Labels)

encoder = OneHotEncoder(sparse_output = False)              # Sparse Matrix aus Daten erzeugen (sparse_output = false -> entählt auch Nullen -> numpy Array)
X_encoded = encoder.fit_transform(X)                        # Eingabedaten (Text) -> Binärspalten
feature_names = encoder.get_feature_names_out(X.columns)    # Spaltennamen für die transformierte Matrix aus den feauters ziehen

model = DecisionTreeClassifier(criterion = "entropy",       # Verwende Informationsgewinn, um Baum zu erstellen
                               random_state = 67)           # Reproduzierbare Ergenisse, fixieren der Zufallsprozesse im Training
model.fit(X_encoded, y)                                     # Modell trainieren

neue_situation = pd.DataFrame({"Wetter": ["sonnig"],
                               "Temperatur": ["mild"],
                               "Luftfeuchtigkeit": ["hoch"],
                               "Wind": ["stark"]})

neue_situation_encoded = encoder.transform(neue_situation)

vorhersage = model.predict(neue_situation_encoded)          # Vorhersage auf Basis der Trainingsdaten
print(vorhersage[0])

plt.figure(figsize=(18,10))                                 # Größe der Grafischen Fläche (Zoll)
plot_tree(model, feature_names=feature_names,               # Entscheidungsbaum zeichnen
          class_names=["ja", "nein"], filled=True)
plt.show()                                                  # Grafik anzeigen