import math

def poisson_probability(lmbda: float, k: int) -> float:
    """Oblicza prawdopodobieństwo strzelenia k goli przy oczekiwaniu lambda."""
    if lmbda < 0:
        return 0.0
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

def calculate_match_probabilities(home_lambda: float, away_lambda: float, max_goals: int = 5):
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