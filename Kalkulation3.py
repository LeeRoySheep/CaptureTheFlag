# ========================================
# 🏳️‍🌈 CAPTURE THE FLAG - FLAGGEN-QUIZ
# ========================================

import random
import urllib.request
import json
import sqlite3
import html_handler_v3 as handle
from File_Handler import FileHandler as f_handle, smooth_image
import asyncio
from Input_Handler import check_int_input, exit_game


# =========================================================
# 🎯 FUNKTION ZUR BEWERTUNG DER BEVÖLKERUNGS-SCHÄTZUNG
# =========================================================

def get_points_population(user_guess, correct_answer):
    """
    Berechnet die Abweichung zwischen geschätzter und tatsächlicher Bevölkerungszahl
    und gibt entsprechende Punkte zurück.

    Param1: user_guess - geschätzte Einwohnerzahl
    Param2: correct_answer - tatsächliche Einwohnerzahl
    Rückgabe: Punkte als Integer zwischen 0 und 10
    """
    diversion = float(user_guess/correct_answer)
    if diversion <= 1:
        return int(10 * diversion)
    else:
        diversion = 2 - diversion
        if diversion > 0:
            return int(10 * diversion)
        else:
            return 0


# =========================================================
# 🏆 HIGHSCORE-DATENBANK
# =========================================================

