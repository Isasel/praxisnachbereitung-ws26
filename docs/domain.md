# Aufgabe B: ER-Modell für die Geräteausleihe
## Mermaid-ERD

```mermaid
erDiagram
    Person ||--o{ Assignment : leiht_aus
    Device ||--o{ Assignment : wird_ausgeliehen

    Person {
        int mitarbeiter_id PK
        string vorname
        string nachname
        string abteilung
        string standort
    }

    Device {
        int geraetenummer PK
        string geraete_typ
        string modell
        date kauf_datum
        decimal netto_kaufpreis
        string standort
    }

    Assignment {
        int ausleih_id PK
        int mitarbeiter_id FK
        int geraetenummer FK
        datetime ausgabe_datum
        datetime rueckgabe_datum
    }
```
## Fachregeln

- **R1 - Höchstens eine aktive Ausleihe für ein Gerät** 
- **R2 - Verfügbar oder ausgeliehen:** Ein Gerät ist ausgeliehen wenn `rueckgabe_datum IS NULL` gilt. 
- **R3 - Gültige Zeitfolge:** Ein eingetragener Rückgabezeitpunkt darf nicht vor dem Ausgabezeitpunkt liegen und für das selbe Gerät nicht im selben Zeitrahmen überschneiden.
- **R4 - Stabile Kennungen** IDs werden nicht neu vergeben 
