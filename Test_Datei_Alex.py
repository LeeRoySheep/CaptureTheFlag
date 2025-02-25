import random
import urllib.request
import json
from PIL import Image
from io import BytesIO
import requests
import sqlite3


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
    print("2. Es gibt Fragen zur Flagge, Hauptstadt und Bevölkerung.")
    print("3. Im Anfänger-Modus gibt es Multiple-Choice-Fragen.")
    print("4. Im Pro-Modus müssen die Antworten direkt eingegeben werden.")
    print("5. Für jede richtige Antwort gibt es einen Punkt.")
    print("6. Am Ende gewinnt der Spieler mit den meisten Punkten!\n")


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


def get_population_guess():
    while True:
        population_answer = input("👥 Wie viele Einwohner hat das Land? (Grobe Schätzung erlaubt): ")
        if population_answer.replace(',', '').isdigit():
            return int(population_answer.replace(',', ''))
        else:
            print("⚠️ Ungültige Eingabe. Bitte eine Zahl eingeben.")


# ------------------------ Spielstart ------------------------
def start_game():
    print("\n🌎 Willkommen bei Capture the Flag - Flaggen-Quiz!")
    ask_for_rules()

    player_count = int(input("👥 Wie viele Spieler spielen mit? "))
    players = [input(f"👤 Spieler {i + 1}, wie heißt du? ") for i in range(player_count)]
    difficulty = input("💡 Wähle den Schwierigkeitsgrad (1 = Anfänger | 2 = Pro): ")
    rounds = int(input("🔁 Wie viele Runden möchtest du spielen? "))

    country_data = get_country_data()
    country_names = list(country_data.keys())
    score = {player: 0 for player in players}

    for _ in range(rounds):
        used_countries = random.sample(country_names, len(players))

        for i, player in enumerate(players):
            country = used_countries[i]
            flag_url = country_data[country]['flag']
            Image.open(BytesIO(requests.get(flag_url).content)).show()
            capital = country_data[country]['capital']
            population = country_data[country]['population']
            #print(f"{player}, deine Flagge: {flag_url}")

            if difficulty == "1":
                choices = random.sample(country_names, 3) + [country]
                random.shuffle(choices)
                for j, choice in enumerate(choices, 1):
                    print(f"{j}. {choice}")
                answer = input("🌍 Wähle die richtige Nummer: ")
                if choices[int(answer) - 1] == country:
                    score[player] += 1
                    print("✅ Richtig!")
                else:
                    print(f"❌ Falsch! Die richtige Antwort war {country}.")
            else:
                answer = input("🌍 Nenne das Land zur Flagge: ")
                if answer.strip().lower() == country.lower():
                    score[player] += 1
                    print("✅ Richtig!")
                else:
                    print(f"❌ Falsch! Die richtige Antwort war {country}.")

            capital_answer = input(f"🏙️ Was ist die Hauptstadt von {country}? ")
            if capital_answer.strip().lower() == capital.lower():
                score[player] += 1
                print("✅ Richtig!")
            else:
                print(f"❌ Falsch! Die richtige Antwort war {capital}.")

            population_guess = get_population_guess()
            if abs(population_guess - population) / population <= 0.1:
                score[player] += 1
                print("✅ Richtig! Punkt erhalten.")
            print(f"ℹ️ Die tatsächliche Einwohnerzahl ist {population}.")

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