def create_highscore_db():
    """
    Erstellt die SQLite-Datenbank für die Highscores,
    falls sie noch nicht existiert.
    """
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS highscores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT,
            score INTEGER
        )
    ''')
    conn.commit()
    conn.close()


def save_highscore(player_name, score):
    """
    Speichert den Highscore eines Spielers in der SQLite-Datenbank.

    Param1: player_name - Name des Spielers
    Param2: score - Erzielte Punktzahl
    """
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute('INSERT INTO highscores (player_name, score) VALUES (?, ?)', (player_name, score))
    conn.commit()
    conn.close()


def get_top_highscores(limit=5):
    """
    Ruft die besten Highscores aus der Datenbank ab.

    Param1: limit - Anzahl der anzuzeigenden Highscores (Standard: 5)
    Rückgabe: Liste der besten Spieler mit ihren Punktzahlen
    """
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute('SELECT player_name, score FROM highscores ORDER BY score DESC LIMIT ?', (limit,))
    top_scores = c.fetchall()
    conn.close()
    return top_scores


# =========================================================
# 🌍 LÄNDER-DATEN ABRUFEN
# =========================================================

def get_country_data(timeout=10):
    """
    Erstellt ein Wörterbuch mit Länderinformationen (Name, Hauptstadt, Bevölkerung, Flagge).
    Die Daten stammen aus einer API und Wikipedia.

    Param1: timeout - Maximale Wartezeit für die Datenabfrage (in Sekunden)
    Rückgabe: Dictionary mit Länderinformationen
    """
    url = "https://restcountries.com/v3.1/all"
    try:
        import ssl
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=context) as response:
            data = json.loads(response.read().decode())

        country_dict = {}
        country_flag_dict = {}
        
        # Daten aus der API abrufen
        for country in data:
            name = country.get("translations").get("deu").get("common") #country.get('name', {}).get('common', 'Unbekannt')
            flag_url = country.get('flags', {}).get('png', 'Keine Flagge verfügbar')
            country_flag_dict[name] = flag_url
        try:
            # Asynchrones Abrufen der Wikipedia-Daten
            successful_extractions = asyncio.run(handle.fetch_all_countries([*country_flag_dict.keys()],timeout))[0]
            for country, capital, population in successful_extractions:
                country_dict[country] = {"capital": capital, 'population': population, "flag": country_flag_dict[country]}
        except NameError as false_name:
            print(false_name, "\nCreating dictionary from Wikipedia please wait!")
        except TypeError as type_err:
            print(type_err,"\nDictionary for quiz still loading please be patient!")
        except ValueError as val_err:
            print(val_err,"\nDictionary still loading please wait!")
        except RuntimeError:
            print(f"Wikipage for country {name} not found!\nDictionary still loading!")
        return country_dict
    except Exception as e:
        print(f"Fehler beim Abruf der Daten: {e}")
        return {}


# =========================================================
# 📜 SPIELREGELN ANZEIGEN
# =========================================================

def show_rules():
    """
    Gibt die Spielregeln aus einer Datei im Terminal aus.
    """
    print(f_handle('rules.txt').txt_file_to_str())


def ask_for_rules():
    """
    Fragt den Spieler, ob er die Regeln sehen möchte, und zeigt sie gegebenenfalls an.
    """
    while True:
        try:
            rules_choice = input("📋 Möchtest du die Spielregeln sehen? (Ja/Nein): ").strip().lower()
            if rules_choice in ["ja", "nein"]:
                if rules_choice == "ja":
                    show_rules()
                break
            else:
                raise ValueError("⚠️ Ungültige Eingabe! Bitte Ja oder Nein angeben.")
        except ValueError as e:
            print(e)


# =========================================================
# 👥 SPIELER-EINGABEN
# =========================================================

def get_players(prompt):
    '''
    function to get number of players form user as integer
    biger than 0
    return: value as int>0
    '''
    while True:
        try:
            value = input(prompt).strip()
            if value.lower() == "exit":
                exit_game()
            value = int(value)
            if value > 0:
                return value
            else:
                print("⚠️ Bitte eine Zahl größer als 0 eingeben.")
        except ValueError:
            print("⚠️ Ungültige Eingabe. Bitte eine Zahl eingeben oder 'exit' zum Beenden.")


# =========================================================
# 🎮 Schwierigkeitsgrad
# =========================================================

def get_valid_difficulty():
    """
    Funktion zur Auswahl des Schwierigkeitsgrads.
    Gibt 1 für Multiple-Choice-Antworten zurück (Anfänger-Modus).
    Gibt 2 für freie Texteingabe zurück (Profi-Modus).

    Rückgabe:
    - difficulty (str): '1' für Anfänger, '2' für Pro.
    """
    while True:
        difficulty = input("💡 Wähle den Schwierigkeitsgrad (1 = Anfänger | 2 = Pro): ").strip()
        
        # Möglichkeit, das Spiel jederzeit zu verlassen
        if difficulty.lower() == "exit":
            exit_game()
        
        # Überprüfung auf gültige Eingabe
        if difficulty in ["1", "2"]:
            return difficulty
        else:
            print("⚠️ Ungültige Eingabe. Bitte '1' für Anfänger oder '2' für Pro eingeben oder 'exit' zum Beenden.")


# =========================================================
# 🎮 SPIELSTART
# =========================================================

def start_game():
    """
    Hauptfunktion des Spiels. Fragt die Spieleranzahl, Runden und den Schwierigkeitsgrad ab.
    Danach wird das Quiz mit Flaggen, Hauptstädten und Bevölkerungszahlen gespielt.
    """
    print("\n🌎 Willkommen bei Capture the Flag - Flaggen-Quiz!")
    ask_for_rules()

    player_count = get_players("👥 Wie viele Spieler spielen mit? ")
    players = [input(f"👤 Spieler {i + 1}, wie heißt du? ") for i in range(player_count)]
    difficulty = get_valid_difficulty()
    rounds = get_players("🔁 Wie viele Runden möchtest du spielen? ")
    country_data = get_country_data()
    print()
    score = {player: 0 for player in players}

    for _ in range(rounds):
        for player in players:
            country_names = list(country_data.keys())
            country = random.choice(country_names)
            flag_url = country_data[country]['flag']
            # converts the image to print in terminal 
            # inform of ANSI Escape codes 
            #img = Image.open(BytesIO(requests.get().content)).convert("CMYK").convert("RGB")#.show()
            #output = climage.convert_pil(img, is_unicode=True, width=60)
            print(f"Spieler: {player}, deine Flagge:\n")
            #print(output)
            smooth_image(flag_url)

            capital = country_data[country]['capital']
            population = country_data[country]['population']

            if difficulty == "1":
                country_choices = random.sample(country_names, 3) + [country]
                random.shuffle(country_choices)
                for j, choice in enumerate(country_choices, 1):
                    print(f"{j}. {choice}")
                print("🌍 Wähle das richtige Land:")
                country_answer = check_int_input(min=1,max=4)
                if country_choices[int(country_answer) - 1] == country:
                    score[player] += 10
                    print("✅ Richtig!")
                else:
                    print(f"❌ Falsch! Die richtige Antwort war {country}.")

                capital_choices = random.sample(
                    [c['capital'] for c in country_data.values() if c['capital'] != capital], 3) + [capital]
                random.shuffle(capital_choices)
                for j, choice in enumerate(capital_choices, 1):
                    print(f"{j}. {choice}")
                print("🏙️ Wähle die richtige Hauptstadt:")
                capital_answer = check_int_input(min=1,max=4)
                if capital_choices[int(capital_answer) - 1] == capital:
                    score[player] += 10
                    print("✅ Richtig!")
                else:
                    print(f"❌ Falsch! Die richtige Antwort war {capital}.")

                population_choices = random.sample(
                    [c['population'] for c in country_data.values() if c['population'] != population], 3) + [population]
                random.shuffle(population_choices)
                for j, choice in enumerate(population_choices, 1):
                    print(f"{j}. {choice}")
                print("👥 Wähle die richtige Einwohnerzahl:")
                population_answer = check_int_input(min=1,max=4)
                if int(population_choices[int(population_answer) - 1]) == population:
                    score[player] += get_points_population(int(population_choices[int(population_answer) - 1]),int(population))
                    print("✅ Richtig!")
                else:
                    print(f"❌ Falsch! Die richtige Antwort war {population}.")
                    del country_data[country]
            # -------------Pro-Handling
            else: 
                country_answer = input("🌍 Nenne das Land zur Flagge: ")
                if country_answer.strip().lower() == country.lower():
                    score[player] += 10
                    print("✅ Richtig!")
                else:
                    print(f"❌ Falsch! Die richtige Antwort war {country}.")

                capital_answer = input("🏙️ Nenne die Hauptstadt: ")
                if capital_answer.strip().lower() == capital.lower():
                    score[player] += 10
                    print("✅ Richtig!")
                else:
                    print(f"❌ Falsch! Die richtige Antwort war {capital}.")
                while True:
                    try:
                        population_answer = int(input("👥 Schätze die Einwohnerzahl des Landes: "))
                        break
                    except ValueError as val_err:
                        print("Falsche Eingabe!\nBitte geben Sie einen Integer größer 0 ein!")
                points_population = get_points_population(population_answer, population)
                score[player] += points_population
                print(
                    f"🏆 Du hast {points_population} Punkte für die Einwohnerzahl erhalten."
                    + f"Die richtige Antwort lautet: {population}"
                    )
                del country_data[country]


    print("\n🎉 Spiel beendet! Punktestand:")
    for player, points in score.items():
        print(f"🏅 {player}: {points} Punkte")
    
    print("\n🔥 Die besten 5 Spieler aller Zeiten:")
    for player, points in score.items():
        save_highscore(player, points)
    for i, (player_name, score) in enumerate(get_top_highscores(), 1):
        print(f"{i}. {player_name} - {score} Punkte")


if __name__ == "__main__":
    create_highscore_db()
    start_game()





"""
📜 Endprotokoll: Capture the Flag - Flaggen-Quiz
Dieses Dokument beschreibt die wichtigsten Funktionen und den Ablauf des Spiels Capture the Flag - Flaggen-Quiz .

🛠 Programmierung von:
👨‍💻 **Alexander Thielemeier**
👩‍💻 **Sadia Aschrafi**
👨‍💻 **Nicolas Heyer**
👨‍💻 **Leroy Stevenson**
👨‍💻 **Joshua Paoletti**

Co-Programmierer & Mentor:
🧑‍🏫 **Ishan Rastogi**

🛠 Funktionen
1️⃣ get_points_population(Benutzerschätzung, richtige_Antwort)

Parameter:
user_guess(int) – Die geschätzte Einwohnerzahl
correct_answer(int) – Die tatsächliche Einwohnerzahl
Rückgabe:
Punkte (int), basierend auf der Genauigkeit der Schätzung

2️⃣ Länderdaten abrufen (`get_country_data(timeout=10))
Lädt die Länderinformationen (Name, Hauptstadt, Bevölkerung, Flaggen-URL) a

Parameter:
timeout(int, optional) – Maximale Wartezeit für den aufbau der 10 sec
Rückgabe:
Wörterbuch mit Ländern und deren Details ( name, capital, population, `flaggen)

3️⃣ Highscore speichern (`ssave_highscore(name, score))
Speichert den Highscore eines Spielers in einer SQLite-Datenbank.

Parameter:
name(str) – Name des Spielers
score(int) – Erzielte punkte

4️⃣ Beste Highscores abrufen (`get_top_highscores(get_top_highscores(limit=5))
Liest die besten Spielergebnisse aus der Highscore-Datenbank.

Parameter:
limit(int, optional) – Anzahl der angezeigten Highscore
Rückgabe:
Liste der besten Spielergebnisse als Tupel ( (player_name, score))

5️⃣ Spielregeln anzeigen ( show_rules())
Liest die Spielregeln aus einer Datei ( rules.txt) und gibt sie im Terminal aus.

6️⃣ Spiel starten ( start_game())
Der Hauptprozess des Spiels, in allen Teilen

🕹️ Spielablauf
1️⃣ Der Spieler gibt an, wie viele Personen mitspielen.
2️⃣ Jeder Spieler gibt seinen Namen ein.
3️⃣ Der Schwierigkeitsgrad wird gewählt:

🟢 Anfänger-Modus (Multiple-Choice-Fragen)
🔴 Pro-Modus (Freitext,Zahlen)
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
"""