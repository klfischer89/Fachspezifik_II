# Datenreplikation

In diesem Projekt wird ein Entscheidungsbaum mit Paketdaten angelernt um zu entscheiden ob ein Paket normal, per Express versendet werden soll oder ob eine weitere Prüfung notwendig ist. Die Daten werden über einen Kafka-Server übermittelt. Dabei werden die Daten von einem Producer gesendet und von einem Consumer empfangen. Dieser gibt die einzelnen Nachrichten weiter an einen Entscheidungsbaum um für jede Paket eine Entscheidung, wie zuvor beschrieben, zu fällen. Die Entscheidung für jedes Paket wird auf der Konsole ausgegeben. Aueßrdem wird der Entscheidungsbaum grafisch dargestellt.

## Bereitstellen der Daten

- Die daten werden in einer separaten Methode `provide_data()` zur Verfügung gestellt. Die Daten sind in einem Dictionary gespeichert und enthalten folgende Merkmale (Schlüssel): `Gewicht, Zielregion, Wert, Zerbrechlich, Entscheidung` 
- Die Werte zu den Schlüsseln bestehen aus listen. Beispiel:
```python
"Gewicht": [
            "leicht", "schwer", "mittel", "schwer", "leicht",
            "mittel", "schwer", "leicht", "mittel", "schwer",
            "leicht", "mittel", "schwer", "leicht", "mittel",
            "schwer", "leicht", "mittel", "schwer", "leicht"
        ]
``` 

## Entscheidungsbaum erstellen

1. Daten in einen DataFrame speichern
2. Eingabevariablen (Features) festlegen `Gewicht, Zielregion, Wert, Zerbrechlich`
3. Zielvariable (Label) festlegen `Entscheidung`
4. OneHotEncoder zum Erstellen eine Sparse-Matrix, umwandeln der Eingabevariablen
5. Entscheidungsbaum erstellen mit `DecisionTreeClassifier` mit folgenden Parametern: `criterion = entropy, random_state = 42` . Zum Aufbau des Entscheidungsbaum wird der Informationsgewinn genutzt. Es wurde ein random_state vergeben um reproduzierbare Ergebnisse des Modells zu erhalten
7. Modell mit Features und Labels trainieren
8. Speichern des Modells und des Encoders in Dateien um diese persistent in weiteren Skripten/Funktionen nutzen zu können
```python
joblib.dump(model, 'mein_paket_modell.pkl')                             
joblib.dump(encoder, 'mein_onehot_encoder.pkl')
```

## Producer erzeugen und Paketdaten senden

- Um den Producer nutzen zu können wurde ein lokaler Kafka-Server aufgesetzt. Dieser hat die Adresse `localhost:9092`. Die Daten die vom Producer gesendet werden, werden durch eine lambda Funktion von Text zu Binär umgewandelt und folgen der `UTF-8` Codierung.
```python
# Kafka-Produzent initialisieren
    produzent = KafkaProducer(bootstrap_servers = ["localhost:9092"],                           
                              value_serializer = lambda wert:json.dumps(wert).encode("utf-8")) 
```
- Um die Werte der Originaldaten, die als Listen vorliegen, als einzelne Nachrichten zu versenden wird die `zip()` Funktion verwendet und nur die Features aus den Daten extrahiert und zu jedem Eintrag in den Originaldaten zu einer Nachricht zusammen gesetzt.
```python
# einzelne Werte aus den Daten extrahieren
        for gewicht, zielregion, wert, zerbrechlich, in zip(data["Gewicht"], data["Zielregion"], data["Wert"], 
                                                                         data["Zerbrechlich"]):
            
            # Nachricht zum Senden vorbereiten
            nachricht = {
                "Gewicht": gewicht,
                "Zielregion": zielregion,
                "Wert": wert,
                "Zerbrechlich": zerbrechlich,
            }
```
- Bei dem Senden, wird zwischen den Nachrichten 0.5 Sekunden gewartet.

## Consumer erzeugen und Paketdaten empfangen

- Der Consumer wurde wie folgt initiallisiert um nur neu erhaltene Nachrichten zu empfangen und sich zu schließen, wenn 5 Sekungen lang keine Nachrichten eingegangen sind:
```python
# Konsument initialisieren
    konsument = KafkaConsumer("datenreplikation",                                                 # Topic
                                bootstrap_servers = "localhost:9092",                             # Server Adresse
                                auto_offset_reset = "latest",                                     # Beim ersten Start, ab der ersten Nachricht lesen
                                consumer_timeout_ms=5000,                                         # timeout wenn 5 Sekunden lang keine Nachricht kommt
                                enable_auto_commit = True,                                        # merken welche Nachrichten bereits gelesen wurden
                                group_id = "paket_gruppe_1",                                      # Gruppe für Konsumenten
                                value_deserializer = lambda x: json.loads(x.decode("utf-8")))
```
- Der Konsument übergibt eine Nachricht an das `decision_making()` um für jedes Paket direkt eine Entscheidung zu treffen.

## Entscheidungen für Pakete treffen

- Das Decision Making verwendet das Modell und den Encoder, die bei der Erstellung des Entscheidungsbaums in `pkl` Dateien gespeichert wurden
- Die Nachricht die von einem Consumer an die Entscheidungsfindung weiter geschickt wurde, wird als DataFrame gespeichert
- Der DataFrame wird durch den Encoders transformiert
- Die transformierten Daten werden dem Modell übergeben, um eine Vorhersage zu treffen.
- Die Vorhersage wird auf der Konsole ausgegeben

## Visualisierung des Ergebnisses und des Entscheidungsbaums

- Zum Erstellen einer grafischen Darstellung des Entscheidungsbaums werden das Modell und der Encoder aus den `pkl` Dateien geladen
- Die Größe der Grafischen Darstellung wird festgelegt
- Mittels `plot_tree` wird die Darstellung des Baums formatiert
```python
# Baum mit erweiterten Formatierungen zeichnen
    plot_tree(
        model, 
        feature_names=encoder.get_feature_names_out(),               
        class_names=["normal", "pruefen", "express"], 
        filled=True,
        rounded=True,       # Abgerundete Ecken für moderne Optik
        fontsize=10,        # Schriftgröße fixieren, damit nichts überlappt
        precision=2,        # Nachkommastellen bei Splitting-Kriterien begrenzen
        max_depth=10        # WICHTIG: Begrenzt die Tiefe der Anzeige, falls der Baum zu groß ist
    )
```
- Es wird ein Titel hinzugefügt
- Die Grafik wird abgespeichert `plt.savefig("entscheidungsbaum.png", bbox_inches='tight', dpi=300)` und angezeigt.

## Logging

- Das Logging wurde über `logging` mit der `basicConfig` und dem `level=INFO` realisiert
- folgende Fehler werden mit `timestamp`, `nachricht`und `fehlercode` geloggt:
```python
Exception
```