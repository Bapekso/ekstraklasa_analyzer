import questionary
from tabulate import tabulate

def show_main_menu():
    return questionary.select(
        "Wybierz opcje z menu:",
        choices=[
            "1. Zobacz tabele Ekstraklasy",
            "2. Zobacz szczegoly poszczegolnej druzyny",
            "3. Porownaj dwie druzyny (Symulacja Poissona)",
            "4. Wyjscie"
        ]
    ).ask()

def ask_for_poisson_lambdas():
    home = float(questionary.text("Podaj oczekiwana liczbe goli gospodarza (lambda):", default="1.5").ask())
    away = float(questionary.text("Podaj oczekiwana liczbe goli goscia (lambda):", default="1.0").ask())
    return home, away

def render_standings_table(standings_data):
    """Wyświetla tabelę ligową zgodnie ze strukturą danych z sportapi.ai."""
    if not standings_data:
        print("Brak danych tabeli do wyswietlenia.")
        return

    items = []
    if isinstance(standings_data, list):
        items = standings_data
    elif isinstance(standings_data, dict):
        items = standings_data.get("standings", standings_data.get("table", standings_data.get("data", [])))

    if not items:
        print("Brak danych w odpowiedzi API.")
        return

    table_rows = []
    headers = ["Poz.", "Druzyna", "Mecze", "W", "R", "P", "Bramki", "Pkt"]

    for idx, item in enumerate(items, 1):
        team_info = item.get("team", {})
        if isinstance(team_info, dict):
            team_name = team_info.get("name", item.get("team_name", "Nieznana"))
        else:
            team_name = item.get("team_name", str(team_info) if team_info else "Nieznana")

        position = item.get("position", item.get("rank", idx))
        played = item.get("played", item.get("playedMatches", 0))
        won = item.get("won", item.get("win", 0))
        drawn = item.get("draw", item.get("drawn", 0))
        lost = item.get("lost", item.get("loss", 0))
        
        goals_for = item.get("goals_for", item.get("goalsFor", item.get("for", 0)))
        goals_against = item.get("goals_against", item.get("goalsAgainst", item.get("against", 0)))
        
        points = item.get("points", item.get("pts", 0))

        row = [
            position,
            team_name,
            played,
            won,
            drawn,
            lost,
            f"{goals_for}:{goals_against}",
            points
        ]
        table_rows.append(row)

    print("\n" + tabulate(table_rows, headers=headers, tablefmt="grid") + "\n")

def render_simulation_results(home_lambda, away_lambda, results):
    """Wyświetla pełne podsumowanie symulacji Poissona wraz z rozkładem wyników."""
    summary_data = [
        ["Wygrana Gospodarza (1)", f"{results['home_win']:.2f}%"],
        ["Remis (X)", f"{results['draw']:.2f}%"],
        ["Wygrana Goscia (2)", f"{results['away_win']:.2f}%"]
    ]
    
    print(f"\n--- WYNIKI SYMULACJI (Gospodarz λ={home_lambda} vs Gosc λ={away_lambda}) ---")
    print(tabulate(summary_data, headers=["Scenariusz", "Prawdopodobienstwo"], tablefmt="simple"))

    print("\nNajbardziej prawdopodobne wyniki:")
    score_rows = []
    # Sortujemy wyniki od najbardziej do najmniej prawdopodobnego
    sorted_scores = sorted(results['matrix'].items(), key=lambda x: x[1], reverse=True)
    
    # Pokazujemy top 6 najbardziej prawdopodobnych wyników
    top_scores = sorted_scores[:6]
    for (h, a), prob in top_scores:
        score_rows.append([f"{h}:{a}", f"{prob:.2f}%"])
        
    print(tabulate(score_rows, headers=["Wynik", "Szansa"], tablefmt="grid"))
    print()