from services.api_client import SportAPIClient
from core.calculator import calculate_match_probabilities
from ui.views import (
    show_main_menu,
    ask_for_team_choice,
    ask_for_poisson_lambdas,
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
            print("\nPobieranie listy drużyn...")
            standings_data = client.get_standings()
            team_id = ask_for_team_choice(standings_data)
            
            if team_id:
                team_data = client.get_team_details(int(team_id))
                if team_data:
                    team_info = team_data.get("team", team_data if isinstance(team_data, dict) else {})
                    print("\n--- SZCZEGOLY DRUZYNY ---")
                    print(f"Nazwa: {team_info.get('name', 'Brak danych')}")
                    print(f"Miasto: {team_info.get('city', 'Brak danych')}")
                    print(f"Stadion: {team_info.get('stadium_name', 'Brak danych')}")
                    print(f"Trener: {team_info.get('coach_name', 'Brak danych')}\n")
            else:
                print("Nie wybrano drużyny.")

        elif choice.startswith("3."):
            home_lambda, away_lambda = ask_for_poisson_lambdas()
            results = calculate_match_probabilities(home_lambda, away_lambda)
            render_simulation_results(home_lambda, away_lambda, results)

        input("Naciśnij Enter, aby powrócić do menu...")

if __name__ == "__main__":
    main()