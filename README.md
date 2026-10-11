Wir haben die CSV eingeleen und sie danach in Power Query angepasst.

Es kam zu Problemen bei der Währung, da sie in der csv mit einem . statt einem , gespeichert wurder
=> Wir haben das Gebietsbereich angepasst.

Dann haben wir die Tabellen zusammengefüht

Dann haben wir Pivottabellen erzeugt.

---

## Tag 2 – Aufgabe A: Setup und Tests (PowerShell)

### 1. Ausführungsort

Alle PowerShell-Codeblöcke können direkt aus dem Repository-Hauptordner
`C:\dev\GitHub\praxisnachbereitung-ws26` kopiert und ausgeführt werden.
Die Docker-Befehle enthalten den Pfad zur Compose-Datei; ein Ordnerwechsel
ist nicht nötig. Das gilt auch für beide MQTT-Terminals.

### 2. Dienste starten und Status prüfen

```powershell
docker compose -f .\minimal-starter-db-light-plus-mqtt\minimal-starter-db-light-plus-mqtt\docker-compose.yml up -d --build
docker compose -f .\minimal-starter-db-light-plus-mqtt\minimal-starter-db-light-plus-mqtt\docker-compose.yml ps
```

Erwartung: `api`, `db` und `mqtt` laufen; bei `db` steht zusätzlich `healthy`.
Wenn die Dienste bereits laufen, reicht zur Kontrolle `docker compose -f .\minimal-starter-db-light-plus-mqtt\minimal-starter-db-light-plus-mqtt\docker-compose.yml ps`.

### 3. Health-Check, Swagger und Oberfläche

```powershell
curl.exe --fail --silent --show-error http://localhost:8000/health
```

Erwartete Antwort:

```json
{"status":"ok","db":"ok","mqtt":"ok"}
```

Im Browser öffnen:

```powershell
Start-Process 'http://localhost:8000/health'
Start-Process 'http://localhost:8000/docs'
Start-Process 'http://localhost:8000/'
```

Swagger zusätzlich im Terminal prüfen (erwartet: `200`):

```powershell
(Invoke-WebRequest -UseBasicParsing 'http://localhost:8000/docs').StatusCode
```

### 4. Datenbank prüfen

Tabellen direkt anzeigen:

```powershell
docker compose -f .\minimal-starter-db-light-plus-mqtt\minimal-starter-db-light-plus-mqtt\docker-compose.yml exec -T db psql -U appuser -d appdb -c '\dt'
```

Erwartung: Tabelle `public.device` wird aufgelistet.

Alternativ die Datenbank interaktiv öffnen:

```powershell
docker compose -f .\minimal-starter-db-light-plus-mqtt\minimal-starter-db-light-plus-mqtt\docker-compose.yml exec db psql -U appuser -d appdb
```

Im PostgreSQL-Prompt nacheinander eingeben:

```text
\dt
\q
```

`\dt` zeigt die Tabellen, `\q` beendet den Datenbank-Client.
Im Übungsblatt ist `qsql` ein Tippfehler; richtig ist `psql`.

Optional die Beispieldaten über die API prüfen:

```powershell
curl.exe --fail --silent --show-error http://localhost:8000/reports/device-status
```

Erwartung: JSON mit Gerätestatus und der jeweiligen Anzahl.

### 5. MQTT testen (zwei Terminals)

In Terminal 1 abonnieren:

```powershell
docker compose -f .\minimal-starter-db-light-plus-mqtt\minimal-starter-db-light-plus-mqtt\docker-compose.yml exec mqtt mosquitto_sub -h localhost -p 1883 -t 'demo/#' -v -C 1
```

Der Befehl wartet auf eine Nachricht. In Terminal 2 senden:

```powershell
docker compose -f .\minimal-starter-db-light-plus-mqtt\minimal-starter-db-light-plus-mqtt\docker-compose.yml exec mqtt mosquitto_pub -h localhost -p 1883 -t 'demo/test' -m 'hello'
```

Erwartete Ausgabe in Terminal 1:

```text
demo/test hello
```

Der Subscriber beendet sich nach der ersten Nachricht automatisch.
Die MQTT-Programme laufen im Container; eine lokale Mosquitto-Installation
unter Windows ist dafür nicht nötig.

### 6. Logs bei Problemen ansehen

```powershell
docker compose -f .\minimal-starter-db-light-plus-mqtt\minimal-starter-db-light-plus-mqtt\docker-compose.yml logs --tail 50 api
docker compose -f .\minimal-starter-db-light-plus-mqtt\minimal-starter-db-light-plus-mqtt\docker-compose.yml logs --tail 50 db
docker compose -f .\minimal-starter-db-light-plus-mqtt\minimal-starter-db-light-plus-mqtt\docker-compose.yml logs --tail 50 mqtt
```

API-Logs fortlaufend beobachten:

```powershell
docker compose -f .\minimal-starter-db-light-plus-mqtt\minimal-starter-db-light-plus-mqtt\docker-compose.yml logs -f api
```

Mit `Strg+C` die Log-Anzeige beenden. Die Container laufen dabei weiter.
