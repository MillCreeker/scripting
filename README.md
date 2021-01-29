# Template Repository

## About
### Authors/Contributors
* [Tobias Weigl](mailto:tobias.weigl@edu.fh-joanneum.at)
* [Jan Mühlbacher](mailto:jan.muehlbacher@edu.fh-joanneum.at)
* [Sebastian Toporsch](mailto:sebastian.toporsch@edu.fh-joanneum.at)

## BackUpr

### Description
Backupsystem auf Datenbank. Das System verfügt über eine config Datei, in der festgelegt wird welche Dateien/Ordner gesichert werden sollen. Diese Sicherung erfolgt dann in regelmäßigen Abständen (z.B einmal täglich). Gesichert werden die Dateien auf einer Datenbank, die vom Script angesprochen wird.\

Das Script überprüft, ob die ausgewählten Dateien auf der Datenbank korrekt abgespeichert wurden.\

Die Ergebnisse des Backups werden in einer Logdatei gespeichert (alle Dateien erfolgreich gesichert, Prozessdetails).

### Abgearbeitete Punkte:
* Access to Files
* Access to Database
* Regex
* Runnable as cronjob

# Todo
* read database date out of config
* read cronjob data out of config and start cronjob through python script