from kafka import KafkaProducer
import json
import time

def daten_produzent():
    
    # Kafka-Server initialisieren
    produzent = KafkaProducer(bootstrap_server = ["localhost:9092"],                            # Adresse des Kafka-Server
                              api_versoin = (0,10,1),                                           # Sprache des Servers
                              value_serializer = lambda wert:json.dumps(wert).encode("utf-8"))  # Umwandlung der Daten für die Übertragung
    # Fehlerbehandlung
    try:
        for i in range(10):
            nachricht = {"id": i,
                         "name": f"name-{i}",
                         "wert": i*10}
            produzent.send("datensynchornisation", value = nachricht)   # Nachrichten mit Topic "datensynchonisation senden"
            print(f"Gesendet: {nachricht}")
            time.sleep(1)                                               # 1 Sekunde Pause zwischen dem senden
        
    except Exception as fehler:
        print(f"Fehler beim Senden der Nachricht: {fehler}")
    finally:
        produzent.flush()                                               # Alle Nachrichten die noch nicht gesendet wurden senden
        produzent.close(timeout = 5)                                    # Schließen nach 5 Sekunden

if __name__ == "__main__":
    daten_produzent()