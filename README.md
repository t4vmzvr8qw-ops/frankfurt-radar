# Frankfurt Radar

## Funktionen
- Kuratiertes Frankfurt-Discovery-Dashboard mit acht Startorten
- Interaktive Karte, Kategorie- und Stadtteilfilter, Favoriten und eigener Aktivitätsplaner
- Aktuelle lokale **Nachrichtenartikel** zu Events, Gastronomie und Kultur via Google-News-RSS/GitHub Actions
- Link zum offiziellen Visit-Frankfurt-Veranstaltungskalender und JSON-Backup

## Wichtige Grenzen
**Nachrichtendatum ist nicht Veranstaltungsdatum.** Diese App behauptet nicht, einen live verifizierten Veranstaltungskalender einzubinden. Konkrete Termine/Öffnungszeiten beim Veranstalter oder im verlinkten offiziellen Kalender prüfen. Für den RSS-Feed **GitHub Actions** als Pages-Source auswählen. Der Startfeed ist leer bis zum ersten erfolgreichen Workflow.

## Installation über GitHub Pages

1. ZIP entpacken. **Für jede App ein eigenes GitHub-Repository** anlegen (öffentlich, wenn GitHub Pages kostenlos genutzt werden soll).
2. Den **Inhalt des entpackten App-Ordners** in das Repo-Root hochladen oder via Git pushen. Die versteckte `.github`-Struktur muss mit übernommen werden, falls vorhanden.
3. Unter **Repository → Settings → Pages** einstellen: für Market Pulse und Frankfurt Radar **Source: GitHub Actions**; bei den vier anderen **Deploy from a branch**, Branch `main`, `/(root)`.
4. Nach dem Deployment die bereitgestellte Pages-URL auf dem iPhone in Safari öffnen und unter Teilen **Zum Home-Bildschirm** wählen.
5. Falls Updates zunächst nicht sichtbar sind: Seite neu laden und ggf. den Homescreen-Link schließen und neu öffnen. Die Service-Worker-Datei nutzt bei Internetzugang eine Network-first-Strategie.

### Lokal ausprobieren

Im jeweiligen Ordner ausführen:

```sh
python3 -m http.server 8000
```

Dann `http://localhost:8000` im Browser öffnen. Für RSS-Apps muss zuvor das jeweilige `scripts/fetch_*.py` ausgeführt werden, um Online-Schlagzeilen abzurufen.

### Datenschutz

Persönliche Daten werden im lokalen Browser-Speicher gespeichert (bei Bildern IndexedDB). Es gibt keine Anmeldung und keine Synchronisierung. Der Quellcode eines öffentlichen GitHub-Repositorys ist öffentlich, **deine lokal eingegebenen Daten jedoch nicht im Repo enthalten**. Drittanbieter-Dienste für Karten, Wetter und RSS können übliche Verbindungsdaten erhalten. Import/Export von persönlichen Daten ist in den App-Einstellungen verfügbar (Bilder gesondert beachten).

### Technische Details

- Reines HTML/CSS/JavaScript, keine Build-Pipeline, keine bezahlten Dienste oder verpflichtenden API-Keys
- Responsiv für iPhone und Desktop, Hell-/Dunkelmodus, PWA-Manifest und Service Worker
- API-/Netzwerkzugriff erforderlich für aktuelle Feeds und externe Karten/Wetter
- **Prototypen:** vor produktivem Einsatz oder Veröffentlichung mit echten Daten bitte weitere Tests durchführen

## Events nach Datum (Version 2)

Der neue Tab **Events** zeigt Veranstaltungen direkt in der App. Datum wählen, Heute/Morgen oder sieben Tage ab Datum einstellen, Kategorie und Suche nutzen, Veranstaltung direkt in Meine Pläne übernehmen. Die Events werden als echte Termine (nicht Veröffentlichungsdaten von Nachrichten) aus öffentlich erreichbaren strukturierten Feeds von Evensos und Goethe-Universität Frankfurt übernommen. Eine Quelle kann zeitweise ausfallen oder nur einen Teil der Events anbieten. Keine behauptete Vollständigkeit oder Live-Garantie.

Für den automatischen Import muss die Datei `.github/workflows/deploy.yml` im Repository existieren und der Workflow einmal erfolgreich laufen. Er führt `scripts/fetch_events.py` aus und veröffentlicht `data/events.json`. Bei fehlenden Daten wird der letzte erfolgreiche Feed beibehalten. Die App benötigt keine persönlichen Kalenderberechtigungen. Der Original-Link erscheint optional nur zur Prüfung/Anmeldung; die Eventdetails stehen direkt in der App.
