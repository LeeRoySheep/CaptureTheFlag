import random
import wikipedia
import urllib.request
import json
from PIL import Image
from io import BytesIO
import requests


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


# Funktion zum Abrufen von Ländern, Hauptstädten, Einwohnerzahlen und Flaggen
def get_country_data():
    url = "https://restcountries.com/v3.1/all"
    try:
        import ssl
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=context) as response:
            data = json.loads(response.read().decode())

        country_dict = {}

# Schleife zum Extrahieren von Name, Hauptstadt, Bevölkerung und Flagge jedes Landes
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

# Spielregeln und Spielablauf anzeigen
def show_rules():
    print("Spielablauf:")
    print("1. Bitte Spielteilnehmer, Spielername, Schwierigkeitsstufe und Rundenanzahl auswählen. ")
    print("2. Es wird eine zufällige Flagge angezeigt. Bitte das entsprechende Land dazu angeben.")
    print("3. Danach wird nach der Hauptstadt der ausgegebenen Flagge gefragt.")
    print("4. Als nächstes wird die Einwohnerzahl des Landes abgefragt.")
    print("5. Falls mehrere Spieler spielen ist nun der nächste Spieler an der Reihe!")
    print("6. Dieser Prozess wiederholt sich nun so oft wie der Spieler entsprechende Runden angegeben hat.")
    print("--------------------")
    print("Spielregeln:")
    print("- Es gibt einen Anfänger Modus mit Multiple Choice.")
    print("- Im Pro Modus muss man direkt die Abtwort geben.")
    print("- Für jede richtige Antwort gibt es einen Punkt.")
    print("- Am Ende des Spiels gewinnt der Spieler mit den meisten Punkten.")

# Abfrage ob Spieler die Spielregeln sehen möchte
def ask_for_rules():
    while True:
        try:
            rules_choice = input("Möchtest du eine Einleitung zum Spiel? (Ja/Nein): ").strip().lower()
            if rules_choice in ["ja", "nein"]:
                if rules_choice == "ja":
                    show_rules()
                break
            else:
                raise ValueError("Ungültige Eingabe! Bitte Ja oder Nein angeben!")
        except ValueError as e:
            print(e)

# Abfrage zur Anzahl der Spieler
def get_player_count():
    while True:
        try:
            count = int(input("Wie viele Spieler spielen mit? "))
            if count > 0:
                return count
            else:
                print("Bitte eine Zahl größer als 0 eingeben.")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl eingeben.")

# Begrüßung der Spieler
def greet_players(player_count):
    players = []
    for i in range(1, player_count + 1):
        name = input(f"Spieler {i}, wie heißt du? ")
        players.append(name)
        print(f"Willkommen, {name}!")
    return players

# Schwierigkeitsgrad auswählen
def choose_difficulty():
    while True:
        difficulty = input("Wähle den Schwierigkeitsgrad (1 = Anfänger | 2 = Pro): ").strip().lower()
        if difficulty in ["1", "anfänger"]:
            return "anfänger"
        elif difficulty in ["2", "pro"]:
            return "pro"
        else:
            print("Bitte 1 für 'Anfänger' oder 2 für 'Pro' eingeben.")

# Hauptfunktion zum Starten des Spiels
def start_game():
    print("Willkommen bei Capture the Flag - Flaggen-Quiz!")
    ask_for_rules()

    player_count = get_player_count()
    players = greet_players(player_count)
    difficulty = choose_difficulty()
    rounds = int(input("Wie viele Runden möchtest du spielen? "))

    country_data = get_country_data()
    country_names = list(country_data.keys())
    score = {player: 0 for player in players}

    for _ in range(rounds):
        country = random.choice(country_names)
        flag_url = country_data[country]['flag']
        Image.open(BytesIO(requests.get(flag_url).content)).show()
        capital = country_data[country]['capital']
        population = country_data[country]['population']
        # print(f"Flaggen-URL: {flag_url}")

        for player in players:
            print(f"{player} ist dran!")
            if difficulty == "anfänger":
                choices = random.sample(country_names, 3) + [country]
                random.shuffle(choices)
                for i, choice in enumerate(choices, 1):
                    print(f"{i}. {choice}")
                answer = input("Wähle die richtige Nummer: ")
                if choices[int(answer) - 1] == country:
                    score[player] += 1
                    print("Richtig!")
                else:
                    print(f"Falsch! Die richtige Antwort war {country}.")
            else:
                answer = input("Nenne das Land zur Flagge: ")
                if answer.strip().lower() == country.lower():
                    score[player] += 1
                    print("Richtig!")
                else:
                    print(f"Falsch! Die richtige Antwort war {country}.")

            # Abfrage der Hauptstadt
            capital_answer = input(f"Was ist die Hauptstadt von {country}? ")
            if capital_answer.strip().lower() == capital.lower():
                score[player] += 1
                print("Richtig!")
            else:
                print(f"Falsch! Die richtige Antwort war {capital}.")

            # Abfrage der Einwohnerzahl
            population_answer = input(f"Wie viele Einwohner hat {country}? (Grobe Schätzung erlaubt) ")
            if population_answer.replace(',', '').isdigit():
                score[player] += get_points_population(int(population_answer), int(population))
                print(f"Die tatsächliche Einwohnerzahl ist {population}.")
            else:
                print("Ungültige Eingabe.")

# Endstand anzeigen
    print("Spiel beendet! Punktestand:")
    for player, points in score.items():
        print(f"{player}: {points} Punkte")

# Hauptfunktion aufrufen
if __name__ == "__main__":
    start_game()
