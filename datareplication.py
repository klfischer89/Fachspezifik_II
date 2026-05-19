from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
import time
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree      
from sklearn.preprocessing import OneHotEncoder                 
import matplotlib.pyplot as plt              
import logging
from dataclasses import dataclass
import joblib

def log_etl_conf():
    # monitoring the process on level INFO and log in file etl.log
    logging.basicConfig(filename="datereplication.log", level=logging.INFO, format="%(asctime) s - %(message) s")

def write_log(e):
    logging.error("Fehler aufgetreten: %s", e)

def provide_data():
    data = { 
        "Gewicht": [
            "leicht", "schwer", "mittel", "schwer", "leicht",
            "mittel", "schwer", "leicht", "mittel", "schwer",
            "leicht", "mittel", "schwer", "leicht", "mittel",
            "schwer", "leicht", "mittel", "schwer", "leicht"
        ],
        
        "Zielregion": [
            "national", "international", "national", "national", "international",
            "international", "national", "national", "international", "international",
            "national", "national", "national", "international", "international",
            "international", "national", "national", "national", "international"
        ],
        
        "Wert": [
            "niedrig", "hoch", "hoch", "niedrig", "hoch",
            "niedrig", "hoch", "niedrig", "hoch", "hoch",
            "hoch", "niedrig", "hoch", "niedrig", "hoch",
            "niedrig", "niedrig", "hoch", "niedrig", "hoch"
        ],
        
        "Zerbrechlich": [
            "nein", "ja", "nein", "ja", "nein",
            "nein", "ja", "nein", "ja", "nein",
            "nein", "nein", "nein", "ja", "nein",
            "ja", "ja", "ja", "nein", "ja"
        ],
        
        "Entscheidung": [
            "normal", "pruefen", "express", "pruefen", "express",
            "normal", "pruefen", "normal", "pruefen", "express",
            "express", "normal", "express", "pruefen", "express",
            "pruefen", "pruefen", "pruefen", "normal", "pruefen"
        ]
    }

    return data


    model: object
    feature_names: list

def create_decision_tree(data):

    df = pd.DataFrame(data)                                                # Erstellung eines Dataframe aus Dict (Schlüssel-Wertpaare)
    X = df[["Gewicht", "Zielregion", "Wert", "Zerbrechlich"]]              # Eingabevariablen (Features)
    y = df["Entscheidung"]                                                 # Zielvariable (Labels)

    encoder = OneHotEncoder(sparse_output = False)                          # Sparse Matrix aus Daten erzeugen (sparse_output = false -> entählt auch Nullen -> numpy Array)
    X_encoded = encoder.fit_transform(X)                                    # Eingabedaten (Text) -> Binärspalten

    model = DecisionTreeClassifier(criterion = "entropy",                   # Verwende Informationsgewinn, um Baum zu erstellen
                                random_state = 42)                          # Reproduzierbare Ergenisse, fixieren der Zufallsprozesse im Training
    model.fit(X_encoded, y)                                                 # Modell trainieren

    joblib.dump(model, 'mein_paket_modell.pkl')                             # Modell und Encoder persistent speichern
    joblib.dump(encoder, 'mein_onehot_encoder.pkl')

def data_producer(data):
    
    # Kafka-Produzent initialisieren
    produzent = KafkaProducer(bootstrap_servers = ["localhost:9092"],                            # Adresse des Kafka-Server
                              value_serializer = lambda wert:json.dumps(wert).encode("utf-8"))   # Umwandlung der Daten für die Übertragung, Text --> Byte
    
    # Daten senden, nur die Features, später soll mit dem Entscheidungsbaum Vorhersagen getroffen werden
    try:

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

            # Nachricht senden
            produzent.send("datenreplikation", value = nachricht)   
            print(f"\033[32mGesendet: {nachricht}\033[0m")

            # zwischen dem Senden von Nachrichten, 0.5 Sekunden warten
            time.sleep(0.5)                                               

    # Fehlerbeandlung    
    except Exception as fehler:
        print(f"\033[31mFehler beim Senden der Nachricht: {fehler}\033[0m")
        write_log(fehler)

    finally:                                                            
        produzent.flush()                                               # Alle Nachrichten die noch nicht gesendet wurden senden
        produzent.close(timeout = 5)                                    # Produzenten nach 5 Sekunden schließen

def data_consumer():
    
    # Konsument initialisieren
    konsument = KafkaConsumer("datenreplikation",                                                 # Topic
                                bootstrap_servers = "localhost:9092",                             # Server Adresse
                                auto_offset_reset = "latest",                                     # Beim ersten Start, ab der ersten Nachricht lesen
                                consumer_timeout_ms=5000,                                         # timeout wenn 5 Sekunden lang keine Nachricht kommt
                                enable_auto_commit = True,                                        # merken welche Nachrichten bereits gelesen wurden
                                group_id = "paket_gruppe_1",                                      # Gruppe für Konsumenten
                                value_deserializer = lambda x: json.loads(x.decode("utf-8")))     # Bytes --> Text                
    print("\033[32mWarten auf Nachricht...\033[0m")

    try:
        for index, nachricht in enumerate(konsument, start=101):

            # Jede eintreffende Nachricht
            aktuelle_daten = nachricht.value

            # Direkte Ausgabe 
            print(f"\033[32mPaket P-{index} empfangen: \033[33m{aktuelle_daten}\033[0m")

            # Übergabe an den Entscheidungsbaum, um eine Vorhersage zu treffen
            decision_making(aktuelle_daten)

    # Fehlerbehandlung
    except Exception as fehler:
        print(f"\033[33mFehler beim Empfang der Nachricht: {fehler}\033[0m")
        write_log(fehler)

    # Konsumenten schließen
    finally:
        konsument.close()

def decision_making(nachricht):
    # model und encoder aus Dateien laden
    model = joblib.load('mein_paket_modell.pkl')
    encoder = joblib.load('mein_onehot_encoder.pkl')

    # nachricht eines consumers zu einem DataFrame konvertieren
    dfNachricht = pd.DataFrame([nachricht])

    # Nachricht mit OneHotEncoder umwandeln
    nachricht_encoded = encoder.transform(dfNachricht)                      

    # Modell trifft Vorhersage
    vorhersage = model.predict(nachricht_encoded)                                                                  
    print(f"\033[32mEntscheidung für dieses Paket \033[33m---> {vorhersage[0]}\033[0m")

def show_tree():
    # Modell aus Datei laden
    model = joblib.load('mein_paket_modell.pkl')
    encoder = joblib.load('mein_onehot_encoder.pkl')

    # Bildgröße und Auflösung
    plt.figure(figsize=(16, 8), dpi=150)

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

    # Titel hinzufügen
    plt.title("Entscheidungsbaum - Paket-Klassifizierung", fontsize=16, fontweight='bold', pad=20)

    # Ränder minimieren und Grafik sauber abspeichern
    plt.tight_layout()
    plt.savefig("entscheidungsbaum.png", bbox_inches='tight', dpi=300)
    plt.show()       

# Main line
if __name__ == "__main__":
    
    try:
        log_etl_conf()
        data = provide_data()
        create_decision_tree(data)
        data_producer(data)
        data_consumer()
        show_tree()

    except Exception as fehler:
        print(f"\033[33m Es ist ein Fehler aufgetreten: {fehler}\033[0m")
        write_log(fehler)