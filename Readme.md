# Capture the Flag Readme

Dies ist eine kurze Beschreibung zur Installation und zum Spiel **Capture the Flag**

## Installation Guide

Zum installieren kopieren Sie dies in ihre Python Console um alle Pakete zu installieren.
> *'pip3 install -r requirements.txt'*

 from your working folder or the folder where you want to store Capture the flag

## Usage and/or Rules

 Capture is a round based quiz fetching flags from the wikipedia and other quiz related Data.
 For Correct answers you get Points and for false answers the maximum Points to win get less.
 You can Play with 1 Player in Version 0.1, but we are planning to open you a multiplayer quiz game in Version 1.0

## Contribution and Copyright

 This Game is only using quoted images and Information from Wikipedia.
 We assume it is illegal to use this game for commercial reasons.
 Still it is all open source and feel free to use the code base for your own Games or even help us develop a greater gaming experience.

## 📜 Endprotokoll: Capture the Flag - Flaggen-Quiz

Dieses Dokument beschreibt die wichtigsten Funktionen und den Ablauf des Spiels Capture the Flag - Flaggen-Quiz .

### 🛠 Programmierung von

👨‍💻 **Alexander Thielemeier**
👩‍💻 **Sadia Aschrafi**
👨‍💻 **Nicolas Heyer**
👨‍💻 **Leroy Stevenson**
👨‍💻 **Joshua Paoletti**

#### vCo-Programmierer & Mentor

🧑‍🏫 **Ishan Rastogi**

### 🛠 Funktionen

1️⃣ get_points_population(Benutzerschätzung, richtige_Antwort)

#### Parameter

user_guess(int) – Die geschätzte Einwohnerzahl
correct_answer(int) – Die tatsächliche Einwohnerzahl
Rückgabe:
Punkte (int), basierend auf der Genauigkeit der Schätzung

### 2️⃣ Länderdaten abrufen (`get_country_data(timeout=10))

Lädt die Länderinformationen (Name, Hauptstadt, Bevölkerung, Flaggen-URL) a

#### Parameter

timeout(int, optional) – Maximale Wartezeit für den aufbau der 10 sec
Rückgabe:
Wörterbuch mit Ländern und deren Details ( name, capital, population, `flaggen)

### 3️⃣ Highscore speichern (`ssave_highscore(name, score))

Speichert den Highscore eines Spielers in einer SQLite-Datenbank.

#### Parameter

name(str) – Name des Spielers
score(int) – Erzielte punkte

### 4️⃣ Beste Highscores abrufen (`get_top_highscores(get_top_highscores(limit=5))

Liest die besten Spielergebnisse aus der Highscore-Datenbank.

#### Parameter:

limit(int, optional) – Anzahl der angezeigten Highscore
Rückgabe:
Liste der besten Spielergebnisse als Tupel ( (player_name, score))

### 5️⃣ Spielregeln anzeigen ( show_rules())

Liest die Spielregeln aus einer Datei ( rules.txt) und gibt sie im Terminal aus.

### 6️⃣ Spiel starten ( start_game())

Der Hauptprozess des Spiels, in allen Teilen

## 🕹️ Spielablauf

1️⃣ Der Spieler gibt an, wie viele Personen mitspielen.    
2️⃣ Jeder Spieler gibt seinen Namen ein.    
3️⃣ Der Schwierigkeitsgrad wird gewählt:    

 🟢 Anfänger-Modus (Multiple-Choice-Fragen) .   
 🔴 Pro-Modus (Freitext,Zahlen) .   
 4️⃣ Die Anzahl der Runden wird festgelegt.    
 5️⃣ **In jeder Runde muss die SpIn jeder Runde müssen die Spieler:    
Das Land anhand der Flagge erraten.    
Die Hauptstadt nennen.    
Die ungefähre Einwohnerzahl schätzen.    
6️⃣ Am Ende wird der Sieger bestimmt und die besten Highscores werden gespeichert.    

🏆 Highscore-System    
Die besten Ergebnisse aller Zeiten werden in einer SQLite-Datenbank geladen     
Nach jedem Spiel werden die Top 5 Spieler angezeigt.    
Falls ein Spieler einen Highscore erreicht, wird dies hervorgehoben.    
