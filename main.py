import questionary
from services.api_client import SportAPIClient
from core.calculator import calculate_match_probabilities
from ui.views import (
    show_main_menu,
    render_standings_table,
    render_simulation_results
)

def main():
    client = SportAPIClient()
    print("=== ANALIZATOR EKSTRAKLASY CLI ===")

    while True:
        choice = show_main_menu()

        if not choice or choice.startswith("4."):
            print("\nZamykanie aplikacji. Do zobaczenia!")
            break

        elif choice.startswith("1."):
            print("\nPobieranie tabeli Ekstraklasy...")
            data = client.get_standings()
            render_standings_table(data)

        elif choice.startswith("2."):
            print("\nPobieranie tabeli...")
            standings_data = client.get_standings()
            
            items = []
            if isinstance(standings_data, list):
                items = standings_data
            elif isinstance(standings_data, dict):
                items = standings_data.get("standings", standings_data.get("table", standings_data.get("data", [])))

            if not items:
                print("Brak danych tabeli.")
            else:
                choices = []
                team_data_map = {}

                for item in items:
                    team_info = item.get("team", {})
                    team_name = team_info.get("name", item.get("team_name", "Nieznana")) if isinstance(team_info, dict) else item.get("team_name", str(team_info))
                    choices.append(team_name)
                    team_data_map[team_name] = item

                selected_name = questionary.select("Wybierz drużynę:", choices=choices).ask()

                if selected_name and selected_name in team_data_map:
                    t = team_data_map[selected_name]
                    
                    position = t.get("position", t.get("rank", "-"))
                    played = t.get("played", t.get("playedMatches", 0))
                    won = t.get("won", t.get("win", 0))
                    drawn = t.get("draw", t.get("drawn", 0))
                    lost = t.get("lost", t.get("loss", 0))
                    goals_for = t.get("goals_for", t.get("goalsFor", t.get("for", 0)))
                    goals_against = t.get("goals_against", t.get("goalsAgainst", t.get("against", 0)))
                    points = t.get("points", t.get("pts", 0))

                    print(f"\n--- STATYSTYKI Z TABELI: {selected_name} ---")
                    print(f"Pozycja w tabeli: {position}")
                    print(f"Rozegrane mecze: {played}")
                    print(f"Wygrane: {won} | Remisy: {drawn} | Porażki: {lost}")
                    print(f"Bramki: {goals_for}:{goals_against}")
                    print(f"Punkty: {points}\n")
                else:
                    print("Nie wybrano drużyny.")

        elif choice.startswith("3."):
            print("\nPobieranie tabeli do symulacji...")
            standings_data = client.get_standings()
            
            items = []
            if isinstance(standings_data, list):
                items = standings_data
            elif isinstance(standings_data, dict):
                items = standings_data.get("standings", standings_data.get("table", standings_data.get("data", [])))

            if not items or len(items) < 2:
                print("Za mało danych w tabeli, aby przeprowadzić symulację.")
            else:
                choices = []
                team_data_map = {}

                for item in items:
                    team_info = item.get("team", {})
                    team_name = team_info.get("name", item.get("team_name", "Nieznana")) if isinstance(team_info, dict) else item.get("team_name", str(team_info))
                    choices.append(team_name)
                    team_data_map[team_name] = item

                # Wybór gospodarza i gościa
                home_team = questionary.select("Wybierz drużynę gospodarzy:", choices=choices).ask()
                away_team = questionary.select("Wybierz drużynę gości:", choices=choices).ask()

                if home_team and away_team:
                    if home_team == away_team:
                        print("Nie możesz wybrać tej samej drużyny jako gospodarza i gościa!")
                    else:
                        h_data = team_data_map[home_team]
                        a_data = team_data_map[away_team]

                        # Obliczanie prostych wskaźników średniej bramek na mecz (lambda)
                        h_played = max(int(h_data.get("played", h_data.get("playedMatches", 1))), 1)
                        a_played = max(int(a_data.get("played", a_data.get("playedMatches", 1))), 1)

                        h_goals_scored = int(h_data.get("goals_for", h_data.get("goalsFor", h_data.get("for", 0))))
                        h_goals_conceded = int(h_data.get("goals_against", h_data.get("goalsAgainst", h_data.get("against", 0))))
                        
                        a_goals_scored = int(a_data.get("goals_for", a_data.get("goalsFor", a_data.get("for", 0))))
                        a_goals_conceded = int(a_data.get("goals_against", a_data.get("goalsAgainst", a_data.get("against", 0))))

                        # Prosta baza do lambd: średnia strzelonych przez gospodarza + średnia straconych przez gościa (podzielone na 2)
                        home_lambda = round(((h_goals_scored / h_played) + (a_goals_conceded / a_played)) / 2, 2)
                        away_lambda = round(((a_goals_scored / a_played) + (h_goals_conceded / h_played)) / 2, 2)

                        # Zabezpieczenie przed wartością 0
                        home_lambda = max(home_lambda, 0.2)
                        away_lambda = max(away_lambda, 0.2)

                        print(f"\n[AUTO-LAMBDA] Gospodarz ({home_team}): {home_lambda} | Gość ({away_team}): {away_lambda}")

                        results = calculate_match_probabilities(home_lambda, away_lambda)
                        render_simulation_results(home_lambda, away_lambda, results)
                else:
                    print("Przerwano wybór drużyn.")

        input("Naciśnij Enter, aby powrócić do menu...")

if __name__ == "__main__":
    main()