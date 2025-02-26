import random
import urllib.request
import json
from PIL import Image
from io import BytesIO
import requests
import sqlite3
import sys
import html_handler_2 as handle
import climage
from File_Handler import FileHandler as f_handle
  




# -----functoin to give points for population gase by diversion-----
def get_points_population(user_guess, correct_answer):
    '''
    function that calculates the diversion between answer and real value
    and returns points calculated by diversion as float to arounded integer
    param1: user_guesss
    param2: correct_answer
    return: 10 >= int(10 * diversion) >= 0
    '''
    diversion = float(user_guess/correct_answer)
    if diversion <= 1:
        return int(10 * diversion)
    else:
        diversion = 2 - diversion
        if diversion > 0:
            return int(10 * diversion)
        else:
            return 0


# ------------------------ Datenbank für Highscores ------------------------
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
    function that checks for new highscores at end of game and
    saves the score and player name to a sqlite3 based database
    param1: player_name
    param2: score
    """
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute('INSERT INTO highscores (player_name, score) VALUES (?, ?)', (player_name, score))
    conn.commit()
    conn.close()


def get_top_highscores(limit=5):
    """
    function to read the highscores from a sqlite3 based database
    and returns them as list of tuples
    param1: limit with default value 5
    return: top_scores
    """
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute('SELECT player_name, score FROM highscores ORDER BY score DESC LIMIT ?', (limit,))
    top_scores = c.fetchall()
    conn.close()
    return top_scores


# ------------------------ Länder-Daten abrufen ------------------------
def get_country_data():
    """
    function to create a dictionary of dictionaries with
    main keys as 'name' of countries, each refering to a dictionary
    of 'flag_url' key refering to an url refering to flag image as '.png',
    both extracted from a '.json' file.
    And population as key for number of inhabitants and capital_city as key for the 
    capital city in the country, both extracted from Wikipedia.
    return: countries_dict 
    """
    url = "https://restcountries.com/v3.1/all"
    try:
        import ssl
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=context) as response:
            data = json.loads(response.read().decode())

        country_dict = {}
        for country in data:
            try:
                name = country.get("translations").get("deu").get("common") #country.get('name', {}).get('common', 'Unbekannt')
                country_object = handle.CountryInfo(name)
                capital = country_object.get_capital_city() #country.get('capital', ['Unbekannt'])[0]
                population = country_object.get_inhabitants()
                flag_url = country.get('flags', {}).get('png', 'Keine Flagge verfügbar')
                country_dict[name] = {'capital': capital, 'population': population, 'flag': flag_url}
            except NameError as false_name:
                print(false_name, "\nCreating dictionary from Wikipedia please wait!")
                continue
            except TypeError as type_err:
                print(type_err,"\nDictionary for quiz still loading please be patient!")
                continue
            except ValueError as val_err:
                print(val_err,"\nDictionary still loading please wait!")
                continue
            except RuntimeError as page_not_found:
                print(f"Wikipage for country {name} not found!\nDictionary still loading!")
                continue
        print(len(country_dict))
        return country_dict
    except Exception as e:
        print(f"Fehler beim Abruf der Daten: {e}")
        return {}


# ------------------------ Spielregeln ------------------------
def show_rules():
    '''
    void function printing rules to Terminal saved in rules.txt
    '''
    print(f_handle('rules.txt').txt_file_to_str())


def ask_for_rules():
    '''
    void function to that asks for player input and prints rules 
    if wanted by player
    '''
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


def exit_game():
    """
    void function to end game any time
    """
    print("🚪 Spiel wird beendet. Danke fürs Spielen!")
    sys.exit()

# ------------------------Spieler------------------------
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


# ---------------------Schwierigkeitsgrad---------------------
def get_valid_difficulty():
    """
    function that returns 1 for multiple choice answers
    and 2 for free text input as answer for profesional players
    retrun: difficulty
    """
    while True:
        difficulty = input("💡 Wähle den Schwierigkeitsgrad (1 = Anfänger | 2 = Pro): ").strip()
        if difficulty.lower() == "exit":
            exit_game()
        if difficulty in ["1", "2"]:
            return difficulty
        else:
            print("⚠️ Ungültige Eingabe. Bitte '1' für Anfänger oder '2' für Pro eingeben oder 'exit' zum Beenden.")



# ------------------------ Spielstart ------------------------
def start_game():
    '''
    void main function to arrange the game handling of input and output 
    and back end functions
    '''
    print("\n🌎 Willkommen bei Capture the Flag - Flaggen-Quiz!")
    ask_for_rules()

    player_count = get_players("👥 Wie viele Spieler spielen mit? ")
    players = [input(f"👤 Spieler {i + 1}, wie heißt du? ") for i in range(player_count)]
    difficulty = get_valid_difficulty()
    rounds = get_players("🔁 Wie viele Runden möchtest du spielen? ")

    country_data = get_country_data()
    country_names = list(country_data.keys())
    score = {player: 0 for player in players}

    for _ in range(rounds):
        for player in players:
            country = random.choice(country_names)
            flag_url = country_data[country]['flag']
            # converts the image to print in terminal 
            # inform of ANSI Escape codes 
            img = Image.open(BytesIO(requests.get(flag_url).content)).convert("RGB")#.show()
            output = climage.convert_pil(img, is_unicode=True, width=20)
            print(f"Spieler: {player}, deine Flagge:\n\n")
            print(output)

            capital = country_data[country]['capital']
            population = country_data[country]['population']

            if difficulty == "1":
                country_choices = random.sample(country_names, 3) + [country]
                random.shuffle(country_choices)
                for j, choice in enumerate(country_choices, 1):
                    print(f"{j}. {choice}")
                country_answer = input("🌍 Wähle das richtige Land: ")
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
                capital_answer = input("🏙️ Wähle die richtige Hauptstadt: ")
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
                population_answer = input("👥 Wähle die richtige Einwohnerzahl: ")
                if int(population_choices[int(population_answer) - 1]) == population:
                    score[player] += get_points_population(int(population_choices[int(population_answer) - 1]),int(population))
                    print("✅ Richtig!")
                else:
                    print(f"❌ Falsch! Die richtige Antwort war {population}.")
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
                print(f"🏆 Du hast {points_population} Punkte für die Einwohnerzahl erhalten."
                      + f"Die richtige Antwort lautet: {population}")


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
# Endprotokoll: Capture the Flag - Flaggen-Quiz

Dieses Endprotokoll beschreibt die wichtigsten Funktionen des Spiels *Capture the Flag - Flaggen-Quiz* sowie deren Funktionsweise.

## Funktionen

### 1. **get_points_population(user_guess, correct_answer)**
Berechnet die Punkte basierend auf der Abweichung zwischen der geschätzten und der tatsächlichen Bevölkerungszahl.
- Parameter: `user_guess` (int), `correct_answer` (int)
- Rückgabe: Punkte (int)

### 2. **get_country_data()**
Lädt die Länderinformationen (Name, Hauptstadt, Bevölkerung, Flaggen-URL) aus der API https://restcountries.com/v3.1/all.
- Rückgabe: Dictionary mit Ländern und deren Details

### 3. **save_highscore(name, score)**
Speichert den Highscore eines Spielers in der Liste `highscores`.
- Parameter: `name` (str), `score` (int)

### 4. **display_highscores()**
Zeigt die Top 10 Highscores in absteigender Reihenfolge an.

### 5. **start_game(simulated_input=None)**
Der Hauptprozess des Spiels, der die Anzahl der Spieler, Runden und den Schwierigkeitsgrad abfragt. Es zeigt zufällig gewählte Länderflaggen an, fordert den Spieler auf, das Land, die Hauptstadt und die ungefähre Bevölkerungszahl zu erraten.
- Parameter: `simulated_input` (list, optional) für Testzwecke

### Ablauf
1. Der Spieler wählt die Anzahl der Spieler.
2. Jeder Spieler gibt seinen Namen ein.
3. Der Spieler wählt den Schwierigkeitsgrad (1 = Anfänger, 2 = Pro).
4. Der Spieler wählt die Anzahl der Runden.
5. Für jede Runde:
    - Die Flagge eines zufälligen Landes wird angezeigt.
    - Der Spieler rät das Land, die Hauptstadt und die Einwohnerzahl.
6. Am Ende des Spiels werden die Punkte angezeigt und in die Highscore-Liste eingetragen.

### Fehlerbehandlung
- Ungültige Eingaben werden abgefangen.
- Fehlt die API-Antwort, wird das Spiel abgebrochen.
- Das Programm berücksichtigt, dass die Bevölkerungszahl möglicherweise nicht genau erraten wird.
"""