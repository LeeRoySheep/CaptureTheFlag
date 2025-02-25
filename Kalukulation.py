import random
import urllib.request
import json
from PIL import Image
from io import BytesIO
import requests
import sqlite3
import sys


# -----functoin to give points for population gase by diversion-----
def get_points_population(user_guess, correct_answer):
    '''
    function that calculates the diversion between answer and real value
    and returns points calculated by diversion as rounded integer
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
    """Erstellt die SQLite-Datenbank für die Highscores, falls sie noch nicht existiert."""
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
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute('INSERT INTO highscores (player_name, score) VALUES (?, ?)', (player_name, score))
    conn.commit()
    conn.close()


def get_top_highscores(limit=5):
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute('SELECT player_name, score FROM highscores ORDER BY score DESC LIMIT ?', (limit,))
    top_scores = c.fetchall()
    conn.close()
    return top_scores


# ------------------------ Länder-Daten abrufen ------------------------
def get_country_data():
    url = "https://restcountries.com/v3.1/all"
    try:
        import ssl
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=context) as response:
            data = json.loads(response.read().decode())

        country_dict = {}
        for country in data:
            name = country.get('name', {}).get('common', 'Unbekannt')
            capital = country.get('capital', ['Unbekannt'])[0]
            population = country.get('population', 'Unbekannt')
            flag_url = country.get('flags', {}).get('png', 'Keine Flagge verfügbar')
            country_dict[name] = {'capital': capital, 'population': population, 'flag': flag_url}

        return country_dict
    except Exception as e:
        print(f"Fehler beim Abruf der Daten: {e}")
        return {}


# ------------------------ Spielregeln ------------------------
def show_rules():
    print("\n📜 Spielablauf:")
    print("1. Jeder Spieler bekommt eine zufällige Flagge angezeigt.")
    print("2. Errate das Land zur Flagge.")
    print("3. Danach wird die Hauptstadt und die Einwohnerzahl des Landes abgefragt.")
    print("4. Im Anfänger-Modus gibt es Multiple-Choice-Fragen.")
    print("5. Im Pro-Modus müssen die Antworten direkt eingegeben werden.")
    print("6. Für jede richtige Antwort gibt es 10 Punkte.")
    print("7. Bei der Einwohnerzahl werden pro 10% Abweichung 1 Punkt abgezogen.")
    print("8. Am Ende gewinnt der Spieler mit den meisten Punkten!")
    print("9. Du kannst jederzeit mit 'exit' das Spiel beenden.\n")


def ask_for_rules():
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
    print("🚪 Spiel wird beendet. Danke fürs Spielen!")
    sys.exit()


def get_players(prompt):
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


def get_valid_difficulty():
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
            Image.open(BytesIO(requests.get(flag_url).content)).show()
            print(f"{player}, deine Flagge: {flag_url}")

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
