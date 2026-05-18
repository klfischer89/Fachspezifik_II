# ETL Prozess

In diesem Projekt werden Kundendaten aus einer CSV Datei mit 100 Einträgen ausgelesen. Die Daten werden nach dem Auslesen aufbereitet und bereinigt, um fehlende Werte oder falsche Datentypen zu vermeiden und zu korrigieren. Die Daten werden anschließend in eine SQLite Datenbank gespeichert. Zur Visualisierung der Daten wird das Alter der Kunden herangezogen, in Kategorien eingeteilt und in einem Histogramm dargestellt.

Das Projekt untersützt Logging um Fehler im ETL Prozess transparent und nachvollziehbar zu machen.

## Einlesen der CSV-Datei

- Öffnen der Datei mit with open, damit die Datei automatisch wieder geschlossen wird. Für die Codierung wird UTF-8 verwendet. Die Datei liegt im Unterverzeichnis "data" und heißt kunden.csv.`with open("data/kunden.csv", newline="", encoding="utf-8") as file:`
- Die Datei wird über `DictReader`geöffnet und zur weiteren Verarbeitung in eine `list`konvertiert

## Datenbereinigung und Fehlerhafte Datensätze

- Die Bereinigung der Daten umfasst mehrer Schritte, um:
    - fehlende Werte durch Standardwerte zu erstezen
    - Datentypen umzuwandeln
    - Business Regeln zu entpsrechen
    - Konformität von Zeichenketten sicherzustellen
- Dazu wird eine Liste mit allen Feldern erstellt um als Referenz bei der weiteren Verarbeitung zu dienen `define_fields()` und mittels `type` der Datentyp jedes Feldes ermittelt `check_datatypes`

1. Leere Felder in den Datensätzen ermitteln `check_empty_fields()`
2. Datentypen konvertieren, fehlende Werte ersetzen, Business Regeln prüfen `convert_data()`
    - `customer_id` zu int konvertieren
    - fehlende Werte für `email` auf "None" setzen
    - `age` zu int konvertieren und fehlende Werte durch 0 ersetzen
    - `registration_date` in ein Datum mit dem Format "YYYY-MM-DD"" konvertieren und Werte die "None, "", invalid-date" sind durch "1900-01-01" ersetzen
    - prüfen ob ein Kunde volljährig ist, wenn nicht dann den `status` des Kunden auf "inactive" setzen
3. Datensätze mit fehlenden Einträgen werden in eine separate Liste gespeichert `save_missing_values()`
4. E-Mail Adressen anhand eines Musters (Regex: `r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'`) validieren `check_email()`
5. Prüfen ob der Status eines Kunden "active, inactive, deleted" ist und andernfalls auf inactie setzen `check_status()`, mit Hilfe einer Referenzliste aller erlaubten Status
6. Prüfen der Felder `firstname, lastname, city` auf Zahlen und Sonderzeichen mit einem Pattern (Regex: `r"^[a-zA-ZäöüÄÖÜß]+$"`)

## SQL Tabelle erstellen und Daten in die Datenbank speichern

- mit `sqlite3` wird eine Verbindung zu der Datenbank `customers.db` aufgebaut
- Tabelle erstellen mit SQL `create_database()`
```SQL
CREATE TABLE IF NOT EXISTS customers(
                    customer_id INTEGER Primary Key,
                    firstname TEXT NOT NULL,
                    lastname TEXT NOT NULL,
                    email TEXT NOT NULL,
                    city TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    registration_date DATE NOT NULL,
                    status TEXT NOT NULL)' 
``` 
- Verbindung wieder schließen

- Daten in die Datenbank speichern `fill_database()`
```SQL
INSERT INTO customers (customer_id,firstname,lastname,email,city,age,registration_date,status)
                        VALUES (?,?,?,?,?,?,?,?)""",
                        (kunde['customer_id'], kunde['first_name'], kunde['last_name'], kunde['email'], kunde['city'], kunde['age'], kunde['registration_date'], kunde['status'])
```

## Daten laden und visualisieren

- Die Daten werden aus der Datenbank geladen `load_data()` dazu wird erneut eine Verbindung über sqlite3 hergestellt
- SELECT Statement
```SQL
SELECT customer_id, age FROM customers
```
- Die Daten werden dann in einer Liste gespeichert

- Zur Visualisierung der Daten werden aus dieser Liste die relevanten Daten (`id, age`) extrahiert
- Das Alter wird mittels Grenzen in Kategorien eingeteilt `[0, 20, 40, 60, 80, 100]`
- Die Daten werden in einem Histogramm dargestellt

## Logging

- Das Logging wurde über `logging` mit der `basicConfig` und dem `level=INFO` realisiert
- folgende Fehler werden mit `timestamp`, `nachricht`und `fehlercode` geloggt:
```python
FileNotFoundError
TypeError
ValueError
KeyError
OverflowError
sqlite3.Error
sqlite3.OperationalError 
```