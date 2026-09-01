# Fitnessstudio-Managementsystem

Ein System zur Verwaltung von Mitgliedern, Kursen und Buchungen für ein
Fitnessstudio. Projekt im Rahmen des DBMS-Moduls (THGA Bochum, Dozent:
Stephan Bökelmann).

Das System besteht aus einer PostgreSQL-Datenbank, einem FastAPI-Backend,
einem Tkinter-Frontend und wird über Docker Compose orchestriert. Zusätzlich
gibt es ein `.deb`-Installationspaket für das Frontend.

## Repository-Layout

```
api/                    # FastAPI-Backend
db/                     # Datenbankschema und Seed-Daten
frontend/               # Tkinter-Frontend (Quellcode)
gym-frontend-deb/       # Build-Struktur für das .deb-Paket
gym-frontend-deb.deb    # fertiges Installationspaket
docker-compose.yml      # Orchestrierung aller Services
```

## Betrieb des Systems

Anforderungen: Docker, Docker Compose.

```
docker compose up -d --build
```

Dies startet PostgreSQL (mit Beispieldaten befüllt) und das FastAPI-Backend
unter http://localhost:8000. Die interaktive API-Dokumentation ist unter
http://localhost:8000/docs verfügbar.

## Betrieb des Frontends

```
sudo apt install ./gym-frontend-deb.deb
gym-frontend
```

Oder direkt starten, ohne Installation:

```
cd frontend
python3 app.py
```

## Sicherheit

Alle schreibenden API-Endpunkte sind über einen `X-API-Key`-Header
abgesichert.

## Erstellung der Dokumentation (PDF)

Die vollständige Projektdokumentation befindet sich in einem separaten
Repository: [-gym-management-docs](https://github.com/rouaa63/-gym-management-docs)

## Entwicklungsprozess

Dieser Abschnitt dokumentiert den Schritt-für-Schritt-Prozess, der zum Bau
des Systems verwendet wurde, in der Reihenfolge, in der es tatsächlich
entwickelt wurde.

### Schritt 1 – Datenbankeinrichtung mit Docker Compose

Die PostgreSQL-Datenbank wurde als Container gestartet, wobei das Schema
und die Seed-Daten (Mitglieder, Kurse, Buchungen) beim ersten Start
automatisch geladen wurden.

```
docker compose up -d
```

**Verifikation:** Der Datenbankcontainer läuft im gesunden Zustand.

```
docker compose ps
```

`screen1`: <img width="1365" height="166" alt="image" src="https://github.com/user-attachments/assets/7a3bfdab-1cf1-46a4-a527-908333618f13" />


**Verifikation:** Abfrage der geseedeten Daten direkt über `psql`.

```
docker compose exec db psql -U <user> -d gymdb -c "SELECT * FROM members;"
```

`screen2`: <img width="1365" height="263" alt="image" src="https://github.com/user-attachments/assets/a2005254-af68-40d9-94d0-e646ef7d976c" />


### Schritt 2 – FastAPI-Backend

Das Backend wurde mit FastAPI gebaut und stellt CRUD-Endpunkte für
Mitglieder, Kurse und Buchungen bereit, inklusive der N:M-Beziehung
zwischen Mitgliedern und Kursen.

```
cd api
uvicorn main:app --reload
```

**Verifikation:** Die automatisch generierte Swagger-Benutzeroberfläche,
die alle Endpunkte auflistet.

`screen3`: <img width="1485" height="728" alt="لقطة الشاشة 2026-09-01 105357" src="https://github.com/user-attachments/assets/4f1d150a-42c4-42b1-b940-83bcbc649b0d" />







**Verifikation:** Rückgabe von geseedeten Daten über `GET /members`.

`screen4` : <img width="1429" height="635" alt="image" src="https://github.com/user-attachments/assets/ec832f70-7799-437d-9038-e3be659ee611" />


**Verifikation:** Erstellen einer neuen Buchung über `POST /bookings`
(Demonstration der N:M-Beziehung zwischen Mitgliedern und Kursen).

`screen5` : <img width="1326" height="349" alt="لقطة الشاشة 2026-09-01 105818" src="https://github.com/user-attachments/assets/825894ba-af39-434b-b472-108c6a3dee67" />


### Schritt 3 – Tkinter-Frontend

Das Frontend wurde mit Tkinter gebaut und bietet drei Bereiche: Mitglieder,
Kurse und Buchungen.

```
cd frontend
python3 app.py
```

**Verifikation:** Die Startoberfläche des Frontends mit den drei Tabs.

`screen6` : <img width="1532" height="807" alt="لقطة الشاشة 2026-09-01 110228" src="https://github.com/user-attachments/assets/5b67657f-2b55-4228-98b9-030c5405cdbc" />



**Verifikation:** Anlegen eines neuen Mitglieds über die Oberfläche.

`screen7`: <img width="712" height="362" alt="لقطة الشاشة 2026-09-01 110330" src="https://github.com/user-attachments/assets/34543d1d-a854-4788-9ea7-91ae00c8d2be" />



**Verifikation:** Buchung eines Kurses für ein Mitglied über die Oberfläche.

`screen8`: <img width="1182" height="509" alt="لقطة الشاشة 2026-09-01 110453" src="https://github.com/user-attachments/assets/ac41c624-52cb-4632-89ac-412309bd805d" />


### Schritt 4 – Paketierung als `.deb`

Das Frontend wurde zusätzlich als `.deb`-Paket verpackt, um eine einfache
Installation unter Linux zu ermöglichen.

```
sudo apt install ./gym-frontend-deb.deb
```


## Demo-Video

Ein 8–10-minütiges Demo-Video des Systems ist hier verfügbar:https://youtu.be/ppxhwYo4cLQ

## Verwandtes Repository

Die vollständige Projektdokumentation (LaTeX-Quelle, PDF-Build via
GitHub Actions) befindet sich unter:
[-gym-management-docs](https://github.com/rouaa63/-gym-management-docs)
