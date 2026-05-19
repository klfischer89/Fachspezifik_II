from kafka import KafkaConsumer
import json

def daten_konsument():
    
    konsument = KafkaConsumer("datensynchronisation",                                             # Topic
                                bootstrap_server = "localhost:9092",                              # Server Adresse
                                api_version = (0,10,1),                                           # Sprache des Server
                                auto_offset = "earliest",                                         # Beim ersten Start, ab der ersten Nachricht lesen
                                enable_auto_commit = True,                                        # merken welche Nachrichten bereits gelesen wurden
                                group_id = "konsument-gruppe1",                                   # Gruppe für Konsumenten
                                value_deserializer = lambda x: json.loads(x.decode("utf-8")))     # Bytes --> Text                
    print("Warten auf Nachricht...")

    try:
        for nachricht in konsument:
            daten = nachricht.value
            print(f"Empfangen: {daten}")

    except Exception as fehler:
        print(f"Fehler ist aufgetreten: {fehler}")
    finally:
        konsument.close()


if __name__ == "__main__":
    daten_konsument()