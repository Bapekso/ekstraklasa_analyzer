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

def ask_for_team_id():
    return questionary.text("Podaj ID druzyny:").ask()

def ask_for_poisson_lambdas():
    home = float(questionary.text("Podaj oczekiwana liczbe goli gospodarza (lambda):", default="1.5").ask())
    away = float(questionary.text("Podaj oczekiwana liczbe goli goscia (lambda):", default="1.0").ask())
    return home, away

def render_standings_table(standings_data):
    """Wyświetla tabelę ligową w estetycznej formie tekstowej."""
    if not standings_data or "standings" not in standings_data:
        print("Brak danych tabeli do wyswietlenia.")
        return

    table_rows = []
    headers = ["Poz.", "Druzyna", "Mecze", "W", "R", "P", "Bramki", "Pkt"]

    for item in standings_data.get("standings", []):
        row = [
            item.get("position", "-"),
            item.get("team_name", "Nieznana"),
            item.get("played", 0),
            item.get("won", 0),
            item.get("drawn", 0),
            item.get("lost", 0),
            f"{item.get('goals_for', 0)}:{item.get('goals_against', 0)}",
            item.get("points", 0)
        ]
        table_rows.append(row)

    print("\n" + tabulate(table_rows, headers=headers, tablefmt="grid") + "\n")

def render_simulation_results(home_lambda, away_lambda, results):
    """Wyświetla podsumowanie symulacji Poissona."""
    summary_data = [
        ["Wygrana Gospodarza (1)", f"{results['home_win']:.2f}%"],
        ["Remis (X)", f"{results['draw']:.2f}%"],
        ["Wygrana Goscia (2)", f"{results['away_win']:.2f}%"]
    ]
    
    print(f"\n--- WYNIKI SYMULACJI (Gospodarz λ={home_lambda} vs Gosc λ={away_lambda}) ---")
    print(tabulate(summary_data, headers=["Scenariusz", "Prawdopodobienstwo"], tablefmt="simple"))

    best_score = max(results['matrix'].items(), key=lambda x: x[1])
    print(f"\nNajbardziej prawdopodobny wynik: {best_score[0][0]}:{best_score[0][1]} ({best_score[1]:.2f}%)\n")