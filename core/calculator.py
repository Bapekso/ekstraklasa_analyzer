import math

def poisson_probability(lmbda: float, k: int) -> float:
    """Oblicza prawdopodobieństwo strzelenia k goli przy oczekiwaniu lambda."""
    if lmbda < 0:
        return 0.0
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

def calculate_team_lambdas(home_team_data, away_team_data, all_teams_data):
    """
    Oblicza lambdy na podstawie siły ataku i obrony drużyn względem średniej ligowej
    oraz uwzględnia atut własnego boiska.
    """
    total_goals = 0
    total_matches = 0

    # 1. Obliczamy średnią liczbę bramek w całej lidze
    for team in all_teams_data:
        played = int(team.get("played", team.get("playedMatches", 0)))
        goals = int(team.get("goals_for", team.get("goalsFor", team.get("for", 0))))
        total_goals += goals
        total_matches += played

    if total_matches == 0:
        return 1.5, 1.0  # Fallback w razie pustych danych

    league_avg_goals = total_goals / total_matches

    # 2. Pobieramy statystyki gospodarza i gościa
    h_played = max(int(home_team_data.get("played", home_team_data.get("playedMatches", 1))), 1)
    h_gf = int(home_team_data.get("goals_for", home_team_data.get("goalsFor", home_team_data.get("for", 0))))
    h_ga = int(home_team_data.get("goals_against", home_team_data.get("goalsAgainst", home_team_data.get("against", 0))))

    a_played = max(int(away_team_data.get("played", away_team_data.get("playedMatches", 1))), 1)
    a_gf = int(away_team_data.get("goals_for", away_team_data.get("goalsFor", away_team_data.get("for", 0))))
    a_ga = int(away_team_data.get("goals_against", away_team_data.get("goalsAgainst", away_team_data.get("against", 0))))

    # 3. Obliczamy wskaźniki siły ataku i obrony względem średniej ligowej
    # Siła ataku = średnia bramek drużyny / średnia ligowa
    home_attack = (h_gf / h_played) / league_avg_goals if league_avg_goals > 0 else 1.0
    home_defense = (h_ga / h_played) / league_avg_goals if league_avg_goals > 0 else 1.0

    away_attack = (a_gf / a_played) / league_avg_goals if league_avg_goals > 0 else 1.0
    away_defense = (a_ga / a_played) / league_avg_goals if league_avg_goals > 0 else 1.0

    # 4. Atut własnego boiska (standardowo w modelach dodaje ~15% skuteczności gospodarzowi)
    HOME_ADVANTAGE = 1.15

    # 5. Ostateczne przewidywane bramki (lambda)
    # Lambda gospodarza = Siła ataku gospodarza * Siła obrony gościa * Średnia ligowa * Atut boiska
    home_lambda = home_attack * away_defense * league_avg_goals * HOME_ADVANTAGE
    
    # Lambda gościa = Siła ataku gościa * Siła obrony gospodarza * Średnia ligowa
    away_lambda = away_attack * home_defense * league_avg_goals

    # Bezpieczne zaokrąglenie (minimum 0.2, żeby model nie zerował szans całkowicie)
    home_lambda = max(round(home_lambda, 2), 0.2)
    away_lambda = max(round(away_lambda, 2), 0.2)

    return home_lambda, away_lambda

def calculate_match_probabilities(home_lambda: float, away_lambda: float, max_goals: int = 6):
    """Oblicza macierz wyników oraz szanse procentowe 1X2."""
    matrix = {}
    home_win_prob = 0.0
    draw_prob = 0.0
    away_win_prob = 0.0

    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            p_home = poisson_probability(home_lambda, h)
            p_away = poisson_probability(away_lambda, a)
            prob = p_home * p_away * 100
            matrix[(h, a)] = prob

            if h > a:
                home_win_prob += prob
            elif h == a:
                draw_prob += prob
            else:
                away_win_prob += prob

    return {
        "matrix": matrix,
        "home_win": home_win_prob,
        "draw": draw_prob,
        "away_win": away_win_prob
    }