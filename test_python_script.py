import pandas as pd

def read_excel(path):
    try:
        df = pd.read_excel(path)
        print(f"Erfolgreich eingelesen: {path}\n")
        print("Inhalt der Excel-Tabelle:")
        print("-" * 50)
        print(df)
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{path}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
if __name__ == "__main__":
    path = "./excel/Praxis Nachbereitung Übung Tag 1.xlsx"
    read_excel(path)